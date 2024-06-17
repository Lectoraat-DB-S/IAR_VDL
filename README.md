# VDL Project

**Team/Project members:**  
Jan Groen, Dave Stitselaar, Niels van Dam.  



<br>
<br>

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
- []()

Temp template:

# template-repository 🦾  
codering  

Tijdens het opleveren van code zien we graag dat er een README bestand wordt meegeleverd, dit maakt het gemakkelijker voor een ander om met jouw code verder te gaan of er gebruik van te maken.
Deze README beschrijft het project, wat je nodig hebt om de code te gebruiken en hoe je de code kunt gebruiken. Uiteraard kan dit ietsje afwijken aan de hand van welke taal je hebt geprogrammeerd, maar blijf het liefst zo dicht bij mogelijk bij deze standaarden.

De volgende dingen zien we graag in een README:
- beschrijving: graag zien we een korte beschrijving van je project. dus een korte uitleg wat je code doet als je het gebruikt.
- imports en versies: graag zien we een lijst met alle imports, packages, software, etc die je hebt gebruikt met de versies. Denk hierbij aan je python versie, dat je iets met "pip install" hebt geinstalleerd of dat je ubuntu 23.04 als operating system hebt gebruikt (dus ook welke versie je hebt geinstalleerd). (test dus ook je code op een andere laptop!!! hierdoor weet je zeker dat je alles genoteerd hebt)
- architectuur: graag zien we een korte beschrijving van de architectuur van je project. welke bestanden hebben welke bestanden nodig en wat kun je in welk bestand vinden.
- reference: graag zien we een lijst met welke code je niet zelf hebt gemaakt of gebaseerd hebt op een ander zijn code met daarbij een link naar de originele code en een datum waarop je die code hebt geraadpleegd. Dit zorgt ervoor dat de juiste mensen credit krijgen. (let op, ook als je een functie ergens vandaan haalt en aanpast hoor je nog steeds te zeggen wie daar credit voor krijgt).
- usage: op het moment dat je extra hardware zoals een robot gebruikt is het fijn als er ook iets uitgelegd wordt over hoe je alles hebt aangesloten en opgestart. Misschien is het wel van belang dat je eerst het programma op de cobot start voordat je de python code op je laptop start.

- commenting: in code is het vrij normaal om comments te gebruiken om je code duidelijker te maken. Graag zien we dan ook dat dit gedaan wordt.
	- functie beschrijving: Liefst zien we dat er per functie met een comment uitgelegd wordt hoe de functie werkt en waarvoor ie bedoeld wordt (dit kan vaak in 1 zin). mocht de functie lang zijn dan zien we ook graag comments tussendoor.
	- Bestand beschrijving: Liefst zien we bovenaan elk bestand dat er een korte beschrijving staat van welke functies er in het bestand geprogrammeerd zijn.
	- Variabele beschrijving:

Een ReadMe schrijf je in Markdown. in de volgende link vind je wat voorbeelden over hoe je deze kunt stylen:
https://github.com/lifeparticle/Markdown-Cheatsheet

mocht je wat inspiratie willen kun je op de github hieronder even kijken.
https://github.com/matiassingers/awesome-readme

https://integrity.mit.edu/handbook/academic-integrity-handbook
