## @package URCommunication
# A module/package designed to allow a remote computer to communicate with a Universal Robots Cobot through python.
#
# Utilises socket connections to communicate through sending and recieving URScript commands and returns.

import socket
import time

# Configurable settings.
## Standard interpreter port, only change this if your Cobot needs a different port.
PORT_INTERPRETER = 30020
## How long it takes before requests/recieves time out.
TIMEOUT_DURATION = 2
## How long should the program wait for the initial connection to be made.
LONG_TIMEOUT_DURATION = 20
## Set these higher if there are issues with buffer sizes being too small.
STD_BUFFER_SIZE = 1024 
# Demo configurations, change these to match the needed values for your implementation in the script files used.
## Perron038 Cobot IP address.
IP_UR = "192.168.0.13"
## Custom port used in returnData.script file.
PORT_RECIEVE = 30022

DEBUG_MODE = False

def greenLightUR(target):
    """!
    A function to synchronise the PolyScope code/script and the remote device.

    This function starts a socket connection to the interpreter port,
    then calls it to end the interpreter, before closing the connection.
    To make use of this, a "interpreter_mode()" command must be called before the main function in the URScript file used.
    
    \param [in] target The IP Address of the target device to connect to, in string format.
    """

    cGreenLight = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    cGreenLight.settimeout(LONG_TIMEOUT_DURATION)
    cGreenLight.connect((target,PORT_INTERPRETER))
    cGreenLight.send(("end_interpreter()"+"\n").encode('utf8'))
    cGreenLight.close()
    time.sleep(1)

def connectReadWrite(target=IP_UR,in_port=PORT_RECIEVE):
    """!
    A function to connect both a output and input socket from the remote device to the UR/Polyscope.

    This function starts two connections, a output and input.
    The output is used to send commands to the Cobot.
    The input is used to recieve responses from the Cobot.

    \param [in] target The IP Address of the target device to connect to.
    \param [in] in_port The Port used to get responses from the cobot.
    
    \retval writeConnection The connection to write to.
    \retval readConnection The connection to read input from. 
    """

    # Creating the sockets.
    writeConnection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    readConnection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # Setting the timeout.
    writeConnection.settimeout(TIMEOUT_DURATION)
    readConnection.settimeout(LONG_TIMEOUT_DURATION)

    # Connecting the readconnection.
    try:
        readConnection.bind(('',in_port))
        readConnection.listen()
        readConnection,address = readConnection.accept()

    except OverflowError:
        print("[ERROR] Readconnection's Port value not between 0 to 65535. Currently: " + str(in_port))
        return 1,1
    # except TimeoutError as err:
    #     print("[ERROR] Readconnection's Connection attempt timed out: " + str(err.__traceback__))
    #     return 2,2
    
    # Connecting the writeConnection.
    try:
        writeConnection.connect((target,PORT_INTERPRETER))
    except TimeoutError:
        print("[ERROR] WriteConnection unable to connect, is the Cobot in Interpreter Mode?")
        return 3,3
    
    # Reset read connection to normal timeout.
    readConnection.settimeout(TIMEOUT_DURATION)

    return writeConnection,readConnection

def asyncWrite(command,write_conn):
    """!
    A function that writes a URScript Command to the robot.
    Does not wait for a return-response from the Cobot before continuing with the python script.
    This function does however wait until the Cobot has send the Acknowledgement (ACK) or failure signal.

    \param [in] command String containing the URScript command, if this statement cannot run, a failure signal will return.
    \param [in] write_conn The writing Connection generated by the connect functions.

    \retval State The value stating if the function ran properly: 0 means it ran correctly, 1 means a timeout error, 2 means a rejection error.
    """

    try:
        write_conn.send((command+"\n").encode("utf8"))
        if DEBUG_MODE:
            print("[DEBUG] " + (command+"\n"))
        response = write_conn.recv(STD_BUFFER_SIZE).decode("utf8")
        if not response.startswith("ack"):
            raise ValueError(response)
    except TimeoutError:
        print("[ERROR] No Ack or Failure signal, timed out.")
        return 1
    except ValueError as err:
        print("[ERROR] Command not recognised/accepted: " + err.args[0], end='')
        return 2
    return 0

def syncWrite(command,write_conn,read_conn,timeout=10):
    """!
    A function that writes a command to the Cobot, after which it halts execution until a "exec_done" response is recieved.
    This function listens to both the acknowledgement and a "done" signal when the cobot has executed the command.

    (This function uses the asyncwrite function with some extra wrapping.)

    \param [in] command String containing the URScript command, if this statement cannot run, a failure signal will return.
    \param [in] write_conn The writing Connection generated by the connect functions.
    \param [in] read_conn The reading Connection generated by the "connectReadWrite" function.

    \retval State The value stating if the function ran properly: 0 means it ran correctly.
    """
    curTimeout = read_conn.gettimeout()
    read_conn.settimeout(timeout)

    try:
        if asyncWrite("run_sync(" + command + ")",write_conn) != 0:
            raise RuntimeError('write_failed')
    except RuntimeError as err:
        if err.args[0] == 'write_failed':
            print("[ERROR] Write Command failed, see previous outputs.")
            read_conn.settimeout(timeout)
            return 2
    
    try:
        response = read_conn.recv(STD_BUFFER_SIZE).decode("utf8")
        if not response.startswith("exec_done"):
            raise ValueError()
    except TimeoutError:
        print("[ERROR] Read timed out.")
        read_conn.settimeout(timeout)
        return 1
    except ValueError:
        print("[ERROR] Recieved signal not expected:" + str(response))
        read_conn.settimeout(timeout)
        return 3
    read_conn.settimeout(timeout)
    return 0

def readWrite(command,write_conn,read_conn):
    """!
    A function to write to the Cobot and wait for custom data as response. (I.E The cobot's TCP Position, joint data, etc.)
    
    This function also uses the asyncWrite command with a wrapper, but instead of expecting a static response, it returns the data that was send back.
    <Params & Retval's to be added.>
    """
    try:
        if asyncWrite("reply(" + command + ")",write_conn) != 0:
            raise RuntimeError('write_failed')
    except RuntimeError as err:
        if err.args[0] == 'write_failed':
            print("[ERROR] Write Command failed, see previous outputs.")
            return 2
    
    try:
        response = read_conn.recv(STD_BUFFER_SIZE).decode("utf8")
    except TimeoutError:
        print("[ERROR] Read timed out.")
        return 1
    return response

def read(read_conn):
    """!
    A function that reads input from the Read Connection generated by earlier functions.

    Function waits for recv input with the standard buffer size.

    \param [in] read_conn The Read Connection.

    \retval input The recieved signal, decoded to UTF8.
    """

    try:
        input = read_conn.recv(STD_BUFFER_SIZE).decode("utf8")
    except TimeoutError:
        print("[ERROR] Read command timed out, nothing received.")
        return 1
    return input

def closeConnection(conn,write = True):
    """!
    A function to shut down a socket connection.

    If the connection is writable, the 2nd arg can be set to true to write the "end_interpreter()" command.

    \param [in] conn The Connection to shut down.
    \param [in] write A boolean that deter('responder')mines wether a connection can be written to, defaults to True.

    \retval State Returns 0 if succeeded.
    """

    if write:
        asyncWrite("end_interpreter()",conn)
        conn.shutdown(socket.SHUT_RD)
        conn.close()
    else:
        conn.shutdown(socket.SHUT_RD)
        conn.close()
    return 0

def closeReadWrite(write_conn,read_conn):
    asyncWrite("end_interpreter()",write_conn)
    write_conn.shutdown(socket.SHUT_RD)
    read_conn.shutdown(socket.SHUT_RD)
    write_conn.close()
    read_conn.close()
    return 0

def poseToValues(pose):
    # Take apart the values.
    pose = pose.split(",")
    # Remove unusual parts of string.
    pose[0] = pose[0].removeprefix("p[")
    pose[5] = pose[5].removesuffix("]")
    # Convert strings to float.
    [float(i) for i in pose]
    return pose