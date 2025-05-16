import tkinter as tk
import random
from PIL import Image, ImageTk
import os

mängija_kaart_imgid = []
vastase_kaart_imgid = []

def loe_kaart():
    mast = random.choice(['r', 'b'])  # 'r' - красная, 'b' - черная
    number = random.randint(2, 11)
    return (mast, number)

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
    global mängija_nimi, mängija_summa, vastane_summa, mängija_kaardid, vastase_kaardid, mängija_kaart_imgid, vastase_kaart_imgid

    mängija_nimi = mängija_nimi_entry.get().strip()
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
    for lbl in vastase_kaart_imgid:
        lbl.destroy()
    mängija_kaart_imgid = []
    vastase_kaart_imgid = []

    alustamisnupp.place_forget()
    võta_kaart_nupp.config(state=tk.NORMAL)
    peatu_nupp.config(state=tk.NORMAL)

def võta_kaart():
    global mängija_summa, mängija_kaardid, mängija_kaart_imgid
    kaart = loe_kaart()
    mängija_kaardid.append(kaart)
    mängija_summa += kaart[1]
    mängija_kaardid_label.config(text=f"Mängija kaardid: {mängija_kaardid}")
    mängija_summa_label.config(text=f"Summa: {mängija_summa}")

    try:
        img = Image.open(f"{kaart[0]}{kaart[1]}.png")
        img = img.resize((100, 140))
        img_tk = ImageTk.PhotoImage(img)
        kaart_lbl = tk.Label(aken, image=img_tk)
        kaart_lbl.image = img_tk  # Сохраняем ссылку
        x_pos = 70 + len(mängija_kaart_imgid) * 110
        kaart_lbl.place(x=x_pos, y=400)
        mängija_kaart_imgid.append(kaart_lbl)
    except Exception as e:
        print(f"Ошибка при отображении карты: {e}")

    if mängija_summa > 21:
        lõppseis("Kaotasid! Ületasid 21!")

def peatu():
    global mängija_summa, vastane_summa, vastase_kaardid, vastase_kaart_imgid
    while vastane_summa < 17:
        kaart = loe_kaart()
        vastase_kaardid.append(kaart)
        vastane_summa += kaart[1]
        try:
            img = Image.open(f"{kaart[0]}{kaart[1]}.png")
            img = img.resize((100, 140))
            img_tk = ImageTk.PhotoImage(img)
            kaart_lbl = tk.Label(aken, image=img_tk)
            kaart_lbl.image = img_tk
            x_pos = 70 + len(vastase_kaart_imgid) * 110
            kaart_lbl.place(x=x_pos, y=100)
            vastase_kaart_imgid.append(kaart_lbl)
        except Exception as e:
            print(f"Ошибка при отображении карты противника: {e}")

    vastane_kaardid_label.config(text=f"Vastase kaardid: {vastase_kaardid}")
    vastane_summa_label.config(text=f"Summa: {vastane_summa}")
    lõppseis(arvuta_tulemus(mängija_summa, vastane_summa))

def lõppseis(tulemus):
    print(f"Lõppseis: {tulemus}") 
    lõppseis_label.config(text=f"Tulemus: {tulemus}")
    alustamisnupp.config(text="Mängi uuesti", command=alusta_mängu)
    alustamisnupp.place(x=750, y=470)
    võta_kaart_nupp.config(state=tk.DISABLED)
    peatu_nupp.config(state=tk.DISABLED)
    salvesta_tulemus(mängija_nimi, tulemus, mängija_summa)

def salvesta_tulemus(nimi, tulemus, summa):
    path = os.path.abspath("tulemused.txt")
    print(f"Kirjutan faili: {path}")  
    with open("tulemused.txt", "a", encoding="utf-8") as f:
        f.write(f"{nimi}, {tulemus}, {summa}\n")

def vaata_tulemusi():
    try:
        with open("tulemusedd.txt", "r", encoding="utf-8") as f:
            andmed = f.readlines()
    except FileNotFoundError:
        lõppseis_label.config(text="Tulemuste faili ei leitud.")
        return
    except UnicodeDecodeError:
        lõppseis_label.config(text="Viga faili kodeeringus. Kustuta tulemused.txt ja proovi uuesti.")
        return

    tulemuste_aken = tk.Toplevel(aken)
    tulemuste_aken.title("Mängu tulemused")
    tulemuste_aken.geometry("400x400")

    tulemused_txt = tk.Text(tulemuste_aken, wrap=tk.WORD)
    tulemused_txt.pack(expand=True, fill=tk.BOTH)
    tulemused_txt.insert(tk.END, ''.join(andmed))
    tulemused_txt.config(state=tk.DISABLED)



aken = tk.Tk()
aken.title("Mäng 21")
aken.geometry("1080x700")


try:
    taust_img = Image.open("new3.jpg")
    taust_img = taust_img.resize((1200, 700))
    taust_img_tk = ImageTk.PhotoImage(taust_img)
    taust_label = tk.Label(aken, image=taust_img_tk)
    taust_label.place(x=0, y=0, relwidth=1, relheight=1)
    taust_label.image = taust_img_tk
except Exception as e:
    print(f"Фон не загружен: {e}")

mängija_nimi_label = tk.Label(aken, text="Sisesta Mängija nimi:", font=('Times New Roman', 10), bg='darkred', fg="white")
mängija_nimi_label.place(x=750, y=200)
mängija_nimi_entry = tk.Entry(aken)
mängija_nimi_entry.place(x=750, y=220)

alustamisnupp = tk.Button(aken, text="Alusta mängu", command=alusta_mängu, font=('Times New Roman', 10), bg='darkred', fg="white")
alustamisnupp.place(x=750, y=150)

mängija_kaardid_label = tk.Label(aken, text="Mängija kaardid: []", font=('Times New Roman', 10), bg='darkred', fg="white")
mängija_kaardid_label.place(x=750, y=250)
mängija_summa_label = tk.Label(aken, text="Summa: 0", font=('Times New Roman', 10), bg='darkred', fg="white")
mängija_summa_label.place(x=750, y=350)

vastane_kaardid_label = tk.Label(aken, text="Vastase kaardid: ?", font=('Times New Roman', 10), bg='darkred', fg="white")
vastane_kaardid_label.place(x=750, y=370)
vastane_summa_label = tk.Label(aken, text="Summa: ?", font=('Times New Roman', 10), bg='darkred', fg="white")
vastane_summa_label.place(x=750, y=390)

võta_kaart_nupp = tk.Button(aken, text="Võta kaart", command=võta_kaart, state=tk.DISABLED, font=('Times New Roman', 10), bg='darkred', fg="white")
võta_kaart_nupp.place(x=750, y=285)

peatu_nupp = tk.Button(aken, text="Peatu", command=peatu, state=tk.DISABLED, font=('Times New Roman', 10), bg='darkred', fg="white")
peatu_nupp.place(x=750, y=320)

lõppseis_label = tk.Label(aken, text="Tulemus:", font=('Times New Roman', 10), bg='darkred', fg="white")
lõppseis_label.place(x=750, y=420)


vaata_tulemusi_nupp = tk.Button(aken, text="Vaata tulemusi", command=vaata_tulemusi, font=('Times New Roman', 10), bg='darkred', fg="white")
vaata_tulemusi_nupp.place(x=750, y=440)


aken.mainloop()
