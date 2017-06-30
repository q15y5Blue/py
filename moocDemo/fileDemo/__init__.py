#文件读写练习
f= open(r'D:\test\test.html',"r")
f2=open(r'D:\test\output.html',"w")
f2.write(f.read())
f.close()