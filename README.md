# JEUX SignToKids

Ce dépôt contient l'ensemble des codes et ressources ayant permis de créer des jeux destinés à un public d'enfants sourds. La création de ces jeux s'est faite dans le cadre d'un stage de Master 1 Traitement Automatique des Langues afin de faciliter l'intégration des enfants sourds dans le monde de l'éducation. Ce stage a lui été réalisé dans le cadre du Projet SignToKids dont vous pouvez trouver une description [ici](https://injs-bordeaux.org/signtokids/).



Chaque jeu a été codé en python et rendu accessible à l'aide de la framework web Flask. Les langages utilisés sont Python, HTML, CSS et JavaScript.

## JEU DU QUI-EST-CE

Le jeu du Qui-est-ce est composé de trois thématiques : animaux, nourriture et habitats.

Pour chaque thème, un ensemble d'images est renvoyé à l'utilisateur. Des "attributs" vidéos sont ensuite envoyés et permettent d'éliminer les éléments e répondant pas à cet attribut. Dans le cas des plats, si l'attribut "tomate j'ai" est envoyé, nous pouvons éliminer l'ensemble des plats de contenant pas de tomate. Ces attributs sont uniquement envoyés en LSF. Il ne reste à la fin qu'une seule image correspondant à l'élément choisi par l'ordinateur. Les parties sont crées aléatoirement et permettent ainsi de renouveller l'expérience de jeu de l'utilisateur. Vous trouverez une démo ci-dessous :

<video src='presentation/demo_videos/demo_qui_est_ce.mp4' width=/></video>



