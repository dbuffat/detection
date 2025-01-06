.. Réponse aux questions

Réponse aux Questions
=====================

Première Partie - Applications à des données simulées
-----------------------------------------------------

Signal simple et bruit blanc gaussien
_____________________________________

Le pas séparant deux longueurs d'onde est de 0.8 nm, calculé comme suit : (1400-600)/1000. Il convient de prendre en compte la précision de l'appareil de mesure ou de la machine lors de cette évaluation.

Signal complexe et bruit gaussien coloré
________________________________________

Le pas d'échantillonnage de notre signal, exprimé en secondes, est de 1/100 s. Cela implique qu'il y a 100 incréments dans une seconde.

Lors de la représentation graphique de fs, il est manifeste que sa forme est atypique. Cette caractéristique est due à la symétrie hermitienne des signaux réels, où les coefficients de Fourier pour les fréquences positives et négatives sont des conjugués complexes.

Comparaison avec d'autres outils
________________________________

1. Il apparaît que les méthodes de corrélation proposées par SciPy tendent à surestimer la position du signal. Nous estimons que cela peut être attribué au fait que SciPy renvoie la position du pic du signal plutôt que celle de son apparition. Cette différence d'interprétation pourrait expliquer pourquoi cette méthode est plus rapide.

2. Nous observons un facteur de 100 dans la différence de temps de calcul entre les deux méthodes. Cela résulte du fait que SciPy est considérablement optimisé par rapport à notre propre méthode. Il est probable que SciPy soit implémenté de manière à exécuter les calculs à la vitesse du langage C.

3. Un facteur similaire de 100 est également observé dans les émissions de CO2. Cette tendance semble logique, car il s'agit d'une moyenne d'émissions par unité de temps. Ainsi, si la durée est multipliée par un facteur de 100, les émissions de CO2 suivent proportionnellement cette variation.

Seconde Partie - Application à des données de LIGO
--------------------------------------------------

La valeur du SNR (en valeur absolue) atteint son maximum pour le modèle des masses autour de 35 masses solaires. En recherchant l'article scientifique relatif à cette détection (première détection d'ondes gravitationnelles), nous trouvons l'article suivant : `ArXiv <https://arxiv.org/pdf/1602.03837>`_: *Observation of Gravitational Waves from a Binary Black Hole Merger*. Les masses des trous noirs sont estimées à 36 et 29 masses solaires.

Le pic de détection à 35 masses solaires est donc bien situé dans ce domaine. De plus, notre méthode fait varier les masses de la même manière. Il serait pertinent d'envisager d'introduire une complexification de notre approche pour étudier cette situation pour des masses différentes.

Dans ce cas, cela pourrait être réalisé en ajoutant une seconde boucle `for` dans le fichier `main_lg` du module `__main__.py`.
