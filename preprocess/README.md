# Etapes de pré-traitement

	python3.6 check_data.py -i <input.h5>

Filtrage manuel des valeurs aberrantes. Sortie : filtered.h5

	python3.6 mirror.py -i filtered.h5

Doublement du jeu de données en appliquant un effet miroir sur les images et en inversant la direction. Sortie : mirrored.h5

	python3.6 combine.py

ATTENTION : les fichier à combiner sont renseignés dans le code directement. Rassemble plusieurs fichiers en un seul. Sortie : combined.h5

	python3.6 preprocess.py -i combined.h5

Applique divers pré-traîtement sur les images (ajout de bruit, variations d'exposition/contraste, ajout d'obstacle). Entièrement paramétrable dans le code. Peut agrandir le jeu de données ou traiter de façon linéaire.