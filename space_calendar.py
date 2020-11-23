import requests
import urllib.request
from tkinter import *
from tkcalendar import *
from PIL import Image, ImageTk
import base64, io

#Commented out for security reasons
apiKey = 'smk2vJYgU4G8EzOnuwBFnQaOvcmTbd5vzDfh6DRm'

root = Tk()
root.title('Space Calendar')
root.geometry("1000x1000")

cal = Calendar(root, selectmode="day")
cal.pack(pady=20, fill = "both", expand = True)

##Gets the JSON value for the given date
def fetchAPOD(deadVar):
    URL_APOD = "https://api.nasa.gov/planetary/apod"
    params = {
    'api_key' : apiKey,
    'date' : deadVar,
    'hd' : 'True'
    }
    return requests.get(URL_APOD, params = params).json()

#Displays the selected date's info and image on the GUI
def get_image():
    selection = str(cal.selection_get().year) + "-" + str(cal.selection_get().month) + "-" + str(cal.selection_get().day)
    selection = fetchAPOD(selection)
    label.config(text = "Title: " + selection["title"])
    explanation.config(text = selection["explanation"])
    explanation.pack()

    #Get image out of jpg, since Tkinter can't use that
    r = requests.get(selection["hdurl"], stream = True)
    aux_im = Image.open(io.BytesIO(r.content))
    aux_im = aux_im.resize((750, 750), Image.ANTIALIAS)
    aux_im = ImageTk.PhotoImage(aux_im)
    img_label.config(image = aux_im)
    img_label.image = aux_im #Need this to prevent image from disappearing b/c of Tkinter quirks

button = Button(root, text = "Get image", command = get_image)
button.pack()

label = Label(root, text = "")
label.pack()

explanation = Label(root, text = "", wraplength = 900)
explanation.pack()

img_label = Label(root, image = "")
img_label.pack()

root.mainloop()
