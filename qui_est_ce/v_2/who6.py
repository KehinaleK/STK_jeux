#Choses à implémenter :
#Si la génération des animaux de fait automatiquement, deux animaux ne doivent pas avoir exactement les mêmes caratéristiques "oui"
#Interface graphique ?
#Possibilité de rejouer
#Implémenter des vies lorsqu'on choisi mal un animal ?
#Il faudrait incorporer une gestion des choix_attribut choisi basé sur le nombre d'animaux ayant cet attribut également.
#IL faudrait que nous ayons des attributs de plus en plus spécifique pour toujours finir avec un seul animal et ne pas envoyer des attributs qui n'éliminent personne.
#Ajouter un indice de spécificité ?
#Ajouter une condition unique à chaque animal, dire que l'attribut choisi doit toujours avoir plusieurs yes (outre l'animal choisi). Jusqu'à qu'il ne reste que l'attribut unique. 

import random

def main():
    while True:
        dico = base_animaux()
        premier_choix, liste = choix_animal(dico)
        attributs_positifs = suppression_attributs_negatifs(dico, premier_choix)
        while len(liste) > 1:
            liste_attributs, choix_attribut = choix_caracteristique(attributs_positifs)
            liste_a_eliminer, liste_a_conserver = gestion_elimination(dico, choix_attribut, liste)
            new_liste = elimination(choix_attribut, liste_a_eliminer, liste_a_conserver, liste)
            liste = liste_a_conserver
            print(liste)
            if len(liste) != 1:
                del attributs_positifs[choix_attribut]
                print(f"Il reste {len(liste)} animaux : {liste}.\nPassons à la manche suivante.")
            else:
                print(f"Bravo ! Vous avez trouvé l'animal '{premier_choix}'.")
                break

def base_animaux(): #Création d'un dictionnaire qui recense les caractéristiques de tous les animaux.

    a_des_ailes = "[ailes][avoir]"
    peut_respirer_sous_leau = "[respirer][sous][l'eau][possible]"
    a_quatre_pattes = "[quatre][pattes][avoir]"
    a_des_moustaches = "[moustaches][avoir]"
    est_un_felin = "[felin][être]"
    est_un_canide = "[canide][être]"
    vie_climat_froid = "[climat][froid][vivre]"
    unique_aigle = "[Emblème][États-Unis]"
    unique_chat = "[Divinité][Égypte]"
    unique_chien = "[meilleur][ami][homme]"
    unique_poisson = "[vivre][bocal][possibilité]"
    unique_loutre = "[dans][l'eau][dormir][sur][dos]"
    unique_manchot = "[penguin][confondre][souvent]"
    unique_loup = "[avec][pleine][lune][connexion]"
    unique_lynx = "[Tigre][blanc][ressemblance]"

    #est_un_animal_domestique = "[animal][domestique][être]"
    #a_un_bec = "[bec][avoir]" 
    #a_des_plumes = "[plumes][avoir]"
    #peut_voler = "[voler][pouvoir]"

    dico = {
        "aigle" : 
            {
            unique_aigle : "oui",
            a_des_ailes : "oui", 
            peut_respirer_sous_leau : "non", 
            a_quatre_pattes : "non", 
            a_des_moustaches : "non", 
            est_un_felin : "non", 
            est_un_canide : "non",
            vie_climat_froid : "non"
            },
        "chat" : 
            {
            unique_chat : "oui",
            a_des_ailes : "non", 
            peut_respirer_sous_leau : "non", 
            a_quatre_pattes : "oui", 
            a_des_moustaches : "oui", 
            est_un_felin : "oui", 
            est_un_canide : "non",
            vie_climat_froid : "non"},
        "chien" : 
            {
             unique_chien : "oui",   
             a_des_ailes : "non", 
             peut_respirer_sous_leau : "non", 
             a_quatre_pattes : "oui", 
             a_des_moustaches : "oui", 
             est_un_felin : "non", 
             est_un_canide : "oui",
             vie_climat_froid : "non"},
        "poisson" : 
            {
             unique_poisson : "oui",
             a_des_ailes : "non", 
             peut_respirer_sous_leau : "oui", 
             a_quatre_pattes : "non", 
             a_des_moustaches : "non", 
             est_un_felin : "non", 
             est_un_canide : "non",
             vie_climat_froid : "non"},
        "loutre" : 
            {
            unique_loutre : "oui",
            a_des_ailes : "non",
            peut_respirer_sous_leau : "oui", 
            a_quatre_pattes : "oui", 
            a_des_moustaches : "oui", 
            est_un_felin : "non", 
            est_un_canide : "non",
            vie_climat_froid : "non"},
        "manchot" : 
            {
             unique_manchot : "oui",
             a_des_ailes : "oui", 
             peut_respirer_sous_leau : "non", 
             a_quatre_pattes : "oui", 
             a_des_moustaches : "non", 
             est_un_felin : "non", 
             est_un_canide : "non",
             vie_climat_froid : "oui"},
        "loup" :
            {
             unique_loup : "oui",   
             a_des_ailes : "non", 
             peut_respirer_sous_leau : "non", 
             a_quatre_pattes : "oui", 
             a_des_moustaches : "oui", 
             est_un_felin : "non", 
             est_un_canide : "oui",
             vie_climat_froid : "oui"},
        "lynx" : 
            {
            unique_lynx : "oui",
            a_des_ailes : "non", 
            peut_respirer_sous_leau : "non", 
            a_quatre_pattes : "oui", 
            a_des_moustaches : "oui", 
            est_un_felin : "oui",
            est_un_canide : "non",
            vie_climat_froid : "oui"}
    }

    return dico


def choix_animal(dico): #Choix de l'animal par l'ordinateur.

    #Création d'une liste d'animaux à partir du dictionnaire
    liste = list(dico.keys())
    #print(liste)

    #Choix par l'ordinateur d'un des animaux
    choix = random.choice(liste)
    print(choix)
    return choix, liste

def suppression_attributs_negatifs(dico, choix): #Création d'un nouveau dictionnaire sans les caractéristiques "non" de l'animal choisi.
    
    animal_choisi_attributs = dico[choix]
    attributs_positifs = {key : value for key, value in animal_choisi_attributs.items() if value == "oui"}
    
    #print(attributs_positifs)
    return attributs_positifs

def choix_caracteristique(attributs_positifs): #Choix de la caractéristique à afficher par l'ordinateur. 
    
    liste_attributs = list(attributs_positifs.keys())
    count_attributs_positifs = len(liste_attributs)
    #print(count_attributs_positifs)
    choix_attribut = random.choice(liste_attributs)
    print(liste_attributs)
    print(choix_attribut)
    return liste_attributs, choix_attribut

def gestion_elimination(dico, choix_attribut, liste): #Créer une liste contenant les animaux à éliminer. 

    liste_a_eliminer = []
    liste_a_conserver = []

    for animal in dico:
        if animal in liste:
            animal_caracteristique = dico[animal]
            for cle in animal_caracteristique:
                if cle == choix_attribut:
                    if animal_caracteristique[cle] == "non":
                        liste_a_eliminer.append(animal)
                    else:
                        liste_a_conserver.append(animal)
                            
    print(liste_a_eliminer, liste_a_conserver)
    return liste_a_eliminer, liste_a_conserver

def elimination(choix_attribut, liste_a_eliminer, liste_a_conserver, liste): #Élimination des animaux non correspondants par l'utilisateur. 

    animaux_elimines = []
    while len(liste_a_eliminer) > 0:
        
        choix_utilisateur = input(f"Quel(s) animal(aux) ne possède(nt) pas la caractéristique : {choix_attribut} ?\nNombre d'animaux à éliminer : {len(liste_a_eliminer)}.\nVotre réponse : ")

        if choix_utilisateur in liste_a_conserver:
            print(f"Raté ! L'animal '{choix_utilisateur}' possède bien la caractéristique {choix_attribut}. Ré-essayez.")
        elif choix_utilisateur in liste_a_eliminer:
            liste_a_eliminer.remove(choix_utilisateur)
            print(liste_a_eliminer)
            print(f"Bravo ! L'animal '{choix_utilisateur}' ne possède pas la caractéristique {choix_attribut}. Il vous reste {len(liste_a_eliminer)} animaux à éliminer.")
        else:
            print("Réponse invalide. Ré-essayez.")


main()