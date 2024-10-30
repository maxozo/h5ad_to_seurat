#!/usr/bin/env python
import scanpy as sc
import argparse
import anndata as ad
import numpy as np
from scipy import sparse
import pandas as pd
parser = argparse.ArgumentParser(
    description="""
        Convert H5AD to Seurat
        """
)

# parser.add_argument(
#     '--outdir',
#     action='store',
#     dest='outdir',
#     required=True,
#     help='outdir'
# )

parser.add_argument(
    '--outname',
    action='store',
    dest='outname',
    required=True,
    help='outname'
)

parser.add_argument(
    '-h5', '--h5_anndata',
    action='store',
    dest='h5',
    required=True,
    help='H5 AnnData file.'
)

options = parser.parse_args()
outname = options.outname 
h5 = options.h5
print(f'Converting {h5}')
adata3 = sc.read_h5ad(filename=h5)
            
try:
    if adata3.raw.shape != adata3.X.shape:
        del adata3.raw
    else:
        _='same dims'
except:
    _='no layers'
        
# del adata3.raw
# adata3 = adata3[:50, :]
# del adata3.raw
# Loop through all keys in the uns layer of adata3
for key in list(adata3.uns.keys()):
    try:
        # Check if the uns[key] is a scalar or array-like object that applies to all cells
        if isinstance(adata3.uns[key], (str, int, float)):
            # If it's a single value, broadcast it to all cells in obs
            adata3.obs[key] = adata3.uns[key]
        
        elif len(adata3.uns[key]) == adata3.n_obs:
            # If it's a list or array with the same length as the number of cells, add to obs
            adata3.obs[key] = adata3.uns[key]
        
        elif len(adata3.uns[key]) == adata3.n_vars:
            # If it's a list or array with the same length as the number of variables (genes), add to var
            adata3.var[key] = adata3.uns[key]
        
        else:
            # Handle or skip the case where the data is not compatible (e.g., unstructured data)
            print(f"Skipping {key}: incompatible size or structure.")
    
    except Exception as e:
        print(f"Error processing key {key}: {e}")
    
    # Remove the key from uns once it's been processed
    del adata3.uns[key]

# del adata3.varm
# del adata3.obsp
adata3.X = sparse.csr_matrix(adata3.X)
adata3.X = adata3.X.astype(np.float32)

for c1 in adata3.obs.columns:
    try:
        adata3.obs[c1] = adata3.obs[c1].cat.add_categories("Unknown").fillna('Unknown')
    except:
        _=''

adata3.write(
    f'tmp__{outname}.h5ad'
)

# subset_adata.write(
#     f'/lustre/scratch127/humgen/teams/hgi/mo11/tmp_projects127/random_work/anja/tmp.h5ad'
# )