import zipfile
import os
import time

def zipFiles(files:list):
    fileName = str(int(time.time()))+'.zip'
    z = zipfile.ZipFile(fileName, "w")
    for file in files:
        dir, base_filename = os.path.split(file)
        z.write(file,base_filename)
    z.close()
    return (os.path.join(os.getcwd(), fileName),fileName)

def zipDir(path):
    fileName = str(int(time.time()))+'.zip'
    zipf = zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()
    return (os.path.join(os.getcwd(), fileName),fileName)

# print(makeZip(['.//test.txt','.//test2.txt']))
# zipDir('D:\\project\\remote-file-search\\')