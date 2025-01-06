import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import time
import codecarbon as cc
import logging

version = "1.0"

logging.getLogger("codecarbon").disabled = True

class BruitBlanc:
    """
    Classe modélisant un signal bruité et permettant d'effectuer diverses opérations statistiques
    pour analyser le rapport signal-bruit (SNR), l'influence de l'amplitude du signal, du bruit et 
    de la déviation standard du modèle, et d'autres analyses.

    Attributs :
    -----------
    lambda_0 : float
        Longueur d'onde de référence (en nm).
    a_signal : float
        Amplitude du signal.
    a_bruit : float
        Amplitude du bruit.
    sigma_model : float
        Écart-type du modèle de signal.
    opt : bool
        Indicateur d'activation des optimisations.
    redshift_th : float
        Redshift théorique (décalage vers le rouge).
    lambda_obs : float
        Longueur d'onde observée après décalage.
    lambda_gen : ndarray
        Tableau des longueurs d'onde générées pour le signal.
    signal : ndarray
        Signal généré.
    bruit : ndarray
        Bruit ajouté au signal.
    simulate_data : ndarray
        Données simulées combinant le signal et le bruit.
    model : ndarray
        Modèle théorique basé sur une loi normale.
    snr : ndarray
        Rapport signal-bruit (SNR) calculé.
    """
    
    def __init__(self, lambda_0=656.3, A_signal=100.0, A_bruit=1.0, sigma_model=8.0, opt=False):
        
        self.lambda_0 = lambda_0
        self.a_signal = A_signal
        self.a_bruit = A_bruit
        self.sigma_model = sigma_model
        self.opt = opt
        
        self.redshift_th = None
        self.lambda_obs = None
        self.lambda_gen = None
        self.signal = None
        self.bruit = None
        self.simulate_data = None
        self.model = None
        self.snr = None
        
        self._compile_data()
    
    def Main(self):
        """
        Effectue les opérations principales de la classe BruitBlanc en générant et affichant les 
        graphiques correspondants pour l'analyse du signal, du bruit et du SNR.

        La méthode appelle les différentes méthodes de la classe pour :
        - Afficher les graphiques du signal, des données simulées, et du SNR.
        - Afficher l'influence de l'amplitude du signal, du bruit et de la déviation standard du modèle.
        - Calculer et afficher les performances d'exécution et les émissions de CO2.
        
        Paramètres d'initialisation :
        -----------------------------
        lambda_0 : float, optionnel
            Longueur d'onde de référence (en nm), par défaut 656.3 nm.
        A_signal : float, optionnel
            Amplitude du signal, par défaut 100.0.
        A_bruit : float, optionnel
            Amplitude du bruit, par défaut 1.0.
        sigma_model : float, optionnel
            Écart-type du modèle de signal, par défaut 8.0.
        opt : bool, optionnel
            Indicateur d'activation des optimisations, par défaut False.
        """

        self.Detection()
        self.Plot()
        self.TimeTracker()
        self.CarbonTracker()

    def _compile_data(self):
        """
        Compile toutes les données nécessaires pour l'analyse du signal : 
        calcul de la longueur d'onde observée, génération du signal, ajout du bruit, 
        simulation des données, création du modèle, et calcul du SNR.

        Cette méthode est appelée automatiquement lors de l'initialisation de l'objet.
        
        Retourne :
        ----------
        Aucun.
        """
        
        self._lambda_obs()
        self._lambda_gen()
        self._signal()
        self._bruit()
        self._simulate_data()
        self._model()
        self.SNR()

    def TurnOpt(self):
        """
        Active ou désactive l'optimisation des calculs en inversant l'état de l'attribut 'opt'.

        Retourne :
        ----------
        Aucun.
        """
        
        self.opt = not self.opt
    
    def _update_SNR(self):
        """
        Met à jour le rapport signal-bruit (SNR) en recalculant les corrélations et en utilisant 
        les données et le modèle actuels.

        Retourne :
        ----------
        Aucun.
        """
        
        self.SNR()
        
    def _update_signal_amplitude(self, A_signal):
        """
        Met à jour l'amplitude du signal et recalcule les données simulées et le rapport signal-bruit (SNR).

        Paramètres :
        ------------
        A_signal : float
            Nouvelle amplitude du signal.

        Retourne :
        ----------
        Aucun.
        """
        
        self.signal = self.signal / self.a_signal
        self.a_signal = A_signal
        self.signal = self.signal * self.a_signal
        self._simulate_data()
        self.SNR()
    
    def _update_bruit_amplitude(self, A_bruit):
        """
        Met à jour l'amplitude du bruit et recalcule les données simulées et le rapport signal-bruit (SNR).

        Paramètres :
        ------------
        A_bruit : float
            Nouvelle amplitude du bruit.

        Retourne :
        ----------
        Aucun.
        """
        
        self.bruit = self.bruit / self.a_bruit
        self.a_bruit = A_bruit
        self.bruit = self.bruit * self.a_bruit
        self._simulate_data()
        self.SNR()
        
    def _update_sigma_model(self, sigma_model):
        """
        Met à jour la déviation standard du modèle et recalcule le rapport signal-bruit (SNR).

        Paramètres :
        ------------
        sigma_model : float
            Nouvelle déviation standard du modèle.

        Retourne :
        ----------
        Aucun.
        """
        
        self.sigma_model = sigma_model
        self._model()
        self.SNR()

    def _lambda_obs(self):
        """
        Calcule la longueur d'onde observée en fonction du décalage vers le rouge théorique.

        Retourne :
        ----------
        Aucun.
        """
        
        self.redshift_th = np.random.uniform(0.0, 1.0)
        self.lambda_obs = self.lambda_0*(1+self.redshift_th)

    def _lambda_gen(self):
        """
        Génère un tableau de longueurs d'onde (en nm) dans la gamme spécifiée.

        Retourne :
        ----------
        Aucun.
        """
        
        self.lambda_gen = np.linspace(600, 1400, num=1000)
        print(f"Pas utiliser pour l'echantillonage : {self.lambda_gen[1] - self.lambda_gen[0]} nm.")

    def _signal(self): 
        """
        Génère le signal basé sur une distribution normale avec l'amplitude spécifiée et le décalage vers le rouge.

        Retourne :
        ----------
        Aucun.
        """
        
        self.signal = self.a_signal*sp.stats.norm.pdf(self.lambda_gen, self.lambda_obs, self.lambda_obs*0.01)

    def _bruit(self):
        """
        Génère un bruit gaussien blanc avec l'amplitude spécifiée.

        Retourne :
        ----------
        Aucun.
        """
        
        self.bruit = self.a_bruit*np.random.normal(size=1000)

    def _simulate_data(self):
        """
        Génère les données simulées en combinant le signal et le bruit.

        Retourne :
        ----------
        Aucun.
        """
        
        self.simulate_data = self.signal+self.bruit

    def _model(self):
        """
        Génère le modèle basé sur une distribution normale pour ajuster le signal observé.

        Retourne :
        ----------
        Aucun.
        """
        
        h = (1400 - 600) / 1000
        x = np.arange(60) * h
        self.model = sp.stats.norm.pdf(x, x[29], self.sigma_model)

    def _correlation(self, vector_data):
        """
        Applique une corrélation croisée manuelle pour estimer le SNR entre le signal observé et le bruit.

        Paramètres :
        ------------
        vector_data : ndarray
            Série temporelle à corréler avec le modèle.

        Retourne :
        ----------
        ndarray
            Série des corrélations pour chaque décalage.
        """
        
        f_g = self.model
        N_g = np.size(f_g)
        d = vector_data
        N = np.size(d)
        l = []

        for i in range(N-N_g):
            l.append(np.sum(f_g * d[i:i+N_g]))

        return np.array(l)
    
    def _correlation_scipy(self, vector_data):
        """
        Applique une corrélation croisée en utilisant la fonction de corrélation de SciPy pour estimer le SNR.

        Paramètres :
        ------------
        vector_data : ndarray
            Série temporelle à corréler avec le modèle.

        Retourne :
        ----------
        ndarray
            Série des corrélations pour chaque décalage.
        """
        
        return sp.signal.correlate(vector_data, self.model)

    def SNR(self):
        """
        Calcule le rapport signal-bruit (SNR) en utilisant la corrélation croisée et l'écart-type du bruit.

        Retourne :
        ----------
        Aucun.
        """
        
        if self.opt:
            tau_bruit = self._correlation_scipy(self.bruit)
            tau_obs = self._correlation_scipy(self.simulate_data)
        else:
            tau_bruit = self._correlation(self.bruit)
            tau_obs = self._correlation(self.simulate_data)
 
        sigma_bruit = np.std(tau_bruit)
        self.snr = tau_obs / sigma_bruit

    def Detection(self):
        """
        Détecte la position du signal en fonction du SNR et compare le redshift détecté au redshift théorique.

        Retourne :
        ----------
        Aucun.
        """
        
        p0 = np.argmax(self.snr)
        if (self.snr[p0]>3):
            print(f'Position du signal en p0 = {p0}.')
            d = self.lambda_gen
            lambda_max = d[p0]
            print(f'z = {(lambda_max - self.lambda_0) / self.lambda_0}, avec z_th = {self.redshift_th}')
        else:
            print("Aucun signal detectee.")
            
    def _redshift(self):
        """
        Calcule le redshift (décalage vers le rouge) estimé à partir du rapport signal-bruit (SNR).
        Le redshift est calculé en fonction de la position maximale du SNR. Si la position est au-dessus 
        d'un seuil, le redshift est estimé à partir de la longueur d'onde générée à cette position.
        
        Retourne :
        ----------
        float ou None
            Le redshift estimé, ou None si la position maximale est inférieure au seuil.
        """
        
        p0 = np.argmax(self.snr)
        if (p0>3):
            return self.lambda_gen[p0]
        else:
            return None

    def TimeTracker(self):
        """
        Suivi du temps d'exécution des calculs de rapport signal-bruit (SNR) avec et sans optimisation.
        
        La méthode mesure le temps d'exécution de 1000 itérations de mise à jour du SNR avec l'optimisation activée
        et désactivée, puis affiche les résultats.
        
        Retourne :
        ----------
        Aucun.
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
        Suivi des émissions de CO2 générées par les calculs de rapport signal-bruit (SNR) avec et sans optimisation.
        
        La méthode mesure les émissions de CO2 pour 1000 itérations de mise à jour du SNR avec l'optimisation activée
        et désactivée, puis affiche les résultats.
        
        Retourne :
        ----------
        Aucun.
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
        
    def Plot(self):
        """
        Affiche tous les graphiques (Signal, Données simulées, SNR, etc.) sur une seule page.

        Retourne :
        ----------
        Aucun.
        """
        # Créer une figure avec plusieurs sous-graphes
        fig, axs = plt.subplots(3, 2, figsize=(16, 9))
        plt.subplots_adjust(hspace=0.3)

        # Tracer le signal
        axs[0, 0].plot(self.lambda_gen, self.signal)
        axs[0, 0].set_title("Signal provenant d'une loi normale")
        axs[0, 0].set_xlabel(r'$\lambda$ (nm)')

        # Tracer les données simulées
        axs[0, 1].plot(self.lambda_gen, self.simulate_data)
        axs[0, 1].set_title("Pseudo-donnees, signal dans un bruit gaussien blanc")
        axs[0, 1].set_xlabel(r'$\lambda$ (nm)')

        # Tracer le SNR
        axs[1, 0].plot(self.snr, color='red', label=f'Opt = {self.opt}')
        self.TurnOpt()
        self._update_SNR()
        axs[1, 0].plot(self.snr, color='blue', label=f'Opt = {self.opt}')
        axs[1, 0].legend()
        axs[1, 0].set_title("Fluctuations du SNR")

        # Tracer l'influence de l'amplitude du signal sur le redshift
        x = None
        y = None

        x = []
        y = []
        for i in range(100):
            self._update_signal_amplitude(i+1)
            l = self._redshift()
            x.append(i+1)
            y.append((l-self.lambda_0)/self.lambda_0)
        axs[1, 1].plot(x, y)
        axs[1, 1].set_title("Influence de l'amplitude du signal sur sa detection")
        axs[1, 1].set_xlabel('Amplitude du signal')
        axs[1, 1].set_ylabel('Redshift deduit')
        axs[1, 1].axhline(self.redshift_th, color='red', linestyle='--', label='redshift generer')
        axs[1, 1].legend()

        # Tracer l'influence de l'amplitude du bruit sur le redshift
        x = None
        y = None

        x = []
        y = []
        for i in range(100):
            self._update_bruit_amplitude(i+1)
            l = self._redshift()
            x.append(i+1)
            y.append((l-self.lambda_0)/self.lambda_0)
        axs[2, 0].plot(x, y)
        axs[2, 0].set_title("Influence de l'amplitude du bruit sur la detection du signal")
        axs[2, 0].set_xlabel('Amplitude du bruit')
        axs[2, 0].set_ylabel('Redshift deduit')
        axs[2, 0].axhline(self.redshift_th, color='red', linestyle='--', label='redshift generer')
        axs[2, 0].legend()

        # Tracer l'influence de la déviation standard du modèle sur le redshift
        x = None
        y = None
        x = []
        y = []
        self._update_bruit_amplitude(1.0)
        for i in range(100):
            self._update_sigma_model(i+1)
            l = self._redshift()
            x.append(i+1)
            y.append((l-self.lambda_0)/self.lambda_0)
        axs[2, 1].plot(x, y)
        axs[2, 1].set_title("Influence de la deviation standard du modele sur la detection du signal")
        axs[2, 1].set_xlabel('Deviation standard du modele')
        axs[2, 1].set_ylabel('Redshift deduit')
        axs[2, 1].axhline(self.redshift_th, color='red', linestyle='--', label='redshift generer')
        axs[2, 1].legend()

        # Afficher les graphiques
        plt.tight_layout()
        plt.show()