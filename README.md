<!-- TP1_DBuffat_MThomeer documentation master file, created by
sphinx-quickstart on Wed Dec  4 18:42:30 2024.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive. -->

# TP1 - Filtrage adapté aux signaux

Lien de la page GitLab avec la documentation  [Documentation](https://m2cosmo-tp1-4ecb4e.pages.in2p3.fr/)


# Contents:

- [README](#readme)
- [Fonctionnalités](#fonctionnalites)
- [Installation](#installation)
- [Utilisation](#bruitblanc)
- [Contributions](#contributions)
- [License](#license)

- [Réponses aux Questions](#reponse-aux-questions)

- [Première Partie](#premiere-partie---applications-a-des-donnees-simulees)
- [Signal simple et bruit blanc gaussien](#signal-simple-et-bruit-blanc-gaussien)
- [Signal complexe et bruit gaussien colore](#signal-complexe-et-bruit-gaussien-colore)
- [Comparaison a d'autres outils](#comparaison-a-dautres-outils)

- [Seconde partie - Application a des donnees de LIGO](#seconde-partie---application-a-des-donnees-de-ligo)

- [Documentation](#documentation-du-logiciel)
- [BruitBlanc](#bruitblanc)
- [BruitColore](#bruitcolore)
- [Ligo](#ligo)

# README

Le readme du projet

## Fonctionnalites

Le logiciel permet de detecter un signal monochrome dans un bruit blanc simulé. 

Il permet de détecter un signal complexe avec du bruit coloré.

Enfin il permet de detecter une onde gravitationnelle dans un signal bruité, et d'en déduire une masse approximative pour les deux trois noirs sources.

## Installation

1. Clonez le dépôt GitHub :
   
    ```bash
    $ git clone git@gitlab.in2p3.fr:dimitri.buffat/m2cosmo_tp1.git
    ```
   
2. Allez dans le dossier du package :

    ```bash
    $ cd m2cosmo_tp1
    ```
   
3. Installez le package à l'aide de pip :

    ```bash
    $ pip install .
    ```
   
    Si vous n'avez pas pip, vous pouvez utiliser : 
   
    ```bash
    $ python3 setup.py install
    ```

## Utilisation

Après installation, il suffit de taper 
  ```bash
      $ ligo
  ```
pour detecter l'onde gravitationnelle dans le signal GW150914

  ```bash
      $ bruit_blanc
  ```
Pour faire la simulation d'un émission avec un redshift, et déduire le rédshift d'émission

  ```bash
      $ bruit_colore
  ```
Pour détecter un signal similaire à celui d'une onde gravitationnelle dans un bruit coloré

## Contributions

Les contributions sont les bienvenues! Pour contribuer à 2048 veuillez suivre ces étapes :

1. Forkez le projet.

2. Créez une branche pour votre fonctionnalité 
	```bash
	$ git checkout -b feature-nouvelle-fonctionnalité
	```

3. Commitez vos changements.
	```bash
	$ git commit -m 'Ajout d\'une nouvelle fonctionnalité'
	```

4. Poussez votre branche.
	```bash
	$ git push origin feature-nouvelle-fonctionnalité
	```


5. Ouvrez une Pull Request.

## License

Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus de détails.

# Reponse aux questions

## Premiere Partie - Applications a des donnees simulees

### Signal simple et bruit blanc gaussien

Le pas séparant deux longueurs d'onde est d'environ 0.8 nm, calculé comme suit : (1400-600)/1000. Il convient de prendre en compte la précision machine lors de cette évaluation.

### Signal complexe et bruit gaussien colore

Le pas d'échantillonnage de notre signal, exprimé en secondes, est de 1/100 s. Cela implique qu'il y a 100 incréments dans une seconde.

Lors de la représentation graphique de fs, il est manifeste que sa forme est atypique. Cette caractéristique est due à la symétrie hermitienne des signaux réels, où les coefficients de Fourier pour les fréquences positives et négatives sont des conjugués complexes.

### Comparaison a d'autres outils

1. Il apparaît que les méthodes de corrélation proposées par SciPy tendent à surestimer la position du signal. Nous estimons que cela peut être attribué au fait que SciPy renvoie la position du pic du signal plutôt que celle de son apparition. Cette différence d'interprétation pourrait expliquer pourquoi cette méthode est plus rapide.

2. Nous observons un facteur de 100 dans la différence de temps de calcul entre les deux méthodes. Cela résulte du fait que SciPy est considérablement optimisé par rapport à notre propre méthode. Il est probable que SciPy soit implémenté de manière à exécuter les calculs à la vitesse du langage C.

3. Un facteur similaire de 100 est également observé dans les émissions de CO2. Cette tendance semble logique, car il s'agit d'une moyenne d'émissions par unité de temps. Ainsi, si la durée est multipliée par un facteur de 100, les émissions de CO2 suivent proportionnellement cette variation.

## Seconde partie - Application a des donnees de LIGO

La valeur du SNR (en valeur absolue) atteint son maximum pour le modèle des masses autour de 35 masses solaires. En recherchant l'article scientifique relatif à cette détection (première détection d'ondes gravitationnelles), nous trouvons l'article suivant : `ArXiv <https://arxiv.org/pdf/1602.03837>`_: *Observation of Gravitational Waves from a Binary Black Hole Merger*. Les masses des trous noirs sont estimées à 36 et 29 masses solaires.

Le pic de détection à 35 masses solaires est donc bien situé dans ce domaine. De plus, notre méthode fait varier les masses de la même manière. Il serait pertinent d'envisager d'introduire une complexification de notre approche pour étudier cette situation pour des masses différentes.

Dans ce cas, cela pourrait être réalisé en ajoutant une seconde boucle `for` dans le fichier `main_lg` du module `__main__.py`.

# Documentation du logiciel

Lien de la page GitLab avec la documentation  [Documentation](https://m2cosmo-tp1-4ecb4e.pages.in2p3.fr/)

## BruitBlanc

Bases : `object`

Classe modélisant un signal bruité et permettant d’effectuer diverses opérations statistiques
pour analyser le rapport signal-bruit (SNR), l’influence de l’amplitude du signal, du bruit et 
de la déviation standard du modèle, et d’autres analyses.

#### Attributs :

`lambda_0`
: Longueur d’onde de référence (en nm).

`a_signal`
: Amplitude du signal.

`a_bruit`
: Amplitude du bruit.

`sigma_model`
: Écart-type du modèle de signal.

`opt`
: Indicateur d’activation des optimisations.

`redshift_th`
: Redshift théorique (décalage vers le rouge).

`lambda_obs`
: Longueur d’onde observée après décalage.

`lambda_gen`
: Tableau des longueurs d’onde générées pour le signal.

`signal`
: Signal généré.

`bruit`
: Bruit ajouté au signal.

`simulate_data`
: Données simulées combinant le signal et le bruit.

`model`
: Modèle théorique basé sur une loi normale.

`snr`
: Rapport signal-bruit (SNR) calculé.

### Main()

Effectue les opérations principales de la classe BruitBlanc en générant et affichant les 
graphiques correspondants pour l’analyse du signal, du bruit et du SNR.

La méthode appelle les différentes méthodes de la classe pour :
- Afficher les graphiques du signal, des données simulées, et du SNR.
- Afficher l’influence de l’amplitude du signal, du bruit et de la déviation standard du modèle.
- Calculer et afficher les performances d’exécution et les émissions de CO2.

#### Paramètres d’initialisation :

`lambda_0`
: Longueur d’onde de référence (en nm), par défaut 656.3 nm.

`A_signal`
: Amplitude du signal, par défaut 100.0.

`A_bruit`
: Amplitude du bruit, par défaut 1.0.

`sigma_model`
: Écart-type du modèle de signal, par défaut 8.0.

`opt`
: Indicateur d’activation des optimisations, par défaut False.

### compile_data()

Compile toutes les données nécessaires pour l’analyse du signal : 
calcul de la longueur d’onde observée, génération du signal, ajout du bruit, 
simulation des données, création du modèle, et calcul du SNR.

Cette méthode est appelée automatiquement lors de l’initialisation de l’objet.

#### Retourne :

Aucun.

### TurnOpt()

Active ou désactive l’optimisation des calculs en inversant l’état de l’attribut “opt”.

#### Retourne :

Aucun.

### update_SNR()

Met à jour le rapport signal-bruit (SNR) en recalculant les corrélations et en utilisant 
les données et le modèle actuels.

#### Retourne :

Aucun.

### update_signal_amplitude(A_signal)

Met à jour l’amplitude du signal et recalcule les données simulées et le rapport signal-bruit (SNR).

#### Paramètres :

`A_signal`
: Nouvelle amplitude du signal.

#### Retourne :

Aucun.

### update_bruit_amplitude(A_bruit)

Met à jour l’amplitude du bruit et recalcule les données simulées et le rapport signal-bruit (SNR).

#### Paramètres :

`A_bruit`
: Nouvelle amplitude du bruit.

#### Retourne :

Aucun.

### update_sigma_model(sigma_model)

Met à jour la déviation standard du modèle et recalcule le rapport signal-bruit (SNR).

#### Paramètres :

`sigma_model`
: Nouvelle déviation standard du modèle.

#### Retourne :

Aucun.

### lambda_obs()

Calcule la longueur d’onde observée en fonction du décalage vers le rouge théorique.

#### Retourne :

Aucun.

### lambda_gen()

Génère un tableau de longueurs d’onde (en nm) dans la gamme spécifiée.

#### Retourne :

Aucun.

### signal()

Génère le signal basé sur une distribution normale avec l’amplitude spécifiée et le décalage vers le rouge.

#### Retourne :

Aucun.

### bruit()

Génère un bruit gaussien blanc avec l’amplitude spécifiée.

#### Retourne :

Aucun.

### simulate_data()

Génère les données simulées en combinant le signal et le bruit.

#### Retourne :

Aucun.

### model()

Génère le modèle basé sur une distribution normale pour ajuster le signal observé.

#### Retourne :

Aucun.

### correlation(vector_data)

Applique une corrélation croisée manuelle pour estimer le SNR entre le signal observé et le bruit.

#### Paramètres :

`vector_data`
: Série temporelle à corréler avec le modèle.

#### Retourne :

`ndarray`
: Série des corrélations pour chaque décalage.

### correlation_scipy(vector_data)

Applique une corrélation croisée en utilisant la fonction de corrélation de SciPy pour estimer le SNR.

#### Paramètres :

`vector_data`
: Série temporelle à corréler avec le modèle.

#### Retourne :

`ndarray`
: Série des corrélations pour chaque décalage.

### SNR()

Calcule le rapport signal-bruit (SNR) en utilisant la corrélation croisée et l’écart-type du bruit.

#### Retourne :

Aucun.

### Detection()

Détecte la position du signal en fonction du SNR et compare le redshift détecté au redshift théorique.

#### Retourne :

Aucun.

### redshift()

Calcule le redshift (décalage vers le rouge) estimé à partir du rapport signal-bruit (SNR).
Le redshift est calculé en fonction de la position maximale du SNR. Si la position est au-dessus 
d’un seuil, le redshift est estimé à partir de la longueur d’onde générée à cette position.

#### Retourne :

`float` ou `None`
: Le redshift estimé, ou None si la position maximale est inférieure au seuil.

### TimeTracker()

Suivi du temps d’exécution des calculs de rapport signal-bruit (SNR) avec et sans optimisation.

La méthode mesure le temps d’exécution de 1000 itérations de mise à jour du SNR avec l’optimisation activée
et désactivée, puis affiche les résultats.

#### Retourne :

Aucun.

### CarbonTracker()

Suivi des émissions de CO2 générées par les calculs de rapport signal-bruit (SNR) avec et sans optimisation.

La méthode mesure les émissions de CO2 pour 1000 itérations de mise à jour du SNR avec l’optimisation activée
et désactivée, puis affiche les résultats.

#### Retourne :

Aucun.

### Plot()

Affiche tous les graphiques (Signal, Données simulées, SNR, etc.) sur une seule page.

#### Retourne :

Aucun.


## BruitColore

Bases : `object`

Classe représentant un modèle de bruit coloré.

### Description :

La classe BruitColore génère et manipule des signaux bruités à partir d’un modèle
de bruit coloré. Elle permet de calculer la densité spectrale de puissance (PSD),
de simuler des données bruitées, de calculer et d’analyser le rapport signal-bruit
(SNR), et d’effectuer diverses opérations comme le suivi du temps d’exécution et des
émissions de CO2.

### Attributs :

`gamma`
: Exposant pour la densité spectrale de puissance (PSD), défini par défaut à 1.2.

`opt`
: Indicateur de l’option de performance, défini par défaut à False.

`time_th`
: Temps théorique du signal.

`time_gen`
: Echelle de temps générée pour les simulations.

`signal`
: Signal simulé.

`psd`
: Densité spectrale de puissance (PSD) calculée.

`bruit`
: Bruit coloré généré.

`data`
: Données simulées avec bruit.

`cov`
: Matrice de covariance du bruit.

`model`
: Modèle de signal utilisé pour la détection.

`fg`
: Filtre de détection.

`snr`
: Rapport signal-bruit (SNR).

### Main()

Exécute le processus principal, génère les graphiques et effectue la détection.

#### Description :

Cette méthode trace plusieurs graphiques illustrant les différentes étapes du modèle
de bruit coloré et effectue la détection du signal. Elle trace aussi les graphiques
pour visualiser les données simulées et les résultats obtenus. Enfin, elle exécute
les fonctions de suivi du temps et des émissions de CO2.

#### Paramètres d’initialisation:

`gamma`
: Exposant pour la densité spectrale de puissance (PSD).

`opt`
: Indicateur de l’option de performance (utilise True pour une version optimisée).

####compile_data()

Compile toutes les données nécessaires pour les simulations.

#### Description :

Cette méthode appelle toutes les fonctions nécessaires pour générer et préparer
les différentes données : signal, PSD, bruit coloré, données simulées, covariance,
modèle de signal, filtre de détection, et rapport signal-bruit (SNR).

#### Paramètres :

Aucun.

#### Retourne :

Aucun.

### TurnOpt()

Bascule l’option de performance.

#### Description :

Cette méthode inverse la valeur de l’attribut opt, activant ou désactivant
la version optimisée de certaines fonctions.

#### Paramètres :

Aucun.

#### Retourne :

Aucun.

### update_gamma(gamma)

Met à jour la valeur de l’exposant gamma et recalcul les résultats associés.

#### Description :

Cette méthode met à jour la valeur de gamma, puis appelle les méthodes nécessaires
pour recalculer la PSD, la covariance, le modèle, le filtre de détection, et le rapport
signal-bruit (SNR).

#### Paramètres :

`gamma`
: Nouvelle valeur de l’exposant gamma pour la PSD.

#### Retourne :

Aucun.

### update_SNR()

Recalcule le rapport signal-bruit (SNR).

#### Description :

Cette méthode appelle la fonction SNR pour mettre à jour le rapport signal-bruit
en fonction des données actuelles.

#### Paramètres :

Aucun.

#### Retourne :

Aucun.

### time_gen()

Génère une échelle de temps entre 0 et 10 secondes avec 1000 points.

#### Description :

Cette méthode génère une échelle de temps pour les simulations, allant de 0 à 10 secondes,
avec un total de 1000 points échantillonnés uniformément.

#### Paramètres :

Aucun.

#### Retourne :

Aucun.

### signal()

Génère un signal simulé en fonction du temps.

#### Description :

Cette méthode génère un signal basé sur l’échelle de temps précédemment définie. Le signal
est calculé comme une fonction sinusoidale avec une amplitude et une fréquence dépendant du temps.

#### Paramètres :

Aucun.

#### Retourne :

Aucun.

### fft_freq()

Calcule les fréquences de Fourier pour les échelles de temps.

#### Description :

Cette méthode calcule et retourne les spectres de Fourier en fréquences pour les échelles
de temps correspondantes à fd (échelle de 10 secondes) et fs (échelle de 1 seconde).

#### Paramètres :

Aucun.

#### Retourne :

`tuple`
: Retourne un tuple (fd, fs), où fd et fs sont des tableaux numpy représentant
  les fréquences de Fourier sur les échelles de temps respectives.

### fft_signal()

Calcule la transformée de Fourier du signal.

#### Description :

Cette méthode calcule la transformée de Fourier du signal simulé.

#### Paramètres :

Aucun.

#### Retourne :

`numpy.ndarray`
: La transformée de Fourier du signal simulé.

### PSD(cov=False)

Calcule la densité spectrale de puissance (PSD).

#### Description :

Cette méthode calcule la densité spectrale de puissance (PSD) pour le bruit coloré
en utilisant l’exposant gamma. Si cov est défini à True, elle calcule la PSD
sur la base des fréquences de l’échelle de temps fs.

#### Paramètres :

`cov`
: Si True, calcule la PSD pour l’échelle de temps fs.

#### Retourne :

`numpy.ndarray`
: La densité spectrale de puissance calculée.

### bruit_blanc(n=1000)

Génère un bruit blanc gaussien.

#### Description :

Cette méthode génère un bruit blanc gaussien d’une longueur donnée.

#### Paramètres :

`n`
: Le nombre d’échantillons à générer.

#### Retourne :

`numpy.ndarray`
: Un tableau numpy contenant un bruit blanc gaussien de taille n.

### bruit_colore(n=1000)

Génère un bruit coloré.

#### Description :

Cette méthode génère un bruit coloré en utilisant la transformée de Fourier du bruit blanc
et en la multipliant par la racine carrée de la densité spectrale de puissance (PSD).

#### Paramètres :

`n`
: Le nombre d’échantillons à générer.

#### Retourne :

`numpy.ndarray`
: Un tableau numpy contenant un bruit coloré de taille n.

### simulate_data()

Simule les données en ajoutant du bruit au signal.

#### Description :

Cette méthode génère les données simulées en ajoutant le bruit coloré au signal simulé.
Elle insère également un délai aléatoire avant de superposer le signal.

#### Paramètres :

Aucun.

#### Retourne :

Aucun.

### covariance()

Calcule la matrice de covariance du bruit.

#### Description :

Cette méthode génère un bruit coloré à l’aide de la fonction bruit_colore et calcule
la matrice de covariance en effectuant une moyenne sur 1000 échantillons de bruit. La matrice
est utilisée pour le filtrage et l’analyse du bruit dans le modèle.

#### Paramètres :

Aucun.

#### Retourne :

Aucun. La matrice de covariance est stockée dans l’attribut cov.

### model()

Calcule le modèle utilisé pour rechercher le signal.

#### Description :

Cette méthode génère un modèle de signal en utilisant une fonction sinusoidale basée sur
l’échelle de temps et une fréquence. Le modèle sera utilisé dans la détection du signal.

#### Paramètres :

Aucun.

#### Retourne :

Aucun. Le modèle est stocké dans l’attribut model.

### filter_g()

Calcule le filtre adapté pour la détection du signal.

#### Description :

Cette méthode calcule le filtre fg qui est utilisé pour détecter le signal dans les données
simulées. Elle inverse la matrice de covariance et effectue une multiplication matricielle
pour obtenir le filtre.

#### Paramètres :

Aucun.

#### Retourne :

Aucun. Le filtre est stocké dans l’attribut fg.

### correlation(vector_data)

Calcule la corrélation entre les données et le filtre.

#### Description :

Cette méthode calcule la corrélation entre le vecteur de données et le filtre fg pour estimer
la présence du signal dans les données bruitées. La corrélation est calculée par une somme des
produits de convolution.

#### Paramètres :

`vector_data`
: Le vecteur de données à corréler avec le filtre.

#### Retourne :

`numpy.ndarray`
: Un tableau contenant la corrélation calculée entre le filtre et les données.

### correlation_scipy(vector_data)

Calcule la corrélation entre les données et le modèle en utilisant scipy.signal.correlate.

#### Description :

Cette méthode utilise la fonction correlate de scipy.signal pour calculer la corrélation
entre le vecteur de données et le modèle.

#### Paramètres :

`vector_data`
: Le vecteur de données à corréler avec le modèle.

#### Retourne :

`numpy.ndarray`
: Un tableau contenant la corrélation calculée entre le modèle et les données.

### SNR()

Calcule le rapport signal-bruit (SNR) pour les données simulées.

#### Description :

Cette méthode calcule le rapport signal-bruit (SNR) en effectuant une corrélation entre le bruit
et les données. Le SNR est calculé pour évaluer la présence du signal par rapport au bruit.

#### Paramètres :

Aucun.

#### Retourne :

Aucun. Le SNR est stocké dans l’attribut snr.

### Detection()

Détecte le signal en comparant le rapport signal-bruit (SNR) avec un seuil.

#### Description :

Cette méthode effectue la détection du signal en analysant le rapport signal-bruit (SNR). Si
le SNR dépasse un seuil de 3, le signal est détecté, et la position du signal ainsi que l’heure
sont affichées.

#### Paramètres :

Aucun.

#### Retourne :

Aucun. Affiche un message indiquant la position du signal et l’heure à laquelle il est détecté,
ou un message indiquant qu’aucun signal n’a été détecté.

### TimeTracker()

Suit le temps d’exécution des calculs avec et sans optimisation.

#### Description :

Cette méthode mesure et compare le temps d’exécution pour 1000 itérations de la fonction update_SNR
avec l’option d’optimisation activée et désactivée. Le temps d’exécution est affiché pour les deux cas.

#### Paramètres :

Aucun.

#### Retourne :

Aucun. Affiche le temps d’exécution pour les deux cas d’optimisation.

### CarbonTracker()

Suit les émissions de CO2 pendant les calculs avec et sans optimisation.

#### Description :

Cette méthode suit et affiche les émissions de CO2 générées pendant 1000 itérations de la fonction
update_SNR, en activant et désactivant l’optimisation. Les émissions sont suivies à l’aide d’un
tracker de CO2.

#### Paramètres :

Aucun.

#### Retourne :

Aucun. Affiche les émissions de CO2 pour les deux cas d’optimisation.

### PlotAll()

Trace tous les graphiques sur une seule page avec des subplots.

#### Description :

Cette méthode génère une série de graphiques pour visualiser différentes étapes du processus,
y compris le signal simulé, le bruit coloré, la densité spectrale de puissance (PSD), les données
simulées, le rapport signal-bruit (SNR), et d’autres visualisations. Les graphiques sont affichés
dans une grille 3x3.

#### Paramètres :

Aucun.

#### Retourne :

Aucun. Affiche les graphiques sur une fenêtre.


## ligo

Bases : `object`

Classe pour analyser les données d’événements d’ondes gravitationnelles.

Cette classe permet de charger, filtrer et analyser les données d’événements
d’ondes gravitationnelles, de calculer le rapport signal-bruit (SNR), et de générer
des formes d’ondes gravitationnelles. Elle permet également de visualiser ces résultats
à travers des graphiques.

### Attributs :

 `event`
 : Objet représentant l’événement d’onde gravitationnelle.

 `detector`: str
 : Nom du détecteur (ex. « H1 » pour Hanford).

 `strain`
 : Série temporelle brute des contraintes.

 `filtered_strain`
 : Série temporelle après filtrage passe-haut.

 `time`
 : Tableau des temps associés aux données.

 `dt`
 : Intervalle de temps entre deux échantillons.

 `time_tot`
 : Temps total de la série temporelle.

 `psd`
 : Densité spectrale de puissance (PSD) brute.

 `psd_interpolated`
 : PSD interpolée pour le filtrage.

 `m1`
 : Masse du premier objet compact (en masses solaires).

 `m2`
 : Masse du second objet compact (en masses solaires).

 `f_min`
 : Fréquence minimale utilisée pour l’analyse.

 `duration`
 : Durée de la simulation de la forme d’onde (en secondes).

 `hp`
 : Polarisation « + » de la forme d’onde gravitationnelle.

 `snr`
 : Rapport signal-bruit (SNR) calculé.

### Main()

#### Paramètres de bases :

`event`
: Nom de l’événement (ex. « GW150914 »).

`detector`
: Nom du détecteur (ex. « H1 »).

`m1`
: Masse du premier objet compact (en masses solaires).

`m2`
: Masse du second objet compact (en masses solaires).

`f_min`
: Fréquence minimale pour l’analyse (en Hz).

`duration`
: Durée pour la forme d’onde (en secondes).

`dt`
: Intervalle de temps entre les échantillons (en secondes).

### load_data()

Charge les données de l’événement et calcule la PSD interpolée.

#### Description :

Cette méthode charge les données de l’événement d’onde gravitationnelle et effectue
un filtrage passe-haut pour éliminer les basses fréquences non pertinentes. Elle calcule
également la densité spectrale de puissance (PSD) et l’interpole pour le filtrage.

#### Paramètres :

Aucun.

#### Retourne :

Aucun.

### generate_waveform()

Génère la forme d’onde gravitationnelle pour les masses spécifiées.

#### Description :

Cette méthode génère la forme d’onde gravitationnelle pour les objets compacts
spécifiés par leurs masses et la fréquence minimale. La polarisation « + » est
calculée à l’aide de l’approximant “SEOBNRv4_opt”.

#### Paramètres :

Aucun.

#### Retourne :

Aucun.

### filter_data()

Applique le filtre de corrélation croisée pour calculer le SNR.

#### Description :

Cette méthode applique un filtre de corrélation croisée sur la forme d’onde générée
et la série temporelle filtrée afin de calculer le rapport signal-bruit (SNR). Elle utilise
la densité spectrale de puissance (PSD) interpolée et affiche les résultats pertinents.

#### Paramètres :

Aucun.

#### Retourne :

Aucun.

### plot_data()

Génère un ensemble de graphiques pour analyser les données et leurs propriétés.

#### Description :

Cette méthode affiche plusieurs graphiques relatifs aux données de l’événement, à la forme
d’onde gravitationnelle générée, à la densité spectrale de puissance (PSD), et au rapport
signal-bruit (SNR). Les graphiques incluent :

> - La série temporelle brute de l’événement GW150914 sur le détecteur H1.
> - La série temporelle filtrée de l’événement GW150914 sur le détecteur H1.
> - La densité spectrale de puissance (PSD) du bruit interpolée.
> - L’amplitude de la polarisation « + » de la forme d’onde gravitationnelle.
> - Le rapport signal-bruit (SNR) en fonction du temps.

#### Paramètres :

Aucun.

#### Retourne :

Aucun. Les graphiques sont affichés.

