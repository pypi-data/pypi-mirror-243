import tkinter as tk
from tkinter import filedialog
global file
import tkinter.font as tkFont
import matplotlib.pyplot as plt  
from wordcloud import WordCloud
import jieba
from PIL import Image
import numpy as np
import requests as re
import os
import datetime

def listchange():
    global path
    path = '词云图'+ datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")
    logical = os.path.exists(path)
    if not logical:
        os.mkdir(path)
        os.mkdir(os.path.join(path,'辅助文件'))

def download():
    listchange()

    data = re.get('https://math.halashuo.cn/stop.txt').content

    with open(path+'/辅助文件/stop.txt', "wb") as f:
        f.write(data)

def downloadzt():
    data = re.get('https://math.halashuo.cn/STSONG.TTF').content

    with open(path+'/辅助文件/FSTSONG.TTF', "wb") as f:
        f.write(data)

def plot(file,p_name):

    if if_drop.get():
        an = file.split('/')[-1].split('.')[0]
        file =  os.path.join(path,"辅助文件",f"{an}_out.txt")
    try:
        f = open(file,'r',encoding='utf-8').read()  #生成词云的文档
    except:
        f = open(file,'r',encoding='gbk').read()  #生成词云的文档
    f = jieba.lcut(f)
    f = ' '.join(f)


    try:
        wordcloud = WordCloud(
            background_color='white',  # 背景颜色，根据图片背景设置，默认为黑色
            mask=img_array,  # 笼罩图
            font_path='C:\Windows\Fonts\STZHONGS.TTF',  # 若有中文需要设置才会显示中文
            width=1000,
            height=860,
            margin=2).generate(f)  # generate 可以对全部文本进行自动分词
        # 参数 width，height，margin分别对应宽度像素，长度像素，边缘空白处
    except:
        error.set('您应该高贵的是mac系统，正在下载字体.....')
        downloadzt()
        error.set('您应该高贵的是mac系统，字体下载完成！')
        wordcloud = WordCloud(
            background_color='white',  # 背景颜色，根据图片背景设置，默认为黑色
            mask=img_array,  # 笼罩图
            font_path=path+'/辅助文件/FSTSONG.TTF',  # 若有中文需要设置才会显示中文
            width=1000,
            height=860,
            margin=2).generate(f)  # generate 可以对全部文本进行自动分词

    plt.imshow(wordcloud)  
    plt.axis('off')
    error.set('运行成功~，请再' + path + '路径下查看生成内容')

    with open( os.path.join(path,'Read_must.txt'), 'w') as f:
        f.write('Must 文件内文件不可删除~~~,本目录下文件可以删除~')
    #wordcloud.to_file("词云图1.jpg")
    plt.savefig(os.path.join(path,p_name), dpi = 1200,bbox_inches = 'tight')
    plt.show()

def drop_unless(filename):
    # 创建停用词列表
    def stopwordslist():
        stopwords = [line.strip() for line in open(os.path.join(path,'辅助文件/stop.txt'),encoding='UTF-8').readlines()]
        return stopwords
     
    # 对句子进行中文分词
    def seg_depart(sentence):
        # 对文档中的每一行进行中文分词
        # print("正在分词")
        sentence_depart = jieba.cut(sentence.strip())
        # 创建一个停用词列表
        stopwords = stopwordslist()
        # 输出结果为outstr
        outstr = ''
        # 去停用词
        for word in sentence_depart:
            if word not in stopwords:
                if word != '\t':
                    outstr += word
                    outstr += " "
        return outstr
     
    # 给出文档路径
    an = filename.split('/')[-1].split('.')[0]
    outfilename = path+f"/辅助文件/{an}_out.txt"
    try:
        print('2')
        inputs = open(filename, 'r',encoding='utf-8')
        outputs = open(outfilename, 'w',encoding='utf-8')
    except:
        print('1')
        inputs = open(filename, 'r',encoding='ISO-8859-1')
        outputs = open(outfilename, 'w',encoding='ISO-8859-1')
         

    # 将输出结果写入ou.txt中
    for line in inputs:
        line_seg = seg_depart(line)
        outputs.write(line_seg + '\n')
        
    outputs.close()
    inputs.close()
    error.set('预处理完成~,可以开始制作~')

def upload_file():
    selectFile = tk.filedialog.askopenfilename()
    entry1.insert(0, selectFile)
    file1 = entry1.get()
    file.set(file1)
    print('上传的文件为: {}'.format(file.get()))

# 上传背景图

def upload_file1():
    global img_array
    selectFile = tk.filedialog.askopenfilename()
    entry2.insert(0, selectFile)
    file2 = entry2.get()
    file1.set(file2)
    print('上传的背景图: {}'.format(file1.get()))
    img = Image.open(file2)
    img_array = np.array(img)


def begin_plot(file,name1):
    plot(file,name1)

def a():
    print(if_drop.get())

def win():
    global name,file,file1,error,if_drop,img_array,entry1,entry2
    download()

    img_array = np.zeros((800, 1000))
    root = tk.Tk()
    #root.iconphoto(False, tk.PhotoImage(file='grey_model/need/word.png'))

    name = tk.StringVar()
    file = tk.StringVar()
    file1 = tk.StringVar()

    error = tk.StringVar()
    error.set('欢迎使用，系统一切正常~')


    if_drop = tk.BooleanVar()
    if_drop.set('False')
    myfont = tkFont.Font(family='华文行楷', size=30, \
                         weight=tkFont.BOLD, slant=tkFont.ITALIC)

    root.title('词云图生成系统')
    frm = tk.Frame(root)
    frm1 = tk.Frame(root)
    frm1.grid(row=0)

    label1 = tk.Label(frm1, text='欢迎来到词云图生成系统',font = myfont,fg = '#00FF7F')
    label1.grid(row=0)

    frm.grid(row = 1, padx='20', pady='30')
    btn = tk.Button(frm, text='上传语料文件', command=upload_file)
    btn.grid(row=0, column=0, ipadx='3', ipady='3', padx='10', pady='10')
    entry1 = tk.Entry(frm, width='40')
    entry1.grid(row=0, column=1)

    btn1 = tk.Button(frm, text='上传背景图(非必须)', command=upload_file1)
    btn1.grid(row=1, column=0, ipadx='3', ipady='3', padx='10', pady='10')
    entry2 = tk.Entry(frm, width='40')
    entry2.grid(row=1, column=1)

    label2 = tk.Label(frm, text = '导出词云图片命名:',\
                            borderwidth = 6,
                            relief="ridge",).grid(row = 2, column = 0,\
                                                   ipadx='3', ipady='3', padx='10', pady='20')
    input2 = tk.Entry(frm,width='20',textvariable = name).grid (row=2,column=1)


    drop = tk.Checkbutton(frm, text = '文本预处理', variable = if_drop,\
                          command = lambda:drop_unless(file.get()))
    drop.grid(row = 3, column = 0)

    begin_work = tk.Button(frm, text = '开始制作', \
                           command = lambda:begin_plot(file.get(),name.get()))
    begin_work.grid(row =3,column = 1 )

    error_v = tk.Label(frm, textvariable = error, fg = 'red', borderwidth = 2,
                            width = 70,
                            relief="ridge",)
    error_v.grid(row = 4,columnspan = 2,rowspan = 2)


    root.mainloop()
win()