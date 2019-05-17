import os
import re
import sys
from zip import zipDir,zipFiles
from smtp import sendMail
import smtplib

path = 'd:\\111\\'
files = []

searchType = input("[1]:search files  [2]:search dir  ")
searchType = int(searchType)
print("What file/dir do you want to search?")
print("*RegExp is also support*")
print("input example:[.pdf] [.jpg] [foo.jpg] [bar]")
searchStr = input()

# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    searchTarget = 0
    if(searchType == 1):
        searchTarget = f
    elif(searchType == 2):
        searchTarget = d

    for target in searchTarget:
        patternStr = re.compile(searchStr)
        results = patternStr.findall(target)
        if(len(results)>0):
            files.append(os.path.join(r, target))

counter = 0
if(len(files)==0):
    print("no match result")
    sys.exit(0)
for f in files:
    print(counter,f)
    counter += 1

zipName = None
zipPath = None
if(searchType == 1):
    print("*use space to split muilt-target*")
    selectTargets = input("Choose what you want to upload: ")
    selectTargets = selectTargets.split()
    print("Select:")
    zipPaths = []
    for target in selectTargets:
        target = int(target)
        zipPaths.append(files[target])
        print(files[target])
    zipPath,zipName = zipFiles(zipPaths)

elif(searchType == 2):
    selectTargets = input("Choose what you want to upload: ")
    selectTargets = int(selectTargets)
    print("Target dir:")
    print(files[selectTargets])
    zipPath,zipName = zipDir(files[selectTargets])

print(zipPath,zipName)
try:
    sendMail('p208p2002@gmail.com','Your Files','Your Files',['p208p2002@gmail.com'],[zipPath])
except Exception as e:
    print (e)
    sys.exit(0)
finally:
    print("send mail success")
