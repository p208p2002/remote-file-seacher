import os
import re
path = 'd:\\111\\'
files = []

searchType = input("[1]:search files  [2]:search dir  ")
searchType = int(searchType)

# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    searchTarget = 0
    if(searchType == 1):
        searchTarget = f
    elif(searchType == 2):
        searchTarget = d

    for target in searchTarget:
        patternStr = re.compile('.js')
        results = patternStr.findall(target)
        if(len(results)>0):
            files.append(os.path.join(r, target))

counter = 0
for f in files:
    print(counter,f)
    counter += 1

selectTarget = input("Choose what you want to upload: ")
selectTarget = int(selectTarget)
print("You choose \""+files[selectTarget]+"\"")