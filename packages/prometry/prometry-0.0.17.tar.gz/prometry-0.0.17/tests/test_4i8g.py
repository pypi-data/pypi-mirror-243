import os, sys
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(Path(__file__).parent),"src"))
from prometry import pdbloader as pl
from prometry import pdbgeometry as pg


import pandas as pd

DATADIR = "tests/data/"
ls_structures = ['4i8g']

def test_backbone():
    #ls_geos = ['CA[aa|VAL]:CA+1[aa|HIS]']
    ls_geos = ['CA[aa|VAL]:CA+1']
    #ls_geos = ['CA:CA+1']
    pobjs = []
    for pdb in ls_structures:            
        pla = pl.PdbLoader(pdb,DATADIR,cif=False,source="ebi")
        po = pla.load_pdb()
        pobjs.append(po)
    gm = pg.GeometryMaker(pobjs)
    df = gm.calculateGeometry(ls_geos)
    print(df.max())
    print(df[["info_CA[aa|VAL]:CA+1","CA[aa|VAL]:CA+1"]])
    #print(df[["info_CA[aa|VAL]:CA+1[aa|HIS]","CA[aa|VAL]:CA+1[aa|HIS]"]])


if __name__ == "__main__":    
    test_backbone()