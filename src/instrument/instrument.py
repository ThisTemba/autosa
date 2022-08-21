import datetime
import time
from bandsData import bands
import pyvisa
from instrument.imgTransfer import saveImageToController


def getInstResource(resources):
    usbResources = [r for r in resources if "USB" in r]
    instrUsbResources = [r for r in usbResources if "::INSTR" in r]
    return instrUsbResources[0]


def getInst(instResource):
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource(instResource)
    return inst


def recordBand(inst, folder, filename, controllerOutFolder, dur=5):
    # RECORD
    inst.write(":INIT:REST")
    inst.write(":INIT:CONT ON")
    time.sleep(dur)
    inst.write(":INIT:CONT OFF")

    # SAVE
    csvFilename = f"{folder}/{filename}.csv"
    pngFilename = f"{folder}/{filename}.png"
    inst.write(f':MMEM:STOR:TRAC:DATA ALL, "{csvFilename}"')
    inst.write(f':MMEM:STOR:SCR "{pngFilename}"')

    saveImageToController(inst, pngFilename, controllerOutFolder)
    saveImageToController(inst, csvFilename, controllerOutFolder)
    return


def recallState(inst, stateFolder, filename):
    inst.write(f":MMEM:LOAD:STAT '{stateFolder}/{filename}'")
    return


def recallCorr(inst, corrFolder, filename):
    inst.write(f":MMEM:LOAD:CORR 1,'{corrFolder}/{filename}'")
    return


def setCoupling(inst, coupling):
    inst.write(f":INP:COUP {coupling}")
    # print(inst.query(f":INP:COUP?"))


def getRunFilename(runIndex, bandName, siteName, notes=""):
    runNumber = "%02d" % runIndex
    d = datetime.datetime.now()
    month = str(int(d.strftime("%m")))
    date = d.strftime("%d")
    runId = f"{month}{date}-{runNumber}"

    if notes == "":
        filename = f"{runId} {siteName} {bandName}"
    else:
        filename = f"{runId} {siteName} {notes} {bandName}"
    return filename


def recordBands(
    resource,
    siteName,
    lastRunIndex,
    stateFolder,
    corrFolder,
    outFolder,
    bandKeys,
    controllerOutFolder,
):
    inst = getInst(resource)
    for i, key in enumerate(bandKeys):
        bandName = key
        runIndex = i + 1 + lastRunIndex
        coupling = bands[key]["coupling"]

        stateFilename = bands[key]["stateFilename"]
        corrFilename = bands[key]["corrFilename"]
        runFilename = getRunFilename(runIndex, bandName, siteName)

        recallState(inst, stateFolder, stateFilename)
        recallCorr(inst, corrFolder, corrFilename)
        setCoupling(inst, coupling)

        recordBand(
            inst,
            outFolder,
            runFilename,
            controllerOutFolder,
            2,
        )
