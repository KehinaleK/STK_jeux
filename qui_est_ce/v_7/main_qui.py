from flask import Flask, render_template, session, request, jsonify, redirect, url_for
from donnees import dico_habitats, dico_animaux, dico_nourriture
import random
import json
import os

# KEHINA IL FAUT COUPER LA FIN DE GRATTE CIEL ET AJOUTER LA VRAIE VIDEO DE LA CARAVANE !!!!

app = Flask(__name__)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.debug = True
app.secret_key = 'your_secret_key'



def deroulement_partie(liste, dico):
    print("on va ici deux fois")
    choix = random.choice(liste)
    session['choix'] = choix

    element_choisi_attributs = dico[choix] # On obtient tous les attributs de l'élément choisi.

    for key, value in element_choisi_attributs.items():
        if "unique" in key and value == True:
            attribut_unique = key
    # On obtient l'attribut unique de l'élément ! 
    attributs_positifs = {key : value for key, value in element_choisi_attributs.items() if value == True and "unique" not in key} # On garde seulement ceux qui sont positifs et on dégage l'attribut unique ! 
    liste_attributs = list(attributs_positifs.keys()) # On obtient une liste des attributs positifs. 

    liste_attributs_mix = []
    while len(liste_attributs) > 0:
        choix_mix = random.choice(liste_attributs)
        liste_attributs_mix.append(choix_mix)
        liste_attributs.remove(choix_mix)

    liste_attributs_mix.append(attribut_unique)
    # Donc ici on obtient toutes les propriétés qui vont être envoyées à l'élève. 
    # Il faut maintenant qu'on associe toutes les propriétés à des éléments à éliminer. 


    liste_elimination = [] # Une liste de liste.
    elem_elimines = set() # elements éliminés. 
    attributs_a_elem = []

    for attribut in liste_attributs_mix:
        current_elimination = []  # Liste des elements à éliminer pour chaque attribut envoyé à l'utilisateur. 
        for elem, val in dico.items():
            if elem not in elem_elimines and val.get(attribut, True) == False:
                current_elimination.append(elem)
                elem_elimines.add(elem)
        
        if current_elimination:
            liste_elimination.append(current_elimination)
        else:
            attributs_a_elem.append(attribut)

    for elem in attributs_a_elem:
        for attribut in liste_attributs_mix:
            if elem == attribut:
                liste_attributs_mix.remove(attribut)

    return liste_elimination, liste_attributs_mix



@app.route('/')
def menu_pendu():
    return render_template('menu_qui.html', themes=["habitats", "animaux", "nourriture"])

@app.route('/<themes>')
def lancer_partie(themes):
    return render_template('lancer_partie.html', themes=themes)

@app.route('/game_start/<themes>')
def game_start(themes):
    print(themes)
    if themes == 'habitats':
        image_files = os.listdir('static/habitats/images/')
        dico_images = {file.split('.')[0]: 'habitats/images/' + file for file in image_files}
        dico, liste = dico_habitats()
    elif themes == 'animaux':
        #print("we go there")
        image_files = os.listdir('static/animaux/images/')
        dico_images = {file.split('.')[0]: 'animaux/images/' + file for file in image_files}
        dico, liste = dico_animaux()
        #print(dico, liste)
    elif themes == 'nourriture':
        image_files = os.listdir('static/animaux/images/')
        dico_images = {file.split('.')[0]: 'animaux/images/' + file for file in image_files}
        dico, liste = dico_nourriture()


    liste_elimination, attributs_mix = deroulement_partie(liste, dico)
    session['attributs_mix'] = attributs_mix
    session['liste_elimination'] = liste_elimination
    session['current_index'] = 0  

    first_attribute = attributs_mix[0]
    eliminable_elements = liste_elimination[0]  

    eliminable_images = [dico_images[element] for element in eliminable_elements if element in dico_images]
    images_eliminees = []
    session['images_eliminees'] = images_eliminees

    choix = session['choix']
    choix_image = dico_images[choix]
    session['choix_image'] = choix_image
    print(choix_image)

    return render_template('affichage_images.html', dico=dico_images, attribute=first_attribute, eliminable_images=eliminable_images, images_eliminees=images_eliminees)

@app.route('/next_attribute/<themes>')
def next_attribute(themes):

    if themes == 'habitats' and 'current_index' in session:
        current_index = session['current_index'] + 1
        longueur = len(session['attributs_mix'])
        if current_index != longueur:
            session['current_index'] = current_index
            next_attribute = url_for('static', filename=session['attributs_mix'][current_index])
            eliminable_habitats = session['liste_elimination'][current_index]
            image_files = os.listdir('static/habitats/images/')
            habitat_images = {file.split('.')[0]: 'habitats/images/' + file for file in image_files}
            eliminable_images = [habitat_images[habitat] for habitat in eliminable_habitats if habitat in habitat_images]
            images_eliminees = session.get('images_eliminees', [])
            images_eliminees.extend(eliminable_images)
            session['images_eliminees'] = images_eliminees
            return jsonify(attribute=next_attribute, eliminable_images=eliminable_images, images_eliminees=images_eliminees)

        else:

            image_files = os.listdir('static/habitats/images/')
            habitat_images = {file.split('.')[0]: 'habitats/images/' + file for file in image_files}
            end_game_url = url_for('end_game')
            return jsonify(game_over=True, redirect_url=end_game_url)
       
@app.route('/end_game')
def end_game():
    choix = session.get('choix')
    final_image = session.get('choix_image')
    return render_template('fin_de_partie.html', final_image=final_image, choix=choix)



if __name__ == '__main__':
    app.run(debug=True)