import PIL
from PIL import Image
from numpy import array, moveaxis, indices, dstack
import pandas as pd
import os
import re
import base64
import codecs
image_path = r'C:\Anode\Images'
csvs = [f for f in os.scandir(image_path) if f]
images = []
csv_dir = 'C:/Anode/Images'
df = pd.DataFrame()
image_data=''
df["Tank"]=''
for image_file in csvs:
    if image_file.path.endswith('.JPG'):    
        basewidth = 300
        img = Image.open(image_file.path)
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        resizedir = r'C:/Anode/resized/'
        if not os.path.exists(resizedir):
            os.makedirs(resizedir)
        img.save(resizedir+ image_file.name)
        with open(resizedir + image_file.name, "rb") as f:
            data = f.read()
            img_data = (codecs.encode(obj = data, encoding = "base64"))
            data = "data:image/jpeg;base64," + img_data.decode('utf-8')
            #data = data[1:].replace("'", "")
            print(len(data))
            name =image_file.name[:6]
            print(name)
            dataset = {'Tank': name,
                    'Image':data,}
            df = df.append(dataset, ignore_index = True)
df.to_csv(r'C:\Anode\g.csv', index = False)
