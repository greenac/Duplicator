import sys
import os
from File import File
from ScreenDivider import ScreenDivider

class Compare:
    def __init__(self, pathList):
        self.pathList = pathList
        self.rootFiles = {}
        self.targetFiles = {}
        self.equalFiles = {}
        self.screenDivider = ScreenDivider()

    def fillTargetFiles(self):
        targetPaths = self.pathList
        # remove root dir
        del targetPaths[0]
        for path in targetPaths:
            if os.path.isdir(path):
                self.searchTargetDir(path)
        return None

    def fillRootFiles(self):
        rootPath = self.pathList[0]
        if os.path.isdir(rootPath):
            self.searchRootDir(rootPath)
        return None

    def searchTargetDir(self, path):
        filesInDir = os.listdir(path)
        targetList = []
        self.targetFiles[path] = targetList
        for aFile in filesInDir:
            pathWithDir = path + aFile
            if os.path.isdir(pathWithDir):
                pathWithDir = pathWithDir + "/"
                self.searchTargetDir(pathWithDir)
            else:
                fileSize = os.path.getsize(pathWithDir)
                thisFile = File(aFile, fileSize)
                self.targetFiles[path].append(thisFile)
        return None

    def searchRootDir(self, path):
        filesInDir = os.listdir(path)
        targetList = []
        self.rootFiles[path] = targetList
        for aFile in filesInDir:
            pathWithDir = path + aFile
            if os.path.isdir(pathWithDir):
                if pathWithDir[len(pathWithDir) - 1] != '/':
                    pathWithDir += "/"
                self.searchRootDir(pathWithDir)
            else:
                fileSize = os.path.getsize(pathWithDir)
                thisFile = File(aFile, fileSize)
                self.rootFiles[path].append(thisFile)
        return None

    def printTargetSearch(self):
        keys = self.targetFiles.keys()
        for key in keys:
            targetList = self.targetFiles[key]
            if len(targetList) != 0:
                self.screenDivider.acrossScreen('-')
                print("Files in directory:", key + "\n")
                for aFile in targetList:
                    print(aFile.fileName)
        return None

    def printRootSearch(self):
        keys = self.rootFiles.keys()
        print("keys are:")
        for key in keys:
            print(key)
        for key in keys:
            rootList = self.rootFiles[key]
            if len(rootList) != 0:
                self.screenDivider.acrossScreen('-')
                print("Files in directory:", key + "\n")
                for aFile in rootList:
                    print(aFile.fileName)
        return None

    def compareFiles(self):
        tKeys = self.targetFiles.keys()
        rKeys = self.rootFiles.keys()
        for rKey in rKeys:
            rList = self.rootFiles[rKey]
            for rFile in rList:
                for tKey in tKeys:
                    tList = self.targetFiles[tKey]
                    for tFile in tList:
                        if tFile.fileName == rFile.fileName and tFile.fileSize == rFile.fileSize:
                            keyList = [rKey, tKey]
                            self.equalFiles[rFile.fileName] = keyList
        return None

    def printEqualFiles(self):
        keys = self.equalFiles.keys()
        for key in keys:
            pathList = self.equalFiles[key]
            print("--", key, "-- exists in directories:")
            print("ROOT   --", pathList[0])
            print("TARGET --", pathList[1])
            self.screenDivider.acrossScreen('-')
        return None

    def removeRepeatFiles(self):
        keys = self.equalFiles.keys()
        for key in keys:
            pathList = self.equalFiles[key]
            pathToRemove = pathList[1] + key
            os.remove(pathToRemove)
        print("\n....", len(keys), "files have been removed ....\n\n")
        return None
