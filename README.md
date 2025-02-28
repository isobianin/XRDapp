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
![[media/mpl_home_large.png|24]] - Home: get back to the original view ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)
![[media/import-content.png|24]] - Import Data: when selected, navigate to the folder with data and select files to be loaded into XRDapp
![[media/temperature-low.png|24]] - Load Temperatures: an optional feature which allows XRDapp to load a .txt file with temperatures that were used during the XRD run
![[media/stretch-vertically.png|24]] - Fit Screen: fit the current curve into the screen
![[media/cursor.png|24]] - Toggle Cursor: turns on or off a cursor that snaps to the closest data point
![[media/toggle-list-icon.png|24]] - Toggle File List: controls visibility of the loaded files list
![[media/toggle-grid-icon.png|24]] - Toggle Grid: activates minor and major grids that spans vertically and horizontally. Each can be individually toggled on or off
![[media/set-ticks-icon.png|24]] - Set Ticks: set spacing between x or y axis divisions
![[media/font-size-icon.png|24]] - Set Font Size: set font size of each individual text element
![[media/mpl_back_large.png|24]] - Previous View: go back to the previous view of the current curve ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)
![[media/mpl_forward_large.png|24]] - Next View: go to the view you had before clicking "Previous view" ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)
![[media/mpl_move_large.png|24]] - Pan View: move the curve inside the viewing window (matplotlib toolbar function)
![[media/mpl_zoom.png|24]] - Zoom: select an area to zoom into ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)
![[media/mpl_axis.png|24]] - Edit Axis: edit min and max shown values, change the colour of the curve, change text entries for axes, change line style and choose markers ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)
![[media/mpl_filesave_large.png|24]] - Save Figure: take a screencap of the current view ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)

![[media/info-icon.png|24]] - App Info: information regarding the current version, developers and contact details
![[media/convert-icon.png|24]] - Convert Data: convert the loaded data into .txt file. XRDapp will create a new folder in the same directory as the loaded files and place converted files in it
![[media/clear-data-icon.png|24]] - Clear Data: clear the loaded data cache
# Using XRDapp
Start using XRDapp by pressing ![[media/import-content.png|24]] and loading the data. When the data is loaded, you can browse through XRD curves with a help of up and down arrow buttons on your keyboard or by clicking the filename in the loaded files list window. Use ![[media/temperature-low.png|24]] to load a .txt file with temperature values, which will be displayed above the viewing window. To zoom in to an area of interest, use ![[media/mpl_zoom.png|24]]. If the given curve has small intensity (y-axis value), press ![[media/stretch-vertically.png|24]] to fit it to the screen. Pressing ![[media/mpl_home_large.png|24]] automatically rescales everything back to the highest intensity among all loaded files. To convert loaded files into .txt file, press ![[media/convert-icon.png|24]], which will create a folder called "XRDapp converted" in the folder where the data was loaded from. Press either ![[media/clear-data-icon.png|24]] to clear the data or ![[media/import-content.png|24]] to load different files.

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