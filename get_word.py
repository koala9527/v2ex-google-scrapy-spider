import csv
import jieba.analyse as analyse
from PIL import Image
import matplotlib.pyplot as plt
import wordcloud
import numpy as np


all_text=''
# 读取csv,把所有的句子连成一句话
with open('./word.csv')as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        print(row[0])
        all_text+=row[0]+';'

image1 = Image.open('./juejin.jpg') # 打开一个背景图作素材
tags = analyse.extract_tags(all_text, topK=100) #著名的结巴分词，挑选出最常见的100个次
text = ' '.join(tags) #把100歌词的列表改为空格间隔的一行字符串给云词这个库使用
MASK = np.array(image1) #词云的遮照为nampy数组
# 下面就是调WordCloud的api身成一张图，注意字体文件需要根据自己的系统找，我的是ubuntu的。
WC = wordcloud.WordCloud(font_path= "/usr/share/fonts/truetype/arphic/ukai.ttc",max_words=2000,mask = MASK,height= 400,width=400,background_color='white',repeat=False,mode='RGBA') #设置词云图对象属性
#生成图片
con = WC.generate(text)
# 展示图片
plt.imshow(con)
# 关闭坐标轴,plt这是一个科学计算相关的库
plt.axis("off")
plt.show()
print(tags)
