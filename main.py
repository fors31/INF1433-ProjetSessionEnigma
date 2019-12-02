from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import re

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

TAB_COMPLET = [REFLECTEUR, ROTOR3_HAUT, ROTOR3_BAS, ROTOR2_HAUT, ROTOR2_BAS, ROTOR1_HAUT, ROTOR1_BAS, ALPHABET]

class ErreurConfiguration(Exception):

    def __init__(self, erreur):
        self.erreur = erreur

class Enigma:

    def __init__(self, window):
        # Initialisation de la fenêtre
        self.encrypt_state = True
        self.window = window
        window.title("Enigma")
        window.geometry("900x650")

        self.grid_rows = [1, 3, 4, 6, 7, 9, 10, 12]
        self.text_a_chiffer = None

        self.grid_reflecteur = []

        self.grid_rotor3_haut = []
        self.grid_rotor3_bas = []

        self.grid_rotor2_haut = []
        self.grid_rotor2_bas = []

        self.grid_rotor1_haut = []
        self.grid_rotor1_bas = []

        self.grid_alphabet = []

        self.premier_rotor = ""
        self.premier_direction = ""
        self.premier_deplacement = 0

        self.deuxieme_rotor = ""
        self.deuxieme_direction = ""
        self.deuxieme_deplacement = 0

        self.troisieme_rotor = ""
        self.troisieme_direction = ""
        self.troisieme_deplacement = 0

        self.ordre = []
        self.tab_rotors = []

        self.count = 26
        self.num_config = 0

        # Espacement entre les rotors
        Label(window, text=" ", font=("Helvetica", 12)).grid(row=0)
        Label(window, text=" ", font=("Helvetica", 12)).grid(row=2)
        Label(window, text=" ", font=("Helvetica", 12)).grid(row=5)
        Label(window, text=" ", font=("Helvetica", 12)).grid(row=8)
        Label(window, text=" ", font=("Helvetica", 12)).grid(row=11)

        # Création des grilles pour chaque rotor

        self.tabulation_rotors()
        self.grid_reflecteur_text = Label(window, text="Réflecteur", font=("Helvetica", 12)).grid(row=1, column=29)
        self.grid_rotor3_text = Label(window, text="Rotor 3", font=("Helvetica", 12)).grid(row=3, column=29, rowspan=2)
        self.grid_rotor2_text = Label(window, text="Rotor 2", font=("Helvetica", 12)).grid(row=6, column=29, rowspan=2)
        self.grid_rotor1_text = Label(window, text="Rotor 1", font=("Helvetica", 12)).grid(row=9, column=29, rowspan=2)

        self.R3 = (self.grid_rotor3_haut, self.grid_rotor3_bas)
        self.R2 = (self.grid_rotor2_haut, self.grid_rotor2_bas)
        self.R1 = (self.grid_rotor1_haut, self.grid_rotor1_bas)

        Label(window, text=" ", font=("Helvetica", 12)).grid(row=13)

        Separator(window, orient=HORIZONTAL).grid(row=14, columnspan=34, sticky='ew')
        Separator(window, orient=HORIZONTAL).grid(row=15, columnspan=34, sticky='ew')

        Label(window, text=" ", font=("Helvetica", 16)).grid(row=16)
        Label(window,
              text="Zone pour saisir la clé sous forme de trois triplets. Exemple : (R3, G, +7)(R1, D, -6)(R2, D, +5)",
              font=("Helvetica", 10)).grid(row=17, columnspan=30)

        Label(window, text="Clé", font=("Helvetica", 12)).grid(row=18, column=6)
        self.entree_clef = Entry(window, font=("Helvetica", 12), width="30")
        self.entree_clef.grid(row=18, column=7, columnspan=12)

        Label(window, text=" ", font=("Helvetica", 12)).grid(row=19)

        Separator(window, orient=HORIZONTAL).grid(row=20, columnspan=34, sticky='ew')
        Separator(window, orient=HORIZONTAL).grid(row=21, columnspan=34, sticky='ew')

        self.text_source = Text(window, font=("Helvetica", 12), height=4)
        self.text_source.insert(END,
                           "Zone de texte pour taper le message à encrypter ou pour afficher le résultat de décryption")
        self.text_source.bind("<FocusIn>", self.effacer)
        self.text_source.grid(row=22, rowspan=3, columnspan=26)

        Separator(window, orient=HORIZONTAL).grid(row=25, columnspan=34, sticky='ew')
        Separator(window, orient=HORIZONTAL).grid(row=26, columnspan=34, sticky='ew')

        Label(window, text=" ", font=("Helvetica", 3)).grid(row=27)

        self.config = Button(window, text="Configurer rotors", command=self.configurer)
        self.config.grid(row=28, column=1, columnspan=4)
        self.encrypt = Button(window, text="Encrypter ↓↓", command=self.chiffrer, state=DISABLED)
        self.encrypt.grid(row=28, column=6, columnspan=4)
        self.next_step = Button(window, text="Étape suivante", command=self.etape_suivate, state=DISABLED)
        self.next_step.grid(row=28, column=11, columnspan=4)
        self.decrypt = Button(window, text="Décrypter ↑↑", command=self.dechiffrer, state=DISABLED)
        self.decrypt.grid(row=28, column=16, columnspan=4)
        self.reset = Button(window, text="Réinitialiser", command=self.reinitialiser)
        self.reset.grid(row=28, column=21, columnspan=4)

        Label(window, text=" ", font=("Helvetica", 3)).grid(row=29)

        Separator(window, orient=HORIZONTAL).grid(row=30, columnspan=34, sticky='ew')
        Separator(window, orient=HORIZONTAL).grid(row=31, columnspan=34, sticky='ew')

        self.text_cible = Text(window, font=("Helvetica", 12), height=4)
        self.text_cible.insert(END,
                          "Zone de texte pour taper le message à décrypter ou pour afficher le résultat d'encryption")
        self.text_cible.bind("<FocusIn>", self.effacer)
        self.text_cible.grid(row=32, rowspan=3, columnspan=26)

    def tabulation_rotors(self):

        #Réflecteur
        self.grid_reflecteur = [Label(self.window, text=v, font=("Helvetica", 12), relief=SUNKEN, width=3, anchor=CENTER)
                                for v in REFLECTEUR]

        #Rotor 3
        self.grid_rotor3_haut = [Label(self.window, text=v, font=("Helvetica", 12), relief=SUNKEN, width=3, anchor=CENTER)
                                for v in ROTOR3_HAUT]
        self.grid_rotor3_bas = [Label(self.window, text=v, font=("Helvetica", 12), relief=SUNKEN, width=3, anchor=CENTER)
                                for v in ROTOR3_BAS]

        #Rotor 2
        self.grid_rotor2_haut = [Label(self.window, text=v, font=("Helvetica", 12), relief=SUNKEN, width=3, anchor=CENTER)
                                for v in ROTOR2_HAUT]
        self.grid_rotor2_bas = [Label(self.window, text=v, font=("Helvetica", 12), relief=SUNKEN, width=3, anchor=CENTER)
                                for v in ROTOR2_BAS]

        #Rotor 1
        self.grid_rotor1_haut = [Label(self.window, text=v, font=("Helvetica", 12), relief=SUNKEN, width=3, anchor=CENTER)
                                for v in ROTOR1_HAUT]
        self.grid_rotor1_bas = [Label(self.window, text=v, font=("Helvetica", 12), relief=SUNKEN, width=3, anchor=CENTER)
                                for v in ROTOR1_BAS]

        #Alphabet
        self.grid_alphabet = [Label(self.window, text=v, font=("Helvetica", 12), relief=SUNKEN, width=3, anchor=CENTER)
                              for v in ALPHABET]

        self.tab_rotors = [self.grid_reflecteur, self.grid_rotor3_haut, self.grid_rotor3_bas, self.grid_rotor2_haut,
                           self.grid_rotor2_bas, self.grid_rotor1_haut, self.grid_rotor1_bas, self.grid_alphabet]

        for x in self.tab_rotors:
            rangee = self.grid_rows.pop(0)
            for i, k in enumerate(x):
                k.grid(row=rangee, column=i)

        self.grid_rows = [1, 3, 4, 6, 7, 9, 10, 12]

    def effacer(self, event):
        fenetre = str(event.widget)
        if str(event.widget.get(1.0, END)) == "Zone de texte pour taper le message à encrypter ou pour afficher le résultat de décryption\n" \
            or str(event.widget.get(1.0, END)) == "Zone de texte pour taper le message à décrypter ou pour afficher le résultat d'encryption\n":
            event.widget.delete(1.0, END)

        def test_text(event):
            if fenetre == ".!text" and ord(str(event.widget.get(1.0, END))[0]) == 10:
                event.widget.insert(END, "Zone de texte pour taper le message à encrypter ou pour afficher le résultat de décryption")
            elif fenetre == ".!text2" and ord(str(event.widget.get(1.0, END))[0]) == 10:
                event.widget.insert(END,"Zone de texte pour taper le message à décrypter ou pour afficher le résultat d'encryption")

        event.widget.bind("<FocusOut>", test_text)

    def configurer(self):
        text = self.entree_clef.get()
        text_re = re.findall("\([^)]*\)", text)
        try:
            premier = text_re[0].replace("(", "").replace(")", "").replace(" ", "").split(",")
            deuxieme = text_re[1].replace("(", "").replace(")", "").replace(" ", "").split(",")
            troisieme = text_re[2].replace("(", "").replace(")", "").replace(" ", "").split(",")

            complet = [premier, deuxieme, troisieme]

            for x in complet:
                if x[0] != "R1" and x[0] != "R2" and x[0] != "R3":
                    raise ErreurConfiguration("Erreur de rotor!")
                if x[1] != "D" and x[1] != "G":
                    raise ErreurConfiguration("Erreur de direction!")
                if int(x[2]) < -26 or int(x[2]) > 26:
                    raise ErreurConfiguration("Le chiffre doit se trouver entre -26 et 26!")

            if len(set([complet[0][0], complet[1][0], complet[2][0]])) != 3:
                raise ErreurConfiguration("Répétition de rotor!")

            self.premier_rotor = premier[0]
            self.premier_direction = premier[1]
            self.premier_deplacement = int(premier[2])

            self.deuxieme_rotor = deuxieme[0]
            self.deuxieme_direction = deuxieme[1]
            self.deuxieme_deplacement = int(deuxieme[2])

            self.troisieme_rotor = troisieme[0]
            self.troisieme_direction = troisieme[1]
            self.troisieme_deplacement = int(troisieme[2])

            self.ordre = [[self.premier_rotor, self.premier_direction, self.premier_deplacement],
                          [self.deuxieme_rotor, self.deuxieme_direction, self.deuxieme_deplacement],
                          [self.troisieme_rotor, self.troisieme_direction, self.troisieme_deplacement]]

            messagebox.showinfo("Configuration", "Configuration enregistrée!")

            self.init_rotors()

        except ErreurConfiguration as e:
            messagebox.showwarning("Erreur", "Configuration erronnée!\n" + e.erreur)

        except:
            messagebox.showwarning("Erreur", "Configuration erronnée!\nVeuillez respecter le format de configuration.")

    def decalage_droit(self, rotor):
        for x in rotor:
            new_col = (x.grid_info()["column"] + 1) % 26
            x.grid(column=new_col)

        end = rotor.pop()
        rotor.insert(0, end)

    def decalage_gauche(self, rotor):
        for x in rotor:
            new_col = (x.grid_info()["column"] - 1) % 26
            x.grid(column=new_col)

        end = rotor.pop(0)
        rotor.append(end)

    def init_rotors(self):
        switch_rotor = {
            "R1": self.R1,
            "R2": self.R2,
            "R3": self.R3
        }
        for x in self.ordre:
            for i in range(abs(x[2])):
                if x[2] > 0:
                    for k in switch_rotor[x[0]]:
                        self.decalage_droit(k)
                else:
                    for k in switch_rotor[x[0]]:
                        self.decalage_gauche(k)

        self.config.config(state=DISABLED)
        self.encrypt.config(state=ACTIVE)
        self.decrypt.config(state=ACTIVE)

    def chiffrer(self):
        self.text_source.config(state=DISABLED)
        self.text_cible.delete(1.0, END)
        self.text_cible.config(state=NORMAL)

        if self.text_a_chiffer == None:
            self.text_a_chiffer = list(self.text_source.get(1.0, END))

        lettre = self.text_a_chiffer.pop(0).upper()

        while not lettre.isalpha():
            lettre = self.text_a_chiffer.pop(0).upper()

        coord_origin = ord(lettre) - 65

        self.grid_alphabet[coord_origin].config(background="Red")

        etape_1 = int(self.grid_rotor1_bas[coord_origin].cget("text"))
        self.grid_rotor1_bas[coord_origin].config(background="Red")

        etape_2 = (coord_origin + etape_1) % 26
        self.grid_rotor2_bas[etape_2].config(background="Red")

        etape_3 = (etape_2 + int(self.grid_rotor2_bas[etape_2].cget("text"))) % 26
        self.grid_rotor3_bas[etape_3].config(background="Red")

        etape_4 = (etape_3 + int(self.grid_rotor3_bas[etape_3].cget("text"))) % 26
        self.grid_reflecteur[etape_4].config(background="Red")

        etape_5 = (etape_4 + int(self.grid_reflecteur[etape_4].cget("text"))) % 26
        self.grid_rotor3_haut[etape_5].config(background="Blue")

        etape_6 = (etape_5 + int(self.grid_rotor3_haut[etape_5].cget("text"))) % 26
        self.grid_rotor2_haut[etape_6].config(background="Blue")

        etape_7 = (etape_6 + int(self.grid_rotor2_haut[etape_6].cget("text"))) % 26
        self.grid_rotor1_haut[etape_7].config(background="Blue")

        coord_final = (etape_7 + int(self.grid_rotor1_haut[etape_7].cget("text"))) % 26

        self.grid_alphabet[coord_final].config(background="Blue")
        lettre_final = chr(coord_final + 65)

        self.text_cible.insert(END, lettre_final)

        self.text_cible.config(state=DISABLED)
        self.next_step.config(state=ACTIVE)
        self.encrypt.config(state=DISABLED)
        self.decrypt.config(state=DISABLED)

        if len(self.text_a_chiffer) == 1:
            messagebox.showinfo("Fin", "Processus terminé!")
            self.next_step.config(state=DISABLED)


    def dechiffrer(self):
        self.encrypt_state = False

        self.text_cible.config(state=DISABLED)
        self.text_source.delete(1.0, END)
        self.text_source.config(state=NORMAL)

        if self.text_a_chiffer == None:
            self.text_a_chiffer = list(self.text_cible.get(1.0, END))

        lettre = self.text_a_chiffer.pop(0).upper()

        while not lettre.isalpha():
            lettre = self.text_a_chiffer.pop(0).upper()

        coord_origin = ord(lettre) - 65

        self.grid_alphabet[coord_origin].config(background="Blue")

        etape_1 = int(self.grid_rotor1_bas[coord_origin].cget("text"))
        self.grid_rotor1_bas[coord_origin].config(background="Blue")

        etape_2 = (coord_origin + etape_1) % 26
        self.grid_rotor2_bas[etape_2].config(background="Blue")

        etape_3 = (etape_2 + int(self.grid_rotor2_bas[etape_2].cget("text"))) % 26
        self.grid_rotor3_bas[etape_3].config(background="Blue")

        etape_4 = (etape_3 + int(self.grid_rotor3_bas[etape_3].cget("text"))) % 26
        self.grid_reflecteur[etape_4].config(background="Blue")

        etape_5 = (etape_4 + int(self.grid_reflecteur[etape_4].cget("text"))) % 26
        self.grid_rotor3_haut[etape_5].config(background="Red")

        etape_6 = (etape_5 + int(self.grid_rotor3_haut[etape_5].cget("text"))) % 26
        self.grid_rotor2_haut[etape_6].config(background="Red")

        etape_7 = (etape_6 + int(self.grid_rotor2_haut[etape_6].cget("text"))) % 26
        self.grid_rotor1_haut[etape_7].config(background="Red")

        coord_final = (etape_7 + int(self.grid_rotor1_haut[etape_7].cget("text"))) % 26

        self.grid_alphabet[coord_final].config(background="Red")
        lettre_final = chr(coord_final + 65)

        self.text_source.insert(END, lettre_final)

        self.text_source.config(state=DISABLED)
        self.next_step.config(state=ACTIVE)
        self.encrypt.config(state=DISABLED)
        self.decrypt.config(state=DISABLED)

        if len(self.text_a_chiffer) == 1:
            messagebox.showinfo("Fin", "Processus terminé!")
            self.next_step.config(state=DISABLED)


    def etape_suivate(self):

        if self.encrypt_state:
            self.encrypt.config(state=ACTIVE)
        else:
            self.decrypt.config(state=ACTIVE)
        color = self.window.cget("bg")

        for i in self.tab_rotors:
            for k in i:
                k.config(background=color)

        switch_rotor = {
            "R1": self.R1,
            "R2": self.R2,
            "R3": self.R3
        }

        direction = self.ordre[self.num_config][1]
        rotor_action = switch_rotor[self.ordre[self.num_config][0]]

        if self.count > 0:
            if direction == "G":
                for k in rotor_action:
                    self.decalage_gauche(k)
            else:
                for k in rotor_action:
                    self.decalage_droit(k)

        elif self.num_config == 2 and self.count == 0:
            self.num_config = 0
            self.count = 27
            self.etape_suivate()

        elif self.num_config != 2 and self.count == 0:
            self.count = 27
            self.num_config += 1
            self.etape_suivate()

        self.count -= 1
        self.next_step.config(state=DISABLED)

    def reinitialiser(self):

        self.text_source.config(state=NORMAL)
        self.text_source.delete(1.0, END)
        self.text_source.insert(END, "Zone de texte pour taper le message à encrypter ou pour afficher le résultat de décryption")

        self.text_cible.config(state=NORMAL)
        self.text_cible.delete(1.0, END)
        self.text_cible.insert(END, "Zone de texte pour taper le message à décrypter ou pour afficher le résultat d'encryption")

        self.entree_clef.delete(0, END)

        self.text_a_chiffer = None
        self.encrypt_state = True

        for x, y in zip(self.tab_rotors, TAB_COMPLET):
            for i in range(26):
                x[i].config(text=y[i])

        for i in self.tab_rotors:
            for k in i:
                k.config(background="SystemButtonFace")

        self.encrypt.config(state=DISABLED)
        self.decrypt.config(state=DISABLED)
        self.config.config(state=ACTIVE)

root = Tk()
start = Enigma(root)
root.mainloop()