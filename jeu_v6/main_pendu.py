from flask import Flask, render_template, session, request
from donnes import choisir_mot, lsf_lettres
import json
import random

app = Flask(__name__)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.debug = True
app.secret_key = 'your_secret_key'

def game_mode_1(mot_choisi):
    lettres = list(mot_choisi)
    longueur_mot = len(lettres)
    lettres_devinees = ["_"] * longueur_mot
    lettres_courantes = list("eastirnulodmcpévhgfb")
    lettres_peu_courantes = list("qjàxèêzykôûwâîüùëœçï")
    alphabet = list("eastirnulodmcpévhgfbqjàxèêzykôûwâîüùëœçï")
    diacritiques = list("éàèêôûâîûùüëœçï")
    liste_affichage = []
    liste_reponses = []

    vies = 3

    while lettres != lettres_devinees and vies != 0:
        if not any(lettre in diacritiques for lettre in lettres):
            for lettre in diacritiques:
                if lettre not in ["à", "è", "ç"] and lettre in lettres_courantes:
                    lettres_courantes.remove(lettre)
                elif lettre not in ["à", "è", "ç"] and lettre in lettres_peu_courantes:
                    lettres_peu_courantes.remove(lettre)
                elif lettre not in ["à", "è", "ç"] and lettre in alphabet:
                    alphabet.remove(lettre)

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

        liste_reponses.append(raison)
        liste_affichage.append(choix_ordinateur)

    print(liste_affichage, lettres, lettres_devinees)
    for i, j in zip(liste_affichage, liste_reponses):
        print(i, j)
    return liste_affichage, vies, liste_reponses
@app.route('/')
def menu_pendu():
    return render_template('menu_pendu.html', game_modes=["1", "2", "3"])

@app.route('/<game_mode>')
def menu_difficultes(game_mode):
    return render_template('menu_difficultes.html', game_mode=game_mode, difficultes=["Facile", "Moyen", "Difficile"])

@app.route('/<game_mode>/<difficulte>')
def lancer_partie(game_mode, difficulte):
    mot_choisi = choisir_mot(difficulte)
    session['mot_choisi'] = mot_choisi
    if game_mode == "1":
        liste_affichage, vies, liste_reponses = game_mode_1(mot_choisi)
        session['liste_affichage'] = liste_affichage
        session['vies'] = vies
        session['liste_reponses'] = liste_reponses
        currentIndex = 0
        return render_template('lancer_partie.html', game_mode=game_mode, difficulte=difficulte, mot_choisi=mot_choisi, liste_affichage=liste_affichage, vies=vies, currentIndex=currentIndex)

@app.route('/<game_mode>/<difficulte>/affichage', methods=["GET", "POST"])
def affichage(game_mode, difficulte):
    if request.method == 'POST':
        liste_affichage = session.get('liste_affichage', [])
        liste_reponses = session.get('liste_reponses', [])
        currentIndex = request.form.get('currentIndex', 0)
        vies = session.get('vies', 3)
        liste_reponses_json = json.dumps(liste_reponses)
        liste_affichage_json = json.dumps(liste_affichage)
        print(liste_affichage_json)
        print(liste_reponses_json)

        response = request.form['response']
        is_correct = response == 'oui'

        if not is_correct:
            vies -= 1

        session['vies'] = vies
        session['currentIndex'] = int(currentIndex) + 1  # Increment the current index for the next letter

        return render_template('affichage_lettre.html', game_mode=game_mode, difficulte=difficulte,liste_affichage=liste_affichage, liste_affichage_json=liste_affichage_json, liste_reponses_json=liste_reponses_json, lsf_lettres=lsf_lettres, currentIndex=currentIndex, vies=vies)
    else:
        liste_affichage = session.get('liste_affichage', [])
        liste_reponses = session.get('liste_reponses', [])
        currentIndex = request.form.get('currentIndex', 0)
        vies = session.get('vies', 3)
        liste_reponses_json = json.dumps(liste_reponses)
        liste_affichage_json = json.dumps(liste_affichage)
        print(liste_affichage_json)
        print(liste_reponses_json)
        
        return render_template('affichage_lettre.html', game_mode=game_mode, difficulte=difficulte, liste_affichage = liste_affichage, liste_affichage_json=liste_affichage_json, liste_reponses_json=liste_reponses_json, lsf_lettres=lsf_lettres, currentIndex=currentIndex, vies=vies)

@app.route('/fin_de_partie')
def fin_de_partie():
    return render_template('fin_de_partie.html')

if __name__ == '__main__':
    app.run(debug=True)
