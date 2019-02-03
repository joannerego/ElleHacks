import io
import os
import json
from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToJson
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from picturegrabber import *

# Set up credentials for google sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('ellehacks-131b924b6792.json', scope)
gs = gspread.authorize(credentials)

# Open the sheet then clear the previous results
worksheet = gs.open("URLs").sheet1
cellrange = worksheet.range('A2:D420')
for cell in cellrange:
    cell.value = ''
worksheet.update_cells(cellrange)

# Set up the Google credentials that's necessary to run this
credenpath = 'C:\\Users\sassy\Documents\ellehacks-72465fb9c9e4.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credenpath

# Instantiates a client
client = vision.ImageAnnotatorClient()
grabber = PictureGrabber('http://www.airliners.net/')

# Gets the file name of the image to use
files = []
images = []
things = []
urls = grabber.geturls()
print(urls)
files = (os.listdir('resources'))

for file in files:
    file_name = os.path.join(os.path.dirname(__file__), 'resources' + '\\' + file)
    # print(file_name)

    # Load the image into memory (open the file I guess)
    with (io.open(file_name, 'rb')) as image_file:
        content = image_file.read()
        images.append(content)


x = 2 # Used for looping through the spreadsheet
for picture in urls:
    url = types.ImageSource(image_uri=picture)  # Change a string into URL that google understands
    image = types.Image(source=url)  # Using 'source' instead of 'content' allows us to use URLs instead of files
    worksheet.update_cell(x, 1, picture)


    # Performs label dectection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    #Image properties?
    text = client.document_text_detection(image=image)
    texts = text.text_annotations

    # Face properties
    face = client.face_detection(image=image)
    faces = face.face_annotations

    # Use a for loop for all the text descriptions
    textstring = ""
    for word in texts:
        textstring += word.description + " "
        worksheet.update_cell(x, 3, textstring)

    # Adds labels to the spreadsheet
    labelstring = ""
    for label in labels:
        labelstring += label.description + " "
        worksheet.update_cell(x, 2, labelstring)


    for nose in faces:
        worksheet.update_cell(x, 4, nose.joy_likelihood)
    x += 1


# keys = urls
# values = things
# print(type(labels))
# goodvalues = MessageToJson(labels)
# dick = dict(zip(keys, goodvalues))
# print(dick)
#
# jason = json.dumps(dick)
# print(jason)
