import numpy as np
from skimage import io
from skimage.transform import rotate
from skimage.color import rgb2gray
from deskew import determine_skew
import jsonpickle
import cv2
from flask import Flask, request, Response
app = Flask(__name__)

def trace(logtext):
    """Just put a trace in the excecution window (command)
 
    Parameters
    ----------
    items : logtext
        Text to display
    Return
    ------
        Nothing
    """
    print("---> " + logtext)

def deskew_image(image):
    """This function effectively deskew the image.
 
    Parameters
    ----------
    items : image
        Image in binary format (use cv2.imdecode before)
    Return
    ------
        rotated image (deskewed)
    """
    trace("Deskew Image")
    # switch to grayscale the image first
    grayscale = rgb2gray(image)
    # Calculate the rotation angle
    angle = determine_skew(grayscale)
    # deskew the image
    rotated = rotate(image, angle, resize=True) * 255
    return rotated.astype(np.uint8)

# Check
@app.route('/check', methods=['GET'])
def check():
    """This function is also a web service call route (/check). it
 
    Parameters
    ----------
    items : image
        Image in binary format (use cv2.imdecode before)
    Return
    ------
        output (JSON format): if the value is "{'status' : 'Service running' }" that means the service is ok.
    """
    output = {}
    try:
        output['status'] = "Service running"
        response_pickled = jsonpickle.encode(output)
    except:
        response_pickled = "{'status' : 'Error while checking service availability' }"
        
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/deskew', methods=['POST'])
def deskew():
    """This function is also a web service call route (/check). it
    
    HTTP GET Parameter:
        targetfile : filename to the target file (in which the deskewed image will be stored)
    HTTP POST Parameter:
         file : binary file sent through the POST http request as single file
         
    Parameters
    ----------
        Nothing
    Return
    ------
        output (JSON format): if the value is "{'status' : 'Saved' }" that means the the image has been saved correctly
    """

    output = {}
    
    try:
        # Get destination filename
        targetfile = request.args.get("targetfile")
        
        # Get binary file, convert string of image data to uint8 and decode image
        data = request.data
        trace("Request content < {0} ... >".format(data[0:50]))
        
        nparr = np.frombuffer(data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image_out = deskew_image(image)
        trace("Image output < {0} ... >".format(image_out[0:50]))
        
        cv2.imwrite(targetfile, image_out)
        trace("Save file < {0}  >".format(targetfile))
        
        output['status'] = "Saved"
        # Prepare response, encode JSON to return
        response_pickled = jsonpickle.encode(output)
    except:
        response_pickled = "{'status' : 'Error while deskewing image' }"

    return Response(response=response_pickled, status=200, mimetype="application/json")

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8090)