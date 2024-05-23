import random

"""
Ce fichier permet la création d'un dictionnaire de vidéos pour l'alphabet et de mots classés par difficulté.
Il permet également de choisir le mot envoyé au joueur par l'ordinateur en fonction de la difficulté choisie.
Ce programme et les variables qu'il retourne sont utilisés dans le programme main_pendu.py.
"""
lsf_lettres = {lettre: f"/alpha/{lettre}.mp4" for lettre in 'eastirnulodmcpévhgfbqjàxèêzykôwâî'}

def liste_mots(path_file):

    dico = {"Facile": [], "Moyen": [], "Difficile": []}
    with open(path_file, "r") as fichier:
        for mot in fichier:
            mot = mot.strip()
            if not mot:
                continue
            if mot in ["Facile", "Moyen", "Difficile"]:
                difficulte = mot
            else:
                dico[difficulte].append(mot)
    return dico

def image():
    dico_image = {}
    dico = liste_mots(path_file="mots.txt")
    for mots in dico.values():
        for mot in mots:
            chemin_image = f"/images/{mot.lower()}.png"
            dico_image[mot.lower()] = chemin_image
 
    return dico_image

def choisir_mot(difficulte):
    mots = liste_mots("mots.txt")[difficulte]
    mot_choisi = random.choice(mots).lower()
    return mot_choisi