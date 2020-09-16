# blueprism-deskew-skill
This Blue Prism Skill deskew images by using Python (embedded) Web Service. The purpose is pretty simple. If you have any deskewed images like scanned documents this Blue Prism Skill will rotate them automatically to make easier for example the OCR work.  
This skill does not work alone. It comes with a separate Web Service developped in Python with the deskew library (describred here https://github.com/sbrunner/deskew). The Blue Prism VBO launch (if needed) this web service on the server side and manages the Web services calls to deskew the requested images.
![Deskew description](https://raw.githubusercontent.com/datacorner/blueprism-deskew-skill/master/img/bpdeskew.jpg)

# What's inside this Blue Prism Skill ?
A global description of how this service was built can be found here : https://www.datacorner.fr/bp-deskew/  
The Python deskew library features are described in more details here : https://www.datacorner.fr/deskew/

The github directory contains several files:  
* **ci_rotated.jpg** it's just a test file (rotated image) you could use once you've installed the skill to check it works  
* **imageutils.py** contains the Python code which deploys the Web service and do the magic stuff !
* **LocalImagesUtils_X.X.bprelease** Blue Prism Exports (from the version 6.8) of the VBO which harness the Python web service to make easier use of the deskew
* **runWsImageUtils.bat** is a windows command which launch the Web Service to make is in listening mode.
