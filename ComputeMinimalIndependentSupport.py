import sys
import os
import time
def parseOutput(fileName):
    f = open(fileName,'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        if (line.strip().startswith('v')):
            return line
    return ''
def main():
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    logFile = sys.argv[3]
    timeout = sys.argv[4]
    timeTaken = time.time()
    gmusFile = inputFile[:-4]+'.gcnf'
    tempOutFile = inputFile[:-4]+'.tcnf'
    f = open(outputFile,'w')
    f.close()
    f = open(logFile,'w')
    f.close()
    cmd = './togmus '+inputFile+' '+gmusFile
    os.system(cmd)
    timeTaken = timeTaken-time.time()
    indMap = {}
    maxTry = 10
    attempts = 0
    for i in range(5):
        timeTaken = time.time()
        cmd = './muser2 -v 0 -grp -comp -minisats -order 4 -T '+str(timeout)+' '+gmusFile+' > '+tempOutFile
        os.system(cmd)
        indVars = parseOutput(tempOutFile)
        if (not(indMap.has_key(indVars))):
            indMap[indVars] = 1
        else:
            
            attempts += 1
            if (attempts >= maxTry):
                break
            else:
                i -= 1
                continue
        timeTaken = time.time() - timeTaken
        f = open(outputFile,'a')
        f.write(indVars)
        f.close()
        f = open(logFile,'a')
        f.write(str(i)+':'+str(i+attempts)+':'+str(timeTaken)+'\n')
        f.close()
    cmd = 'rm '+tempOutFile
    os.system(cmd)
    cmd = 'rm '+gmusFile
    os.system(cmd)
main()
