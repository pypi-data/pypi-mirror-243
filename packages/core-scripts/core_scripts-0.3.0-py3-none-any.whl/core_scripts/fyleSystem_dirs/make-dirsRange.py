from subprocess import run
from pathlib import PurePath
from sys import argv

destination = argv[1]
rangeStar = argv[2]
rangeEnd = argv[3]

def getLocation():
    if (destination):
        return destination
    location = PurePath(input("Donde quieres crear "))
    return location

def getRangeStar():
        if (rangeStar):
             return rangeStar         
        dirStar = int(input("En donde empezamos a crear "))
        return dirStar

def getRangeEnd():
     if (rangeEnd):
          return rangeEnd
     dirEnd =int(input("Donder terminamos ")) + 1
     return dirEnd

dirs = range(getRangeStar(),getRangeEnd())

for dir in dirs:
    run(f'cd "{getLocation()}" && mkdir {dir}',shell=True)
