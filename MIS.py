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

def usage():
    usageStr = "Usage: python MIS.py [options] <inputFileName.cnf>\n"
    usageStr += "options are entered as -object=value where object can be \n"
    usageStr += "timeout: (optional) timeout for iteration in seconds (default:3000 seconds)\n"
    usageStr += "logging: (optional) 0/1 : 0 for turnoff and 1 for turn on. (default: 0)\n"
    usageStr += "output: (optional) supply the output file destination (default: inputFileName.out)\n"
    usageStr += "log: (optional) supply the log file destination (deafult : log.txt)\n"
    usageStr += "max: (optional) up to 'max' number of minimal independent supports will be generated (default: 1)"
    print usageStr
    exit(1)

#returns default values for all parameters except outputfile which depends on inputfile
def defaultParams():
    return 3000, 0, 'log.txt', 1    #timeout, logging, log, max

#action=0 -> print help
#action=1 -> couldn't understand argument. error will pass the string
#action=2 -> no inputfile
#action=3 -> input file not last in argument list. Fail gracefully with error to avoid confusion with old style of arguments
#action=4 -> all set. go.
def getInputs():
    paramMap={}
    action=0
    error = ''
    acceptedParams={'timeout','logging','output','log','max'}
    for i in range(1,len(sys.argv)):
        if (not(sys.argv[i][0] == '-')):
            paramMap['inputFile'] = sys.argv[i]
            if i!=len(sys.argv)-1:
                action = 3
                error = "inputFileName should be last in param list. Use '-h' parameter to print usage."
            else:
                action = 4
            return action,error, paramMap
        else:
            if (sys.argv[i][1] == 'h'):
                action = 0
                return action,error,paramMap
            fieldValues = sys.argv[i][1:].strip().split('=')
            if (not(fieldValues[0] in acceptedParams)):
                action = 1
                error = "Could not understand the option "+str(fieldValues[0])+"\n"
                return action,error,paramMap
            else:
                paramMap[fieldValues[0]] = fieldValues[1]
    action =2
    error = "No inputfile\n"
    return action,error,paramMap

def main():
    action,error,paramMap = getInputs()
    if (action == 0):
        usage()
        exit(1)
    if (action == 1 or action == 2 or action == 3):
        print error
        exit(1)
    inputFile = paramMap['inputFile']
    extension=inputFile[-4:]
    if extension =='.cnf':
        outputFile =  inputFile[:-4]+".out"
    else:
        outputFile = inputFile+".out"
    timeout, shouldLog, logFile, maxIters = defaultParams() 
    
    if (paramMap.has_key('timeout')):
        timeout = float(paramMap['timeout'])+10 #extra protection for time sync
    if (paramMap.has_key('output')):
        outputFile = paramMap['output']
    if (paramMap.has_key('log')):
        logFile = paramMap['log']
    if (paramMap.has_key('logging')):
        if (paramMap['logging'] == '0'):
            shouldLog = False
        if (paramMap['logging'] == '1'):
            shouldLog = True
    if (paramMap.has_key('max')):
        maxIters = paramMap['max']
        
    timeTaken = time.time()
    if extension =='.cnf':
        gmusFile = inputFile[:-4]+'.gcnf'
        tempOutFile = inputFile[:-4]+'.tcnf'
    else:
        gmusFile = inputFile+'.gcnf'
        tempOutFile = inputFile+'.tcnf'
    f = open(outputFile,'w')
    f.close()
    if shouldLog==1:
        f = open(logFile,'w')
        f.close()
    cmd = './togmus '+inputFile+' '+gmusFile
    os.system(cmd)
    timeTaken = timeTaken-time.time()
    indMap = {}
    maxTry = 10
    attempts = 0
    for i in range(int(maxIters)):
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
        if shouldLog==1:
            f = open(logFile,'a')
            f.write(str(i)+':'+str(i+attempts)+':'+str(timeTaken)+'\n')
            f.close()
    cmd = 'rm '+tempOutFile
    os.system(cmd)
    cmd = 'rm '+gmusFile
    os.system(cmd)
main()
