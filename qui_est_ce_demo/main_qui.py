from flask import Flask, render_template, session, request, jsonify, redirect, url_for
from donnees import dico_habitats, dico_animaux, dico_nourriture
import random
import os

"""
Ce programme contient la logique du jeu du qui-est-ce. Il utilise les données (dictionnaires et listes) contenues dans le fichier donnees.py.
Ce programme utilise Flask comme framework pour python.
"""

"""Configuration de l'application."""

app = Flask(__name__) # Créer une instance de l'application 
app.config['SESSION_COOKIE_SAMESITE'] = 'None' 
app.secret_key = 'your_secret_key'


def deroulement_partie(liste, dico):

    """
    Le fonction deroulement_partie permet d'obtenir les données issues de donnees.py utiles pour le déroulement de la partie.

    Paramètres : 
    liste (List[str]): liste des éléments parmi lequels l'ordinateur choisi l'élément à trouver (liste d'animaux, d'habitats ou de plats).
    dico (Dict): dictionnaire contenant l'ensemble de nos éléments en clés et des dictionnaires en valeurs. Ces dictionnaires ont pour clés les attributs
    envoyés à l'utilisateur et en valeurs des valeurs Booléenes. 

    Retourne :
    liste_elimination (List[List[str]]): liste de listes. La liste contient autant de listes que d'attributs envoyés à l'utilisateur.
    Dans chaque liste se trouve les éléments devant être éliminés par l'utilisateur et ayant donc une valeur False pour l'attribut envoyé.
    liste_attributs_mix (List[str]): liste des vidéos correspondant à celles envoyées à l'utilisateur. Ces vidéos correspondent à des attributs
    vrais pour l'élément choisi et devant être trouvé en fin de partie. Quand l'ensemble des éléments présents dans la liste correspondante au tour de la vidéo
    dans liste_elimination sont éliminés, nous passons à la prochaine vidéo de liste_attributs_mix. 
    """

    # Choix de l'élément à trouver
    choix = random.choice(liste)
    session['choix'] = choix
    
    # Obtention de tous les attributs pour lesquels l'élément a une valeur True
    element_choisi_attributs = dico[choix]
    for key, value in element_choisi_attributs.items():
        if "unique" in key and value == True:
            attribut_unique = key

    attributs_positifs = {key : value for key, value in element_choisi_attributs.items() if value == True and "unique" not in key} 
    liste_attributs = list(attributs_positifs.keys())

    # Obtention de la même liste mais mélangée pour éviter d'avoir les attributs toujours dans le même sens
    liste_attributs_mix = []
    while len(liste_attributs) > 0:
        choix_mix = random.choice(liste_attributs)
        liste_attributs_mix.append(choix_mix)
        liste_attributs.remove(choix_mix)

    liste_attributs_mix.append(attribut_unique)

    # On garde les attributs permettant d'éliminer les autres éléments que ceux choisis
    liste_elimination = [] 
    elem_elimines = set() 
    attributs_a_elem = []

    for attribut in liste_attributs_mix:
        current_elimination = [] 
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

    """
    Cette fonction correpond à la route du menu du jeu.
    Elle renvoie le template du menu et les valeurs pouvant être attribuées à la variable "themes". 
    """

    return render_template('menu_qui.html', themes=["habitats", "animaux", "nourriture"])


# @app.route('/regles')
# def regles():

#     """
#     Cette fonction correpond à la route du menu "règles" du jeu.
#     Elle renvoie le template du menu contenant la vidéo des règles.
#     """

#     return render_template('menu_regles.html')

@app.route('/<themes>')
def lancer_partie(themes):

    """
    Cette fonction correpond à la route de la page précédent le début du jeu.
    Elle renvoie le template de la page et la variable "themes" permettant de suivre le thème choisi précédemment.
    """

    return render_template('lancer_partie.html', themes=themes)

@app.route('/debut_jeu/<themes>')
def debut_jeu(themes):
    
    """
    Cette fonction correpond à la route permettant de charger la grille d'images du jeu et le premier attribut envoyé à l'utilisateur.
    Elle renvoie le template "affichage_images" et les variables : 
    dico : dictionnaire d'images pour chaque élément.
    attribut : premier attribut envoyé à l'utilisateur.
    elimable_images : images à éliminer.
    images_eliminees : liste_vide contenant les images qui vont être éliminées. 
    themes : theme choisi par l'utilisateur.
    """

    # Pour chaque thème, on obtient le dico et la liste utilisés dans la fonction deroulement_partie permettant d'obtenir
    # un élément à deviner et les éléments à éliminer ainsi que les attributs à envoyer à l'utilisateur.
    session['themes'] = themes
    if themes == 'habitats':
        image_files = os.listdir('static/habitats/images/')
        dico_images = {file.split('.')[0]: 'habitats/images/' + file for file in image_files}
        dico, liste = dico_habitats()
    
    elif themes == 'animaux':
        image_files = os.listdir('static/animaux/images/')
        dico_images = {file.split('.')[0]: 'animaux/images/' + file for file in image_files}
        dico, liste = dico_animaux()
     
    elif themes == 'nourriture':
        image_files = os.listdir('static/nourriture/images/')
        dico_images = {file.split('.')[0]: 'nourriture/images/' + file for file in image_files}
        dico, liste = dico_nourriture()
        
    liste_elimination, attributs_mix = deroulement_partie(liste, dico)
    # On stock ces valeurs pour la prochaine route
    session['attributs_mix'] = attributs_mix
    session['liste_elimination'] = liste_elimination

    # On crée un index pour gérer le passage à un autre élément de nos listes en fonction des éliminations
    session['current_index'] = 0  

    # Obtention du premier attribut à envoyer et de la première liste d'éléments à éliminer
    first_attribut = attributs_mix[0]
    eliminable_elements = liste_elimination[0]  

    # Création de la liste des images à éliminer
    eliminable_images = [dico_images[element] for element in eliminable_elements if element in dico_images]
    
    # Création de la liste permettant de stocker les éléments éliminés
    images_eliminees = []

    # On stock l'élément choisi et son image pour l'écran de fin de partie
    session['images_eliminees'] = images_eliminees
    choix = session['choix']
    choix_image = dico_images[choix]
    session['choix_image'] = choix_image

    return render_template('affichage_images.html', dico=dico_images, attribut=first_attribut, eliminable_images=eliminable_images, images_eliminees=images_eliminees, themes=themes)


@app.route('/next_attribute/<themes>')
def next_attribute(themes):

    """
    Cette fonction permet d'afficher le reste des attributs envoyés à l'utilisateur et de gérer les éléments déjà éliminés.
    Elle renvoie également la template "affichage_images" et les mêmes variables que pour la route précédente.
    """

    # S'assurer que l'index est bien obtenu. Si oui, nous l'augmentons de un pour passer à l'attribut suivant
    if 'current_index' in session:
        current_index = session['current_index'] + 1
        longueur = len(session['attributs_mix'])

        # Tant que l'index n'atteint pas la fin de la liste des éléments à éliminer, nous continuons d'appliquer la logique de jeu
        if current_index != longueur: 
            session['current_index'] = current_index
            # Obtention de la vidéo de l'attribut à afficher
            next_attribute = url_for('static', filename=session['attributs_mix'][current_index])
            # Obtention des éléments à éliminer
            eliminable_elements = session['liste_elimination'][current_index]
            # Obtention des images du jeu
            image_files = os.listdir(f'static/{themes}/images/')
            # Création d'un dictionnaire associant nos éléments à leurs images
            dico_images = {file.split('.')[0]: f'{themes}/images/' + file for file in image_files}
            # Obtention d'une liste d'images à éliminer
            eliminable_images = [dico_images[element] for element in eliminable_elements if element in dico_images]
            # Obtention des images déjà éliminées
            images_eliminees = session.get('images_eliminees')
            images_eliminees.extend(eliminable_images)
            session['images_eliminees'] = images_eliminees

            return jsonify(attribut=next_attribute, eliminable_images=eliminable_images, images_eliminees=images_eliminees, themes=themes)

        else:
            # Si nous atteignons la fin de la liste des éléments à éliminer,
            # nous renvoyons le template de la fin de partie
            fin_jeu_url = url_for('fin_jeu')
            # Nous attribuons une valeurs booléene à "game_over" (définie dans le template)
            return jsonify(game_over=True, redirect_url=fin_jeu_url)
       

@app.route('/fin_jeu')
def fin_jeu():

    """
    Cette fonction correspond à la route "fin_jeu" permettant d'afficher le contenu de la template d'écran de fin.
    Elle retourne le template "fin_de_partie" et les variables final_image, choix et themes permettant d'afficher l'élément qu'il fallait trouver.
    """

    choix = session.get('choix')
    choix = choix.upper()
    if "_" in choix:
        choix = choix.replace("_", " ")
    
    final_image = session.get('choix_image')
    themes = session.get('themes')  
    return render_template('fin_de_partie.html', final_image=final_image, choix=choix, themes=themes)


# Éxecution de l'application
if __name__ == '__main__':
    app.run(debug=True)