import numpy as np
from numpy import asarray
import sys
from skimage import io
from skimage.transform import rotate
from skimage.color import rgb2gray
from deskew import determine_skew
import jsonpickle
import cv2
from flask import Flask, request, Response
from pdf2image import convert_from_path, convert_from_bytes

app = Flask(__name__)

def trace(logtext):
    """Just put a trace in the excecution window (command)
    Parameters
        logtext : Text to display
    Return
        Nothing
    """
    print("---> " + logtext)

def deskew_image(image):
    """This function effectively deskew the image.
    Parameters
        image : Image in binary format (use cv2.imdecode before)
    Return
        rotated image (deskewed)
    """
    trace("Deskew image")
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
    """This function is also a web service call route (/check).
    Parameters
        Nothing
    Return
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
    """This function is also a web service call route (/deskew). it deskew an image (image format)
    HTTP GET Parameter:
        targetfile : filename to the target file (in which the deskewed image will be stored)
    HTTP POST Parameter:
         file : binary file sent through the POST http request as single file
    Parameters
        Nothing
    Return
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
        
        cv2.imwrite(targetfile, image_out)
        trace("Save file < {0}  >".format(targetfile))
        
        output['status'] = "Saved"
        # Prepare response, encode JSON to return
        response_pickled = jsonpickle.encode(output)
    except:
        response_pickled = "{'status' : 'Error while deskewing image' }"

    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/deskewpdf', methods=['POST'])
def deskewpdf():
    """This function is also a web service call route (/deskew). it deskew a set of images included in a pdf file
    HTTP GET Parameter:
        targetdirectory : filename to the target file (in which the deskewed image will be stored)
        pages: list here the pages to extract from the pdf file (separated by a comma). If nothing specified all pages will be extracted and saved.
        filenameprefix: set the filename prefix for the deskewed images into the target directory
    HTTP POST Parameter:
         file : binary file sent through the POST http request as single file
    Parameters
        Nothing
    Return
        output (JSON format): if the value is "{'status' : 'Saved' }" that means the the image has been saved correctly
    """

    output = {}
    
    try:
        # Get destination directory
        targetdirectory = request.args.get("targetdirectory")
        trace("Destination directory < {0} >".format(targetdirectory))
        
        # Get Pages to extract
        pagetoextract = request.args.get("pages")
        trace("Requested pages to extract < {0} >".format(pagetoextract))

        # Get prefix for the saved images
        prefix = request.args.get("filenameprefix")
        trace("Prefix for image extracted < {0} >".format(prefix))
        
        # Get binary file, convert string of image data to uint8 and decode image
        data = request.data
        trace("Request content (image sent) < {0} ... >".format(data[0:10]))
        
        # read the pdf file
        pdfContents = convert_from_bytes(data)
        trace ("Number of pages in the pdf file: " + str(len(pdfContents)))
        output['Number of pages'] = len(pdfContents)

        # Lists the pages to extract
        pagelist = []
        if (pagetoextract == ""):
            trace ("No pages specified. We're going to extract all the pages!")
            for i in range(len(pdfContents)):
                pagelist.append(str(i+1))
        else:
            pagelist = pagetoextract.split(",")
        trace ("Pages to extract: " + str(pagelist))
        
        # Deskew the images page per page
        for page in pagelist:
            trace("Extract page < {0} ... >".format(int(page.strip())-1))
            pageNum = int(page.strip())-1
            trace("Image < {0} ... >".format(type(pdfContents[pageNum])))
            image_out = deskew_image(asarray(pdfContents[pageNum]))
            targetfilename = targetdirectory + "/" + prefix + str(pageNum) + ".jpg"
            cv2.imwrite(targetfilename, image_out)
            trace("Save file < {0}  >".format(targetfilename))
        
        output['status'] = "Saved"
        # Prepare response, encode JSON to return
        response_pickled = jsonpickle.encode(output)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        response_pickled = "{'status' : 'Error while deskewing image' }"

    return Response(response=response_pickled, status=200, mimetype="application/json")

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8090)