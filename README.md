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
* **runWsImageUtils.bat** is a windows command which launch the Web Service to make is in listening mode. This command will be called by the vbo when a deskew will be requested.

# How to install this skill ?
The sections below describes how to use the Blue Prism skill.

## The Python side
First you have to install a Python environment. I recommand to install Anaconda (https://www.anaconda.com/) or you can just install Python here : https://www.python.org/  
One you've installed Python you'll need ton install additional libraries to make the Web Service work. To do that you can use the pip utility or conda if you're working with anaconda. These are the required libraries :
* numpy (just install by typing in the command line pip install numpy)
* skimage
* deskew
* cv2
* flask
* jsonpickle

One all these packages have been sucessfully installed you can start by copying the files (into the Github directory) locally: ie. into a Blue Prism Windows server folder.
Now, open the **runWsImageUtils.bat** file :

```
@CALL C:\Users\admin\Anaconda3\Scripts\activate.bat C:\Users\admin\Anaconda3
python "C:\BP Assets\services\imageutils\imageutils.py"
```

You will need to change 2 things :
1. Change the anaconda directory to reflect your Python environment.  
2. Change the directory to reflect where you had copied the files previously.  

Normally you don't have to change anything in the Python code. I know the exception management and other good developer stuff is not yet done but i would want it simple and easy to adapt and change. SO don't hesitate to make your modification in there (and share it through Github!).  

## The Blue Prism side

The Blue Prism stuff is really easy to deploy and use.
1. Open the blue Prism Studio and import the bprelease file. One you've done that you should have two new assets: a web service and a vbo (object).
2. If you've made some change in the Python code like for example changing the URL (or the port) you may need now to do some change in the Blue Prism Web Service definition. Otherwise do not change anything at this stage.
3. Open the vbo named pyImageUtils
4. select the run service action (tab) and change the data item command to reflect your environment.
5. save it

Note: the Blue Prism export is compatible for Blue Prism 6.8 and later.

## Last check

The new skill should work now. Just run the deskew action (in the pyImageUtils object) and see the generated image (Cf. https://www.datacorner.fr/bp-deskew/)

# in case of troubles

If you have any troubles in using or deploying this skill just put a comment in my website here : https://www.datacorner.fr/bp-deskew/ 

# Terms of use

This code is free, and distributed under the GNU General Public License version 3 (GPL v3). Essentially, this means that you are free to do almost exactly what you want with the program, including distributing it among your friends, making it available for download from your web site, selling it (either by itself or as part of some bigger software package), or using it as the starting point for a software project of your own.  

The only real limitation is that whenever you distribute this code in some way, you must always include the full source code, or a pointer to where the source code can be found. If you make any changes to the source code, these changes must also be made available under the GPL.

For full details, read the copy of the GPL v3 found in the file named Copying.txt.
