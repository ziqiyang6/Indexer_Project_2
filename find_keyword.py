import os

rootDir = os.getcwd()

def scan_file(filename, dirname):
    print(os.path.join(dirname,filename))
    contains = False
    
    

    if("KeyError happened in block" in filename):
        contains = True
    else:
        with open(os.path.join(dirname,filename)) as f:
            lines = f.readlines()
            for l in lines:
                #print(l)
                if("KeyError happened in block" in l):
                    contains = True
                    print(l)
                    break

    if contains:
        print("yes")
        




if __name__ == '__main__':
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            if(os.path.join(dirName,fname) == "/home/tw2623/Indexer-Project/ERD.pdf"):
                continue
            scan_file(fname, dirName)