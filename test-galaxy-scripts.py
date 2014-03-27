from Galaxy.calculate_HRV_indexes import *
from Galaxy.load_RR_data import *
from pyHRV import get_available_indexes

hrv_list = get_available_indexes()
GalaxyLoadRR(input="z_data/A05.txt", output="A05.ibi", column="IBI").execute()
print GalaxyHRVAnalysis(input="A05.ibi", output="test2.txt", indexes=hrv_list).execute()
