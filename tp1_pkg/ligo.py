from pycbc.psd import interpolate
from pycbc.catalog import Merger
from pycbc.waveform import get_td_waveform
import matplotlib.pyplot as plt
from pycbc.filter import highpass, matched_filter
import os

version = "1.0"

class GWData:
    """
    Classe pour analyser les données d'événements d'ondes gravitationnelles.

    Cette classe permet de charger, filtrer et analyser les données d'événements
    d'ondes gravitationnelles, de calculer le rapport signal-bruit (SNR), et de générer
    des formes d'ondes gravitationnelles. Elle permet également de visualiser ces résultats
    à travers des graphiques.

    Attributs :
    -----------
        event : Merger 
        	Objet représentant l'événement d'onde gravitationnelle.
        detector: str
        	Nom du détecteur (ex. "H1" pour Hanford).
        strain : TimeSeries
        	Série temporelle brute des contraintes.
        filtered_strain : TimeSeries
        	Série temporelle après filtrage passe-haut.
        time : numpy.ndarray
        	Tableau des temps associés aux données.
        dt : float
        	Intervalle de temps entre deux échantillons.
        time_tot : float
        	Temps total de la série temporelle.
        psd : FrequencySeries
        	Densité spectrale de puissance (PSD) brute.
        psd_interpolated : FrequencySeries
        	PSD interpolée pour le filtrage.
        m1 : float
        	Masse du premier objet compact (en masses solaires).
        m2 : float
        	Masse du second objet compact (en masses solaires).
        f_min : float
        	Fréquence minimale utilisée pour l'analyse.
        duration : float
        	Durée de la simulation de la forme d'onde (en secondes).
        hp : TimeSeries
        	Polarisation "+" de la forme d'onde gravitationnelle.
        snr : TimeSeries 
        	Rapport signal-bruit (SNR) calculé.
    """

    def __init__(self, event, detector, m1, m2, f_min, duration, dt):
        
        self.event = Merger(event)
        self.detector = detector
        self.strain = None
        self.filtered_strain = None
        self.time = None
        self.dt = None
        self.time_tot = None
        self.psd = None
        self.psd_interpolated = None
        self.m1 = m1
        self.m2 = m2
        self.f_min = f_min
        self.duration = duration
        self.dt = dt
        self.hp = None
        self.snr = None
        
    def Main(self): 
        """
        Paramètres de bases :
        ---------------------
        event : str 
            Nom de l'événement (ex. "GW150914").
        detector : str 
            Nom du détecteur (ex. "H1").
        m1 : float
            Masse du premier objet compact (en masses solaires).
        m2 : float 
            Masse du second objet compact (en masses solaires).
        f_min : float 
            Fréquence minimale pour l'analyse (en Hz).
        duration : float 
            Durée pour la forme d'onde (en secondes).
        dt : float
            Intervalle de temps entre les échantillons (en secondes).
        """
    	
        # Création et chargement des données		
        self.load_data()
        self.generate_waveform()
        self.filter_data()
        self.plot_data()
        plt.show()

    def load_data(self):
        """
        Charge les données de l'événement et calcule la PSD interpolée.

        Description :
        -------------
        Cette méthode charge les données de l'événement d'onde gravitationnelle et effectue
        un filtrage passe-haut pour éliminer les basses fréquences non pertinentes. Elle calcule
        également la densité spectrale de puissance (PSD) et l'interpole pour le filtrage.

        Paramètres :
        ------------
        Aucun.

        Retourne :
        ----------
        Aucun.
        """
        self.strain = self.event.strain(self.detector)
        self.filtered_strain = highpass(self.strain, 15.0)
        self.time = self.strain.sample_times
        self.dt = self.time[1] - self.time[0]
        len_t = len(self.time)
        self.time_tot = self.dt * len_t
        self.psd = self.filtered_strain.psd(4)
        self.psd_interpolated = interpolate(self.psd, self.filtered_strain.delta_f)

    def generate_waveform(self):
        """
        Génère la forme d'onde gravitationnelle pour les masses spécifiées.

        Description :
        -------------
        Cette méthode génère la forme d'onde gravitationnelle pour les objets compacts
        spécifiés par leurs masses et la fréquence minimale. La polarisation "+" est
        calculée à l'aide de l'approximant 'SEOBNRv4_opt'.

        Paramètres :
        ------------
        Aucun.

        Retourne :
        ----------
        Aucun.
        """
        self.hp, _ = get_td_waveform(
            approximant='SEOBNRv4_opt',
            mass1=self.m1, 
            mass2=self.m2, 
            f_lower=self.f_min,
            delta_t=self.dt, 
            duration=self.duration
        )
        self.hp.resize(len(self.strain))

    def filter_data(self):
        """
        Applique le filtre de corrélation croisée pour calculer le SNR.

        Description :
        -------------
        Cette méthode applique un filtre de corrélation croisée sur la forme d'onde générée
        et la série temporelle filtrée afin de calculer le rapport signal-bruit (SNR). Elle utilise
        la densité spectrale de puissance (PSD) interpolée et affiche les résultats pertinents.

        Paramètres :
        ------------
        Aucun.

        Retourne :
        ----------
        Aucun.
        """
        self.snr = matched_filter(
            self.hp, 
            self.filtered_strain, 
            psd=self.psd_interpolated, 
            low_frequency_cutoff=self.f_min
        )
        self.snr = self.snr.crop(8, 8)

    def plot_data(self):
        """
        Génère un ensemble de graphiques pour analyser les données et leurs propriétés.

        Description :
        -------------
        Cette méthode affiche plusieurs graphiques relatifs aux données de l'événement, à la forme
        d'onde gravitationnelle générée, à la densité spectrale de puissance (PSD), et au rapport
        signal-bruit (SNR). Les graphiques incluent :
        - La série temporelle brute de l'événement GW150914 sur le détecteur H1.
        
        - La série temporelle filtrée de l'événement GW150914 sur le détecteur H1.
        
        - La densité spectrale de puissance (PSD) du bruit interpolée.
        
        - L'amplitude de la polarisation "+" de la forme d'onde gravitationnelle.
        
        - Le rapport signal-bruit (SNR) en fonction du temps.

        Paramètres :
        ------------
        Aucun.

        Retourne :
        ----------
        Aucun. Les graphiques sont affichés.
        """
        
        output_dir = "./results_ligo/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Créer un gridspec pour personnaliser l'agencement des subplots
        fig = plt.figure(figsize=(16, 9))
        gs = fig.add_gridspec(3, 2)  # Crée une grille de 3x2

        # Subplots 1 et 2
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.plot(self.time, self.strain, label="Hanford (H1)")
        ax1.set_xlabel("Temps (secondes)")
        ax1.set_ylabel("Amplitude de la contrainte (strain)")
        ax1.set_title("Série temporelle de l'événement GW150914 - Hanford (H1)")
        ax1.legend()
        ax1.grid()

        ax2 = fig.add_subplot(gs[0, 1])
        ax2.plot(self.time, self.filtered_strain, label="Hanford (H1) - Filtré")
        ax2.set_xlabel("Temps (secondes)")
        ax2.set_ylabel("Amplitude de la contrainte (strain)")
        ax2.set_title("Série temporelle filtrée de l'événement GW150914 - Hanford (H1)")
        ax2.legend()
        ax2.grid()

        # Subplot 3 et 4
        ax3 = fig.add_subplot(gs[1, 0])
        ax3.loglog(self.psd_interpolated.sample_frequencies, self.psd_interpolated, label="PSD du bruit (interpolée)")
        ax3.set_xlim(3, 3000)
        ax3.set_xlabel("Fréquence (Hz)")
        ax3.set_ylabel('PSD (strain' + r'$^2$' + '.Hz' + r'$^{-1}$)')
        ax3.set_title("Densité spectrale de puissance du bruit interpolée - GW150914")
        ax3.legend()
        ax3.grid()

        ax4 = fig.add_subplot(gs[1, 1])
        ax4.plot(self.hp.sample_times, self.hp, label="Polarisation +")
        ax4.set_xlim(-0.33, 0.05)
        ax4.set_xlabel("Temps (s)")
        ax4.set_ylabel("Amplitude")
        ax4.set_title("Amplitude de la polarisation '+' de l'onde gravitationnelle")
        ax4.legend()
        ax4.grid()

        # Fusionner axes[2, 0] et axes[2, 1] pour que le dernier graphique prenne deux places
        ax5 = fig.add_subplot(gs[2, :])  # Fusionne les deux colonnes sur la dernière ligne
        ax5.plot(self.snr.sample_times, self.snr, label="SNR")
        ax5.set_xlabel("Temps (s)")
        ax5.set_ylabel("Amplitude")
        ax5.set_title("Rapport du bruit sur le signal en fonction du temps")
        ax5.legend()
        ax5.grid()

        # Supprimer l'axe inutilisé (axes[2, 1])
        #fig.delaxes(fig.get_axes()[5])

        # Titre général
        fig.suptitle("Masse des objets : " + str(self.m1) + " M solaire")

        # Ajuster l'espacement entre les subplots
        plt.tight_layout()
        
        plt.savefig(output_dir + "/GW150914_" + str(self.m1) + "_M.png", format="png")
        print("Le fichier est sauvé dans le dossier results_ligo/ au nom : GW150914_" + str(self.m1) + "_M.png")