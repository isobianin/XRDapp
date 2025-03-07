# What is XRDapp

<img src="media/icon_main.png" width="60px" class="center" align="left"/>

XRDapp is a data visualisation tool that aims to streamline the workflow of X-ray diffraction (XRD) analysis. This project is developed for the Open University, School of Engineering and Innovation in collaboration with [James Bowen](https://www.linkedin.com/in/bowenjames/) and [Matthew Kershaw](https://www.linkedin.com/in/matt-kershaw-47634b57/).

# Features
- thanks to [xylib](https://github.com/wojdyr/xylib/tree/master), work with multiple common and obscure XRD file formats
- portable .exe file can be used on many lab and personal machines
- convert loaded files to .txt format so they can be opened and viewed elsewhere
- load temperature values as a separate file to go hand-in-hand with the current data set
- customise the viewing window (data points cursor, minor and major grids, change axis spacing values, change font size, etc.)

# Supported file formats
XRDapp uses the latest [xylib](https://github.com/wojdyr/xylib/tree/master) version compiled from the official repository. In other words, it is at least one commit ahead of the [pip](https://pypi.org/project/xylib-py/) and [fytik](https://github.com/wojdyr/fityk) xylib distribution. The key difference is that this locally compiled version partially supports [RAW4.0](https://github.com/wojdyr/xylib/commit/76c4bbce014b8b43fd8c3535c52c33c9c3018fbd) file format. Additionally, XRDapp has its own way of interpreting RAW4.0 files that are not recognised by [xylib](https://github.com/wojdyr/xylib/tree/master).

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

# User interface
<img src="media/mpl_home_large.png" width="24px" /> - Home: get back to the original view ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)

<img src="media/import-content.png" width="24px" /> - Import Data: when selected, navigate to the folder with data and select files to be loaded into XRDapp

<img src="media/temperature-low.png" width="24px" /> - Load Temperatures: an optional feature which allows XRDapp to load a .txt file with temperatures that were used during the XRD run

<img src="media/stretch-vertically.png" width="24px" /> - Fit Screen: fit the current curve into the screen

<img src="media/cursor.png" width="24px" /> - Toggle Cursor: turns on or off a cursor that snaps to the closest data point

<img src="media/toggle-list-icon.png" width="24px" /> - Toggle File List: controls visibility of the loaded files list

<img src="media/toggle-grid-icon.png" width="24px" /> - Toggle Grid: activates minor and major grids that spans vertically and horizontally. Each can be individually toggled on or off

<img src="media/set-ticks-icon.png" width="24px" /> - Set Ticks: set spacing between x or y axis divisions

<img src="media/font-size-icon.png" width="24px" /> - Set Font Size: set font size of each individual text element

<img src="media/mpl_back_large.png" width="24px" /> - Previous View: go back to the previous view of the current curve ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)

<img src="media/mpl_forward_large.png" width="24px" /> - Next View: go to the view you had before clicking "Previous view" ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)

<img src="media/mpl_move_large.png" width="24px" /> - Pan View: move the curve inside the viewing window (matplotlib toolbar function)

<img src="media/mpl_zoom.png" width="24px" /> - Zoom: select an area to zoom into ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)

<img src="media/mpl_axis.png" width="24px" /> - Edit Axis: edit min and max shown values, change the colour of the curve, change text entries for axes, change line style and choose markers ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)

<img src="media/mpl_filesave_large.png" width="24px" /> - Save Figure: take a screencap of the current view ([matplotlib](https://github.com/matplotlib/matplotlib) toolbar function)


<img src="media/info-icon.png" width="24px" /> - App Info: information regarding the current version, developers and contact details

<img src="media/convert-icon.png" width="24px" /> - Convert Data: convert the loaded data into .txt file. XRDapp will create a new folder in the same directory as the loaded files and place converted files in it

<img src="media/clear-data-icon.png" width="24px" /> - Clear Data: clear the loaded data cache

# Using XRDapp
Start using XRDapp by pressing <img src="media/import-content.png" width="24px" /> and loading the data. When the data is loaded, you can browse through XRD curves with a help of up and down arrow buttons on your keyboard or by clicking the filename in the loaded files list window. Use <img src="media/temperature-low.png" width="24px" /> to load a .txt file with temperature values, which will be displayed above the viewing window. To zoom in to an area of interest, use <img src="media/mpl_zoom.png" width="24px" />. If the given curve has small intensity (y-axis value), press <img src="media/stretch-vertically.png" width="24px" /> to fit it to the screen. Pressing <img src="media/mpl_home_large.png" width="24px" /> automatically rescales everything back to the highest intensity among all loaded files. To convert loaded files into .txt file, press <img src="media/convert-icon.png" width="24px" />, which will create a folder called "XRDapp converted" in the folder where the data was loaded from. Press either <img src="media/clear-data-icon.png" width="24px" /> to clear the data or <img src="media/import-content.png" width="24px" /> to load different files.

[Samples folder](samples/) contains an example of temperature file and RAW4.0 file.

Video demonstration of the basic XRDapp functionality:

<video src='media/video/demo.mov'> 

# Modifying code
The code provided in this repository can be modified. It is important to note that to ensure that the code can run smoothly on your machine, you need to install [xylib](https://github.com/wojdyr/xylib/tree/master). After that, to build your own executable file, use the following command:
```bash
pyinstaller --name XRDApp --onefile --windowed --icon=media\icon_main.ico --add-data "media;media" xrdapp.py
```

# Credits
Many thanks to:
- the developers of [xylib](https://github.com/wojdyr/xylib) for providing quite a comprehensive tool for working with multiple XRD data formats
- the developer of [raw2xyN](https://github.com/MarcoVando/raw2xyN) for realisation of couple of interesting ideas
