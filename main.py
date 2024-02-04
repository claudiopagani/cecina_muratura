##
modelName = "modelloCecina_r01.nxf"
##
import math
import sys
import clr

# clr.AddReference("C:\\Program Files\\NextFEM\\NextFEM Designer 64bit\\NextFEMapi.dll")
import os
from winreg import *  # for reg. access


def NFapiPath():
    addr = r"SOFTWARE\Classes\NextFEM Designer\shell\open\command"
    aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    subkey = None
    aKey = OpenKey(aReg, addr)
    vkey = QueryValueEx(aKey, subkey)
    return os.path.split(vkey[0].replace('"', "").replace("%1", "").strip())[0]


clr.AddReference(NFapiPath() + "\\NextFEMapi.dll")

import NextFEMapi

nf = NextFEMapi.API()

# connect to running instance of NextFEM Designer
isConn = nf.connect()
print("Connected to NextFEM Designer: " + str(isConn))

if isConn:
    # new model
    nf.comm(r"/op/new")
else:
    nf.newModel
print("Opened new NextFEM model")

Lu = nf.getLenUnit()
Fu = nf.getForceUnit()
print("Model units: " + Lu + ", " + Fu)

### Materiali ###
mattoniPieni = nf.addMatFromLib(r"Mattoni pieni LC2")
nf.addOrChangeMaterialProperty(int(mattoniPieni), "FC", str(1.2))
print("Defined materials")


### Casi di carico
nf.addLoadCase("G1")
nf.setLoadCaseType("G1", 0)
nf.addLoadCase("G2")
nf.setLoadCaseType("G2", 0)
nf.addLoadCase("Qk")
nf.setLoadCaseType("Qk", 1)
nf.addLoadCase("Qvento")
nf.setLoadCaseType("Qvento", 2)
nf.addLoadCase("Qneve")
nf.setLoadCaseType("Qneve", 3)

### Applica peso proprio ###
nf.setSelfWeight("G1")
print("Defined loads")


### Sezioni ###
m1_a = nf.addPlanarSection(0.12)
nf.renameSection(m1_a, "M1_a")
m1_b = nf.addPlanarSection(0.24)
nf.renameSection(m1_a, "M1_b")
m1_c = nf.addPlanarSection(0.36)
nf.renameSection(m1_a, "M1_c")
m1_d = nf.addPlanarSection(0.31)
nf.renameSection(m1_a, "M1_d")
m2 = nf.addPlanarSection(0.30)
nf.renameSection(m1_a, "M2")
print("Defined beam sections")

### Definisci allineamenti###
from Maschio import Maschio
from disegnaAllineamento import disegnaAllineamento

allineamento1 = [
    Maschio(0.53, 1.05, 3.3, mattoniPieni, m1_c),
    Maschio(2.84, 1.48, 3.3, mattoniPieni, m1_c),
]
nf = disegnaAllineamento(nf, [0, 0], 0, allineamento1)

allineamento2 = [
    Maschio(0.13, 0.26, 3.3, mattoniPieni, m1_c),
    Maschio(1.5, 0.67, 3.3, mattoniPieni, m1_c),
    Maschio(3.07, 0.67, 3.3, mattoniPieni, m1_c),
    Maschio(4.65, 0.67, 3.3, mattoniPieni, m1_c),
    Maschio(6.19, 0.60, 3.3, mattoniPieni, m1_c),
    Maschio(7.95, 1.12, 3.3, mattoniPieni, m1_c),
]
nf = disegnaAllineamento(nf, [3.58, -0.39], 0, allineamento2)

allineamentoG = [
    Maschio(0.16, 0.32, 3.3, mattoniPieni, m1_c),
    Maschio(2.26, 1.74, 3.3, mattoniPieni, m1_c),
]
nf = disegnaAllineamento(nf, [12.09, -0.39], math.pi / 2, allineamentoG)

allineamento3 = [
    Maschio(0.53, 1.05, 3.3, mattoniPieni, m1_c),
    Maschio(2.84, 1.48, 3.3, mattoniPieni, m1_c),
]
nf = disegnaAllineamento(nf, [0, 0], 0, allineamento3)

#############################
if isConn:
    # refresh view - Reset=0, resizeView True
    nf.refreshDesignerView(0, True)
    nf.comm(r"/op/save")
    nf.comm(r"/op/runUI")
else:
    # s = nf.RunModel()
    # print(s)
    print(nf.saveModel(modelName))
    nf.startDesigner(modelName)
    print("Open NextFem")
