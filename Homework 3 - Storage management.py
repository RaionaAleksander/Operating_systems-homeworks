# Kodutöö 3 - Salvestusruumi haldus
# Operatsioonisüsteemid 2022/23 sügis
# Aleksander Ontin


########## Moodulid ##########

from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import messagebox
import string 

############################## Algoritm koos kustutamisega (Algorithm with deletion) ##############################

def algoritmWithDeletion(massiiv, sumbol):
    i = 0
    while (i < len(massiiv)):
        if massiiv[i] == sumbol:
            massiiv[i] = " "
        i = i + 1
    return massiiv


############################## Algoritm koos liitmise või suurendamisega (Algorithm with addition or increase) ##############################

def algoritmWithInsertion(massiiv, sumbol, arv):
    i = 0
    while (arv > 0):
        if (i == len(massiiv)):
            return "FAIL"
        if (massiiv[i] == " " and arv > 0):
            massiiv[i] = sumbol
            arv = arv - 1
        i = i + 1
    return massiiv

############################## Algorithm ##############################

def algoritm(maatriks, jarjend):
    
    if (len(maatriks) > len(jarjend)):
        maatriks = maatriks[:len(jarjend)]
    
    for i in range(len(jarjend)):
        if (jarjend[i][1] != "-" and jarjend[i][1][0] != "+"):
            maatriks[i] = algoritmWithInsertion(maatriks[i], jarjend[i][0], int(jarjend[i][1]))
        elif jarjend[i][1] == "-":
            maatriks[i] = algoritmWithDeletion(maatriks[i], jarjend[i][0])
        else:
            maatriks[i] = algoritmWithInsertion(maatriks[i], jarjend[i][0], int(jarjend[i][1][1:]))
        if (maatriks[i] == "FAIL"):
            return maatriks[: i + 1]
        if (not i + 1 == len(jarjend)):
            maatriks[i + 1] = maatriks[i].copy()
    return maatriks

############################## Lisafunktsioonid ##############################

########### Puhasta tabel ###########

def puhasta(): # Puhastab kogu tahvli
    tahvel.delete('all')
    tahvel_frag.delete('all')

########### Massiivide loomine ###########

# teeb järjendist kahetasemelise listi, mida on mugavam töödelda
def massiiviks(input_jarjend):
    valjund = []
    jupid = input_jarjend.split(";")
    for i in range(len(jupid)):
        hakkliha = jupid[i].split(",")
        saabumine = hakkliha[0]
        kestus = hakkliha[1]
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
            messagebox.showerror(title="Input error", message="Incorrect user pattern!")
            return massiiviks(predef1)
    else:
        return massiiviks(predef1)

########### Maatriksi loomine ###########

def maatriksitegija(m, n): # Maatriksi loomine
    maatriks = [[]] * m # "m" on maatriksi kõrgus ja "n" selle pikkus
    for i in range(len(maatriks)):
        maatriks[i] = [' '] * n
    return maatriks

########### Kontrollimine ###########

def kontrollimine(jarjend): # Suuremate ja väiksemate probleemide või vigade kontrollimine
    if len(jarjend) >= 10: # Sammude arvu kontrollimine
        messagebox.showerror(title="Exceeding the maximum number of events", message="The pattern can contain up to 10 events!")
        return False
    
    Sümbolid = []
    kirjavahemärgid = string.punctuation + " "
    
    for i in range(len(jarjend)): 
        if (jarjend[i][0] in kirjavahemärgid or jarjend[i][0] == ""): # Kontrollimine, et failinimetus on kirjavahemärk või tühik
            messagebox.showerror(title="Incorrect name", message="Names should not consist of punctuation or spaces!")
            return False
        elif (len(jarjend[i][0]) > 1): # Failinimetuse pikkuse kontrollimine
            messagebox.showerror(title="Wrong name size", message="The size of '" + jarjend[i][0] + "' should not be greater than 1 letter!")
            return False
        Sümbolid.append(jarjend[i][0])
            
    Unikaalsed_sümbolid = []
    Unikaalsed = set(Sümbolid)
    
    for sumbol in Unikaalsed:
        Unikaalsed_sümbolid.append(sumbol)
        
    KoosPlussiga = []
    
    for sümbol in Unikaalsed_sümbolid:
        seeonesimene = True
        for i in range(len(Sümbolid)):
            if (Sümbolid[i] == sümbol):
                if (seeonesimene):
                    if (jarjend[i][1] == '-'): # Faili kustutamise kontrollimine enne faili loomist
                        messagebox.showerror(title="Wrong order", message="A file '" + sümbol + "' cannot be deleted before it has been created!")
                        return False
                    elif (jarjend[i][1][0] == '+'): # Faili suurendamise kontrollimine enne faili loomist
                        messagebox.showerror(title="Wrong order", message="A file '" + sümbol + "' cannot be deleted before it has been created!")
                        return False
                    else:
                        seeonesimene = False
                elif (not seeonesimene): # Sama faili loomise kontrollimine pärast faili loomist
                    if (jarjend[i][1][0] != '+' and jarjend[i][1] != '-'):
                        messagebox.showerror(title="Wrong order", message="The same file '" + sümbol + "' cannot be created once it has been created!")
                        return False
                    elif (jarjend[i][1][0] == '+'):
                        KoosPlussiga.append(jarjend[i])
                        seeonesimene = False
                    else:
                        seeonesimene = True
    
    if (len(KoosPlussiga) == 0):
        return True # Kui faili suurendamist ei toimu, võib järgmise punkti jätta märkimata ja tagastada "True" 
    
    for i in range(len(KoosPlussiga)):
        if (KoosPlussiga[i][1] == "+"): # Kontrollimine, kas on olemas mõni number koos plussiga
            messagebox.showerror(title="Missing number where plus", message="The file '" + KoosPlussiga[i][0] + "' is missing a number where plus!")
            return False
    
    return True # Kui probleemi ei ole, tagastatakse väärtus "True"
    
########### Fragmenteerimine ###########

def fragmenteerimine(massiiv): # Meetod, mis otsib viimases sammus fragmenteeritud faile ja loob kaks teksti rida
    failid_viimases_massiivis = set(massiiv)
    failid_viimases_massiivis.remove(" ")
    failid_kokku = len(failid_viimases_massiivis)
    maatriks2 = maatriksitegija(failid_kokku, 3)
    indeks = 0
    for fail in failid_viimases_massiivis:
        maatriks2[indeks][0] = fail
        indeks = indeks + 1
        
    fragmenteeritud_kokku = 0
    
    for i in range(len(maatriks2)):
        maatriks2[i][1] = 0
        maatriks2[i][2] = 1
        fragmenteeritud = False
        abi1lopp = False
        abi1 = 0
        abi2 = 0
        for j in range(len(massiiv)):
            if maatriks2[i][0] == massiiv[j]:
                maatriks2[i][1] = maatriks2[i][1] + 1
                if (not fragmenteeritud and abi1 != abi2):
                    maatriks2[i][2] = 0
                    fragmenteeritud_kokku = fragmenteeritud_kokku + 1
                    fragmenteeritud = True
                    continue
                elif (j + 1 != len(massiiv) and massiiv[j + 1] != maatriks2[i][0]):
                    abi1lopp = True
            else:
                abi2 = abi2 + 1
                if (not abi1lopp):
                    abi1 = abi1 + 1
                    
    # "Allesjäänud failidest on fragmenteerunud **.*%."
    tahvel_frag.create_text(31, 25, text="Remaining files are fragmented " + str(round(fragmenteeritud_kokku/failid_kokku * 100, 1)) + "%.", anchor=W)
    
    failid_kokku = 0
    fragmenteeritud_kokku = 0
    for i in range(len(maatriks2)):
        if maatriks2[i][2] == 1:
            fragmenteeritud_kokku = fragmenteeritud_kokku + maatriks2[i][1]
        failid_kokku = failid_kokku + maatriks2[i][1]
      
    # "Fragmenteerunud failidele kuulub **.**% kasutatud ruumist."
    tahvel_frag.create_text(31, 55, text="For fragmented files is " + str(round((failid_kokku - fragmenteeritud_kokku)/failid_kokku * 100, 2))
                        + "% of the space used.", anchor=W)

########### Teksti kirjutamine tahvlisse ###########

def kirjuta(maatriks): # Kirjutab ülejäänud teksti tahvlile
    Massiivi_vahekaugus = 0
    for i in range(len(maatriks)):
        tahvel.create_text(50, 67 + i*38 + Massiivi_vahekaugus, text="Step " + str(i + 1), font=("Helvetica", 8))
        Massiivi_vahekaugus += 10
    for i in range(48):
        tahvel.create_text(117 + i*28, 38, text=str(i + 1), font=("Helvetica", 7))


########### Graafiku joonistamine tahvlisse ###########

def joonista(maatriks, jarjend): # Iga samm (faili loomine, lisamine, kustutamine) on joonistatud siia
    # Igal failil on oma värv
    Sümbolid = [] 
    for i in range(len(jarjend)):
        Sümbolid.append(jarjend[i][0])           
    Unikaalsed_sümbolid = [] # Nimekiri sisaldab mittekorduvaid elemente
    for sumbol in Sümbolid:
        if sumbol in Unikaalsed_sümbolid:
            continue
        else:
            Unikaalsed_sümbolid.append(sumbol)
        
    Värvid = ["#008100", "#ff0000", "#ffa700", "#4483b5", "#ffff00", "#810081", "#00ff80", "#ff6345", "#00ffff"]
    Failide_värvid = {" ": "#FFFFFF", "-": "#d4d4d4"}
    
    for i in range(len(Unikaalsed_sümbolid)): # Iga tähe (suure või väikese) jaoks kasutatakse erinevat värvi
        Failide_värvid[Unikaalsed_sümbolid[i]] = Värvid[i]
    
    Graafik_algus_pikkus = 102
    Graafik_algus_kõrgus = 50
    Pikkus_ühik = 28
    Kõrgus_ühik = 38
    Massiivi_vahekaugus = 0
    for i in range(len(maatriks)):
        if (maatriks[i] == "FAIL"): #Kui esineb tõrge (faili jaoks ei ole piisavalt ruumi)
            tahvel.create_rectangle(Graafik_algus_pikkus, Graafik_algus_kõrgus + Kõrgus_ühik*i + Massiivi_vahekaugus,
                                Graafik_algus_pikkus + Pikkus_ühik*(j+1), Graafik_algus_kõrgus + Kõrgus_ühik*(i+1) + Massiivi_vahekaugus,
                                    fill="#303030")
            tahvel.create_text(Graafik_algus_pikkus + Pikkus_ühik*24, Graafik_algus_kõrgus + Kõrgus_ühik*i + 18 + Massiivi_vahekaugus,
                            text="There is not enough space for the file!", fill="#880808")
            return i + 1
        for j in range(len(maatriks[i])): # Kui kõik on korras
            tahvel.create_rectangle(Graafik_algus_pikkus + Pikkus_ühik*j, Graafik_algus_kõrgus + Kõrgus_ühik*i + Massiivi_vahekaugus,
                                Graafik_algus_pikkus + Pikkus_ühik*(j+1), Graafik_algus_kõrgus + Kõrgus_ühik*(i+1) + Massiivi_vahekaugus,
                                    fill=Failide_värvid[maatriks[i][j]])
            tahvel.create_text(Graafik_algus_pikkus + (Pikkus_ühik*j) + 15, Graafik_algus_kõrgus + Kõrgus_ühik*i + 18 + Massiivi_vahekaugus,
                            text=maatriks[i][j])
        Massiivi_vahekaugus += 10
        
    fragmenteerimine(maatriks[-1]) # Funktsiooni "fragmenteerimine" üleskutse
    
    return len(maatriks) + 1   


########### Algoritmi jooksutamine ###########

def jooksuta_algoritmi():
    jarjend = massiiviMeister()
    maatriks = maatriksitegija(9, 48)
    kontrollija = kontrollimine(jarjend)
    if (kontrollija): # Kui "kontrollija" on "True", siis teeme jargmised punktid
        puhasta()
        maatriks = algoritm(maatriks, jarjend)
        joonista(maatriks, jarjend)
        kirjuta(maatriks)
    
############################## Muutujad ##############################

predef1 = "A,2;B,3;A,-;C,4;B,+3;D,5;E,15;C,-;F,5"
predef2 = "A,4;B,3;C,6;D,5;C,+2;B,-;E,5;A,-;F,10"
predef3 = "A,2;B,3;C,4;D,5;B,-;E,7;D,-;E,+3;F,10"
predef4 = "A,2;B,3;A,-;C,4;B,+3;D,5;E,15;C,-;F,5"

############################## Graafilise kasutajaliidese loomine ##############################

raam = Tk()
raam.title("Planeerimisalgoritmid")
raam.resizable(False, False)
raam.geometry("1470x840")

var = IntVar()
var.set(1)
Radiobutton(raam, text="Esimene", variable=var, value=1).place(x=10,y=60)
Radiobutton(raam, text="Teine", variable=var, value=2).place(x=10,y=105)
Radiobutton(raam, text="Kolmas", variable=var, value=3).place(x=10,y=150)
Radiobutton(raam, text="Enda oma", variable=var, value=4).place(x=10,y=195)

silt_vali = ttk.Label(raam, text="Select or enter a sequence (in the form A,2;B,3;A,-;C,4;B,+3;D,5;E,15;C,-;F,5)")
silt_vali.place(x=10, y=20)

silt1 = ttk.Label(raam, text=predef1)
silt1.place(x=150, y=66)

silt2 = ttk.Label(raam, text=predef2)
silt2.place(x=150, y=111)

silt3 = ttk.Label(raam, text=predef3)
silt3.place(x=150, y=156)

silt_run = ttk.Label(raam, text="Click the button to start the algorithm")
silt_run.place(x=10, y=250)

silt_vali = ttk.Label(raam, text="Calculations:")
silt_vali.place(x=730, y=20)

kasutaja_jarjend = ttk.Entry(raam)
kasutaja_jarjend.insert(INSERT, predef4)
kasutaja_jarjend.place(x=150, y=205, height=30, width=390)

tahvel = Canvas(raam, width=1470, height=490, background="white")
tahvel.place(x=0, y=345)

käivita_nupp = ttk.Button(raam, text="Run", command = lambda : jooksuta_algoritmi())
käivita_nupp.place(x=10, y=290, height=40, width=120)

puhasta_nupp = ttk.Button(raam, text="Clean the output", command = lambda : puhasta() )
puhasta_nupp.place(x=140, y=290, height=40, width=185)

tahvel_frag = Canvas(raam, width=760, height=100)
tahvel_frag.place(x=700, y=60)

raam.mainloop()