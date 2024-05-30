#!/usr/bin/env python3
# vim: set fileencoding=utf8 :
# Näiteprogramm protsessoriaja planeerijate visualiseerimiseks
# algne autor Sten-Oliver Salumaa
# refaktoreerinud ja muidu muutnud Meelis Roos

from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import messagebox

def puhasta():
    tahvel.delete('all')

# joonistab tahvlile protsesse kujutavad ristkülikud numbrite ja protsesside nimedega
def joonista(jarjend):
    puhasta()
    eelmise_loppx = 28
    kaugus = 0
    diagramm = 944
    prot_aja_pikkus = 0
    for j in jarjend:
        prot_aja_pikkus += j[1]
    for i in range(len(jarjend)):
        protsess = jarjend[i][0]
        kestus = jarjend[i][1]
        protsessi_pikkus = kestus*diagramm/prot_aja_pikkus
        # kujund = tahvel.create_rectangle(eelmise_loppx, 60, eelmise_loppx + kestus * 16,100, fill="green")
            # Mina muutsin stringi kommentaariks, kuna kõik protsessid on automaatselt roheliseks värvitud, ja ma otsustasin ka näidata, kuidas string algselt välja nägi, enne kui ma seda muutsin.
            # Olen loonud täpselt sama rea allpool, ainult muutes argumenti lõpus, nii et iga protsess on erineva värviga 
        kujund = tahvel.create_rectangle(eelmise_loppx, 60, eelmise_loppx + protsessi_pikkus,100,
                                         fill=Protsessi_värvid[protsess])
        keskpaik = eelmise_loppx + protsessi_pikkus/2
        #protsess = Text(raam, font="Arial 15")
        protsessi_id = tahvel.create_text(keskpaik, 80, text=protsess, font="Calibri 7")
        m = tahvel.create_text(eelmise_loppx, 110, text=str(kaugus), font="Calibri 7")
        kaugus += kestus
        eelmise_loppx += protsessi_pikkus
    m = tahvel.create_text(eelmise_loppx, 110, text=str(kaugus), font="Calibri 7")

# teeb järjendist kahetasemelise listi, mida on mugavam töödelda
def massiiviks(input_jarjend):
    valjund = []
    jupid = input_jarjend.split(";")
    for i in range(len(jupid)):
        hakkliha = jupid[i].split(",")
        saabumine = int(hakkliha[0])
        kestus = int(hakkliha[1])
        valjund.append([saabumine, kestus])
    return valjund

# otsustab, millist järjendit teha kahetasemeliseks massiiviks
def massiiviMeister():
    jarjend = []
    if var.get() == 1:
        return massiiviks(predef1)
    elif var.get() == 2:
        return massiiviks(predef2)
    elif var.get() == 3:
        return massiiviks(predef3)
    elif var.get() == 4:
        try:
            return massiiviks(kasutaja_jarjend.get())
        except:
            messagebox.showerror(title="Viga sisendis", message="Vigane kasutaja muster!")
            return massiiviks(predef1)
    else:
        return massiiviks(predef1)

# näitab programmis käimasolevat protsessijada
def massiiviTeavitaja(massiiv):
    text.delete(1.0, END)
    for jupp in massiiv:
        text.insert(INSERT, str(jupp) + "\n")

## Meetodis "kasuvalija" panin kommentaaridesse ebavajalikud tingimused ja lõin õigete nimedega uued tingimused
## Meetodis on ainult neli tingimust ja igaüks neist kutsub konkreetset meetodit
def kasuvalija(jarjend, algoritm):
    if algoritm == "FCFS":
        return FCFS(jarjend) # Kutsub meetodit "FCFS"
    elif algoritm == "SJF":
        return SJF(jarjend) # Kutsub meetodit "SJF"
    elif algoritm == "RR5":
        return RR5(jarjend) # Kutsub meetodit "RR"
    elif algoritm == "2x FCFS":
        return FCFS2x(jarjend) # Kutsub meetodit "FCFS2x"

def jooksuta_algoritmi(algoritm):
    jarjend = massiiviMeister()
    massiiviTeavitaja(jarjend)
    (valjund, ooteaeg) = kasuvalija(jarjend, algoritm)
    joonista(valjund)
    keskm_oot = tahvel.create_text(140, 35, text="Average waiting time:  " + str(ooteaeg), font="Calibri 9")

def FCFS(jarjend): #FCFS
    valjund = []
    jarg = 0
    kogu_ooteaeg = 0
    for i in range(len(jarjend)):
        jarjend[i].append("P" + str(i + 1))
    for protsess in sorted(jarjend, key=lambda x:x[0]):
        saabumine = protsess[0]
        kestus = protsess[1]
        ID = protsess[2]
        if kestus <= 0: # Protsesse, mille ajahulk on väiksem või võrdne 0, ei võeta arvesse
            continue
        if saabumine > (jarg):
                # kui kahe protsessi vahel on "auk", siis jäetakse sinna delay näitamiseks õige pikkusega tühik
                valjund.append([" ", saabumine - jarg])
                valjund.append([ID, kestus])
                jarg = saabumine + kestus
        else:
            # vaatab, kui kaua konkreetne protsess oma järge ootas
            if saabumine < jarg:
                kogu_ooteaeg += jarg - saabumine
            # väljundlisti kirjutatakse protsess koos nime ja kestusega
            valjund.append([ID, kestus])
            jarg += kestus
    # arvutan keskmise ooteaja
    kesk_ooteaeg = round(kogu_ooteaeg / len(jarjend), 2)
    return (valjund, kesk_ooteaeg)
    
def SJF(jarjend): #SJF
    valjund = []
    jarg = 0
    kogu_ooteaeg = 0
    prot_saab_aeg = 0
    koopia = jarjend.copy()
    for i in range(len(jarjend)):
        jarjend[i].append("P" + str(i + 1))
    while 0 < len(jarjend):
        abi = len(jarjend)
        for protsess in sorted(jarjend, key=lambda x:x[1]):
            saabumine = protsess[0]
            kestus = protsess[1]
            ID = protsess[2]
            if kestus <= 0: # Protsesse, mille ajahulk on väiksem või võrdne 0, ei võeta arvesse
                jarjend.remove(protsess)
                break
            if saabumine <= prot_saab_aeg:
                prot_saab_aeg = prot_saab_aeg + kestus
                if saabumine > jarg:
                    # kui kahe protsessi vahel on "auk", siis jäetakse sinna delay näitamiseks õige pikkusega tühik
                    valjund.append([" ", saabumine - jarg])
                    valjund.append([ID, kestus])
                    jarg = saabumine + kestus
                else:
                    # vaatab, kui kaua konkreetne protsess oma järge ootas
                    if saabumine < jarg:
                        kogu_ooteaeg += jarg - saabumine
                    # väljundlisti kirjutatakse protsess koos nime ja kestusega
                    valjund.append([ID, kestus])
                    jarg += kestus
                # Ma asendasin loendi esimese elemendi "x", et sama protsessi ei võetaks korduvalt
                jarjend.remove(protsess)
                break
        if abi == len(jarjend):
            prot_saab_aeg = prot_saab_aeg + 1
    # arvutan keskmise ooteaja
    kesk_ooteaeg = round(kogu_ooteaeg / len(koopia), 2)
    return (valjund, kesk_ooteaeg)

# Erinevate protsesside värvid
# Muutuja on sõnastik, kus iga protsessi number on võti ja selle isikuvärv on väärtus
Protsessi_värvid = {"P1": "#a62525", "P2": "#ff0000", "P3": "#ffa600", "P4": "#ffff00",
                    "P5": "#9af064", "P6": "#008100", "P7": "#177245", "P8": "#00bfff",
                    "P9": "#0f52ba", "P10": "#8b00ff", "P11": "#ffc0cb", "P12": "#d0b084",
                    " ": "#ffffff"}

predef1 = "0,5;6,9;6,5;15,10"
predef2 = "0,2;0,4;12,4;15,5;21,10"
predef3 = "5,6;6,9;11,3;12,7"

# GUI
raam = Tk()
raam.title("Planning algorithms")
raam.resizable(False, False)
raam.geometry("1000x562")

var = IntVar()
var.set(1)
Radiobutton(raam, text="First", variable=var, value=1).place(x=10,y=60)
Radiobutton(raam, text="Second", variable=var, value=2).place(x=10,y=100)
Radiobutton(raam, text="Third", variable=var, value=3).place(x=10,y=140)
Radiobutton(raam, text="My own", variable=var, value=4).place(x=10,y=180)

silt_vali = ttk.Label(raam, text="Choose or enter a sequence (in the form 1,10;4,2;12,3;13,2)")
silt_vali.place(x=10, y=20)

silt1 = ttk.Label(raam, text=predef1)
silt1.place(x=150, y=66)

silt2 = ttk.Label(raam, text=predef2)
silt2.place(x=150, y=106)

silt3 = ttk.Label(raam, text=predef3)
silt3.place(x=150, y=146)

silt_run = ttk.Label(raam, text="Click the button to start the algorithm")
silt_run.place(x=10, y=275)

silt_tahvel = ttk.Label(raam, text="Processes at hand:")
silt_tahvel.place(x=700, y=20)

kasutaja_jarjend = ttk.Entry(raam)
kasutaja_jarjend.insert(INSERT, "0,1;1,11;3,3;4,1;8,6;14,2;25,1")
# Üks eelsisestatud testmustritest võiks olla juhendi juures olevatel näidispiltidel kasutatud muster: 0,1;1,11;3,3;4,1;8,6;14,2;25,1
kasutaja_jarjend.place(x=150, y=190, height=30, width=330)

tahvel = Canvas(raam, width=1000, height=150, background="white")
tahvel.place(x=0, y=380)

FCFS_nupp = ttk.Button(raam, text="FCFS", command = lambda : jooksuta_algoritmi("FCFS"))
FCFS_nupp.place(x=10, y=315, height=40, width=110)

SJF_nupp = ttk.Button(raam, text="SJF", command = lambda : jooksuta_algoritmi("SJF"))
SJF_nupp.place(x=130, y=315, height=40, width=110)

RR5_nupp = ttk.Button(raam, text="RR5", state=DISABLED, command = lambda : jooksuta_algoritmi("RR5"))
RR5_nupp.place(x=250, y=315, height=40, width=110)

FCFS2x_nupp = ttk.Button(raam, text="2x FCFS", state=DISABLED, command = lambda : jooksuta_algoritmi("2x FCFS"))
FCFS2x_nupp.place(x=370, y=315, height=40, width=110)

puhasta_nupp = ttk.Button(raam, text="Clean the output", command = lambda : puhasta() )
puhasta_nupp.place(x=700, y=315, height=40, width=180)

text = Text(raam, width=25, height=9)
text.place(x=700, y=60, height=220, width=250)

jooksuta_algoritmi("SJF")

raam.mainloop()

# Aleksander Ontin