import os
import matplotlib.pyplot as plt
from matplotlib.image import imread
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import Circle, Ellipse
import pandas as pd
import math
#=====================================================================================================

def qhtm():
    """
    To show html file of list of quantum gates included here
    Output: quos.html webpage with a list of various gates
    """
    import webbrowser
    try:
        webbrowser.open((__file__).replace('__init__.py','') + "quos.html")
    except:
        webbrowser.open("quos.html")
#=====================================================================================================

def qxls():
    """
    to download quos.xlsm and qblo.xlsm files
    Output: quos.xlsm to create a plot of specified gates and qblo.xlsm to create Bloch spheres
    """
    from pathlib import Path
    import shutil
    try:
        zdst = str(os.path.join(Path.home(), "Downloads"))
    except:
        zdst = str(Path.home() / "Downloads")    
    try:
        shutil.copy((__file__).replace('__init__.py','') + "quos.xlsm", zdst + "/quos.xlsm")       
    except:
        shutil.copy("quos.xlsm",  zdst + "/quos.xlsm")
    try:
        shutil.copy((__file__).replace('__init__.py','') + "qblo.xlsm", zdst + "/qblo.xlsm")       
    except:
        shutil.copy("quos.xlsm",  zdst + "/qblo.xlsm")
#=====================================================================================================

def qstr(xlsm='quos.xlsm', wsht='Gates'):
    """
    For help to generate a string for a quantum circuit
    Output: String of sgqt strings concatenated by pipe ('|')
    xlsm  : Excel file with a specification of gates
    """
    import pandas as pd
    xdf = pd.read_excel(xlsm, sheet_name=wsht, header=None)
    txt = ""
    for col in range(0, xdf.shape[1]):
        for row in range(0, xdf.shape[0]):
            cel = str(xdf.iloc[row, col])
            if (cel.lower() != "nan"):
                txt = txt + cel + "," + str(row+1) + "," + str(col+1) + "|"
    if txt=="":
        txt = '1,3,0|Q 30 15,5,0|H a,1,1|Y,1,2|Z,2,2|X,3,2|Y,4,2|Z,5,2|X,6,2|S,2,3|T,4,3|V,6,3|'
        txt = txt + 'Rx 30,1,4|Ry 15,2,4|Rz 15,3,4|Rz 30,4,4|Ry 15,5,4|Rx 15,6,4|Ph 15,2,5|'
        txt = txt + 'Pp 30,4,5|O a,1,6|Cd,1,7,Ph 15,2,7|K,3,7|U 30 30 15,4,7|U 15 15 30,6,7|'
        txt = txt + 'C,1,8,X,2,9|Sw,4,8,Sw,6,8|iSw,3,9,iSw,4,9|M a,1,10|'
    print(txt)
    return txt
#=====================================================================================================

def qplt(ssgqt):
    """
    To create a plot of a quantum circuit based on a string
    Output: Matplotlib plot
    ssgqt : String of sgqt strings concatenated by pipe ('|')
    sgqt  : String of g q t strings concatenated by comma
    g     : String of item-name and applicable arguments strings concatenated by space
    q     : a (for all) or Positive integer denoting qudit sequence number
    t     : Positive integer denoting opertation time sequence number
    """
    asgqt = ssgqt.split('|')
    qmx, tmx = 0, 0
    for sgqt in asgqt:
        agqt = sgqt.split(",")
        q, t = agqt[1], int(agqt[2])
        if not (q=="a"):
            if (int(q) > qmx): qmx = int(q)
        if (t > tmx): tmx = t
        if len(agqt) > 3:
            q, t = agqt[4], int(agqt[5])
            if not (q=="a"):
                if (int(q) > qmx): qmx = int(q)
            if (t > tmx): tmx = t

    fig = plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.set_xlim(0, tmx+1)
    ax.set_ylim(-qmx-1, 0)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    try:
        idir = (__file__).replace('__init__.py','') + 'icons/'
    except:
        idir = 'icons/'
    for q in range(1, qmx+1):
        ax.axhline(-q, color='red', lw=1)
        ax.add_artist(AnnotationBbox(
            OffsetImage(imread(idir +'0.jpg')),
            (0, -q), frameon=False))
    for sgqt in asgqt:
        agqt = sgqt.split(",")
        g, q, t = agqt[0].split(" ")[0], agqt[1], int(agqt[2])
        if q=="a":
            r = range(1,qmx+1)
        else:
            r = [int(q)]
        if (t==0) and ((g=="1") or (g=="Q")):
            for p in r:
                ax.add_artist(AnnotationBbox(
                    OffsetImage(imread(idir + g +'.jpg')),
                    (0, -p), frameon=False))
        if (t>0) and (g in ['0','1','Q','I','H','X','Y','Z','S','T','V','Rx','Ry','Rz','Ph','Pp','U','C','Cd','Sw','iSw','M','O','K']):
            for p in r:
                ax.add_artist(AnnotationBbox(
                    OffsetImage(imread(idir + g + '.jpg')),
                    (t, -p), frameon=False))
                if len(agqt) > 3:
                    g1, q1, t1 = agqt[3].split(" ")[0], agqt[4], int(agqt[5])
                    if q1=="a":
                        r1 = range(1,qmx)
                    else:
                        r1 = [int(q1)]
                    for p1 in r1:
                        ax.add_artist(AnnotationBbox(
                            OffsetImage(imread(idir + g1 + '.jpg')),
                            (t1, -p1), frameon=False))
                        plt.plot([t,t1], [-p,-p1], 'b')
    plt.show()
#=====================================================================================================

def qstn(zabc, tint=True):
    """
    To create a number-type string into an integer or a float
    Output: Integer or float
    zabc  : Number-type string
    tint  : True for integer output
    """
    try:
        if tint:
            return int(zabc)
        else:
            return float(zabc)
    except:
        return 0
#=====================================================================================================

def qmat(xS, xT):
    """
    For help to multiply a matrix and a vector to generate a vector
    Output: String for a qubit's 0r 0i 1r 1i parts
    xS    : String for a quantum gate's code, qubit serial number, and time serial number
    xT    : String for a qubit's 0r 0i 1r 1i parts
    """
    xPi = math.pi
    zchk = (xS + " ").split(" ")[0]
    if zchk=="H":
        xA = [1 / math.sqrt(2), 0, 1 / math.sqrt(2), 0, 1 / math.sqrt(2), 0, -1 / math.sqrt(2), 0]
    elif zchk=="X":
        xA = [0, 0, 1, 0, 1, 0, 0, 0]
    elif zchk=="Y":
        xA = [0, 0, 0, -1, 0, 1, 0, 0]
    elif zchk=="Z":
        xA = [1, 0, 0, 0, 0, 0, -1, 0]
    elif zchk=="S":
        xA = [1, 0, 0, 0, 0, 0, 0, 1]
    elif zchk=="T":
        # xA = [1, 0, 0, 0, 0, 0, math.math.cos(xPi / 4), math.sin(xPi / 4)]
        xA = [1, 0, 0, 0, 0, 0, 1 / math.sqrt(2), 1 / math.sqrt(2), 0]
    elif zchk=="V":
        xA = [1 / 2, 1 / 2, 1 / 2, -1 / 2, 1 / 2, -1 / 2, 1 / 2, 1 / 2]
    elif zchk=="Rx":
        xC = float((xS + " ").split(" ")[1])/2.0
        xA = [math.cos(xC), 0, 0, -math.sin(xC), 0, -math.sin(xC), math.cos(xC), 0]
    elif zchk=="Ry":
        xC = float((xS + " ").split(" ")[1])/2.0
        xA = [math.cos(xC), 0, -math.sin(xC), 0, math.sin(xC), 0, math.cos(xC), 0]
    elif zchk=="Rz":
        xC = float((xS + " ").split(" ")[1])/2.0
        xA = [math.cos(xC), -math.sin(xC), 0, 0, 0, 0, math.cos(xC), math.sin(xC)]
    elif zchk=="Ph":
        xC = float((xS + " ").split(" ")[1])
        xA = [math.cos(xC), math.sin(xC), 0, 0, math.cos(xC), math.sin(xC), 0, 0]
    elif zchk=="Pp":
        xC = float((xS + " ").split(" ")[1])
        xA = [1, 0, 0, 0, 0, 0, math.cos(xC), math.sin(xC)]
    elif zchk=="U":
        xC = float((xS + " ").split(" ")[1])/2.0
        xD = float((xS + " ").split(" ")[2])
        xE = float((xS + " ").split(" ")[3])
        xA = [math.cos(xC), 0, -math.sin(xC) * math.cos(xD), math.sin(xC) * math.sin(xD), math.sin(xC) * math.cos(xE), -math.sin(xC) * math.sin(xE), math.cos(xC) * math.cos(xD + xE), math.cos(xC) * math.sin(xD + xE)]
    else:
        xA = [1, 0, 0, 0, 1, 0, 0, 0]

    xB = (xT + "||||").split("|")
    xmat = str(round(float(xA[0])*float(xB[0]) - float(xA[1])*float(xB[1]) + float(xA[2])*float(xB[2]) - float(xA[3])*float(xB[3]), 4)) + "|"
    xmat = xmat + str(round(float(xA[0])*float(xB[1]) + float(xA[1])*float(xB[0]) + float(xA[2])*float(xB[3]) + float(xA[3])*float(xB[2]), 4)) + "|"
    xmat = xmat + str(round(float(xA[4])*float(xB[0]) - float(xA[5])*float(xB[1]) + float(xA[6])*float(xB[2]) - float(xA[7])*float(xB[3]), 4)) + "|"
    xmat = xmat + str(round(float(xA[4])*float(xB[1]) + float(xA[5])*float(xB[0]) + float(xA[6])*float(xB[3]) + float(xA[7])*float(xB[2]), 4))
    return xmat
#=====================================================================================================

def qblo(dtqr):
    """
    For help to plot Bloch spheres for a dataframe of qubits
    Output: Matplotlib plot of Bloch sphere
    dtqr  : Pandas dataframe of t, q, r
    t     : Positive integer denoting opertation time sequence number    
    q     : Character or positive integer denoting qudit sequence number
    r     : "0r|0i|1r|1i" string of real and imaginary parts of qubit states 0 and 1
    """
    ztmx = int(dtqr['Time'].max())+1
    zque = dtqr['Qubi'].unique()
    zquc = len(zque)
    print(str(ztmx) + " " + str(zque) + " " + str(zquc))
    zfig, zaxs = plt.subplots(zquc, ztmx)
    zavs = 3.1457/6.0 #Angle between vertical and slented lines

    zlwt = 1.0
    for ztim in range(ztmx):
        zqun = 0
        for zquv in zque:

            zaxe = zaxs[zqun, ztim]
            zqun = zqun + 1
            zaxe.set_aspect(1)
            zaxe.spines['top'].set_visible(False)
            zaxe.spines['right'].set_visible(False)
            zaxe.spines['bottom'].set_visible(False)
            zaxe.spines['left'].set_visible(False)
            zaxe.get_xaxis().set_visible(False)
            zaxe.get_yaxis().set_visible(False)
            zaxe.get_xaxis().set_ticks([])
            zaxe.get_yaxis().set_ticks([])

            if (len(dtqr[(dtqr['Time']==ztim) & (dtqr['Qubi']==zquv)])>0):

                zres = dtqr[(dtqr['Time']==ztim) & (dtqr['Qubi']==zquv)].iloc[0,2]
                zq0r = qstn(zres[0], False)
                zq0i = qstn(zres[1], False)
                zq1r = qstn(zres[2], False)
                zq1i = qstn(zres[3], False)

                try:
                    ztha = round(1.57285 + 1.57285 * (-zq0r * zq0r - zq0i * zq0i + zq1r * zq1r + zq1i * zq1i) / (
                        zq0r * zq0r + zq0i * zq0i + zq1r * zq1r + zq1i * zq1i), 4)
                    zphi = round(1.57285 * (zq0r * zq0i + zq0r * zq1i + zq1r * zq0i + zq1r * zq1i) / (
                        zq0r * zq0r + zq0i * zq0i + zq1r * zq1r + zq1i * zq1i), 4)
                except:
                    ztha = 0.0
                    zphi = 0.0
                zphj = round(zphi - zavs * math.sin(zphi), 4)
                zxad = round(math.sin(ztha) * math.cos(zphj), 4)
                zyad = -round(math.cos(ztha), 4)

                zaxe.plot([1.0,1.0+zxad], [1.0,1.0+zyad], color="red", lw=3.0)
                zaxe.add_patch(Circle(xy=(1.0,1.0), radius=1.0, edgecolor='gray', fill=False, lw=zlwt))
                zaxe.add_patch(Ellipse(xy=(1.0,1.0), width=2.0, height=0.6, edgecolor='gray', fc='None', lw=zlwt))
                zaxe.plot([1.0,1.0], [1.0,2.2], color='gray', lw=zlwt)
                zaxe.plot([1.0,2.2], [1.0,1.0], color='gray', lw=zlwt)
                zaxe.plot([1.0,0.6], [1.0,0.6], color='gray', lw=zlwt)       
                if (zlwt==1.0): zlwt=0.1

    zfig.savefig("qplt.jpg")
    plt.show()        
    return zfig
#=====================================================================================================

def qsim(ssgqt):
    """
    To simulate a quantum circuit based on a string
    Output: Matplotlib plot
    ssgqt : String of sgqt strings concatenated by pipe ('|')
    sgqt  : String of g q t strings concatenated by comma
    g     : String of item-name and applicable arguments strings concatenated by space
    q     : Positive integer denoting qudit sequence number
    t     : Positive integer denoting opertation time sequence number
    """
    zco0 = ['Item1','Qubi1','Time1','Item2','Qubi2','Time2','Resu']
    zco1 = ['Time','Qubi','Resu']
    zdf0 = pd.DataFrame(columns=zco0)
    zdf1 = pd.DataFrame(columns=zco1)

    for sgqt in ssgqt.split('|'):
        agqt = (sgqt + ",,,,,").split(",")
        i1, q1, t1, i2, q2, t2 = agqt[0], agqt[1], qstn(agqt[2]), agqt[3], agqt[4], qstn(agqt[5])
        zdf0 = pd.concat([zdf0, pd.DataFrame([[i1, q1, t1, i2, q2, t2, ""]], columns=zco0)], ignore_index=True)
    zdft = zdf0["Time1"].unique()
    zdfq = zdf0[zdf0["Qubi1"] != "a"]["Qubi1"].unique()

    for zti1 in zdft:
        zdfa = zdf0[(zdf0["Qubi1"]=="a") & (zdf0["Time1"]==zti1)][zco0]
        if len(zdfa)>0:
            for zqu1 in zdfq:
                zdf0 = pd.concat([zdf0, pd.DataFrame([[zdfa.iloc[0,0], zqu1, zti1, "", "", 0, ""]], columns=zco0)], ignore_index=True)

    for zqu1 in zdfq:
        if len(zdf0[(zdf0["Qubi1"]==zqu1) & (zdf0["Time1"]=="0")])<1:
            zdf1 = pd.concat([zdf1, pd.DataFrame([[0, zqu1, "1|0|0|0"]], columns=zco1)], ignore_index=True)
        else:
            if len(zdf0[(zdf0["Qubi1"]==zqu1) & (zdf0["Time1"]=="0") & (zdf0["Item1"]=="0")])>1:
                zdf1 = pd.concat([zdf1, pd.DataFrame([0, zqu1, "1|0|0|0"], columns=zco1)], ignore_index=True)
            else:
                if len(zdf0[(zdf0["Qubi1"]==zqu1) & (zdf0["Time1"]=="0") & (zdf0["Item1"]=="1")])>1:
                    zdf1 = pd.concat([zdf1, pd.DataFrame([0, zqu1, "0|0|1|0"], columns=zco1)], ignore_index=True)
                else:
                    if len(zdf0[(zdf0["Qubi1"]==zqu1) & (zdf0["Time1"]=="0") & (zdf0["Item1"][0]=="Q")])>1:
                        zres = (zdf0[zdf0["Qubi1"]==zqu1 & zdf0["Time1"]=="0" &  zdf0["Item1"][0]=="Q"][0] + "   ").split(" ")
                        zag1 = float(zres[1])
                        zag2 = float(zres[2])
                        zres = str(round(math.cos(zag1)*math.cos(zag2),4)) + "|" + str(round(math.cos(zag1)*math.sin(zag2),4)) + "|" + str(round(math.sin(zag1)*math.cos(zag2),4)) + "|" + str(round(math.sin(zag1)*math.sin(zag2),4))
                        zdf1 = pd.concat([zdf1, pd.DataFrame([0, zqu1, zres], columns=zco1)], ignore_index=True)

    for zti1 in range(1, int(zdft.max())):
        for zqu1 in zdfq:
            zlin = zdf0[(zdf0["Time1"]==zti1) & (zdf0["Qubi1"]==zqu1)][zco0]
            zad1 = []
            zad2 = []
            if (len(zdf1[(zdf1["Time"]==zti1) & (zdf1["Qubi"]==zqu1)])<1):
                try:
                    zad1 = [zti1, zqu1, zdf1[(zdf1["Time"]==zti1-1) & (zdf1["Qubi"]==zqu1)].iloc[0,2]]
                except:
                    zad1 = [zti1, zqu1, "0|0|0|0"]
            if (zlin.shape[0]>0):
                zit1,zit2,zqu2,zti2,zres = zlin.iloc[0,0],zlin.iloc[0,3],zlin.iloc[0,4],zlin.iloc[0,5],zlin.iloc[0,6]
                if (zit1=='Sw'):                    
                    if (zti1==zti2): # This condition needs to be removed.
                        zad1 = [zti1, zqu1, zdf1[(zdf1["Time"]==zti1-1) & (zdf1["Qubi"]==zqu2)].iloc[0,2]]
                        zad2 = [zti2, zqu2, zdf1[(zdf1["Time"]==zti1-1) & (zdf1["Qubi"]==zqu1)].iloc[0,2]]
                else:
                    if (zit1=='iSw'):
                        if (zti1==zti2): # This condition and the following 3 lines need to be removed.
                            zad1 = [zti1, zqu1, zdf1[(zdf1["Time"]==zti1-1) & (zdf1["Qubi"]==zqu2)].iloc[0,2]]
                            zad2 = [zti2, zqu2, zdf1[(zdf1["Time"]==zti1-1) & (zdf1["Qubi"]==zqu1)].iloc[0,2]]
                    else:
                        ztru = 0
                        try:
                            if (zit1=='C'):
                                if (zdf1[(zdf1["Time"]==zti1-1) & (zdf1["Qubi"]==zqu1)].iloc[0,2]=="0|0|1|0"):
                                    ztru=1
                                else:
                                    if (zit1=='Cd'):
                                        if (zdf1[(zdf1["Time"]==zti1-1) & (zdf1["Qubi"]==zqu1)].iloc[0,2]=="1|0|0|0"):
                                            ztru=1
                        except:
                            z=1
                        if (ztru==1):
                            if (zit2 in ["H","X","Y","Z","S","T","V","Rx","Ry","Rz","Ph","Pp","U"]):
                                zad1 = [zti2, zqu2, qmat(zit1, zdf1[(zdf1["Time"]==zti2-1) & (zdf1["Qubi"]==zqu2)].iloc[0,2])] # "1|0|0|0"
                        else:
                            if (zit1 in ["H","X","Y","Z","S","T","V","Rx","Ry","Rz","Ph","Pp","U"]):
                                zad1 = [zti1, zqu1, qmat(zit1, zdf1[(zdf1["Time"]==zti1-1) & (zdf1["Qubi"]==zqu1)].iloc[0,2])] # "1|0|0|0"
                            else:
                                if (zit1 in ["O","M"]):
                                    zad1 = [zti1, zqu1, zdf1[(zdf1["Time"]==zti1-1) & (zdf1["Qubi"]==zqu1)].iloc[0,2]] # "1|0|0|0"

            if (zad1 != []): zdf1 = pd.concat([zdf1, pd.DataFrame([zad1],columns=zco1)], ignore_index=True)
            if (zad2 != []): zdf1 = pd.concat([zdf1, pd.DataFrame([zad2],columns=zco1)], ignore_index=True)
    zdf1.to_csv("qsim.csv")
    print(zdf1)
    zblo = qblo(zdf1)
    return zdf1, zblo
#=====================================================================================================

# qhtm()
# qxls()
# txt = '1,3,0|Q 30 15,5,0|H,a,1|Y,1,2|Z,2,2|X,3,2|Y,4,2|Z,5,2|X,6,2|S,2,3|T,4,3|V,6,3|'
# txt = txt + 'Rx 30,1,4|Ry 15,2,4|Rz 15,3,4|Rz 30,4,4|Ry 15,5,4|Rx 15,6,4|Ph 15,2,5|'
# txt = txt + 'Pp 30,4,5|O,a,6|Cd,1,7,Ph 15,2,7|K,3,7|U 30 30 15,4,7|U 15 15 30,6,7|'
# txt = txt + 'C,1,8,X,2,9|Sw,4,8,Sw,6,8|iSw,3,9,iSw,4,9|M,a,10'
# qplt(txt)
# qsim(txt)
