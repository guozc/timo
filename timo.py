import os,sys
import tinify
import threading
import time


key = "your key " #enter your key
tinify.key = key
suffix = ["png",'jpg']

global timo_has_done
timo_has_done = 0

def get_image_filenames(input_dir):
    image_name_list = []
    for fn in os.listdir(input_dir):
        if len(fn.split("."))>1:
            if fn.split(".")[-1] in suffix:
                image_name_list.append(fn)
    return image_name_list

def do_timo(filename,total,input_dir,output_dir,index,isperfix,perfix):
    out_name = filename
    if isperfix:
        out_name = perfix+str(index)+"."+filename.split(".")[-1]
    source = tinify.from_file(input_dir+"/"+filename)
    source.to_file(output_dir+"/"+out_name)
    global timo_has_done
    timo_has_done += 1
    print("{0} has done ,total {1},completed {2}".format(out_name,total,timo_has_done))


def main():
    if(len(sys.argv)>1):
        mode_str = input("convert perfix (n/y)")
        isperfix = False
        perfix = ""

        if mode_str is "yes" or mode_str is "y" or mode_str is "Y":
            isperfix = True
            perfix = input("Please enter image perfix:")
        #批量修改需完善，

        print("convert started ...")
        input_dir = sys.argv[1]
        output_dir = "./new_image_{0}".format(int(time.time()))
        os.mkdir(output_dir)
        image_names = get_image_filenames(input_dir)
        total = len(image_names)
        threads = []
        for index,image_name in enumerate(image_names):
           threads.append(threading.Thread(target=do_timo,args=(image_name,total,input_dir,output_dir,index,isperfix,perfix)))
        for t in threads:
            t.start()

if __name__ == '__main__':
    main()