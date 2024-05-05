from flask import Flask, render_template, session, request
from donnees import dico_habitats
import random
import json
import os

app = Flask(__name__)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.debug = True
app.secret_key = 'your_secret_key'

dico_habitats, liste = dico_habitats()

def deroulement_partie(liste):

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

    print("LISTE ELIMINATION", liste_elimination)
    return liste_elimination, liste_attributs_mix

deroulement_partie(liste=liste)


@app.route('/')
def menu_pendu():
    return render_template('menu_qui.html', themes=["habitats", "animaux", "nourriture"])

@app.route('/<themes>')
def lancer_partie(themes):
    return render_template('lancer_partie.html', themes=themes)

@app.route('/game_start/<themes>')
def game_start(themes):
    if themes == 'habitats':
        image_files = os.listdir('static/habitats/')
        habitat_images = {file.split('.')[0]: 'habitats/' + file for file in image_files}

        liste_elimination, attributs_mix = deroulement_partie(liste)
        session['attributs_mix'] = attributs_mix
        session['liste_elimination'] = liste_elimination
        session['current_index'] = 0  # Initialize the index for the first attribute

        first_attribute = attributs_mix[0]
        eliminable_habitats = liste_elimination[0]  # get the first list of eliminable buildings

        eliminable_images = [habitat_images[habitat] for habitat in eliminable_habitats if habitat in habitat_images]
        print("IMAGE A TEJ", eliminable_images)

        return render_template('affichage_images.html', habitats=habitat_images, attribute=first_attribute, eliminable_images=eliminable_images)
    return 'Invalid theme selected', 400

if __name__ == '__main__':
    app.run(debug=True)