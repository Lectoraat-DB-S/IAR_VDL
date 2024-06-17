# VDL Project

**Team/Project members:**  
Jan Groen, Dave Stitselaar, Niels van Dam.  

## Used packages/imports
 - **Time** : Used for the UR to PC connection.
 - **Math** : Used for simple calculations & conversions done in the calibration.
 - **Random** : Used for number generation.
 - **Socket** : Used for the UR to PC connection.
 - **Numpy** : Used for more complex calculations in both the calibration and detection.
 - **PyQt5** : Used in the detection for the GUI.
 - **Shutil** : 
 - **OS** : Used for print formatting and file management in the detection.
 - **CSV** : Used for reading and storing data.
 - **OCC** : Used for the detection.

## Structure
The project is divided into 3 seperate components, the detection (GatenHerkenning), path generation (Pad generatie), and calibration (Kalibratie).

Each of these components are designed to work on their own, although the path generation uses a specific (CSV) format output by the detection part.  

If present, the test folder contains a few files used to test features during development. These files will not function out of the box, and might need some files dragged into their folder.  

## Hardware
This project uses a certain amount of tools, most notably:
- [OnRobot Screwdriver](https://onrobot.com/en/products/onrobot-screwdriver)
- [EM12WD Inductive Sensor](https://www.turck.us/datasheet/_us/edb_1634812_eng_us.pdf)
- [UR10e Cobot](https://www.universal-robots.com/products/ur10-robot/)
- 3D Printed components
	- Screwdriver head (See <T.B.A>)
	- Connector with cable groove (No file available for it)

## Usage Guideline
**Calibration**: Boot up the cobot, load in the Program beforehand (check if the Installation got changed aswell!).
Make sure you start the program on the Cobot before you start the python script, this is due to how the socket connections are used.