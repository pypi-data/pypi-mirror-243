import sys 

sys.path = ['python'] + sys.path

import calc_utility as cu
import rk.utilities as rkut
import utils_noroot as utnr 

log=utnr.getLogger(__name__)
#-------------------------------------
def test_geo_eff():
    l_proc = []
    l_proc.append('psi2_ee')
    l_proc.append('psi2_mm')
    l_proc.append('ctrl_ee')
    l_proc.append('ctrl_mm')
    l_proc.append('rare_ee')
    l_proc.append('rare_mm')

    l_year = ['2011', '2012', '2015', '2016', '2017', '2018']
    
    for proc in l_proc:
        for year in l_year:
            eff, err = cu.getGeomEff(proc, year)
            line = f'{proc:<20}{year:<10}{eff:<10.3f}{err:<10.3e}'
            log.info(line)
#-------------------------------------
if __name__ == '__main__':
    test_geo_eff()

