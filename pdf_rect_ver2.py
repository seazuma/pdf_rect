import os
import shutil
import glob
import pdf2image
import configparser
from PIL import Image,ImageDraw
import numpy as np
import sys

def clear_log_file():
    if LOG_FILE!="":
        with open(LOG_FILE, 'w') as log_file:
            log_file.write("")

def log(message):
    # print(message)
    if LOG_FILE!="":
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(f"{message}\n")

def compare_images(img1, img2): # img2 = template
    n1 = np.array(img1)
    n2 = np.array(img2) 
    Y2,X2,_ = np.shape(n2)
    diff = np.max( np.abs( n1[:Y2, :X2, :] - n2 ) )
    log(str(diff))
    return diff

def load_templates(template_path):
    templates = {}
    png_search = template_path+"template_*.png" 
    for png_path in glob.iglob(png_search):
        key = png_path.split("template_")[-1].split(".png")[0]
        template = Image.open(png_path)
        if template.mode == 'RGBA':
            template = template.convert('RGB')
        templates[key] = template
    return templates

def match_template(img, templates):
    for key, template_img in templates.items():
        diff = compare_images(img, template_img)
        if diff<64:
            return key # matched
    return ""

def process(input_path, output_path, template_path, failed_path, page_start, page_end):
    count = [0,0]
    templates = load_templates(template_path)
    log(f"Found {len(templates)} templates")
    log(f"mypdf2png from {input_path} to {output_path}, page: {page_start} - {page_end}")
    pdf_search = input_path+"*.pdf" 
    for pdf_path in glob.iglob(pdf_search):
        print(f"Load: {pdf_path}")
        try:
            page_list = pdf2image.convert_from_path(pdf_path, first_page=page_start, last_page=page_end, poppler_path=poppler_path)
        except:
            log("Error in pdf2image.convert_from_path")
            continue
        for page_num in range(max(0,page_start-1), min(len(page_list),page_end)):
            log(page_num)
            img = page_list[page_num]
            png_filename = pdf_path[len(input_path):].replace(".pdf", f"_{page_num+1}.png")
            key = match_template(img, templates)
            if key=="":
                if failed_path != "":
                    os.makedirs(failed_path, exist_ok=True)
                    failed_filepath = os.path.join(failed_path, png_filename)
                    img.save(failed_filepath)
                print(f"Failed: {png_filename}")
                count[1]+=1
                continue
            log(f"Matched :{key}")
            try:
                config_layout = configparser.ConfigParser()
                layoutfile_path = os.path.join(template_path, f"layout_{key}.ini")
                config_layout.read(layoutfile_path)
            except:
                log(f"Error in loading {layoutfile_path}")                            
                continue
            for section in config_layout:
                key_list = ["left","top","right","bottom"]
                position = []
                for key in key_list:
                    if key in config_layout[section]:
                       position.append( int(config_layout[section][key]) )
                if len(position) == 4:
                    draw = ImageDraw.Draw(img)
                    draw.rectangle(position, fill=(0,0,0))
            os.makedirs(output_path, exist_ok=True)
            savepath = os.path.join(output_path, png_filename)
            img.save(savepath)
            print(f"Succeed: {png_filename}")
            count[0] += 1
    return count
           
if True: #__name__ == "__main__":
    config = configparser.ConfigParser()
    try:
        config.read("pdf_rect_files/config.ini")
    except:
        print("Failed to open pdf_rect_files/config.ini")
        os.system('PAUSE')
        sys.exit()
    for key in ["poppler_path","input_path","output_path","template_path"]:
        if not key in config["setting"]:
             print(f"Failed to load {key} from config.ini")
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
    input_path = config["setting"]["input_path"]
    output_path = config["setting"]["output_path"]
    template_path = config["setting"]["template_path"]  
    failed_path = config["setting"]["failed_output_path"] if "failed_output_path" in config["setting"] else ""
    LOG_FILE = config["setting"]["log_file"] if "log_file" in config["setting"] else ""
    page_start = int(config["setting"]["page_start"]) if "page_start" in config["setting"] else 1
    page_end = int(config["setting"]["page_end"]) if "page_end" in config["setting"] else 1
    clear_log_file()
    pattern = os.path.join(output_path, "*.png")
    png_files = glob.glob(pattern)
    if png_files:
        user_input = input("Warning: png file found in output. Continue? (y/n): ")
        if user_input.lower() != "y":
            sys.exit()
    count = process(input_path,  output_path, template_path, failed_path, page_start, page_end)
    print(f"Succeed:{count[0]}, Failed: {count[1]}")
    os.system('PAUSE')

