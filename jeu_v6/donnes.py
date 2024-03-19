import random

lsf_lettres = {lettre: f"/alpha/{lettre}.png" for lettre in 'abcdefghijklmnopqrstuvwxyzàâçéèêëîïôœùûü'}

def liste_mots(path_file):

    dossier_images = "/images/"
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
    
    dico_image = {}
    for mots in dico.values():
        for mot in mots:
            chemin_image = f"{dossier_images}{mot}.png"
            dico_image[mot] = chemin_image

    return dico

def choisir_mot(difficulte):
    mots = liste_mots("mots.txt")[difficulte]
    mot_choisi = random.choice(mots).lower()
    return mot_choisi