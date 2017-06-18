import os,sys
from urllib.request import Request,urlopen
import tinify
import threading
import time

#key list 现在是多个，免费的账户有每个使用500次的限制
keys = ["key1","key2","key3"]
suffix = ["png",'jpg']

global timo_has_done
timo_has_done = 0

def get_image_filenames(input_dir):    
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



def do_timo(filename,total,now_dir_name,new_dir_name,index):
    out_name = filename.replace(now_dir_name,new_dir_name,1)
    source = tinify.from_file(filename)
    source.to_file(out_name)
    global timo_has_done
    timo_has_done += 1
    print("{0} has done ,total {1},completed {2}".format(out_name,total,timo_has_done))


def main():
    if(len(sys.argv)>1):

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
            print("convert start ...")
            threads = []
            for index,image_name in enumerate(image_names):
               threads.append(threading.Thread(target=do_timo,args=(image_name,total,now_dir_name,new_dir_name,index)))
            for t in threads:
                t.start()
        else:
            print("please check your key list,compression count may be full !!!")
       
def dirlist(path, allfile,now_dir_name,new_dir_name):  
    filelist =  os.listdir(path)  
  
    for filename in filelist:  
        filepath = os.path.join(path, filename)  
        if os.path.isdir(filepath):           
            dirlist(filepath, allfile,now_dir_name,new_dir_name)
            allfile.append(filepath.replace(now_dir_name,new_dir_name,1))  
    return allfile


if __name__ == '__main__':
    main()