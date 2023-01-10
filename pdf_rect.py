import os
import glob
import pdf2image
import configparser
from PIL import ImageDraw

config = configparser.ConfigParser()
config.read("config.ini")

poppler_search = ""
if "poppler_path" in config["setting"]:
    poppler_search = config["setting"]["poppler_path"]
poppler_path_list = glob.glob(poppler_search + "poppler*/bin")
if len(poppler_path_list) != 0 :
    poppler_path = poppler_path_list[0]
else:
    poppler_path_list = glob.glob("bin*")
    if len(poppler_path_list) != 0 :
        poppler_path = poppler_path_list[0]

input = config["setting"]["input_path"]
output = config["setting"]["output_path"]
page_start = int(config["setting"]["page_start"])
page_end = int(config["setting"]["page_end"])

config_layout = configparser.ConfigParser()
config_layout.read(config["setting"]["layout"])

pdf_search = input+"*.pdf" 

for pdf_path in glob.iglob(pdf_search):
    print("Load: " + pdf_path)
    try:
        page_list = pdf2image.convert_from_path(pdf_path, first_page=page_start, last_page=page_end, poppler_path= poppler_path)
    except:
        print("Error")
        continue
    for pi in range(page_end-page_start+1):
        if pi >= len(page_list):
            break
        im = page_list[pi]
        W,H = im.width,im.height
        for section in config_layout:
            key_list = ["left","top","right","bottom"]
            position = []
            for key in key_list:
                if key in config_layout[section]:
                    position.append( int(config_layout[section][key]) )
            if len(position) == 4:
                colors = [0,0,0]
                for ci,c_key in enumerate(["color_r","color_g","color_b"]):
                    if c_key in config_layout[section]:
                        colors[ci] = int(config_layout[section][c_key])
                draw = ImageDraw.Draw(im)
                draw.rectangle(position, fill=tuple(colors))
        output_path = output + pdf_path[len(input):len(pdf_path)-4] + "_"+str(page_start+pi)+".png"
        for i in range(len(output_path)):
            if output_path[i]=="/" or output_path[i]=="\\":
                 dirname = output_path[:i]
                 if not os.path.isdir(dirname):
                     print("Makedir: " + output_path[:i])
                     os.makedirs(dirname, exist_ok=True)
        im.save(output_path)
        print("Save: " + output_path)
os.system('PAUSE')