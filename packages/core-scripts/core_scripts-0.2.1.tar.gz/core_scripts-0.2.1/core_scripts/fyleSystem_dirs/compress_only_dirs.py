from os import listdir
from os.path import isdir
from pathlib import PurePath
from subprocess import run

def command_cmd(command_,options=False):
        if (options):
            return run(f'{command_}',options,shell=True) 
        return run(f'{command_}',shell=True)

def compress_only_dirs(destination):
    destinationDirs = listdir(destination)
    destinationOnlyDirs = []        
    for destinationDir in destinationDirs:
        dirs = PurePath(f'{destination}/{destinationDir}')
        if (isdir(dirs)):
            destinationOnlyDirs.append(destinationDir)
    for dirs in destinationOnlyDirs:
        command_cmd(f'cd "{destination}" && winrar -ibck a "{dirs}.rar" "{dirs}"')
