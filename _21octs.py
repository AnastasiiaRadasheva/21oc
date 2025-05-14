import tkinter as tk
import random
from PIL import Image, ImageTk

mängija_kaart_imgid = []

def loe_kaart():
    return random.randint(2, 11)

def arvuta_tulemus(mängija_summa, vastane_summa):
    if mängija_summa > 21:
        return "Kaotasid! Ületasid 21!"
    elif vastane_summa > 21:
        return "Võitsid! Vastane ületas 21!"
    elif mängija_summa > vastane_summa:
        return "Võitsid!"
    elif mängija_summa < vastane_summa:
        return "Kaotasid!"
    else:
        return "Viik!"

def alusta_mängu():
    global mängija_nimi, mängija_summa, vastane_summa, mängija_kaardid, vastase_kaardid, mängija_kaart_imgid

    mängija_nimi = mängija_nimi_entry.get()
    if not mängija_nimi:
        lõppseis_label.config(text="Sisesta mängija nimi!")
        return

    mängija_nimi_entry.config(state=tk.DISABLED)

    mängija_summa, vastane_summa = 0, 0
    mängija_kaardid, vastase_kaardid = [], []

    mängija_kaardid_label.config(text="Mängija kaardid: []")
    mängija_summa_label.config(text="Summa: 0")
    vastane_kaardid_label.config(text="Vastase kaardid: ?")
    vastane_summa_label.config(text="Summa: ?")
    lõppseis_label.config(text="Tulemus:")

    # Удаляем старые изображения карт
    for lbl in mängija_kaart_imgid:
        lbl.destroy()
    mängija_kaart_imgid = []

    alustamisnupp.pack_forget()
    võta_kaart_nupp.config(state=tk.NORMAL)
    peatu_nupp.config(state=tk.NORMAL)

def võta_kaart():
    global mängija_summa, mängija_kaardid, mängija_kaart_imgid
    kaart = loe_kaart()
    mängija_kaardid.append(kaart)
    mängija_summa += kaart
    mängija_kaardid_label.config(text=f"Mängija kaardid: {mängija_kaardid}")
    mängija_summa_label.config(text=f"Summa: {mängija_summa}")

    try:
        img = Image.open(f"r{kaart}.png")
        img = img.resize((100, 140))
        img_tk = ImageTk.PhotoImage(img)
        kaart_lbl = tk.Label(aken, image=img_tk)
        kaart_lbl.image = img_tk
        x_pos = 20 + len(mängija_kaart_imgid) * 110
        kaart_lbl.place(x=x_pos, y=500)
        mängija_kaart_imgid.append(kaart_lbl)
    except Exception as e:
        print(f"Ошибка при отображении карты: {e}")

    if mängija_summa > 21:
        lõppseis("Kaotasid! Ületasid 21!")

def peatu():
    global mängija_summa, vastane_summa, vastase_kaardid
    while vastane_summa < 17:
        kaart = loe_kaart()
        vastase_kaardid.append(kaart)
        vastane_summa += kaart
    vastane_kaardid_label.config(text=f"Vastase kaardid: {vastase_kaardid}")
    vastane_summa_label.config(text=f"Summa: {vastane_summa}")
    lõppseis(arvuta_tulemus(mängija_summa, vastane_summa))

def lõppseis(tulemus):
    lõppseis_label.config(text=f"Tulemus: {tulemus}")
    alustamisnupp.config(text="Mängi uuesti", command=alusta_mängu)  
    alustamisnupp.place(x=875, y=470)
    võta_kaart_nupp.config(state=tk.DISABLED)
    peatu_nupp.config(state=tk.DISABLED)
    salvesta_tulemus(mängija_nimi, tulemus, mängija_summa)

def salvesta_tulemus(nimi, tulemus, summa):
    with open("tulemused.txt", "a") as f:
        f.write(f"{nimi}, {tulemus}, {summa}\n")

aken = tk.Tk()
aken.title("Mäng 21")
aken.geometry("1050x750")

mängija_kaart_img_label = tk.Label(aken)
mängija_kaart_img_label.place(x=700, y=250)

mängija_nimi_label = tk.Label(aken, text="Sisesta Mängija nimi:")
mängija_nimi_label.place(x=875, y=200)
mängija_nimi_entry = tk.Entry(aken)
mängija_nimi_entry.place(x=875, y=220)

alustamisnupp = tk.Button(aken, text="Alusta mängu", command=alusta_mängu)
alustamisnupp.place(x=875, y=150)

mängija_kaardid_label = tk.Label(aken, text="Mängija kaardid: []")
mängija_kaardid_label.place(x=875, y=250)
mängija_summa_label = tk.Label(aken, text="Summa: 0")
mängija_summa_label.place(x=875, y=350)
vastane_kaardid_label = tk.Label(aken, text="Vastase kaardid: ?")
vastane_kaardid_label.place(x=875, y=370)
vastane_summa_label = tk.Label(aken, text="Summa: ?")
vastane_summa_label.place(x=875, y=390)

võta_kaart_nupp = tk.Button(aken, text="Võta kaart", command=võta_kaart, state=tk.DISABLED)
võta_kaart_nupp.place(x=875, y=285)

peatu_nupp = tk.Button(aken, text="Peatu", command=peatu, state=tk.DISABLED)
peatu_nupp.place(x=875, y=320)
lõppseis_label = tk.Label(aken, text="Tulemus:")
lõppseis_label.place(x=875, y=420)
aken.mainloop()