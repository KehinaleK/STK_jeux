
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
            choix_ordinateur = random.choice(lettres_courantes)
            liste_affichage.append(choix_ordinateur)
            print(selected_word)
            print(f"nb_lettres_devinees : {nb_lettres_devinees}")
            print(f"lettres devinées : {lettres_devinees}")
            print(lettres, lettres_devinees)
            print(f"nombre de vies : {vies}")
            print("-"*50)
            demande = input(f"La lettre {choix_ordinateur} est elle dans le mot ? ")
            
            if choix_ordinateur in lettres and demande == "oui":
                indices = []
                for i, lettre in enumerate(lettres):
                    if lettre == choix_ordinateur:
                        indices.append(i)
                for index in indices:
                    lettres_devinees[index] = choix_ordinateur
                lettres_courantes.remove(choix_ordinateur)
                alphabet.remove(choix_ordinateur)

            elif choix_ordinateur in lettres and demande == "non":
                indices = []
                for i, lettre in enumerate(lettres):
                    if lettre == choix_ordinateur:
                        indices.append(i)
                for index in indices:
                    lettres_devinees[index] = choix_ordinateur
                lettres_courantes.remove(choix_ordinateur)
                alphabet.remove(choix_ordinateur)
                vies -= 1
                print(f"Attention ! La lettre {choix_ordinateur} était bien dans le mot {selected_word}")

            elif choix_ordinateur not in lettres and demande == "non":
                lettres_courantes.remove(choix_ordinateur)
                alphabet.remove(choix_ordinateur)

            elif choix_ordinateur not in lettres and demande == "oui":
                lettres_courantes.remove(choix_ordinateur)
                alphabet.remove(choix_ordinateur)
                vies -= 1
                print(f"Attention ! La lettre {choix_ordinateur} n'était pas dans le mot {selected_word}")

        else:
            choix_ordinateur = random.choice(alphabet)
            liste_affichage.append(choix_ordinateur)
            print(selected_word)
            print(f"nb_lettres_devinees : {nb_lettres_devinees}")
            print(f"lettres devinées : {lettres_devinees}")
            print(lettres, lettres_devinees)
            print(f"nombre de vies : {vies}")
            print("-"*50)
            demande = input(f"La lettre {choix_ordinateur} est elle dans le mot ? ")

            if choix_ordinateur in lettres and demande == "oui":
                indices = []
                for i, lettre in enumerate(lettres):
                    if lettre == choix_ordinateur:
                        indices.append(i)
                for index in indices:
                    lettres_devinees[index] = choix_ordinateur
                alphabet.remove(choix_ordinateur)

            elif choix_ordinateur in lettres and demande == "non":
                indices = []
                for i, lettre in enumerate(lettres):
                    if lettre == choix_ordinateur:
                        indices.append(i)
                for index in indices:
                    lettres_devinees[index] = choix_ordinateur
                alphabet.remove(choix_ordinateur)
                vies -= 1
                print(f"Attention ! La lettre {choix_ordinateur} était bien dans le mot {selected_word}")

            elif choix_ordinateur not in lettres and demande == "non":
                alphabet.remove(choix_ordinateur)

            elif choix_ordinateur not in lettres and demande == "oui":
                alphabet.remove(choix_ordinateur)
                vies -= 1
                print(f"Attention ! La lettre {choix_ordinateur} n'était pas dans le mot {selected_word}")


    elif len(lettres) <= 5:

        if (nb_lettres_devinees := len(lettres_devinees) - lettres_devinees.count("_")) < 3 and any(lettre in lettres_peu_courantes for lettre in lettres):
            choix_ordinateur = random.choice(lettres_peu_courantes)
            liste_affichage.append(choix_ordinateur)
            print(selected_word)
            print(f"nb_lettres_devinees : {nb_lettres_devinees}")
            print(f"lettres devinées : {lettres_devinees}")
            print(lettres, lettres_devinees)
            print(f"nombre de vies : {vies}")
            print("-"*50)
            demande = input(f"La lettre {choix_ordinateur} est elle dans le mot ? ")

            if choix_ordinateur in lettres and demande == "oui":
                indices = []
                for i, lettre in enumerate(lettres):
                    if lettre == choix_ordinateur:
                        indices.append(i)
                for index in indices:
                    lettres_devinees[index] = choix_ordinateur
                lettres_peu_courantes.remove(choix_ordinateur)
                alphabet.remove(choix_ordinateur)

            elif choix_ordinateur in lettres and demande == "non":
                indices = []
                for i, lettre in enumerate(lettres):
                    if lettre == choix_ordinateur:
                        indices.append(i)
                for index in indices:
                    lettres_devinees[index] = choix_ordinateur
                lettres_peu_courantes.remove(choix_ordinateur)
                alphabet.remove(choix_ordinateur)
                vies -= 1
                print(f"Attention ! La lettre {choix_ordinateur} était bien dans le mot {selected_word}")

            elif choix_ordinateur not in lettres and demande == "non":
                lettres_peu_courantes.remove(choix_ordinateur)
                alphabet.remove(choix_ordinateur)

            elif choix_ordinateur not in lettres and demande == "oui":
                lettres_peu_courantes.remove(choix_ordinateur)
                alphabet.remove(choix_ordinateur)
                vies -= 1
                print(f"Attention ! La lettre {choix_ordinateur} n'était pas dans le mot {selected_word}")

        else:
            choix_ordinateur = random.choice(alphabet)
            liste_affichage.append(choix_ordinateur)
            print(selected_word)
            print(f"nb_lettres_devinees : {nb_lettres_devinees}")
            print(f"lettres devinées : {lettres_devinees}")
            print(lettres, lettres_devinees)
            print(f"nombre de vies : {vies}")
            print("-"*50)
            demande = input(f"La lettre {choix_ordinateur} est elle dans le mot ? ")

            if choix_ordinateur in lettres and demande == "oui":
                indices = []
                for i, lettre in enumerate(lettres):
                    if lettre == choix_ordinateur:
                        indices.append(i)
                for index in indices:
                    lettres_devinees[index] = choix_ordinateur
                alphabet.remove(choix_ordinateur)

            elif choix_ordinateur in lettres and demande == "non":
                indices = []
                for i, lettre in enumerate(lettres):
                    if lettre == choix_ordinateur:
                        indices.append(i)
                for index in indices:
                    lettres_devinees[index] = choix_ordinateur
                alphabet.remove(choix_ordinateur)
                vies -= 1
                print(f"Attention ! La lettre {choix_ordinateur} était bien dans le mot {selected_word}")

            elif choix_ordinateur not in lettres and demande == "non":
                alphabet.remove(choix_ordinateur)

            elif choix_ordinateur not in lettres and demande == "oui":
                alphabet.remove(choix_ordinateur)
                vies -= 1
                print(f"Attention ! La lettre {choix_ordinateur} n'était pas dans le mot {selected_word}")

if vies == 0:
    print("vous avez perdu.")
elif lettres == lettres_devinees:
    print("Vous avez gagné !")