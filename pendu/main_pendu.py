from flask import Flask, render_template, session, request
from donnes import choisir_mot, lsf_lettres, image
import json
import random

"""
Ce programme contient la logique du jeu du pendu. Il utilise les données (dictionnaires et listes) contenues dans le fichier donnees.py.
Ce programme utilise Flask comme framework pour python.
"""

"""Configuration de l'application."""

app = Flask(__name__)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.debug = True
app.secret_key = 'your_secret_key'


def game_mode_logique(mot_choisi):

    """
    La fonction game_mode_logique permet d'obtenir les variables nécessaires à l'affichage et à l'évolution
    des éléments de notre template html pour une partie.

    Paramètres :
    mot_choisi (str): mot choisi aléatoirement en fonction de la difficulté choisie et du dictionnaire de donnees.py.

    Retourne : 

    liste_affichage (List[str]): liste contenant l'ensemble des lettres envoyées par l'ordinateur. 
    vies (int): nombre de vies au début du jeu. 
    liste_reponses (List[bool]): liste contenant des valeurs True ou False correspondant à chaque lettre
    de la liste liste_affichage. Les lettres non présentes dans le mot choisi sont False et les autres True.
    liste_lettres_devinees (List[str]): liste contenant le statut du mot deviné (_ _ _ _, c _ _ _, c h _ _ )
    à chaque tour et permettant d'afficher le niveau de progression du joueur.
    mot_final (str): mot choisi par l'ordinateur.
    """

    # Initialisation de toutes les variables
    lettres = list(mot_choisi)
    longueur_mot = len(lettres)
    lettres_devinees = ["_"] * longueur_mot
    liste_lettres_devinees = [str(lettres_devinees).replace("["," ").replace("]", " ").replace(",", " ").replace("'", "")]
    lettres_courantes = list("eastirnulodmcpévhgfb")
    lettres_peu_courantes = list("qjàxèêzykôwâî")
    alphabet = list("eastirnulodmcpévhgfbqjàxèêzykôwâî")
    diacritiques = list("éàèêôâî")
    liste_affichage = []
    liste_reponses = []
    vies = 3
    
    # Si le mot choisi ne contient pas de diacritiques, alors seul les plus courants peuvent être envoyés à l'utilisateur
    while lettres != lettres_devinees and vies != 0:
        if not any(lettre in diacritiques for lettre in lettres):
            for lettre in diacritiques:
                if lettre not in ["à", "è"] and lettre in lettres_courantes:
                    lettres_courantes.remove(lettre)
                elif lettre not in ["à", "è"] and lettre in lettres_peu_courantes:
                    lettres_peu_courantes.remove(lettre)
                elif lettre not in ["à", "è"] and lettre in alphabet:
                    alphabet.remove(lettre)

        # Pour les mots longs, nous envoyons les lettres les plus courantes assez tôt pour éviter de trop longues parties
        if len(lettres) > 5:
            if (nb_lettres_devinees := len(lettres_devinees) - lettres_devinees.count("_")) < 5 and any(lettre in lettres_courantes for lettre in lettres):
                raison = True
                choix_ordinateur = random.choice(lettres_courantes)

                if choix_ordinateur in lettres:
                    indices = [i for i, lettre in enumerate(lettres) if lettre == choix_ordinateur]
                    for index in indices:
                        lettres_devinees[index] = choix_ordinateur
                    lettres_courantes.remove(choix_ordinateur)
                    alphabet.remove(choix_ordinateur)

                elif choix_ordinateur not in lettres:
                    raison = False
                    lettres_courantes.remove(choix_ordinateur)
                    alphabet.remove(choix_ordinateur)

            else:
                raison = True
                choix_ordinateur = random.choice(alphabet)

                if choix_ordinateur in lettres:
                    indices = [i for i, lettre in enumerate(lettres) if lettre == choix_ordinateur]
                    for index in indices:
                        lettres_devinees[index] = choix_ordinateur
                    alphabet.remove(choix_ordinateur)

                elif choix_ordinateur not in lettres:
                    raison = False
                    alphabet.remove(choix_ordinateur)

        # Pour les mots courts, nous envoyons les lettres courantes plus tard pour éviter les parties trop courtes
        elif len(lettres) <= 5:
            if (nb_lettres_devinees := len(lettres_devinees) - lettres_devinees.count("_")) < 3 and any(lettre in lettres_peu_courantes for lettre in lettres):
                raison = True
                choix_ordinateur = random.choice(lettres_peu_courantes)

                if choix_ordinateur in lettres:
                    indices = [i for i, lettre in enumerate(lettres) if lettre == choix_ordinateur]
                    for index in indices:
                        lettres_devinees[index] = choix_ordinateur
                    lettres_peu_courantes.remove(choix_ordinateur)
                    alphabet.remove(choix_ordinateur)

                elif choix_ordinateur not in lettres:
                    raison = False
                    lettres_peu_courantes.remove(choix_ordinateur)
                    alphabet.remove(choix_ordinateur)

            else:
                raison = True
                choix_ordinateur = random.choice(alphabet)

                if choix_ordinateur in lettres:
                    indices = [i for i, lettre in enumerate(lettres) if lettre == choix_ordinateur]
                    for index in indices:
                        lettres_devinees[index] = choix_ordinateur
                    alphabet.remove(choix_ordinateur)

                elif choix_ordinateur not in lettres:
                    raison = False
                    alphabet.remove(choix_ordinateur)

        # Normalisation des listes utilsées
        liste_reponses.append(raison)
        liste_affichage.append(choix_ordinateur)
        lettres_devinees_str = str(lettres_devinees).replace("["," ").replace("]", " ").replace(",", " ").replace("'", "")
        liste_lettres_devinees.append(lettres_devinees_str)

    # Conversion en majuscule pour une meilleure lecture
    liste_lettres_devinees = [entry.upper() for entry in liste_lettres_devinees]

    # Pour vérification
    # for i, j, k in zip(liste_affichage, liste_reponses, liste_lettres_devinees):
    #     print(i, j, type(k), k)

    mot_final = liste_lettres_devinees[-1]

    return liste_affichage, vies, liste_reponses, liste_lettres_devinees, mot_final


@app.route('/')
def menu_pendu():

    """
    Cette fonction correpond à la route du menu du jeu.
    Elle renvoie le template du menu et les valeurs pouvant être attribuées à la variable "game_mode". 
    """

    return render_template('menu_pendu.html', game_modes=["1", "2", "3"])

@app.route('/regles')
def regles():

    """
    Cette fonction correpond à la route du menu "règles" du jeu.
    Elle renvoie le template du menu contenant la vidéo des règles.
    """
    return render_template('menu_regles.html')

@app.route('/<game_mode>')
def menu_difficultes(game_mode):
    return render_template('menu_difficultes.html', game_mode=game_mode, difficultes=["Facile", "Moyen", "Difficile"])

@app.route('/<game_mode>/<difficulte>')
def lancer_partie(game_mode, difficulte):

    """
    Cette fonction correspond à la route permettant d'afficher le mot choisi par l'ordinateur.
    Elle renvoie les variables de la fonction game_mode_logique pour l'affichage initial des parties.
    """

    mot_choisi = choisir_mot(difficulte)
    session['mot_choisi'] = mot_choisi
    liste_affichage, vies, liste_reponses, liste_lettres_devinees,mot_final = game_mode_logique(mot_choisi)
    session['liste_affichage'] = liste_affichage
    session['vies'] = vies
    session['liste_reponses'] = liste_reponses
    session['liste_lettres_devinees'] = liste_lettres_devinees
    session['mot_final'] = mot_final
    dico_image = image()
    lien_image = dico_image.get(mot_choisi) if game_mode == "1" else ''
    session['lien_image'] = lien_image
    currentIndex = 0

    return render_template('lancer_partie.html', game_mode=game_mode, difficulte=difficulte, mot_choisi=mot_choisi.upper(), liste_affichage=liste_affichage, liste_lettres_devinees=liste_lettres_devinees, vies=vies, currentIndex=currentIndex, lien_image=lien_image)


@app.route('/<game_mode>/<difficulte>/affichage', methods=["GET", "POST"])
def affichage(game_mode, difficulte):

    """
    Cette fonction correspond à la route permettant de gérer les bonnes et mauvaises réponses de l'utilisateur
    ainsi que le passage à une autre lettre et l'actualisation de l'ensemble de nos variables.
    """
    # Pour le premier round, nous obtenons l'ensemble de nos variables puis les actualisons pour les rounds
    # suivants afin de les afficher correctement dans notre template affichage_lettres.html.

    if request.method == 'POST':
        mot_choisi = session.get('mot_choisi')
        mot_choisi = mot_choisi.upper()
        liste_affichage = session.get('liste_affichage', [])
        liste_reponses = session.get('liste_reponses', [])
        liste_lettres_devinees = session.get('liste_lettres_devinees')
        currentIndex = request.form.get('currentIndex', 0)
        vies = session.get('vies', 3)
        lien_image = session.get('lien_image')
        liste_reponses_json = json.dumps(liste_reponses)
        liste_affichage_json = json.dumps(liste_affichage)
        liste_lettres_devinees_json = json.dumps(liste_lettres_devinees)
        response = request.form['response']
        is_correct = response == 'oui'

        if not is_correct:
            vies -= 1

        session['vies'] = vies
        session['currentIndex'] = int(currentIndex) + 1  
    

        return render_template('affichage_lettre.html', game_mode=game_mode, difficulte=difficulte,liste_affichage=liste_affichage, liste_affichage_json=liste_affichage_json, liste_reponses_json=liste_reponses_json, liste_lettres_devinees = liste_lettres_devinees, liste_lettres_devinees_json=liste_lettres_devinees_json, lsf_lettres=lsf_lettres, currentIndex=currentIndex, vies=vies,lien_image=lien_image, mot_choisi=mot_choisi)
    
    else:
        mot_choisi = session.get('mot_choisi')
        mot_choisi = mot_choisi.upper()
        liste_affichage = session.get('liste_affichage', [])
        liste_reponses = session.get('liste_reponses', [])
        liste_lettres_devinees = session.get('liste_lettres_devinees')
        currentIndex = request.form.get('currentIndex', 0)
        vies = session.get('vies', 3)
        lien_image = session.get('lien_image')
        liste_reponses_json = json.dumps(liste_reponses)
        liste_affichage_json = json.dumps(liste_affichage)
        liste_lettres_devinees_json = json.dumps(liste_lettres_devinees)
        
        return render_template('affichage_lettre.html', game_mode=game_mode, difficulte=difficulte, liste_affichage = liste_affichage, liste_affichage_json=liste_affichage_json, liste_reponses_json=liste_reponses_json, liste_lettres_devinees=liste_lettres_devinees, liste_lettres_devinees_json=liste_lettres_devinees_json, lsf_lettres=lsf_lettres, currentIndex=currentIndex, vies=vies, lien_image=lien_image, mot_choisi=mot_choisi)

@app.route('/fin_de_partie')
def fin_de_partie():

    """
    Cette fonction correspond à la route fin_de_partie permettant de gérer les cas de perte ou de victoire
    du joueur.
    """

    mot_final = session.get('mot_final')
    vies = request.args.get('vies', type=int)

    print(vies)
    if vies > 0:
        resultat = "GAGNÉ"
    else:
        resultat = "PERDU"

    return render_template('fin_de_partie.html', resultat=resultat, mot_final=mot_final)


if __name__ == '__main__':
    app.run(debug=True)
