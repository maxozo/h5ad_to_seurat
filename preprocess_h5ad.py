#!/usr/bin/env python
import scanpy as sc
import argparse
import anndata as ad

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
adata3 = sc.read_h5ad(filename=h5)

del adata3.raw
del adata3.uns
del adata3.varm
del adata3.obsp

for c1 in adata3.obs.columns:
    try:
        adata3.obs[c1] = adata3.obs[c1].cat.add_categories("Unknown").fillna('Unknown')
    except:
        _=''

adata3.write(
    f'tmp__{outname}.h5ad',
    compression='gzip'
)