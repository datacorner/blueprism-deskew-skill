# blueprism-deskew-skill
This Blue Prism Skill deskew images (and pdf content) by using a Python (embedded) Web Service. The purpose is pretty simple. If you have any deskewed images like scanned documents this Blue Prism Skill will rotate them automatically to make easier for example the OCR work. The images can also be retrieved from a pdf document as this service is able to extract any pages from a pdf document to manage them as image page per page.
This skill does not work alone as it comes with a separate Web Service developped in Python. The Blue Prism VBO launch (if needed) this web service on the server side and manages the Web services calls to deskew the requested images. In production you should deploy this web service in a separate server (see documentation to use another web server provider as flask to do that). 
![Deskew description](https://raw.githubusercontent.com/datacorner/blueprism-deskew-skill/master/img/bpdeskew.jpg)

To have a better understanding on what this skill do, just have a look on this video : https://www.youtube.com/watch?v=y4KCzo0U46I

# What do you need to make it work properly ?
This skill works with:
* A working Python environment (version 3.6 min) with the libraries described in the chapter "The Python side" below
* Blue Prism version 6.9 (minimum release). A set of dependencies is also needed and described below.

# What's inside this Blue Prism Skill ?
A global description of how this service was built can be found here : https://www.datacorner.fr/bp-deskew/  
The Python deskew library features are described in more details here : https://www.datacorner.fr/deskew/  
NB: This code uses the deskew Python code developped by St�phane Brunner, just take a look on the code on Github here: https://github.com/sbrunner/deskew

The github directory contains several files:  
* **./img/ci_rotated.jpg** it's just a test file (rotated image) you could use once you've installed the skill to check it works  
* **./src folder** contains all the Python code which runs the Web service and do the magic stuff !
* **LocalImagesUtils_X.X.bprelease** Blue Prism Exports (from the version 6.9) of the VBO which harness the Python web service to make easier use of the deskew
* **runWsImageUtils.bat** is a windows command which launch the Web Service to make is in listening mode. This command will be called by the vbo when a deskew will be requested.
* **install_python_packages.cmd** is a windows command which install all the needed python dependencies (by using pip)

# How to install this skill ?
The sections below describes how to use the Blue Prism skill.

## Python configuration
First you have to install a Python environment. I recommand to install Anaconda (https://www.anaconda.com/) or you can just install Python here : https://www.python.org/  
One you've installed Python you'll need ton install additional libraries to make the Web Service work. To do that you can use the pip utility or conda if you're working with anaconda. These are the required libraries :
* numpy (Numpy | pip install numpy)
* skimage (Scikit Image | pip install scikit-image)
* cv2 (OpenCV library | pip install opencv-python)
* flask (Flask | pip install -U Flask)
* jsonpickle (jsonpickle | pip install jsonpickle)
For pdf conversion this skill also uses
* pdf2image ( pip install pdf2image | https://pypi.org/project/pdf2image/)  

You can install all the dependencies by running this command line:  
```
$ pip3 install -r requirements.txt
```

Note: Be careful as this last library uses another tier tool (poppler). Just follow the instructions here to install this in your environment : https://pypi.org/project/pdf2image/
Note (2): a windows command file (install_python_packages.cmd) regroups all these libraries installation directives.  

One all these packages have been sucessfully installed you can start by copying the files (into the Github directory) locally: ie. into a Blue Prism Windows server folder.
Now, open the **runWsImageUtils.bat** file :

This Web service uses Flask to work. So if you're satisfied with this component, don't forget to change some stuff in the code like for example the parameters at the end : app.run(debug=True, host='127.0.0.1', port=8090)
* Switch to False for the debug mode
* Change you serveur address (change the Blue Prism WS wrapper also)
* change you server port (change the Blue Prism WS wrapper also)  

Take a look on the Flask site to see how to deploy in a real production environment : https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/

```
@CALL C:\Users\admin\Anaconda3\Scripts\activate.bat C:\Users\admin\Anaconda3
python "C:\BP Assets\services\imageutils\imageutils.py"
```

You will need to change 2 things :
Line 1 (only if you use Anaconda, otherwise just remove the line). Change the anaconda directory to reflect your Python environment.  
Line 2. Change the directory to reflect where you had copied the files previously.  

Normally you don't have to change anything in the Python code. I know the exception management and other good development stuff is not yet perfect (could it be ?) but i would want it simple and easy to adapt and change. SO don't hesitate to make your modification in there (and share it through Github!).  

If you don't use Anaconda for Python, you could also remove the first line (@CALL C:\Users\admin\Anaconda3\Scripts\activate.bat C:\Users\admin\Anaconda3) from the runWsImageUtils.bat

## Blue Prism configuration

First you have to ensure that libraries are already imported into Blue Prism before importing this skill :
* Utility - Environment
* Utility - JSON
Note: Good news these vbo are by default provided by Blue Prism (by default in the C:\Program Files\Blue Prism Limited\Blue Prism Automate\VBO). However they're not imported, you have to do the import (or checking if they are already installed) manually by yourself before going further.

Once these vbo are imported successfully, you can import the deskew skill:
1. Open the blue Prism Studio and import the bprelease file. One you've done that you should have two new assets: a web service and a vbo (object).
2. If you've made some change in the Python code like for example changing the URL (or the port) you may need now to do some change in the Blue Prism Web Service definition. Otherwise do not change anything at this stage.
3. Change the Blue Prism environment variable value (for pyRunImageUtilsCommandLine) to refer to the command line path you have copied (in the GitHub bundle this is the runWsImageUtils.bat file) in the Blue Prism Environment variable settings.
4. Open the vbo named pyImageUtils
5. save it

Note: the Blue Prism export is compatible for Blue Prism 6.9 and later.

## Last check

The new skill should work now. Just run the deskew action (in the pyImageUtils object) and see the generated image (Cf. https://www.datacorner.fr/bp-deskew/)

# in case of troubles

Please add an issue into Github here : https://github.com/datacorner/blueprism-deskew-skill/issues  
You can also add a comment in my website here : https://www.datacorner.fr/bp-deskew/  

# Terms of use

This code is free, and distributed under the GNU General Public License version 3 (GPL v3). Essentially, this means that you are free to do almost exactly what you want with the program, including distributing it among your friends, making it available for download from your web site, selling it (either by itself or as part of some bigger software package), or using it as the starting point for a software project of your own.  

The only real limitation is that whenever you distribute this code in some way, you must always include the full source code, or a pointer to where the source code can be found. If you make any changes to the source code, these changes must also be made available under the GPL.

For full details, read the copy of the GPL v3 found in the file named Copying.txt.
