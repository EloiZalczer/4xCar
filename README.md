# 4xCar (Prononcer quatre-car)

Projet de fin d'études de **Erwan Dufresne** et **Eloi Zalczer**, Polytech Lille IMA 2019.

Lien vers la compétition [Iron Car](http://www.ironcar.org/) 

Lien vers le [Wiki du projet](https://projets-ima.plil.fr/mediawiki/index.php/IMA5_2018/2019_P44) 

# Utilisation

## Préparation

TODO insérer photo voiture

Notre voiture utilise une carte Arduino Uno à la place d'un shield PWM pour commander les moteurs de la voiture. L'Arduino est alimentée par la Raspberry Pi, qui est elle-même alimentée par une batterie externe. La commande pour le servo-mpteur de direction est placée sur la broche 9 et la commande pour le moteur principal est placée sur la broche 11. 

## Utilisation

Avant toute chose, veuillez vérifier la plage de commande des moteurs de votre voiture. Nos algorithmes sont calibrés pour une T2M Pirate XT-S version Brushless. Deux algorithmes de calibration sont disponibles pour déterminer cette plage de commande. Une fois cette calibration effectuée, modifiez les valeurs dans le fichier *serial_controller.ino* en conséquence et uploadez le code sur l'Arduino. 

Il est conseillé d'utiliser un PC externe pour faire tourner l'application Web, mais il est possible de la faire tourner directement sur la Raspberry Pi. Dans tous les cas, commencez par lancer le serveur avec la commande : 
`node server.js`

Vous pouvez ensuite vous connecter sur n'importe quel navigateur à l'URL **localhost:3000**.

Enfin, lancez l'application embarquée via la commande : 
`python3.6 main.py [-h|--help] [-v|--verbose] [-a|--address <ip_address>] [-m|--manual] [-s|--serial <serial_address>]`

L'initialisation du programme peut prendre quelques dizaines de secondes au premier lancement, en particulier lors d'un lancement en mode automatique car le chargement du modèle Keras prend du temps. Une fois le programme prêt, il suffit de cliquer sur **Start** dans l'application Web pour démarrer la voiture. En mode automatique, cela lancera le pilotage automatique et la voiture démarrera instantanément. En mode manuel, cela permettra de la contrôler via le panneau de commande sur l'application. Durant le pilotage manuel, il est possible de lancer l'enregistrement des images en cliquant sur **Start recording**. Lors de l'arrêt de la voiture, les images ainsi que les commandes associées sont stockées dans un fichier hdf5 horodaté.

Ces données peuvent être visionnées et modifiées. Le script *preprocess.py* permet d'ajouter des variations (exposition, bruit, obstacles, crop) dans les images pour varier le jeu de données. Une fois les données prêtes pour l'entraînement, il est possible de les charger dans le notebook Google Colab pour effectuer l'entraînement du réseau. Après l'entraînement, téléchargez le modèle entraîné et placez-le dans le répertoire *ironcar/models*. Par défaut, le modèle utilisé est entraîné par nos soins.
