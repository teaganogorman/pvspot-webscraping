# pvspot-webscraping
Accesses SolarGIS website and downloads pvspot data for sites

This repository contains a GUI to choose sites and months to download PVSpot data for, as well as the actual webscraper.

The GUI currently works for month data downloads, but a yearly one is in progress.

Ensure both files are in the same folder, and run the "PVSpot_data_GUI.py" file. A GUI will come up where you can choose sites and months, then click OK. 
After that, the webscraper will run. Do not close or interfere with Chrome while the webscraper is running.

Required modules for this to work: selenium, tkinter, math
