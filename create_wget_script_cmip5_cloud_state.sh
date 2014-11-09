#!/bin/sh

#
# Script to create one script per model to download these variables:
#

# Cloud and state info: Amon
# clwvi
# clivi
# clt
# snc
# tas
# tasmin
# tasmax

vartype="cloud_state"
variables="variable=clwvi&variable=clivi&variable=clt&variable=snc&variable=tas&variable=tasmin&variable=tasmax"
#
for model in GFDL-CM3 BCC-CSM1.1 MRI-CGCM3 MPI-ESM-LR CNRM-CM5 IPSL-CM5B-LR IPSL-CM5A-LR IPSL-CM5A-MR MIROC5 CanAM4 HadGEM2-A

do
 mkdir -p ${model}/${vartype}
 curl -o ${model}/${vartype}/wget_${model}_${vartype}.sh "http://pcmdi9.llnl.gov/esg-search/wget/?${variables}&model=${model}&project=CMIP5&experiment=amip&cmor_table=Amon&cmor_table=LImon&ensemble=r1i1p1&distrib=true"
 chmod a+rx ${model}/${vartype}/wget_${model}_${vartype}.sh


done
