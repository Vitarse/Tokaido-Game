import pickle

class Fichier:
    def __init__ (self, nom_fichier):
        self.name = nom_fichier

    def ecrire(self, text):
        fichier = open(f"{self.name}", "wb")
        pickle.dump(text, fichier)
        fichier.close()

    def lire(self):
        fichier = open(f"{self.name}", "rb")
        data = pickle.load(fichier)
        fichier.close()
        return data