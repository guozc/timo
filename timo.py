import os,sys
from urllib.request import Request,urlopen
import tinify
import threading
import time
import base64
from PIL import Image
import shutil
import json

keys = ["yourkey1","yourkey2","yourkey3"]
suffix = ["png","jpg","JPG","JEPG","jepg","PNG"]
suffixMp3 = ["mp3","MP3"]

global timo_has_done
timo_has_done = 0
global base64_has_done
base64_has_done = 0

def get_image_filenames(input_dir):
    image_name_list = []    
    for fn in os.listdir(input_dir):
        if len(fn.split("."))>1:
            if fn.split(".")[-1] in suffix:
                image_name_list.append(fn)
    return image_name_list

image_name_list = []
def get_all_images(input_dir):
    for fn in os.listdir(input_dir):
        filepath = os.path.join(input_dir, fn)
        if os.path.isdir(filepath):           
            get_all_images(filepath)            
        if len(filepath.split("."))>1:
            if filepath.split(".")[-1] in suffix:
                image_name_list.append(filepath)
    return image_name_list

audio_name_list = []
def get_all_audios(input_dir):
    for fn in os.listdir(input_dir):
        filepath = os.path.join(input_dir, fn)
        if os.path.isdir(filepath):           
            get_all_audios(filepath)            
        if len(filepath.split("."))>1:
            if filepath.split(".")[-1] in suffixMp3:
                audio_name_list.append(filepath)
    return audio_name_list

def removeDir(dirPath):
    if not os.path.isdir(dirPath):
        return
    files = os.listdir(dirPath)
    for file in files:
        filePath = os.path.join(dirPath, file)
        if os.path.isfile(filePath):
            os.remove(filePath)
        elif os.path.isdir(filePath):
            removeDir(filePath)
    os.rmdir(dirPath)
       
def dirlist(path, allfile,now_dir_name,new_dir_name):  
    filelist =  os.listdir(path)  
  
    for filename in filelist:  
        filepath = os.path.join(path, filename)  
        if os.path.isdir(filepath):           
            dirlist(filepath, allfile,now_dir_name,new_dir_name)
            allfile.append(filepath.replace(now_dir_name,new_dir_name,1))  
    return allfile

#mode 1 根据百分比;2 根据宽
def do_timo(filename,total,now_dir_name,new_dir_name,index,scale_num,mode):
    out_name = filename.replace(now_dir_name,new_dir_name,1)
  
    if mode is 2:
        scaleWidth = scale_num
        if scaleWidth is not None and scaleWidth is not "":
            source = tinify.from_file(filename)
            resized = source.resize(
                method="scale",
                width = scaleWidth
            )
            resized.to_file(out_name)
        else:
            source = tinify.from_file(filename)
            source.to_file(out_name)            
    else:
        scale_percentage = scale_num
        if scale_percentage < 1:
            image_width = Image.open(filename).size[0]
            image_height = Image.open(filename).size[1]
            source = tinify.from_file(filename)
            resized = source.resize(
                method="fit",
                width = int(image_width*scale_percentage),
                height = int(image_height*scale_percentage)
            )
            resized.to_file(out_name)
        else:
            source = tinify.from_file(filename)
            source.to_file(out_name)

    global timo_has_done
    timo_has_done += 1
    print("{0} has done ,total {1},completed {2}".format(out_name,total,timo_has_done))



preimage = "data:image/png;base64,"
def do_base64(filename,total,now_dir_name,new_dir_name,index):    
    from_png = open(filename,'rb')
    base_temp = base64.b64encode(from_png.read())  
    to_txt = open(filename.replace(now_dir_name,new_dir_name)+".txt",'w')
    to_txt.write(preimage+str(base_temp)[2:-1])
    from_png.close()
    to_txt.close()
    global base64_has_done
    base64_has_done += 1
    print("{0} has done ,total {1},completed {2}".format(filename.replace(now_dir_name,new_dir_name)+".txt",total,base64_has_done))

preaudio = "data:audio/mp3;base64,"
def do_base64_audio(filename,total,now_dir_name,new_dir_name,index):    
    from_png = open(filename,'rb')
    base_temp = base64.b64encode(from_png.read())  
    to_txt = open(filename.replace(now_dir_name,new_dir_name)+".txt",'w')
    to_txt.write(preaudio+str(base_temp)[2:-1])
    from_png.close()
    to_txt.close()
    global base64_has_done
    base64_has_done += 1
    print("{0} has done ,total {1},completed {2}".format(filename.replace(now_dir_name,new_dir_name)+".txt",total,base64_has_done))

def do_tinify_list():
    print("validate keys ...")
    input_dir = sys.argv[1]
    now_dir_name = input_dir.split("\\")[-1]
    new_dir_name = "new_image_{0}".format(int(time.time()))
    output_dir = "./"+new_dir_name

    #建立新的目录及子目录
    dir_list = dirlist(input_dir,[],now_dir_name,new_dir_name)
    os.mkdir(output_dir)
    for dir_path in dir_list[::-1]:
        os.mkdir(dir_path)

    image_names = get_all_images(input_dir)
    total = len(image_names)

    #判断使用哪个Key,一个Key只能使用500次
    key_effective = False
    for key in keys:
        tinify.key = key
        tinify.validate()
        remain = 500-tinify.compression_count
        if remain>total:
            key_effective = True
            break

    if key_effective:
        print("now_key:"+tinify.key)
        #get scale

        mode = input("\nselect scale mode :\n[1]scale by percentage\n[2]scale by fixed width\nenter your choice (default=1):")
        if mode is not "2" :
            mode = 1
        else:
            mode = 2
        print("Scale mode is {0}".format(mode))

        if mode is 1:
            scale_percentage = input("enter scale_percentage,0<scale_percentage<=100,default = 100 :")
            try:
                scale_percentage = float(scale_percentage);
                if scale_percentage>=100.0 or scale_percentage<0:
                    scale_percentage = 100.0
            except:
                scale_percentage = 100.0
            print("convert scale_percentage is "+str(scale_percentage)+"%")
            scale_percentage = scale_percentage/100

            print("convert start ...")
            threads = []
            for index,image_name in enumerate(image_names):
               #threads.append(threading.Thread(target=do_timo,args=(image_name,total,now_dir_name,new_dir_name,index,scale_percentage,2)))
               threads.append(threading.Thread(target=do_timo,args=(image_name,total,now_dir_name,new_dir_name,index,scale_percentage,1)))
            for t in threads:
                t.start()
        elif mode is 2:
            fixedWidth = input("enter fixed width(integer) ,default or wrong input cause no scale:")
            try:
                fixedWidth = int(fixedWidth)
                print("fixed width is {0}".format(fixedWidth))
            except:
                fixedWidth = None
                print("will be no scale")

            print("convert start ...")
            threads = []
            for index,image_name in enumerate(image_names):
               #threads.append(threading.Thread(target=do_timo,args=(image_name,total,now_dir_name,new_dir_name,index,scale_percentage,2)))
               threads.append(threading.Thread(target=do_timo,args=(image_name,total,now_dir_name,new_dir_name,index,fixedWidth,2)))
            for t in threads:
                t.start()
    else:
        print("please check your key list,compression count may be full !!!")






def do_base64_list():
    input_dir = sys.argv[1]
    now_dir_name = input_dir.split("\\")[-1]
    new_dir_name = "base64_"+now_dir_name
    output_dir = "./"+new_dir_name

    #建立新的目录及子目录
    dir_list = dirlist(input_dir,[],now_dir_name,new_dir_name)
    if os.path.exists(output_dir):
        removeDir(output_dir)
    os.mkdir(output_dir)
    for dir_path in dir_list[::-1]:
        os.mkdir(dir_path)

    image_names = get_all_images(input_dir)
    total = len(image_names)

    print("convert base64 start ...")
    threads = []
    for index,image_name in enumerate(image_names):
       threads.append(threading.Thread(target=do_base64,args=(image_name,total,now_dir_name,new_dir_name,index)))
    for t in threads:
        t.start()

def do_base64_list_audio():
    input_dir = sys.argv[1]
    now_dir_name = input_dir.split("\\")[-1]
    new_dir_name = "base64_"+now_dir_name
    output_dir = "./"+new_dir_name

    #建立新的目录及子目录
    dir_list = dirlist(input_dir,[],now_dir_name,new_dir_name)
    if os.path.exists(output_dir):
        removeDir(output_dir)
    os.mkdir(output_dir)
    for dir_path in dir_list[::-1]:
        os.mkdir(dir_path)

    audio_names = get_all_audios(input_dir)
    total = len(audio_names)

    print("convert base64 start ...")
    threads = []
    for index,audio_name in enumerate(audio_names):
       threads.append(threading.Thread(target=do_base64_audio,args=(audio_name,total,now_dir_name,new_dir_name,index)))
    for t in threads:
        t.start()

def do_clip_rename(start_num):
    input_dir = sys.argv[1]
    temp_dir_name = "temp_{0}".format(int(time.time()))
    os.mkdir(input_dir+"\\"+temp_dir_name)
    image_names = get_image_filenames(input_dir)
    try:
        image_names.sort(key=lambda x:int(x.split(".")[-2]))
    except:        
        image_names = get_image_filenames(input_dir)
    print(image_names)
    for i in image_names:
        shutil.move(input_dir+"\\"+i,input_dir+"\\"+temp_dir_name+"\\"+i)

    for i in image_names:
        print(i);
        shutil.move(input_dir+"\\"+temp_dir_name+"\\"+i,input_dir+"\\"+str(start_num)+"."+i.split(".")[-1])
        start_num = start_num+1
    shutil.rmtree(input_dir+"\\"+temp_dir_name)

def do_get_all_imagePath():
    input_dir = sys.argv[1]
    fo = open("foo.txt", "wb")
    json_str = json.dumps(get_all_images(input_dir))
    fo.write(str(json_str).replace("\\\\","\\").replace(input_dir,input_dir.split("\\")[-1]).replace("\\","/").encode(encoding="utf-8"));
    fo.close()

def main():
    if(len(sys.argv)>1):
        feature = input("choose function: \n[1]tinify\n[2]ImageToBase64;\n[3]clip image rename\n[4]get all imagePath\n[5]AudioToBase64;\nenter your choice and press enter:")

        #tinify
        if feature == "1":
            do_tinify_list()
        #base64
        elif feature == "2":
            do_base64_list()
        elif feature == "3":
            start_num = input("enter start number(default=0): ")
            try:
                start_num = int(start_num)
            except:
                start_num = 0
            print("start_num is {0}".format(start_num))
            do_clip_rename(start_num)
        elif feature == "4":
            do_get_all_imagePath()
        elif feature == "5":
            do_base64_list_audio()
if __name__ == '__main__':
    main()