from . import bruit_blanc as bb
from . import bruit_colore as bc
from . import ligo as lg

def main_bb():

    bruit_b = bb.BruitBlanc()
    bruit_b.Main()

def main_bc():

    bruit_c = bc.BruitColore()
    bruit_c.Main()

def main_lg():

	for m in [10, 15, 20, 25, 30, 35, 40, 45, 50]:
		data_l = lg.GWData(event="GW150914", detector="H1", m1=m, m2=m, f_min=20.0, duration=32.0, dt=1 / 4096.0)
		data_l.Main()
	
    
