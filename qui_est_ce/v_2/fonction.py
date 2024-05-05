from flask import Flask, render_template, session, request
from donnees import dico_habitats
import random
import json
import os


dico_habitats, liste = dico_habitats()

def choix(liste): 

    choix = random.choice(liste)
    print(f"ANIMAL CHOISI : {choix}.")
    animal_choisi_attributs = dico_habitats[choix] # On obtient tous les attributs de l'élément choisi.
    for key, value in animal_choisi_attributs.items():
        if "unique" in key and value == True:
            attribut_unique = key
    # On obtient l'attribut unique de l'élément ! 
    attributs_positifs = {key : value for key, value in animal_choisi_attributs.items() if value == True and "unique" not in key} # On garde seulement ceux qui sont positifs et on dégage l'attribut unique ! 
    liste_attributs = list(attributs_positifs.keys()) # On obtient une liste des attributs positifs. 
    print(f"ATTRIBUTS TRUE : {liste_attributs}.")
    liste_attributs_mix = []
    while len(liste_attributs) > 0:
        choix_mix = random.choice(liste_attributs)
        liste_attributs_mix.append(choix_mix)
        liste_attributs.remove(choix_mix)

    liste_attributs_mix.append(attribut_unique)
    print(f"ATTRIBUTS MIX : {liste_attributs_mix}.")
    # Donc ici on obtient toutes les propriétés qui vont être envoyées à l'élève. 
    # Il faut maintenant qu'on associe toutes les propriétés à des éléments à éliminer. 


    liste_elimination = [] # Une liste de liste.
    elem_elimines = set() # elements éliminés. 

    for attribut in liste_attributs_mix:
        current_elimination = []  # Liste des elements à éliminer pour chaque attribut envoyé à l'utilisateur. 
        for elem, val in dico_habitats.items():
            if elem not in elem_elimines and val.get(attribut, True) == False:
                current_elimination.append(elem)
                elem_elimines.add(elem)
        
        liste_elimination.append(current_elimination)

    print(liste_elimination)


choix(liste=liste)



