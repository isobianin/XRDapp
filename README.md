# What is XRDapp
XRDapp is a data visualisation tool that aims to streamline the workflow of X-ray diffraction (XRD) analysis. This project is developed for the Open University, School of Engineering and Innovation in collaboration with [James Bowen](https://www.linkedin.com/in/bowenjames/) and [Matthew Kershaw](https://www.linkedin.com/in/matt-kershaw-47634b57/). 
# Supported file formats
XRDapp works with the following formats (powered by [xylib](https://github.com/wojdyr/xylib/tree/master)):
- plain text, delimiter-separated values (e.g. CSV)
- Crystallographic Information File for Powder Diffraction (pdCIF)
- Siemens/Bruker UXD
- Siemens/Bruker RAW ver. 1/2/3, RAW4.0 (experimental functionality, might not work perfectly)
- Philips UDF
- Philips PC-APD RD raw scan V3/V5
- PANalytical XRDML
- Rigaku DAT
- Sietronics Sieray CPI
- DBWS/DMPLOT data file
- Canberra CNF (from Genie-2000 software; aka CAM format)
- Canberra AccuSpec MCA
- XFIT/Koalariet XDD
- RIET7/LHPM/CSRIET/ILL_D1A5/PSI_DMC DAT
- Vamas ISO14976 _(only experiment modes: SEM or MAPSV or MAPSVDP are supported; only REGULAR scan_mode is supported)_
- Princeton Instruments WinSpec SPE _(only 1-D data is supported)_
- χPLOT [CHI](http://www.esrf.eu/computing/scientific/FIT2D/FIT2D_REF/node115.html#SECTION0001851500000000000000)
- Ron Unwin's Spectra XPS format (VGX-900 compatible)
- Freiberg Instruments XSYG (from lexsyg)
- Bruker SPC/PAR
# Features
- thanks to [xylib](https://github.com/wojdyr/xylib/tree/master), work with multiple common and obscure XRD file formats
- portable .exe file can be used on many lab and personal machines
- convert loaded files to .txt format so they can be opened and viewed elsewhere
- load temperature values as a separate file to go hand-in-hand with the current data set
- customise the viewing window (data points cursor, minor and major grids, change axis spacing values, change font size, etc.)
# Buttons
![Home](media/mpl_home_large.png) - Home: get back to the original view ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)
![Import Data](media/import-content.png) - Import Data: when selected, navigate to the folder with data and select files to be loaded into XRDapp
![Load Temperatures](media/temperature-low.png) - Load Temperatures: an optional feature which allows XRDapp to load a .txt file with temperatures that were used during the XRD run
![Fit Screen](media/stretch-vertically.png) - Fit Screen: fit the current curve into the screen
![Toggle Cursor](media/cursor.png) - Toggle Cursor: turns on or off a cursor that snaps to the closest data point
![Toggle File List](media/toggle-list-icon.png) - Toggle File List: controls visibility of the loaded files list
![Toggle Grid](media/toggle-grid-icon.png) - Toggle Grid: activates minor and major grids that spans vertically and horizontally. Each can be individually toggled on or off
![Set Ticks](media/set-ticks-icon.png) - Set Ticks: set spacing between x or y axis divisions
![Set Font Size](media/font-size-icon.png) - Set Font Size: set font size of each individual text element
![Previous View](media/mpl_back_large.png) - Previous View: go back to the previous view of the current curve ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)
![Next View](media/mpl_forward_large.png) - Next View: go to the view you had before clicking "Previous view" ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)
![Pan View](media/mpl_move_large.png) - Pan View: move the curve inside the viewing window (matplotlib toolbar function)
![Zoom](media/mpl_zoom.png) - Zoom: select an area to zoom into ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)
![Edit Axis](media/mpl_axis.png) - Edit Axis: edit min and max shown values, change the colour of the curve, change text entries for axes, change line style and choose markers ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)
![Save Figure](media/mpl_filesave_large.png) - Save Figure: take a screencap of the current view ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)

![App Info](media/info-icon.png) - App Info: information regarding the current version, developers and contact details
![Convert Data](media/convert-icon.png) - Convert Data: convert the loaded data into .txt file. XRDapp will create a new folder in the same directory as the loaded files and place converted files in it
![Clear Data](media/clear-data-icon.png) - Clear Data: clear the loaded data cache
# Using XRDapp
Start using XRDapp by pressing ![Import Data](media/import-content.png) and loading the data. When the data is loaded, you can browse through XRD curves with a help of up and down arrow buttons on your keyboard or by clicking the filename in the loaded files list window. Use ![Load Temperatures](media/temperature-low.png) to load a .txt file with temperature values, which will be displayed above the viewing window. To zoom in to an area of interest, use ![Zoom](media/mpl_zoom.png). If the given curve has small intensity (y-axis value), press ![Fit Screen](media/stretch-vertically.png) to fit it to the screen. Pressing ![Home](media/mpl_home_large.png) automatically rescales everything back to the highest intensity among all loaded files. To convert loaded files into .txt file, press ![Convert Data](media/convert-icon.png), which will create a folder called "XRDapp converted" in the folder where the data was loaded from. Press either ![Clear Data](media/clear-data-icon.png) to clear the data or ![Import Data](media/import-content.png) to load different files.

[Samples folder](samples/) contains an example of temperature file and RAW4.0 file

# Modifying code
The code provided in this repository can be modified. It is important to note that to ensure that the code can run smoothly on your machine, you need to install [xylib](https://github.com/wojdyr/xylib/tree/master). After that, to build your own executable file, use the following command:
```bash
pyinstaller --name XRDApp --onefile --windowed --icon=media\icon_main.ico --add-data "media;media" xrdapp.py
```
# Credits
Many thanks to:
- the developers of [xylib](https://github.com/wojdyr/xylib) for providing quite a comprehensive tool for working with multiple XRD data formats
- the developer of [raw2xyN](https://github.com/MarcoVando/raw2xyN) for realisation of couple of interesting ideas