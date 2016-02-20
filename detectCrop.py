import cv2, os

def getFilePathToList(filePointer):
    fileArray = filePointer.readlines()
    fileDict = dict()
    iterator = 0
    faceCount = 0
    for ndx in range(len(fileArray)):
        if ".jpg" in fileArray[ndx]:
            faceCount = 0
            fileName = fileArray[ndx].strip('\n')
            fileDict[fileName] = list([0])
            iterator = fileName
        elif '.jpg' in iterator:
            faceCount += 1
            fileDict[iterator][0] = faceCount
            dim = fileArray[ndx].strip('\n').split('\t')
            fileDict[iterator].append(dim)
    return fileDict


def detectAndSave():
    ageGroup = {1:0,5:0,10:0,16:0,28:0,51:0,75:0}
    homeDir = "data"
    outDir = "outDir"
    if not os.path.exists(outDir):
        os.mkdir(outDir)
    for key in ageGroup.keys():
        key = str(key)
        if not os.path.exists(os.path.join(outDir,key)):
            os.mkdir(os.path.join(outDir,key))
    facedata = "haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(facedata)
    for dir in os.listdir(homeDir):
        dirMain = os.path.join(os.path.abspath('./'),homeDir,dir)
        print
        print("Scanning: "+dirMain)
        print
        file = open(dirMain+"/PersonData.txt")
        fileDict = getFilePathToList(file)
        for fileName in fileDict.keys():
            if fileDict[fileName][0] > 0: # the face count > 0
                img = cv2.imread(dirMain+'/'+fileName)
                minisize = (img.shape[1],img.shape[0])
                miniframe = cv2.resize(img, minisize)
                faces = cascade.detectMultiScale(miniframe) # detect faces
                for f in faces:
                    x, y, w, h = [ v for v in f ]
                    for ndx in fileDict[fileName][1:]:
                        if (x < ((int(ndx[0]) + int(ndx[2])) / 2) < x+w) and (y < ((int(ndx[1]) + int(ndx[3])) / 2) < y+h):
                            #cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255))
                            sub_face = img[y:y+h, x:x+w]
                            ageGroup[int(ndx[4])] += 1
                            saveFile = os.path.join(outDir,ndx[4],(str(ageGroup[int(ndx[4])]) + "_" + ndx[5] + ".jpg"))
                            cv2.imwrite(saveFile, sub_face)
                            print("Detected: "+saveFile)

if __name__ == '__main__':
    detectAndSave()
