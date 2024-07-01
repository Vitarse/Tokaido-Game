import PySimpleGUI as sg
import os
import sqlconnectlogin
from sqlconnectlogin import connexion, insert_account
from fichier import Fichier


def add_account():
    layout2 = [
        [sg.Text("Veuillez rentrer les informations suivantes:")],
        [sg.Text("Nom:              "), sg.Input(key="name")],
        [sg.Text("Prénom:          "), sg.Input(key="fname")],
        [sg.Text("Pseudo:          "), sg.Input(key="pseudo")],
        [sg.Text("Identifiant:       "), sg.Input(key="id")],
        [sg.Text("Mot de passe: "), sg.Input(key="mdp")],
        [sg.Text("", key="error", text_color="darkred")],
        [sg.Button("Create"), sg.Button("Cancel")]
        ]
    
    window2 = sg.Window("CREATION COMPTE", layout2, icon = 'python/images/plus.ico')

    while True:
        event , values = window2.read()

        if event == sg.WIN_CLOSED or event == "Cancel":
            break

        if event == "Create":
            name = str(values['name'])
            fname = str(values['fname'])
            pseudo = str(values['pseudo'])
            id = str(values['id'])
            mdp =  str(values['mdp'])
            lcheck = []
            lcheck.append(name)
            lcheck.append(fname)
            lcheck.append(pseudo)
            lcheck.append(id)
            lcheck.append(mdp)
            check = 5
            for e in lcheck:
                if e == "":
                    check -= 1
            if check == 5:
                insert_account(name, fname, pseudo, id, mdp)
                window2['error'].update("")
                sg.popup("Compte créé avec succès !")
                break

            else:
                window2['error'].update("Veuillez remplir tous les champs !")

    window2.close()



layout = [
        [sg.Column([[sg.Text("Bienvenue voyageur !", key="head", font=('Pristina', (30)))]], justification="center")],
        [sg.Column([[sg.Image(filename="python/images/tokaido_logo2.png", key="image")]], justification="center")],
        [sg.Text("Identifiant:", font=('Pristina', (20)))],
        [sg.Input(key="id")],
        [sg.Text("Mot de passe:", font=('Pristina', (20)))],
        [sg.Input(key="mdp")],
        [sg.Text(key="error", text_color="darkred", font=('Pristina', (15)))],
        [sg.Column([[sg.Button("Log In", size=(10, 1), font=('Pristina', (18))), sg.Button("Sign Up", size=(10,1), font=('Pristina', (18))), sg.Exit("Quit", size=(10,1), font=('Pristina', (18)))]], justification="center")]
        ]

window = sg.Window("CONNEXION TOKAIDO", layout, icon = 'python/images/tokaido-connexion.ico', size=(720,560), default_element_size=(200, 200))


while True:
    event , values = window.read()

    if event == sg.WIN_CLOSED or event == "Quit":
        break

    # Check login entrance
    if event == "Log In":

        idt = str(values['id'])
        mdp = str(values['mdp'])

        if connexion(idt, mdp):
            print(f"Bienvenue à vous {sqlconnectlogin.result[0][3]} !")
            window['error'].Update("")
            Fichier("connected_account.dat").ecrire(sqlconnectlogin.result)
            window.close()
            os.system('cmd /k "menu.bat"')
        
        else:
            window['id'].Update("")
            window['mdp'].Update("")
            window['error'].Update("Identifiant ou mot de passe incorrect, veuillez réessayer.")


    if event == "Sign Up":

        add_account()


window.close()