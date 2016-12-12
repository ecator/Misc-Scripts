#-*-coding:utf-8-*-
#Aboboo导出转Anki
import re
import os
import sys
import csv
import shutil
import glob
import time
reload(sys)  
sys.setdefaultencoding('utf8')
output = "Tobeimport.csv"
def Main():
	curpath = os.getcwd()
	print curpath
	lrcfiles = curpath + "/*.lrc"
	mediaPath=curpath+r"/collection.media"
	#创建collection.media目录
	if not os.path.exists(mediaPath): 
		os.makedirs(mediaPath) 
	flist = glob.glob(lrcfiles)
	writer = csv.writer(file(output, 'wb+'))
	pattern1 = re.compile(r'\](.*?)\s*\t')
	pattern2 = re.compile(r'\t\s*(.*?)$')
	i = 0
	for f in flist:
		i = i + 1
		fh = file(f,'r')
		content = fh.read()
		#进行转码，因为ab导出的lrc文件是系统默认编码，需要转换成Python的Unicode编码
		content=content.decode('gbk', 'ignore')
		english = pattern1.findall(content)
		chinese = pattern2.findall(content)
		print content
		print english[0]
		print chinese[0]
		mp3file = f[:-3] + "mp3"
		newname = str(time.time()) + str(i) + ".mp3"
		print mp3file
		print newname
		#把重命名改成复制文件，防止破坏源文件
		#os.rename(mp3file, newname)
		shutil.copyfile(mp3file,mediaPath+"/"+newname)
		question = "[sound:" + newname +"]"
		if not english:
			answer =content[10:]
		elif chinese:
			#有中文的情况
			answer = english[0]+"<br>"+chinese[0] + "<br>" + question
		else:
			#没有中文的情况
			answer = english[0]+ "<br>" + question
		writer.writerow([question, answer])
		fh.close()
	del writer
      
if __name__ == "__main__":
	Main()