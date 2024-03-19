
import random 
import math


liste_mots = ["Antiquité", "Chat", "Main", "Musique", "Génocide", "Prométhée"]
selected_word = random.choice(liste_mots).lower()
lettres = list(selected_word)
longueur_mot = len(lettres)
limite_lettres = math.floor(0.6 * len(lettres))
lettres_devinees = ["_"]*longueur_mot
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
            liste_affichage.append(choix_ordinateur)
            
            if choix_ordinateur in lettres:
                indices = []
                for i, lettre in enumerate(lettres):
                    if lettre == choix_ordinateur:
                        indices.append(i)
                for index in indices:
                    lettres_devinees[index] = choix_ordinateur
                lettres_courantes.remove(choix_ordinateur)
                alphabet.remove(choix_ordinateur)


            elif choix_ordinateur not in lettres:
                lettres_courantes.remove(choix_ordinateur)
                alphabet.remove(choix_ordinateur)
                raison = False
            liste_reponses.append(raison)
        else:
            raison = True
            choix_ordinateur = random.choice(alphabet)
            liste_affichage.append(choix_ordinateur)
            
            if choix_ordinateur in lettres:
                indices = []
                for i, lettre in enumerate(lettres):
                    if lettre == choix_ordinateur:
                        indices.append(i)
                for index in indices:
                    lettres_devinees[index] = choix_ordinateur
                alphabet.remove(choix_ordinateur)


            elif choix_ordinateur not in lettres:
                alphabet.remove(choix_ordinateur)
                raison = False
            liste_reponses.append(raison)

    elif len(lettres) <= 5:

        if (nb_lettres_devinees := len(lettres_devinees) - lettres_devinees.count("_")) < 3 and any(lettre in lettres_peu_courantes for lettre in lettres):
            raison = True
            choix_ordinateur = random.choice(lettres_peu_courantes)
            liste_affichage.append(choix_ordinateur)

            if choix_ordinateur in lettres:
                indices = []
                for i, lettre in enumerate(lettres):
                    if lettre == choix_ordinateur:
                        indices.append(i)
                for index in indices:
                    lettres_devinees[index] = choix_ordinateur
                lettres_peu_courantes.remove(choix_ordinateur)
                alphabet.remove(choix_ordinateur)

        
            elif choix_ordinateur not in lettres:
                lettres_peu_courantes.remove(choix_ordinateur)
                alphabet.remove(choix_ordinateur)
                raison = False
            liste_reponses.append(raison)
        else:
            raison = True
            choix_ordinateur = random.choice(alphabet)
            liste_affichage.append(choix_ordinateur)

            if choix_ordinateur in lettres:
                indices = []
                for i, lettre in enumerate(lettres):
                    if lettre == choix_ordinateur:
                        indices.append(i)
                for index in indices:
                    lettres_devinees[index] = choix_ordinateur
                alphabet.remove(choix_ordinateur)

           
            elif choix_ordinateur not in lettres:
                alphabet.remove(choix_ordinateur)
                raison = False
            liste_reponses.append(raison)

print(selected_word)
for i,j in zip(liste_affichage,liste_reponses):
    print(i, j)

if vies == 0:
    print("vous avez perdu.")
elif lettres == lettres_devinees:
    print("Vous avez gagné !")