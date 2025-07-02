# MemphisRider for NFSU2
Originally conceived as a tool to export and import car presets between save games and Binary, MemphisRider kinda grew into a profile (save game) garage management tool; besides the aformentioned preset import/export feature, you can also export/import entire customized car slots, clear (delete) them and even sort them out. 

## Additional thanks to
* Tango Desktop Project for the UI icons
* [TerminatorVasya](https://github.com/TVasya) for the string hashing code

## Features
* Python-based, so it can be run in platforms besides Windows; Python script and standalone Windows application included.
* Import, export, clear (delete) customized car slots in save games; can also import/export them to Binary preset data for use in career mode as player car, opponent or quick race sponsor.
* Ability to sort customized car slots.
* Ability to add XNAMEs to support add-on cars, with automatic string hashing.
* Ability to change XNAMEs of serialized Binary preset data.

## Requirements
* Python 3 (tested with Python 3.8, 3.10 and 3.13) for script version.
  * Linux users might have to install IDLE3 because it uses one of it's libraries.
  * Windows 7 users can use standalone version as long they have installed the latest VC++ Redistributables (x86); script version needs the [PythonWin7](https://github.com/adang1345/PythonWin7) fork installed.

## Installation/Use
* Unzip the MemphisRider_winExe folder if you're using the Windows standalone app or MemphisRider.py file if you're using the script version.
* For the Windows standalone app: open the MemphisRider_winExe folder and run MemphisRider.exe
* For the Python script version:
  * On Windows:
    * If you have Python 3 as your default Python instance, just double click the MemphisRider.py file
    * Alternatively, open a Powershell/Command Prompt window in the folder you have the MemphisRider.py file and type ``py MemphisRider.py`` and press Enter
  * On Linux:
    * Make the MemphisRider.py file executable by opening a Terminal window in the folder you have the NFS_FCEPaintBooth.py file, then type ``chmod +x MemphisRider.py`` and press Enter
    * If you have Python 3 as your default Python instance, just double click the MemphisRider.py file
    * Alternatively, open a Terminal window in the folder you have the MemphisRider.py file and type ``python3 MemphisRider.py`` and press Enter
* Remember to back up your profile before opening it with MemphisRider in case something goes wrong.

## Construction
|Programs used|Known bugs|May be incompatible with|
|--|--|--|
|IDLE, GIMP (icons)|Imported presets might not appear if imported to locked Career garage slots in profiles that haven't unlocked all car slots in Career garage. To fix it, clear the slot and import again.|No incompatibilites found so far|


