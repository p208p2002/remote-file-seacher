import zipfile
import os
import time

def makeZip(files:list):
    fileName = str(int(time.time()))+'.zip'
    z = zipfile.ZipFile(fileName, "w")
    for file in files:
        z.write(file)
    z.close()
    return (os.path.join(os.getcwd(), fileName))

#print(makeZip(['.//test.txt','.//test2.txt']))