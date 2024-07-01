from mysql.connector import connect
import PySimpleGUI as sg
from datetime import date, datetime
from fichier import Fichier

# Variable globale result que l'on retrouve dans la fonction connexion
result = None
def connexion(idt, mdp):

    global result

    cnx = connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="tokaido"
        )
    
    print(cnx)
    cursor = cnx.cursor()

    # requête qui AFFICHE tout identifiant
    sql = ("SELECT * " "FROM Joueur " "WHERE jou_login = %s " "AND jou_password = %s;")
    data = (f"{idt}", f"{mdp}")

    # on exécute la requête
    cursor.execute(sql, data)
    result = cursor.fetchall()
    print(result)

    cnx.commit()
    cursor.close()
    cnx.close()

    if len(result) >= 1:
        print("TROUVE")
        return True
    else: 
        print("PAS TROUVE")
        return False

def insert_account(name, fname, pseudo, id, mdp):
    # Connexion
    cnx = connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="tokaido"
    )
    print(cnx)
    cursor = cnx.cursor()

    today = datetime.now().date()

    # Query COUNT NB OF Players in database
    count_query = ("SELECT COUNT(jou_nom) "
                    "FROM Joueur;")
    
    cursor.execute(count_query)
    count = cursor.fetchall()
    print(count)

    # Query(s) INSERT => SIGN UP PLAYER
    add_joueur = ("INSERT INTO Joueur "
                    "(jou_id, jou_nom, jou_prenom, jou_pseudo, jou_creation, jou_login, jou_password) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)")

    data_joueur = (count[0][0]+1, f"{name}", f"{fname}", f"{pseudo}", today, f"{id}", f"{mdp}")

    # Execute query 1
    cursor.execute(add_joueur, data_joueur)

    add_stat = ("INSERT INTO Statistiques "
                    "(sta_id, sta_win, sta_lose) "
                    "VALUES (%s, %s, %s)")

    data_stat = (count[0][0]+1, 0, 0)

    # Execute query 2
    cursor.execute(add_stat, data_stat)

    # Make sure data is committed to the database
    cnx.commit()
    cursor.close()
    cnx.close()

def get_stat():

    cnx = connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="tokaido"
        )
    
    print(cnx)
    cursor = cnx.cursor()

    r = Fichier("connected_account.dat").lire()

    # requête qui AFFICHE tout identifiant
    sql = ("SELECT sta_win, sta_lose " "FROM Joueur " "INNER JOIN Statistiques " "ON jou_id = sta_id " "WHERE jou_login = %s " "AND jou_password = %s;")
    data = (f"{r[0][5]}", f"{r[0][6]}")

    # on exécute la requête
    cursor.execute(sql, data)
    result2 = cursor.fetchall()
    Fichier("connected_account_stat.dat").ecrire(result2)
    print(result2)

    cnx.commit()
    cursor.close()
    cnx.close()

def update_winstat(pseudo):

    cnx = connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="tokaido"
        )
    
    print(cnx)
    cursor = cnx.cursor()

    # requête qui AFFICHE tout identifiant
    sql = ("SELECT jou_id, sta_win " "FROM Joueur " "INNER JOIN Statistiques " "ON jou_id = sta_id " "WHERE jou_pseudo = %s;")
    data = (f"{pseudo}",)

    # on exécute la requête
    cursor.execute(sql, data)
    result3 = cursor.fetchall()
    print(result3)
    id_v = result3[0][0]
    victory = result3[0][1]+1

    # requête qui AFFICHE tout identifiant
    sql = ("UPDATE Statistiques " "SET sta_win = %s " "WHERE sta_id = %s;")
    data = (f"{victory}", f"{id_v}")

    # on exécute la requête
    cursor.execute(sql, data)
    result4 = cursor.fetchall()
    print(result4)


    cnx.commit()
    cursor.close()
    cnx.close()

def get_lplayer():

    cnx = connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="tokaido"
        )
    
    print(cnx)
    cursor = cnx.cursor()

    # requête qui AFFICHE tout identifiant
    sql = ("SELECT jou_pseudo, jou_id " "FROM Joueur;")

    # on exécute la requête
    cursor.execute(sql)
    result5 = cursor.fetchall()
    print(result5)

    cnx.commit()
    cursor.close()
    cnx.close()

    return result5