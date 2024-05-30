# Kodutöö 2 - Mäluhaldus
# Operatsioonisüsteemid 2022/23 sügis
# Aleksander Ontin

"""

"Sisemine fragmenteerumine — ükskõik kui väike ka protsess ei oleks, võtab ta enda alla terve tüki"
"Väline fragmenteerumine — vajalik vaba mälu leidub, aga ta ei ole sidus"

Loeng: https://courses.cs.ut.ee/LTAT.06.001/2022_fall/uploads/Main/os_loeng05_2020.pdf


Küsimus:
Kas meie ülesande tingimustel esineb a) sisemist fragmenteerumist ja b) välist fragmenteerumist? Miks?

Vastus:
a). Meie ülesande tingimustel me ei paiguta protsessi erinevaid osi suvalistesse kohtadesse füüsilises mälus,
    seega puudub sisemine fragmenteerumine (Sisemine fragmenteerumine ei esine meie ülesande tingimustel)

b). Meie ülesande tingimustel mälu jagatakse tervete segmentidega kaupa (first-fit, best-fit näiteks),
    seega tekib väline fragmenteerumine (Väline fragmenteerumine esineb meie ülesande tingimustel)

"""

"""
Programmis peavad olema realiseeritud kõik järgmised algoritmid:
    1). first-fit (kasutada esimest sobivat vaba tükki)
    2). last-fit (kasutada viimast sobivat vaba tükki)
    3). best-fit (kasutada väikseimat piisava suurusega vaba tükki, mitme võrdse puhul neist esimest)
    4). worst-fit (kasutada kõige suuremat sobivat tükki, mitme võrdse puhul neist esimest)
    5). random-fit (kasutada juhuslikult valitud tükki)


- Esimene sobiv (first-fit) — kasutatakse esimest piisava suurusega auku.
    Esimest võib lugeda algusest või eelmisest leitud august alates

- Parim sobiv (best-fit) — kasutatakse vähimat piisava suurusega auku.
    Tuleb läbi otsida kogu nimekiri, enamasti on see suuruse järgi järjestatud
        * Vähimad üle jäävad tükid

- Halvim sobiv (worst-fit) — kasutatakse suurimat vaba auku, samuti vaja kogu nimekiri läbi vaadata
        * Suurimad üle jäävad tükid

"""

########## Moodulid ##########

from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import messagebox
import random

############################## 1 first-fit 1 ##############################

def FirstFit(protsessi_sõnastik):
    
    maatriks = maatriksitegija() # Luuakse maatriks, millel on esialgu 10 rida ja 50 veergu
    indeksi_rida = 0 # Luuakse rea indeks. Algab numbriga 0 ja lõpeb numbriga 9 (kui protsesside arv on 10 ja mitte vähem)
    protsessi_numbrid = list(protsessi_sõnastik.keys()) # Protsessi numbrid (nende tähed)
    vabad_kohad = [] # Vabad ruumid protsesside jaoks
    vaba_koht = [] # Vaba ruum protsesside jaoks
    head_kohad = [] # Head ruumid protsesside jaoks (Vaba ruum on suurem või võrdne protsessi kestusega)
    
    for protsessi_indeks in range(len(protsessi_sõnastik)): # Iga protsessi uuritakse tsükli käigus
        protsessi_number = protsessi_numbrid[protsessi_indeks] # Protsessi number 
        protsessi_kestus = protsessi_sõnastik.get(protsessi_number)[0] # Protsessi kestus
        protsessi_maht = protsessi_sõnastik.get(protsessi_number)[1] # Protsessi maht
        i = 0 
        while(i < 50): # Selles tsüklis otsitakse kõik protsessi jaoks vabad kohad
            if maatriks[indeksi_rida][i] == '-':
                vaba_koht = vaba_koht + [i] # Vaba ruumi algus (kust see algab)
                i = i + 1
            else:
                i = i + 1
                continue
            while(i < 50 and maatriks[indeksi_rida][i] == '-'):
                i = i + 1
            vaba_koht = vaba_koht + [i] # Vaba ruumi lõpp (kus see lõpeb)
            vabad_kohad.append(vaba_koht) # Vaba ruumi lisamine
            vaba_koht = []
            i = i + 1
        for koht in vabad_kohad: # See tsükkel otsib kõik head kohad protsessi jaoks, mille suurus on suurem või võrdne protsessi kestusega
            if koht[1] - koht[0] >= protsessi_kestus: # Lõpp - Algus >= Protsessi kestus
                head_kohad.append(koht) # Lisamine
        protsessi_rida = indeksi_rida
        if len(head_kohad) == 0 or protsessi_rida + protsessi_maht > 10: # Kui listi "head_kohad" pikkus on null või kui protsessi maht ületab maatriksi viimase rea
            maatriks = maatriks[:indeksi_rida] # Maatriksist eemaldatakse teatav arv ridu
            maatriks.append("FAIL") # Maatriksisse lisatakse sõna "FAIL"
            return maatriks # Tagastatakse maatriks
        hea_koht = head_kohad[0] # Võetakse esimene hea koht
        for protsessi_rida in range(indeksi_rida, indeksi_rida + protsessi_maht): # Tsüklis asendatakse "-" elemendid suurtähtedega
            # Esimeses tsüklis vaadeldakse maatriksi ridu ja alamtsüklis veerge
            for i in range(hea_koht[0], hea_koht[0] + protsessi_kestus):
                maatriks[protsessi_rida][i] = protsessi_number # Maatriksis asendatakse "-" elemendid suurtähtedega (Protsessi number)
        vabad_kohad = [] # Vabade protsesside nimekiri muutub tühjaks
        head_kohad = [] # Heade protsesside nimekiri muutub tühjaks
        indeksi_rida = indeksi_rida + 1 # Maatriksi reast saab järgmine rida
    return maatriks # Tagastatakse maatriks

############################## 2 last-fit 2 ##############################

def LastFit(protsessi_sõnastik):
    
    maatriks = maatriksitegija() # Luuakse maatriks, millel on esialgu 10 rida ja 50 veergu
    indeksi_rida = 0 # Luuakse rea indeks. Algab numbriga 0 ja lõpeb numbriga 9 (kui protsesside arv on 10 ja mitte vähem)
    protsessi_numbrid = list(protsessi_sõnastik.keys()) # Protsessi numbrid (nende tähed)
    vabad_kohad = [] # Vabad ruumid protsesside jaoks
    vaba_koht = [] # Vaba ruum protsesside jaoks
    head_kohad = [] # Head ruumid protsesside jaoks (Vaba ruum on suurem või võrdne protsessi kestusega)
    
    for protsessi_indeks in range(len(protsessi_sõnastik)): # Iga protsessi uuritakse tsükli käigus
        protsessi_number = protsessi_numbrid[protsessi_indeks] # Protsessi number
        protsessi_kestus = protsessi_sõnastik.get(protsessi_number)[0] # Protsessi kestus
        protsessi_maht = protsessi_sõnastik.get(protsessi_number)[1] # Protsessi maht
        i = 0
        while(i < 50): # Selles tsüklis otsitakse kõik protsessi jaoks vabad kohad
            if maatriks[indeksi_rida][i] == '-':
                vaba_koht = vaba_koht + [i] # Vaba ruumi algus (kust see algab)
                i = i + 1
            else:
                i = i + 1
                continue
            while(i < 50 and maatriks[indeksi_rida][i] == '-'):
                i = i + 1
            vaba_koht = vaba_koht + [i] # Vaba ruumi lõpp (kus see lõpeb)
            vabad_kohad.append(vaba_koht) # Vaba ruumi lisamine
            vaba_koht = [] 
            i = i + 1
        for koht in vabad_kohad: # See tsükkel otsib kõik head kohad protsessi jaoks, mille suurus on suurem või võrdne protsessi kestusega
            if koht[1] - koht[0] >= protsessi_kestus: # Lõpp - Algus >= Protsessi kestus
                head_kohad.append(koht) # Lisamine
        protsessi_rida = indeksi_rida
        if len(head_kohad) == 0 or protsessi_rida + protsessi_maht > 10: # Kui listi "head_kohad" pikkus on null või kui protsessi maht ületab maatriksi viimase rea
            maatriks = maatriks[:indeksi_rida] # Maatriksist eemaldatakse teatav arv ridu
            maatriks.append("FAIL") # Maatriksisse lisatakse sõna "FAIL"
            return maatriks # Tagastatakse maatriks
        hea_koht = head_kohad[-1] # Võetakse viimane hea koht
        for protsessi_rida in range(indeksi_rida, indeksi_rida + protsessi_maht): # Tsüklis asendatakse "-" elemendid suurtähtedega
            # Esimeses tsüklis vaadeldakse maatriksi ridu ja alamtsüklis veerge
            for i in range(hea_koht[0], hea_koht[0] + protsessi_kestus):
                maatriks[protsessi_rida][i] = protsessi_number # Maatriksis asendatakse "-" elemendid suurtähtedega (Protsessi number)
        vabad_kohad = [] # Vabade protsesside nimekiri muutub tühjaks
        head_kohad = [] # Heade protsesside nimekiri muutub tühjaks
        indeksi_rida = indeksi_rida + 1 # Maatriksi reast saab järgmine rida
    return maatriks # Tagastatakse maatriks

############################## 3 best-fit 3 ##############################

def BestFit(protsessi_sõnastik):
    
    maatriks = maatriksitegija() # Luuakse maatriks, millel on esialgu 10 rida ja 50 veergu
    indeksi_rida = 0 # Luuakse rea indeks. Algab numbriga 0 ja lõpeb numbriga 9 (kui protsesside arv on 10 ja mitte vähem)
    protsessi_numbrid = list(protsessi_sõnastik.keys()) # Protsessi numbrid (nende tähed)
    vabad_kohad = [] # Vabad ruumid protsesside jaoks
    vaba_koht = [] # Vaba ruum protsesside jaoks
    head_kohad = [] # Head ruumid protsesside jaoks (Vaba ruum on suurem või võrdne protsessi kestusega)
    
    for protsessi_indeks in range(len(protsessi_sõnastik)): # Iga protsessi uuritakse tsükli käigus
        protsessi_number = protsessi_numbrid[protsessi_indeks] # Protsessi number
        protsessi_kestus = protsessi_sõnastik.get(protsessi_number)[0] # Protsessi kestus
        protsessi_maht = protsessi_sõnastik.get(protsessi_number)[1] # Protsessi maht
        i = 0
        while(i < 50): # Selles tsüklis otsitakse kõik protsessi jaoks vabad kohad
            if maatriks[indeksi_rida][i] == '-':
                vaba_koht = vaba_koht + [i] # Vaba ruumi algus (kust see algab)
                i = i + 1
            else:
                i = i + 1
                continue
            while(i < 50 and maatriks[indeksi_rida][i] == '-'):
                i = i + 1
            vaba_koht = vaba_koht + [i] # Vaba ruumi lõpp (kus see lõpeb)
            vabad_kohad.append(vaba_koht) # Vaba ruumi lisamine
            vaba_koht = []
            i = i + 1
        for koht in vabad_kohad: # See tsükkel otsib kõik head kohad protsessi jaoks, mille suurus on suurem või võrdne protsessi kestusega
            if koht[1] - koht[0] >= protsessi_kestus: # Lõpp - Algus >= Protsessi kestus
                head_kohad.append(koht) # Lisamine
        protsessi_rida = indeksi_rida
        if len(head_kohad) == 0 or protsessi_rida + protsessi_maht > 10: # Kui listi "head_kohad" pikkus on null või kui protsessi maht ületab maatriksi viimase rea
            maatriks = maatriks[:indeksi_rida] # Maatriksist eemaldatakse teatav arv ridu
            maatriks.append("FAIL") # Maatriksisse lisatakse sõna "FAIL"
            return maatriks # Tagastatakse maatriks
        min_indeks = 0
        for indeks in range(len(head_kohad)): # Tsükkel otsib hea ruumi indeksit, mille kestus on lühem kui teistel headel ruumidel
            if head_kohad[indeks][1] - head_kohad[indeks][0] < head_kohad[min_indeks][1] - head_kohad[min_indeks][0]:
                min_indeks = indeks
        hea_koht = head_kohad[min_indeks] # Võetud hea ruumi lühima kestusega
        for protsessi_rida in range(indeksi_rida, indeksi_rida + protsessi_maht): # Tsüklis asendatakse "-" elemendid suurtähtedega
            # Esimeses tsüklis vaadeldakse maatriksi ridu ja alamtsüklis veerge
            for i in range(hea_koht[0], hea_koht[0] + protsessi_kestus):
                maatriks[protsessi_rida][i] = protsessi_number # Maatriksis asendatakse "-" elemendid suurtähtedega (Protsessi number)
        vabad_kohad = [] # Vabade protsesside nimekiri muutub tühjaks
        head_kohad = [] # Heade protsesside nimekiri muutub tühjaks
        indeksi_rida = indeksi_rida + 1 # Maatriksi reast saab järgmine rida
    return maatriks # Tagastatakse maatriks

############################## 4 worst-fit 4 ##############################

def WorstFit(protsessi_sõnastik):
    
    maatriks = maatriksitegija() # Luuakse maatriks, millel on esialgu 10 rida ja 50 veergu
    indeksi_rida = 0 # Luuakse rea indeks. Algab numbriga 0 ja lõpeb numbriga 9 (kui protsesside arv on 10 ja mitte vähem)
    protsessi_numbrid = list(protsessi_sõnastik.keys()) # Protsessi numbrid (nende tähed)
    vabad_kohad = [] # Vabad ruumid protsesside jaoks
    vaba_koht = [] # Vaba ruum protsesside jaoks
    head_kohad = [] # Head ruumid protsesside jaoks (Vaba ruum on suurem või võrdne protsessi kestusega)
    
    for protsessi_indeks in range(len(protsessi_sõnastik)): # Iga protsessi uuritakse tsükli käigus
        protsessi_number = protsessi_numbrid[protsessi_indeks] # Protsessi number
        protsessi_kestus = protsessi_sõnastik.get(protsessi_number)[0] # Protsessi kestus
        protsessi_maht = protsessi_sõnastik.get(protsessi_number)[1] # Protsessi maht
        i = 0
        while(i < 50): # Selles tsüklis otsitakse kõik protsessi jaoks vabad kohad
            if maatriks[indeksi_rida][i] == '-':
                vaba_koht = vaba_koht + [i] # Vaba ruumi algus (kust see algab)
                i = i + 1
            else:
                i = i + 1
                continue
            while(i < 50 and maatriks[indeksi_rida][i] == '-'):
                i = i + 1
            vaba_koht = vaba_koht + [i] # Vaba ruumi lõpp (kus see lõpeb)
            vabad_kohad.append(vaba_koht) # Vaba ruumi lisamine
            vaba_koht = []
            i = i + 1
        for koht in vabad_kohad: # See tsükkel otsib kõik head kohad protsessi jaoks, mille suurus on suurem või võrdne protsessi kestusega
            if koht[1] - koht[0] >= protsessi_kestus: # Lõpp - Algus >= Protsessi kestus
                head_kohad.append(koht) # Lisamine
        protsessi_rida = indeksi_rida
        if len(head_kohad) == 0 or protsessi_rida + protsessi_maht > 10: # Kui listi "head_kohad" pikkus on null või kui protsessi maht ületab maatriksi viimase rea
            maatriks = maatriks[:indeksi_rida] # Maatriksist eemaldatakse teatav arv ridu
            maatriks.append("FAIL") # Maatriksisse lisatakse sõna "FAIL"
            return maatriks # Tagastatakse maatriks
        maks_indeks = 0
        for indeks in range(len(head_kohad)): # Tsükkel otsib hea ruumi indeksit, mille kestus on suurem kui teistel headel ruumidel
            if head_kohad[indeks][1] - head_kohad[indeks][0] > head_kohad[maks_indeks][1] - head_kohad[maks_indeks][0]:
                maks_indeks = indeks
        hea_koht = head_kohad[maks_indeks] # Võetud hea ruumi suurima kestusega
        for protsessi_rida in range(indeksi_rida, indeksi_rida + protsessi_maht): # Tsüklis asendatakse "-" elemendid suurtähtedega
            # Esimeses tsüklis vaadeldakse maatriksi ridu ja alamtsüklis veerge
            for i in range(hea_koht[0], hea_koht[0] + protsessi_kestus):
                maatriks[protsessi_rida][i] = protsessi_number # Maatriksis asendatakse "-" elemendid suurtähtedega (Protsessi number)
        vabad_kohad = [] # Vabade protsesside nimekiri muutub tühjaks
        head_kohad = [] # Heade protsesside nimekiri muutub tühjaks
        indeksi_rida = indeksi_rida + 1 # Maatriksi reast saab järgmine rida
    return maatriks # Tagastatakse maatriks

############################## 5 random-fit 5 ##############################

def RandomFit(protsessi_sõnastik):
    
    maatriks = maatriksitegija() # Luuakse maatriks, millel on esialgu 10 rida ja 50 veergu
    indeksi_rida = 0 # Luuakse rea indeks. Algab numbriga 0 ja lõpeb numbriga 9 (kui protsesside arv on 10 ja mitte vähem)
    protsessi_numbrid = list(protsessi_sõnastik.keys()) # Protsessi numbrid (nende tähed)
    vabad_kohad = [] # Vabad ruumid protsesside jaoks
    vaba_koht = [] # Vaba ruum protsesside jaoks
    head_kohad = [] # Head ruumid protsesside jaoks (Vaba ruum on suurem või võrdne protsessi kestusega)
    
    for protsessi_indeks in range(len(protsessi_sõnastik)): # Iga protsessi uuritakse tsükli käigus
        protsessi_number = protsessi_numbrid[protsessi_indeks] # Protsessi number
        protsessi_kestus = protsessi_sõnastik.get(protsessi_number)[0] # Protsessi kestus
        protsessi_maht = protsessi_sõnastik.get(protsessi_number)[1] # Protsessi maht
        i = 0
        while(i < 50): # Selles tsüklis otsitakse kõik protsessi jaoks vabad kohad
            if maatriks[indeksi_rida][i] == '-':
                vaba_koht = vaba_koht + [i] # Vaba ruumi algus (kust see algab)
                i = i + 1
            else:
                i = i + 1
                continue
            while(i < 50 and maatriks[indeksi_rida][i] == '-'):
                i = i + 1
            vaba_koht = vaba_koht + [i] # Vaba ruumi lõpp (kus see lõpeb)
            vabad_kohad.append(vaba_koht) # Vaba ruumi lisamine
            vaba_koht = []
            i = i + 1
        for koht in vabad_kohad: # See tsükkel otsib kõik head kohad protsessi jaoks, mille suurus on suurem või võrdne protsessi kestusega
            if koht[1] - koht[0] >= protsessi_kestus: # Lõpp - Algus >= Protsessi kestus
                head_kohad.append(koht) # Lisamine
        protsessi_rida = indeksi_rida
        if len(head_kohad) == 0 or protsessi_rida + protsessi_maht > 10: # Kui listi "head_kohad" pikkus on null või kui protsessi maht ületab maatriksi viimase rea
            maatriks = maatriks[:indeksi_rida] # Maatriksist eemaldatakse teatav arv ridu
            maatriks.append("FAIL") # Maatriksisse lisatakse sõna "FAIL"
            return maatriks # Tagastatakse maatriks
        hea_koht = random.choice(head_kohad) # Protsessi jaoks võetakse juhuslikult hea koht
        for protsessi_rida in range(indeksi_rida, indeksi_rida + protsessi_maht): # Tsüklis asendatakse "-" elemendid suurtähtedega
            # Esimeses tsüklis vaadeldakse maatriksi ridu ja alamtsüklis veerge
            for i in range(hea_koht[0], hea_koht[0] + protsessi_kestus):
                maatriks[protsessi_rida][i] = protsessi_number # Maatriksis asendatakse "-" elemendid suurtähtedega (Protsessi number)
        vabad_kohad = [] # Vabade protsesside nimekiri muutub tühjaks
        head_kohad = [] # Heade protsesside nimekiri muutub tühjaks
        indeksi_rida = indeksi_rida + 1 # Maatriksi reast saab järgmine rida
    return maatriks # Tagastatakse maatriks

############################## Lisafunktsioonid ##############################

########### Puhasta tabel ###########

def puhasta(): # Puhastab kogu tahvli
    tahvel.delete('all')

########### Massiivide loomine ###########

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
            messagebox.showerror(title="Input error", message="Incorrect user pattern!")
            return massiiviks(predef1)
    else:
        return massiiviks(predef1)

########### Maatriksi loomine ###########

# Loob 10x50 maatriksi, kus iga element on "-".
def maatriksitegija():
    maatriks = [[]] * 10
    for i in range(len(maatriks)):
        maatriks[i] = ['-'] * 50
    return maatriks

########### Sõnastiku loomine ###########

# Loob sõnastiku, mille võtmed on tähed A kuni J ja väärtused on protsessid
def sõnastikutegija(jarjend):
    suurtähed = 'ABCDEFGHIJ' # Kasutatakse ainult esimesed kümme suurtähte, sest ülesannetes võib olla ainult kümme protsessi või vähem
    protsessi_sõnastik = {} # Luuakse tühi sõnastik
    for i in range(len(jarjend)):
        protsessi_sõnastik[suurtähed[i]] = jarjend[i]
    return protsessi_sõnastik

########### Teksti kirjutamine tahvlisse ###########

def kirjuta(algoritm, protsessi_sõnastik, viga):
    if algoritm == "Worst-fit":
        tahvel.create_text(105, 28, text="Worst-fit", font=('Helvetica', 9, 'bold'))
    elif algoritm == "Random-fit":
        tahvel.create_text(115, 28, text="Random-fit", font=('Helvetica', 9, 'bold'))
    else:
        tahvel.create_text(98, 28, text=algoritm, font=('Helvetica', 9, 'bold'))
    tahvel.create_text(50, 75, text="Stage", font=('Helvetica', 9, 'bold'))
    tahvel.create_text(150, 75, text="Added", font=('Helvetica', 9, 'bold'))
    tahvel.create_text(157, 100, text="process", font=('Helvetica', 9, 'bold'))
    for i in range(10):
        if i == viga:
            break
        tahvel.create_text(50, 140 + i*29, text=str(i + 1))
    for i in range(10):
        if i == viga:
            break
        elif i >= len(protsessi_sõnastik):
            tahvel.create_text(150, 140 + i*29, text="-")
        else:
            võti = list(protsessi_sõnastik.keys())[i]
            tahvel.create_text(150, 140 + i*29, text=võti + " : "
                               + str(protsessi_sõnastik.get(võti)[0]) + "," + str(protsessi_sõnastik.get(võti)[1]))
    for i in range(50):
        tahvel.create_text(235 + i*29, 100, text=str(i))

########### Graafiku joonistamine tahvlisse ###########

def joonista(maatriks):
    Graafik_algus_pikkus = 221
    Graafik_algus_kõrgus = 127
    Pikkus_ühik = 29
    Kõrgus_ühik = 29
    for i in range(len(maatriks)):
        if maatriks[i] == "FAIL":
            tahvel.create_rectangle(Graafik_algus_pikkus, Graafik_algus_kõrgus + Kõrgus_ühik*i,
                                    Graafik_algus_pikkus + Pikkus_ühik*50, Graafik_algus_kõrgus + Kõrgus_ühik*(i+1),
                                    fill=Protsessi_värvid["FAIL"])
            tahvel.create_text(Graafik_algus_pikkus + Pikkus_ühik*25, Graafik_algus_kõrgus + Kõrgus_ühik*i + 15.5,
                              text="Process does not fit in memory", fill="white")
            return i + 1
        else:
            for j in range(len(maatriks[i])):
                tahvel.create_rectangle(Graafik_algus_pikkus + Pikkus_ühik*j, Graafik_algus_kõrgus + Kõrgus_ühik*i,
                                    Graafik_algus_pikkus + Pikkus_ühik*(j+1), Graafik_algus_kõrgus + Kõrgus_ühik*(i+1),
                                        fill=Protsessi_värvid[maatriks[i][j]])
                tahvel.create_text(Graafik_algus_pikkus + (Pikkus_ühik*j) + 14, Graafik_algus_kõrgus + Kõrgus_ühik*i + 15.5,
                              text=maatriks[i][j])
    return len(maatriks) + 1      

########### Algoritmi jooksutamine ###########

def jooksuta_algoritmi(algoritm):
    puhasta()
    jarjend = massiiviMeister()
    if (len(jarjend) >= 11):
        tahvel.create_text(860, 240, text="Up to 10 processes in total!", font=('Helvetica', 10, 'bold'))
        tahvel.create_text(860, 270, text="The number of processes must not exceed 10!", font=('Helvetica', 10, 'bold'))
    else:
        protsessi_sõnastik = sõnastikutegija(jarjend)
        maatriks = kasuvalija(protsessi_sõnastik, algoritm)
        viga = joonista(maatriks)
        kirjuta(algoritm, protsessi_sõnastik, viga)
    
########### Algoritmide otsimine ###########

def kasuvalija(protsessi_sõnastik, algoritm):
    if algoritm == "First-fit":
        return FirstFit(protsessi_sõnastik) # Kutsub meetodit "First-fit"
    elif algoritm == "Last-fit":
        return LastFit(protsessi_sõnastik) # Kutsub meetodit "Last-fit"
    elif algoritm == "Best-fit":
        return BestFit(protsessi_sõnastik) # Kutsub meetodit "Best-fit"
    elif algoritm == "Worst-fit":
        return WorstFit(protsessi_sõnastik) # Kutsub meetodit "Worst-fit"
    elif algoritm == "Random-fit":
        return RandomFit(protsessi_sõnastik) # Kutsub meetodit "Random-fit"

############################## Muutujad ##############################

Protsessi_värvid = {"A": "#008100", "B": "#ff0000", "C": "#ffa700", "D": "#4483b5",
                    "E": "#ffff00", "F": "#810081", "G": "#00ff80", "H": "#ff6345",
                    "I": "#00ffff", "J": "#8b00ff", "-": "#d4d4d4", "FAIL": "#303030"}

predef1 = "4,5;2,7;9,2;4,6;7,1;6,4;8,8;3,6;1,10;9,2"
predef2 = "1,10;6,6;3,9;2,4;1,6;5,2;1,4;5,2;2,1;2,7"
predef3 = "5,10;6,6;3,9;8,4;3,6;5,12;1,4;15,3;3,4;9,7"
predef4 = "1,8;35,4;3,6;4,2;1,4;3,3;1,2;5,1;50,1"

############################## Graafilise kasutajaliidese loomine ##############################

raam = Tk()
raam.title("Planning algorithms")
raam.resizable(False, False)
raam.geometry("1700x825")

var = IntVar()
var.set(1)
Radiobutton(raam, text="First", variable=var, value=1).place(x=10,y=60)
Radiobutton(raam, text="Second", variable=var, value=2).place(x=10,y=105)
Radiobutton(raam, text="Third", variable=var, value=3).place(x=10,y=150)
Radiobutton(raam, text="My own", variable=var, value=4).place(x=10,y=195)

silt_vali = ttk.Label(raam, text="Select or enter a sequence of up to ten elements of the form 3,5;2,7;8,2;4,6;7,1;6,4;8,8;3,6;1,10;9,2")
silt_vali.place(x=10, y=20)

silt1 = ttk.Label(raam, text=predef1)
silt1.place(x=150, y=66)

silt2 = ttk.Label(raam, text=predef2)
silt2.place(x=150, y=111)

silt3 = ttk.Label(raam, text=predef3)
silt3.place(x=150, y=156)

silt_run = ttk.Label(raam, text="Click the button to start the algorithm")
silt_run.place(x=10, y=250)

kasutaja_jarjend = ttk.Entry(raam)
kasutaja_jarjend.insert(INSERT, predef4)
# Üks eelsisestatud testmustritest võiks olla juhendi juures olevatel näidispiltidel kasutatud muster: 1,8;35,4;3,6;4,2;1,4;3,3;1,2;5,1;50,1
kasutaja_jarjend.place(x=150, y=205, height=30, width=365)

tahvel = Canvas(raam, width=1920, height=465, background="white")
tahvel.place(x=0, y=345)

FirstFit_nupp = ttk.Button(raam, text="First-fit", command = lambda : jooksuta_algoritmi("First-fit"))
FirstFit_nupp.place(x=10, y=290, height=40, width=100)

LastFit_nupp = ttk.Button(raam, text="Last-fit", command = lambda : jooksuta_algoritmi("Last-fit"))
LastFit_nupp.place(x=120, y=290, height=40, width=100)

BestFit_nupp = ttk.Button(raam, text="Best-fit", command = lambda : jooksuta_algoritmi("Best-fit"))
BestFit_nupp.place(x=230, y=290, height=40, width=100)

WorstFit_nupp = ttk.Button(raam, text="Worst-fit", command = lambda : jooksuta_algoritmi("Worst-fit"))
WorstFit_nupp.place(x=340, y=290, height=40, width=100)

RandomFit_nupp = ttk.Button(raam, text="Random-fit", command = lambda : jooksuta_algoritmi("Random-fit"))
RandomFit_nupp.place(x=450, y=290, height=40, width=125)

puhasta_nupp = ttk.Button(raam, text="Clean the output", command = lambda : puhasta() )
puhasta_nupp.place(x=585, y=290, height=40, width=175)

raam.mainloop()