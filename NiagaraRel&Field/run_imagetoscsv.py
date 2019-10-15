import PIL
from PIL import Image
from numpy import array, moveaxis, indices, dstack
import pandas as pd
import os
import re
import base64
import codecs
image_path = r'H:\RDDEPT\Satellite Lab\Reliability EC Folders\EC06619 -NIAGARA 2018 TAKASHI\NL TESTING 2019\Photos\2.-Test Time\Thermal Pictures'
subdirs = [f.path for f in os.scandir(image_path) if f.is_dir()]
groups =  {
    "E11":'1',

    'E9':"1",
    'E8':"1",
    'G12':"2",
    'G9':"2",
    'G7':"3",
    'G6':"3",
    'G5':"3",
    'G4':"3",
    'G3':"3",
    'G13':"2",
    'G14':"2",
    'G15':"2",
    'H10':"2",
    'G2':"3",
    "H8":"Low Flow",
    "H9":"Low Flow"
}
images = []
csv_dir = 'C:/Niagara/Images'
df = pd.DataFrame()
image_data=''
df['Date']=''
df["Image"]=''
df["Station"]=''
for sub in subdirs:
    print(sub)
    for image_file in os.scandir(sub):
        if image_file.path.endswith('.JPG'):
            with open(image_file.path, "rb") as f:
                data = f.read()
                img_data = (codecs.encode(obj = data, encoding = "base64"))
                data = "data:image/jpeg;base64," + img_data.decode('utf-8')
                #data = data[1:].replace("'", "")
                print(len(data))
                name =re.sub(r'-.*', "", image_file.name[:-4])
                print(name)
                dataset = {'Station': name,
                        'Date':sub.split('\\')[-1],
                        'Image':data,
                        'Group' : groups.get(name)}
                df = df.append(dataset, ignore_index = True)

with open("saved.jpg", "wb") as fh:
    fh.write(base64.decodebytes(img_data))
df.to_csv(r'C:\Niagara\g.csv', index = False)
