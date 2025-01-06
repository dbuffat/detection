import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import time
import codecarbon as cc
import logging

version = "1.0"

logging.getLogger("codecarbon").disabled = True

class BruitColore:
    """
	Classe représentant un modèle de bruit coloré.

	Description :
	-------------
	La classe `BruitColore` génère et manipule des signaux bruités à partir d'un modèle
	de bruit coloré. Elle permet de calculer la densité spectrale de puissance (PSD),
	de simuler des données bruitées, de calculer et d'analyser le rapport signal-bruit
	(SNR), et d'effectuer diverses opérations comme le suivi du temps d'exécution et des
	émissions de CO2.

	Attributs :
	-----------
	gamma : float
		Exposant pour la densité spectrale de puissance (PSD), défini par défaut à 1.2.
	opt : bool
		Indicateur de l'option de performance, défini par défaut à False.
	time_th : float
		Temps théorique du signal.
	time_gen : numpy.ndarray
		Echelle de temps générée pour les simulations.
	signal : numpy.ndarray
		Signal simulé.
	psd : numpy.ndarray
		Densité spectrale de puissance (PSD) calculée.
	bruit : numpy.ndarray
		Bruit coloré généré.
	data : numpy.ndarray
		Données simulées avec bruit.
	cov : numpy.ndarray
		Matrice de covariance du bruit.
	model : numpy.ndarray
		Modèle de signal utilisé pour la détection.
	fg : numpy.ndarray
		Filtre de détection.
	snr : numpy.ndarray
		Rapport signal-bruit (SNR).
	"""
    
    def __init__(self, gamma=1.2, opt=False):
        
        self.gamma = gamma
        self.opt = opt        
        self.time_th = None
        self.time_gen = None
        self.signal = None
        self.psd = None
        self.bruit = None
        self.data = None
        self.cov = None
        self.model = None
        self.fg = None
        self.snr = None        
        self.compile_data()
                
    def Main(self):
        """
		Exécute le processus principal, génère les graphiques et effectue la détection.

		Description :
		-------------
		Cette méthode trace plusieurs graphiques illustrant les différentes étapes du modèle
		de bruit coloré et effectue la détection du signal. Elle trace aussi les graphiques
		pour visualiser les données simulées et les résultats obtenus. Enfin, elle exécute
		les fonctions de suivi du temps et des émissions de CO2.

		Paramètres d'initialisation:
		----------------------------
		gamma : float, optionnel (défaut = 1.2)
			Exposant pour la densité spectrale de puissance (PSD).
		opt : bool, optionnel (défaut = False)
			Indicateur de l'option de performance (utilise `True` pour une version optimisée).
		"""
        
        self.Detection()
        self.PlotAll()
        
        self.TimeTracker()
        self.CarbonTracker()
        
    def compile_data(self):
        """
		Compile toutes les données nécessaires pour les simulations.

		Description :
		-------------
		Cette méthode appelle toutes les fonctions nécessaires pour générer et préparer
		les différentes données : signal, PSD, bruit coloré, données simulées, covariance,
		modèle de signal, filtre de détection, et rapport signal-bruit (SNR).

		Paramètres :
		------------
		Aucun.

		Retourne :
		----------
		Aucun.
		"""
        
        self._time_gen()
        self._signal()
        self.PSD()
        self._bruit_colore()
        self._simulate_data()
        self._covariance()
        self._model()
        self._filter_g()
        self.SNR()
        
    def TurnOpt(self):
        """
		Bascule l'option de performance.

		Description :
		-------------
		Cette méthode inverse la valeur de l'attribut `opt`, activant ou désactivant
		la version optimisée de certaines fonctions.

		Paramètres :
		------------
		Aucun.

		Retourne :
		----------
		Aucun.
		"""
        
        self.opt = not self.opt
        
    def _update_gamma(self, gamma):
        """
		Met à jour la valeur de l'exposant `gamma` et recalcul les résultats associés.

		Description :
		-------------
		Cette méthode met à jour la valeur de `gamma`, puis appelle les méthodes nécessaires
		pour recalculer la PSD, la covariance, le modèle, le filtre de détection, et le rapport
		signal-bruit (SNR).

		Paramètres :
		------------
		gamma : float
			Nouvelle valeur de l'exposant `gamma` pour la PSD.

		Retourne :
		----------
		Aucun.
		"""
        
        self.gamma = gamma
        self.PSD()
        self._covariance()
        self._model()
        self._filter_g()
        self.SNR()
        
    def _update_SNR(self):
        """
		Recalcule le rapport signal-bruit (SNR).

		Description :
		-------------
		Cette méthode appelle la fonction `SNR` pour mettre à jour le rapport signal-bruit
		en fonction des données actuelles.

		Paramètres :
		------------
		Aucun.

		Retourne :
		----------
		Aucun.
		"""
        
        self.SNR()
    
    def _time_gen(self):
        """
		Génère une échelle de temps entre 0 et 10 secondes avec 1000 points.

		Description :
		-------------
		Cette méthode génère une échelle de temps pour les simulations, allant de 0 à 10 secondes,
		avec un total de 1000 points échantillonnés uniformément.

		Paramètres :
		------------
		Aucun.

		Retourne :
		----------
		Aucun.
		"""
        
        self.time_gen = np.linspace(0, 10, 1000)

    def _signal(self):
        """
		Génère un signal simulé en fonction du temps.

		Description :
		-------------
		Cette méthode génère un signal basé sur l'échelle de temps précédemment définie. Le signal
		est calculé comme une fonction sinusoidale avec une amplitude et une fréquence dépendant du temps.

		Paramètres :
		------------
		Aucun.

		Retourne :
		----------
		Aucun.
		"""
        
        t = self.time_gen[:100]
        print(f"Pas d'echantillonage utiliser pour le signal : {t[1] - t[0]} secondes.")
        A = 3*t
        f = 5*t
        self.signal = A * np.sin(2*np.pi*f*t)

    def _fft_freq(self):
        """
		Calcule les fréquences de Fourier pour les échelles de temps.

		Description :
		-------------
		Cette méthode calcule et retourne les spectres de Fourier en fréquences pour les échelles
		de temps correspondantes à `fd` (échelle de 10 secondes) et `fs` (échelle de 1 seconde).

		Paramètres :
		------------
		Aucun.

		Retourne :
		----------
		tuple
			Retourne un tuple `(fd, fs)`, où `fd` et `fs` sont des tableaux numpy représentant
			les fréquences de Fourier sur les échelles de temps respectives.
		"""
        
        t = self.time_gen
        dt = t[1]-t[0]
        nd = len(t)
        ns = len(t[:100])
    
        fd = np.fft.fftfreq(nd, dt)
        fs = np.fft.fftfreq(ns, dt)
        return fd, fs

    def _fft_signal(self):
        """
		Calcule la transformée de Fourier du signal.

		Description :
		-------------
		Cette méthode calcule la transformée de Fourier du signal simulé.

		Paramètres :
		------------
		Aucun.

		Retourne :
		----------
		numpy.ndarray
			La transformée de Fourier du signal simulé.
		"""
        
        return np.fft.fft(self.signal)
    
    def PSD(self, cov = False):
        """
		Calcule la densité spectrale de puissance (PSD).

		Description :
		-------------
		Cette méthode calcule la densité spectrale de puissance (PSD) pour le bruit coloré
		en utilisant l'exposant `gamma`. Si `cov` est défini à `True`, elle calcule la PSD
		sur la base des fréquences de l'échelle de temps `fs`.

		Paramètres :
		------------
		cov : bool, optionnel (défaut = False)
			Si `True`, calcule la PSD pour l'échelle de temps `fs`.

		Retourne :
		----------
		numpy.ndarray
			La densité spectrale de puissance calculée.
		"""
        
        if cov == False:
            fd = self._fft_freq()[0]
            fd = fd[fd>0]
            psd = (fd/10)**self.gamma + 1
            psd = np.insert(psd, 0, psd[0])
            self.psd = np.concatenate((psd, psd[::-1]))
        else:
            fs = self._fft_freq()[1]
            fs = fs[fs>0]
            psd = (fs/10)**self.gamma + 1
            psd = np.insert(psd, 0, psd[0])
            return np.concatenate((psd, psd[::-1]))

    def _bruit_blanc(self, n=1000):
        """
		Génère un bruit blanc gaussien.

		Description :
		-------------
		Cette méthode génère un bruit blanc gaussien d'une longueur donnée.

		Paramètres :
		------------
		n : int, optionnel (défaut = 1000)
			Le nombre d'échantillons à générer.

		Retourne :
		----------
		numpy.ndarray
			Un tableau numpy contenant un bruit blanc gaussien de taille `n`.
		"""
        
        return np.random.normal(size=n)

    def _bruit_colore(self, n=1000):
        """
		Génère un bruit coloré.

		Description :
		-------------
		Cette méthode génère un bruit coloré en utilisant la transformée de Fourier du bruit blanc
		et en la multipliant par la racine carrée de la densité spectrale de puissance (PSD).

		Paramètres :
		------------
		n : int, optionnel (défaut = 1000)
			Le nombre d'échantillons à générer.

		Retourne :
		----------
		numpy.ndarray
			Un tableau numpy contenant un bruit coloré de taille `n`.
		"""
        
        if n==1000:
            bb = np.fft.fft(self._bruit_blanc(n))
            psd = np.sqrt(self.psd)
            bc = bb * psd
            self.bruit = np.real(np.fft.ifft(bc))
        else:
            bb = np.fft.fft(self._bruit_blanc(n))
            psd = np.sqrt(self.PSD(cov=True))
            bc = bb * psd
            return np.real(np.fft.ifft(bc))
    
    def _simulate_data(self):
        """
		Simule les données en ajoutant du bruit au signal.

		Description :
		-------------
		Cette méthode génère les données simulées en ajoutant le bruit coloré au signal simulé.
		Elle insère également un délai aléatoire avant de superposer le signal.

		Paramètres :
		------------
		Aucun.

		Retourne :
		----------
		Aucun.
		"""
        
        bc = self.bruit
        s = self.signal
        n = len(bc) - len(s)
        sd = np.zeros(n)
        n = np.random.randint(n)
        self.time_th = self.time_gen[n]
        self.data = np.insert(sd, n, s) + bc
    
    def _covariance(self):
        """
		Calcule la matrice de covariance du bruit.

		Description :
		-------------
		Cette méthode génère un bruit coloré à l'aide de la fonction `bruit_colore` et calcule
		la matrice de covariance en effectuant une moyenne sur 1000 échantillons de bruit. La matrice
		est utilisée pour le filtrage et l'analyse du bruit dans le modèle.

		Paramètres :
		------------
		Aucun.

		Retourne :
		----------
		Aucun. La matrice de covariance est stockée dans l'attribut `cov`.
		"""
        
        b = self._bruit_colore(100)
        s = np.zeros((b.size, b.size))
    
        for _ in range(1000):
            b = self._bruit_colore(100)
            s += np.outer(b, b)
        self.cov = s / 1000

    def _model(self):
        """
		Calcule le modèle utilisé pour rechercher le signal.

		Description :
		-------------
		Cette méthode génère un modèle de signal en utilisant une fonction sinusoidale basée sur
		l'échelle de temps et une fréquence. Le modèle sera utilisé dans la détection du signal.

		Paramètres :
		------------
		Aucun.

		Retourne :
		----------
		Aucun. Le modèle est stocké dans l'attribut `model`.
		"""
        
        t = self.time_gen[:100]
        a = t
        f = 5*t
        self.model = a * np.sin(2*np.pi*f*t)

    def _filter_g(self):
        """
		Calcule le filtre adapté pour la détection du signal.

		Description :
		-------------
		Cette méthode calcule le filtre `fg` qui est utilisé pour détecter le signal dans les données
		simulées. Elle inverse la matrice de covariance et effectue une multiplication matricielle
		pour obtenir le filtre.

		Paramètres :
		------------
		Aucun.

		Retourne :
		----------
		Aucun. Le filtre est stocké dans l'attribut `fg`.
		"""
        
        I = np.eye(self.cov.shape[0])
        cov_inv = np.linalg.solve(self.cov, I)
        self.fg = np.matmul(cov_inv, self.model)

    def _correlation(self, vector_data):
        """
		Calcule la corrélation entre les données et le filtre.

		Description :
		-------------
		Cette méthode calcule la corrélation entre le vecteur de données et le filtre `fg` pour estimer
		la présence du signal dans les données bruitées. La corrélation est calculée par une somme des
		produits de convolution.

		Paramètres :
		------------
		vector_data : numpy.ndarray
			Le vecteur de données à corréler avec le filtre.

		Retourne :
		----------
		numpy.ndarray
			Un tableau contenant la corrélation calculée entre le filtre et les données.
		"""
        
        f_g = self.fg
        N_g = np.size(f_g)
        d = vector_data
        N = np.size(d)
        l = []

        for i in range(N-N_g):
            l.append(np.sum(f_g * d[i:i+N_g]))

        return np.array(l)
    
    def _correlation_scipy(self, vector_data):
        """
		Calcule la corrélation entre les données et le modèle en utilisant `scipy.signal.correlate`.

		Description :
		-------------
		Cette méthode utilise la fonction `correlate` de `scipy.signal` pour calculer la corrélation
		entre le vecteur de données et le modèle.

		Paramètres :
		------------
		vector_data : numpy.ndarray
			Le vecteur de données à corréler avec le modèle.

		Retourne :
		----------
		numpy.ndarray
			Un tableau contenant la corrélation calculée entre le modèle et les données.
		"""
        
        return sp.signal.correlate(vector_data, self.fg)

    def SNR(self):
        """
		Calcule le rapport signal-bruit (SNR) pour les données simulées.

		Description :
		-------------
		Cette méthode calcule le rapport signal-bruit (SNR) en effectuant une corrélation entre le bruit
		et les données. Le SNR est calculé pour évaluer la présence du signal par rapport au bruit.

		Paramètres :
		------------
		Aucun.

		Retourne :
		----------
		Aucun. Le SNR est stocké dans l'attribut `snr`.
		"""
        
        if self.opt:
            tau_bruit = self._correlation_scipy(self.bruit)
            tau_obs = self._correlation_scipy(self.data)
        else:
            tau_bruit = self._correlation(self.bruit)
            tau_obs = self._correlation(self.data)

        sigma_bruit = np.std(tau_bruit)
        self.snr = tau_obs / sigma_bruit
    
    def Detection(self):
        """
		Détecte le signal en comparant le rapport signal-bruit (SNR) avec un seuil.

		Description :
		-------------
		Cette méthode effectue la détection du signal en analysant le rapport signal-bruit (SNR). Si
		le SNR dépasse un seuil de 3, le signal est détecté, et la position du signal ainsi que l'heure
		sont affichées.

		Paramètres :
		------------
		Aucun.

		Retourne :
		----------
		Aucun. Affiche un message indiquant la position du signal et l'heure à laquelle il est détecté,
		ou un message indiquant qu'aucun signal n'a été détecté.
		"""
        
        p0 = np.argmax(self.snr)
        if np.max(self.snr)>3:
            print(f'Position du signal en p0 = {p0}.')
            d = self.time_gen
            time_max = d[p0]
            print(f'Signal detecte en t = {time_max} s.\nLe signal doit se trouver a t_th = {self.time_th} s.')
        else:
            print("Aucun signal detectee.")
        
    def TimeTracker(self):
        """
		Suit le temps d'exécution des calculs avec et sans optimisation.

		Description :
		-------------
		Cette méthode mesure et compare le temps d'exécution pour 1000 itérations de la fonction `update_SNR`
		avec l'option d'optimisation activée et désactivée. Le temps d'exécution est affiché pour les deux cas.

		Paramètres :
		------------
		Aucun.

		Retourne :
		----------
		Aucun. Affiche le temps d'exécution pour les deux cas d'optimisation.
		"""
        
        start_time = time.time()
        for _ in range(1000):
            self._update_SNR()
        end_time = time.time()
        print(f"Temps d'execution pour opt = {self.opt} : {end_time - start_time} secondes.")

        self.TurnOpt()

        start_time = time.time()
        for _ in range(1000):
            self._update_SNR()
        end_time = time.time()
        print(f"Temps d'execution pour opt = {self.opt} : {end_time - start_time} secondes.")

    def CarbonTracker(self):
        """
		Suit les émissions de CO2 pendant les calculs avec et sans optimisation.

		Description :
		-------------
		Cette méthode suit et affiche les émissions de CO2 générées pendant 1000 itérations de la fonction
		`update_SNR`, en activant et désactivant l'optimisation. Les émissions sont suivies à l'aide d'un
		tracker de CO2.

		Paramètres :
		------------
		Aucun.

		Retourne :
		----------
		Aucun. Affiche les émissions de CO2 pour les deux cas d'optimisation.
		"""
        
        tracker = cc.EmissionsTracker(save_to_file=False)
        tracker.start()
        for _ in range(1000):
            self._update_SNR()
        emission = tracker.stop()
        print(f"CO2 generer pour opt = {self.opt} : {emission} kg.")
    
        self.TurnOpt()

        tracker = cc.EmissionsTracker()
        tracker.start()
        for _ in range(1000):
            self._update_SNR()
        emission = tracker.stop()
        print(f"CO2 generer pour opt = {self.opt} : {emission} kg.")

    def PlotAll(self):
        """
		Trace tous les graphiques sur une seule page avec des subplots.

		Description :
		-------------
		Cette méthode génère une série de graphiques pour visualiser différentes étapes du processus,
		y compris le signal simulé, le bruit coloré, la densité spectrale de puissance (PSD), les données
		simulées, le rapport signal-bruit (SNR), et d'autres visualisations. Les graphiques sont affichés
		dans une grille 3x3.

		Paramètres :
		------------
		Aucun.

		Retourne :
		----------
		Aucun. Affiche les graphiques sur une fenêtre.
		"""
        fig, axs = plt.subplots(3, 3, figsize=(16, 9))  # Crée une grille 3x3
        axs = axs.ravel()  # Aplatir le tableau des axes pour un accès facile

		# Plot Signal
        axs[0].plot(self.time_gen[:100], self.signal)
        axs[0].set_title('Signal')
        axs[0].set_xlabel('Temps (s)')

		# Plot Fs (Spectre de Fourier fs)
        axs[1].plot(self._fft_freq()[1])
        axs[1].set_title("TF de l'echantillon f_s")

		# Plot Fd (Spectre de Fourier fd)
        axs[2].plot(self._fft_freq()[0])
        axs[2].set_title("TF de l'echantillon f_d")

		# Plot PSD (Densité spectrale de puissance)
        axs[3].plot(self._fft_freq()[0], self.psd)
        axs[3].set_title("PSD")

		# Plot Bruit (Bruit colore)
        axs[4].plot(self.time_gen, self.bruit)
        axs[4].set_title("Bruit colore")

		# Plot Simulate Data (Données simulées)
        axs[5].plot(self.time_gen, self.data)
        axs[5].set_title("Pseudo-donnees")

		# Plot SNR (Fluctuations du SNR)
        axs[6].plot(self.snr, color='red', label=f'Opt = {self.opt}')
        self.TurnOpt()
        self._update_SNR()
        axs[6].plot(self.snr, color='blue', label=f'Opt = {self.opt}')
        axs[6].legend()
        axs[6].set_title("Fluctuations du SNR")

		

		# Supprimer la dernière case vide
        fig.delaxes(axs[7])
        fig.delaxes(axs[8])

		# Ajuster l'espacement entre les sous-graphiques
        plt.tight_layout()
        plt.show()