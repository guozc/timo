# timo

基于TinyPNG tinify 的python脚本，将图片压缩配置到右键菜单
可选功能:

[1]tinify 

[2]图片转换base64,可以进行批量缩放 

[3]修改目标文件夹内图片序列帧的序号 

[4]生成foo.txt记录文件目录下的图片相对路径，服务于https://github.com/superMoDi/preload 

[5]audio(目前只支持mp3格式)转base64


配置说明:
-------------
* python版本3.5 ，依赖包 tinify,base64,PIL(pip install pillow)
* timo.bat 设置 timo.py 的目录 以及 Python35的位置,.bat 放在windows目录下
* timo.py 设置tinypng 的 key,key可以为多个
* timo.reg 修改相应批处理的名字,这里用的是timo.bat
