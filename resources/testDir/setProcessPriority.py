from root import switchBoard, getProcessPID, standardizeString
from sys import argv, exit as sys_exit
from win32api import OpenProcess
from win32process import SetPriorityClass, BELOW_NORMAL_PRIORITY_CLASS, \
    GetPriorityClass
from win32con import IDLE_PRIORITY_CLASS, NORMAL_PRIORITY_CLASS, \
    HIGH_PRIORITY_CLASS, PROCESS_ALL_ACCESS
from psutil import Process, pids

AVAILABLE_SWITCHES = ['l', 'b', 'n', 'h', 'e', 'p', '?']
EXCLUDED_PROCESSES = ["audiodg.exe", "system.exe", "svchost.exe",
                      "system idle process.exe", "system",
                      "system idle process"]


def getExceptionList(argList):

    exceptionList = []

    if "-e" in argList:
        for i in range(len(argList) - 1, 0, -1):

            if argList[i] == "-e":
                argList.remove(argList[i])
                break

            else:
                exceptionList.append(argList[i])
                argList.remove(argList[i])

    return exceptionList


def getPriorityClass(switchList):  # not limited to switchList

    if(len(switchList) == 1):

        if switchList[0] == 'l':
            priorityClass = IDLE_PRIORITY_CLASS

        elif switchList[0] == 'b':
            priorityClass = BELOW_NORMAL_PRIORITY_CLASS

        elif switchList[0] == 'n':
            priorityClass = NORMAL_PRIORITY_CLASS

        elif switchList[0] == 'h':
            priorityClass = HIGH_PRIORITY_CLASS

    else:
        print "Error:Only one switch at a time. Terminating script."
        print "Switches: ", switchList
        sys_exit(1)

    return priorityClass


def getProcessPIDList(argsList):
    processPIDList = []

    for arg in argsList:
        processPIDList.append(getProcessPID(arg))

    return processPIDList


def printPriority(numConst):

    if(numConst == IDLE_PRIORITY_CLASS):
        result = "Low"

    elif(numConst == BELOW_NORMAL_PRIORITY_CLASS):
        result = "Below normal"

    elif(numConst == NORMAL_PRIORITY_CLASS):
        result = "Normal"

    elif(numConst == HIGH_PRIORITY_CLASS):
        result = "High"

    else:
        result = "Invalid priority"
        sys_exit(1)

    return result


def setProcessPriority(procPIDList, priority, exception=False):

    if exception == False:
        for procPID in procPIDList:

            if standardizeString(Process(procPID).name) not in EXCLUDED_PROCESSES:
                handle = OpenProcess(PROCESS_ALL_ACCESS, True, procPID)
                SetPriorityClass(handle, priority)
                print "Changing ", Process(procPID).name, " priority to: ", printPriority(priority)

    else:
        exceptionPIDList = procPIDList  # just to make code more readable

        if len(exceptionPIDList) > 0:
            print "Changing all process priority to ", printPriority(priority), "except: "
        else:
            print "Changing all process priority to ", printPriority(priority)

        for procPID in pids():

            if standardizeString(Process(procPID).name) not in EXCLUDED_PROCESSES and procPID not in exceptionPIDList:

                handle = OpenProcess(PROCESS_ALL_ACCESS, True, procPID)
                SetPriorityClass(handle, priority)

            elif standardizeString(Process(procPID).name) not in EXCLUDED_PROCESSES:
                print "\t", Process(procPID).name




if __name__ == "__main__":

    argv = argv[1:]
    for i in range(0, len(argv)):
        argv[i] = argv[i].replace(',', '')

    exceptionProcessList = getExceptionList(argv)
    switches = switchBoard(argv)

    if "p" in switches:
        if len(argv) == 0:
            tPIDList = pids()
            for i in range(0, len(tPIDList)):
                if standardizeString(Process(tPIDList[i]).name) not in EXCLUDED_PROCESSES:
                    argv.append(Process(tPIDList[i]).name)

        for procPID in getProcessPIDList(argv):
            try:
                if standardizeString(Process(procPID).name) not in EXCLUDED_PROCESSES:
                    print Process(procPID).name.strip(), " priority =", printPriority(GetPriorityClass(OpenProcess(PROCESS_ALL_ACCESS, True, procPID)))
            except error.NoSuchProcess:
                pass
    else:
        priorityClass = getPriorityClass(switches)

        if len(exceptionProcessList) >= 0 and len(argv) == 0:
            exceptionProcessPIDList = getProcessPIDList(exceptionProcessList)
            setProcessPriority(exceptionProcessPIDList, priorityClass, True)
        else:
            processPIDList = getProcessPIDList(argv)
            setProcessPriority(processPIDList, priorityClass)


def changeProcPriority(processName, priorityName):  # for use of other scripts

    def getPriorityFromString(priorityName):
        priorityName = standardizeString(priorityName)
        if priorityName == "high":
            priority = HIGH_PRIORITY_CLASS
        elif priorityName == "normal":
            priority = NORMAL_PRIORITY_CLASS
        elif priorityName == "below normal":
            priority = BELOW_NORMAL_PRIORITY_CLASS
        elif priorityName == "low":
            priority = IDLE_PRIORITY_CLASS
        else:
            print "Invalid priority name given. Valid priority names: 'high', 'normal', 'below normal', 'low'. Terminating script."
            sys_exit(1)

        return priority

    priority = getPriorityFromString(priorityName)
    print "Changing ", processName, " priority to: ", printPriority(priority)

    procPID = getProcessPID(processName)
    handle = OpenProcess(PROCESS_ALL_ACCESS, True, procPID)
    SetPriorityClass(handle, priority)
