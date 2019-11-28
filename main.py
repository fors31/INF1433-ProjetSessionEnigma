from tkinter import *
from tkinter.ttk import *

REFLECTEUR = ["+25", "+23", "+21", "+19", "+17", "+15", "+13", "+11", "+9", "+7", "+5", "+3", "+1", "-1", "-3",
              "-5", "-7", "-9", "-11", "-13", "-15", "-17", "-19", "-21", "-23", "-25"]

ROTOR3_HAUT = ["+12", "-1", "+23", "+10", "+2", "+14", "+5", "-5", "+9", "-2", "-13", "+10", "-2", "-8", "+10",
               "-6", "+6", "-16", "+2", "-1", "-17", "-5", "-14", "-9", "-20", "-10"]
ROTOR3_BAS = ["+1", "+16", "+5", "+17", "+20", "+8", "-2", "+2", "+14", "+6", "+2", "-5", "-12", "-10", "+9", "+10",
              "+5", "-9", "+1", "-14", "-2", "-10", "-6", "+13", "-10", "-23"]

ROTOR2_HAUT = ["+25", "+7", "+17", "-3", "+13", "+19", "+12", "+3", "-1", "+11", "+5", "-5", "-7", "+10", "-2",
               "+1", "-2", "+4", "-17", "-8", "-16", "-18", "-9", "-1", "-22", "-16"]
ROTOR2_BAS = ["+3", "+17", "+22", "+18", "+16", "+7", "+5", "+1", "-7", "+16", "-3", "+8", "+2", "+9", "+2", "-5",
              "-1", "-13", "-12", "-17", "-11", "-4", "+1", "-10", "-19", "-25"]

ROTOR1_HAUT = ["+17", "+4", "+19", "+21", "+7", "+11", "+3", "-5", "+7", "+9", "-10", "+9", "+17", "+6", "-6", "-2",
               "-4", "-7", "-12", "-5", "+3", "+4", "-21", "-16", "-2", "-21"]
ROTOR1_BAS = ["+10", "+21", "+5", "-17", "+21", "-4", "+12", "+16", "+6", "-3", "+7", "-7", "+4", "+2", "+5", "-7",
              "-11", "-17", "-9", "-6", "-9", "-19", "+2", "-3", "-21", "-4"]

ALPHABET =["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

def effacer(event):
    fenetre = str(event.widget)
    if str(event.widget.get(1.0, END)) == "Zone de texte pour taper le message à encrypter ou pour afficher le résultat de décryption\n" \
        or str(event.widget.get(1.0, END)) == "Zone de texte pour taper le message à décrypter ou pour afficher le résultat d'encryption\n":
        event.widget.delete(1.0, END)
    def test_text(event):
        if fenetre == ".!text" and ord(str(event.widget.get(1.0, END))[0]) == 10:
            print(str(event.widget.get(1.0, END)))
            event.widget.insert(END, "Zone de texte pour taper le message à encrypter ou pour afficher le résultat de décryption")
        elif fenetre == ".!text2" and ord(str(event.widget.get(1.0, END))[0]) == 10:
            event.widget.insert(END,"Zone de texte pour taper le message à décrypter ou pour afficher le résultat d'encryption")

    event.widget.bind("<FocusOut>", test_text)


#Initialisation de la fenêtre
window = Tk()
window.title("Enigma")
window.geometry("900x650")

#Espacement entre les rotors
Label(window, text=" ", font=("Helvetica", 12)).grid(row=0)
Label(window, text=" ", font=("Helvetica", 12)).grid(row=2)
Label(window, text=" ", font=("Helvetica", 12)).grid(row=5)
Label(window, text=" ", font=("Helvetica", 12)).grid(row=8)
Label(window, text=" ", font=("Helvetica", 12)).grid(row=11)

#Création des grilles pour chaque rotor
grid_reflecteur = [Label(window, text=v, font=("Helvetica", 12), relief=SUNKEN, width=3, anchor=CENTER).grid(row=1, column=i) for i, v in enumerate(REFLECTEUR)]
grid_reflecteur_text = Label(window, text="Réflecteur",font=("Helvetica", 12)).grid(row=1, column=29)

grid_rotor3_haut = [Label(window, text=v, font=("Helvetica", 12), relief=SUNKEN, width=3, anchor=CENTER).grid(row=3, column=i) for i, v in enumerate(ROTOR3_HAUT)]
grid_rotor3_bas = [Label(window, text=v, font=("Helvetica", 12), relief=SUNKEN, width=3, anchor=CENTER).grid(row=4, column=i) for i, v in enumerate(ROTOR3_BAS)]
grid_rotor3_text = Label(window, text="Rotor 3",font=("Helvetica", 12)).grid(row=3, column=29, rowspan=2)

grid_rotor2_haut = [Label(window, text=v, font=("Helvetica", 12), relief=SUNKEN, width=3, anchor=CENTER).grid(row=6, column=i) for i, v in enumerate(ROTOR2_HAUT)]
grid_rotor2_bas = [Label(window, text=v, font=("Helvetica", 12), relief=SUNKEN, width=3, anchor=CENTER).grid(row=7, column=i) for i, v in enumerate(ROTOR2_BAS)]
grid_rotor2_text = Label(window, text="Rotor 2",font=("Helvetica", 12)).grid(row=6, column=29, rowspan=2)

grid_rotor1_haut = [Label(window, text=v, font=("Helvetica", 12), relief=SUNKEN, width=3, anchor=CENTER).grid(row=9, column=i) for i, v in enumerate(ROTOR1_HAUT)]
grid_rotor1_bas = [Label(window, text=v, font=("Helvetica", 12), relief=SUNKEN, width=3, anchor=CENTER).grid(row=10, column=i) for i, v in enumerate(ROTOR1_BAS)]
grid_rotor1_text = Label(window, text="Rotor 1",font=("Helvetica", 12)).grid(row=9, column=29, rowspan=2)

grid_alphabet = [Label(window, text=v, font=("Helvetica", 12), relief=SUNKEN, width=3, anchor=CENTER).grid(row=12, column=i) for i, v in enumerate(ALPHABET)]

Label(window, text=" ", font=("Helvetica", 12)).grid(row=13)

Separator(window, orient=HORIZONTAL).grid(row=14, columnspan=34, sticky='ew')
Separator(window, orient=HORIZONTAL).grid(row=15, columnspan=34, sticky='ew')

Label(window, text=" ", font=("Helvetica", 16)).grid(row=16)
Label(window, text="Zone pour saisir la clé sous forme de trois triplets. Exemple : (R3, G, +7)(R1, D, -6)(R2, D, +5)",
      font=("Helvetica", 10)).grid(row=17, columnspan=30)

Label(window, text="Clé", font=("Helvetica", 12)).grid(row=18, column=6)
Entry(window, font=("Helvetica", 12), width="30").grid(row=18, column=7, columnspan=12)

Label(window, text=" ", font=("Helvetica", 12)).grid(row=19)

Separator(window, orient=HORIZONTAL).grid(row=20, columnspan=34, sticky='ew')
Separator(window, orient=HORIZONTAL).grid(row=21, columnspan=34, sticky='ew')

text_source = Text(window, font=("Helvetica", 12), height=4)
text_source.insert(END, "Zone de texte pour taper le message à encrypter ou pour afficher le résultat de décryption")
text_source.bind("<FocusIn>", effacer)
text_source.grid(row=22, rowspan=3, columnspan=26)

Separator(window, orient=HORIZONTAL).grid(row=25, columnspan=34, sticky='ew')
Separator(window, orient=HORIZONTAL).grid(row=26, columnspan=34, sticky='ew')

Label(window, text=" ", font=("Helvetica", 3)).grid(row=27)

Button(window, text="Configurer rotors").grid(row=28, column=1, columnspan=4)
Button(window, text="Encrypter").grid(row=28, column=6, columnspan=4)
Button(window, text="Étape suivante").grid(row=28, column=11, columnspan=4)
Button(window, text="Décrypter").grid(row=28, column=16, columnspan=4)
Button(window, text="Réinitialiser").grid(row=28, column=21, columnspan=4)

Label(window, text=" ", font=("Helvetica", 3)).grid(row=29)

Separator(window, orient=HORIZONTAL).grid(row=30, columnspan=34, sticky='ew')
Separator(window, orient=HORIZONTAL).grid(row=31, columnspan=34, sticky='ew')

text_cible = Text(window, font=("Helvetica", 12), height=4)
text_cible.insert(END, "Zone de texte pour taper le message à décrypter ou pour afficher le résultat d'encryption")
text_cible.bind("<FocusIn>", effacer)
text_cible.grid(row=32, rowspan=3, columnspan=26)

def droite():
    for x in tabdelabs:
        new_col = (x.grid_info()["column"] + 1) % 3
        x.grid(column = new_col)

    end = tabdelabs.pop()
    tabdelabs.insert(0, end)

mainloop()