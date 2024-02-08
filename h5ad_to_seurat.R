#!/usr/bin/env Rscript
library(Seurat)
library(SeuratDisk)
library(Matrix)
library(hdf5r)
library(ggplot2)
library(tools)
args = commandArgs(trailingOnly=TRUE)
inputfile_h5ad=args[1]
outname=args[2]
Convert(
  inputfile_h5ad,
  dest = paste(outname,"h5seurat",sep='.'),
  assay = "RNA",
  overwrite = TRUE,
  verbose = TRUE,
)

fileConn<-file("tmp__success")
writeLines(c("tmp__success","tmp__success"), fileConn)
close(fileConn)
# var <- LoadH5Seurat("/lustre/scratch123/hgi/projects/jaguar_analysis/analysis/mo11/my_analysis_folder/adatanormalized.h5seurat",assays = "RNA")
# a=LoadH5Seurat('/lustre/scratch123/hgi/projects/jaguar_analysis/analysis/mo11/my_analysis_folder/test3.h5seurat',assays = "RNA")