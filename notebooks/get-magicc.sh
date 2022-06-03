#!/bin/bash
# Download and extract MAGICC7 for use in this repository.

# MAGICC7 and the parameter set are available from www.magicc.org. After
# registering, you will be sent personal links for downloading. These 
# links are linked to your magicc.org account and can be used to download
# MAGICC.

# Please read the license and expectations of using MAGICC carefully 
# (available at https://magicc.org/download/magicc7), we rely on users 
# to act in a way which brings both new scientific outcomes but also 
# acknowledges the work put into the MAGICC AR6 setup.

# Call this script like
# MAGICC7_LINK="<magicc-link>" MAGICC7_AR6_PARAMETER_SET="<magicc-parameter-set-link>" bash scripts/get-magicc.sh
# e.g. MAGICC7_LINK="www.magicc.org/downloadmagicc" MAGICC7_AR6_PARAMETER_SET="www.magicc.org/downloadmagicc-parameter-set" bash scripts/get-magicc.sh

echo ${MAGICC7_LINK}
# If you modify the output path, remember to ignore the folder from git
MAGICC_OUT_PATH=magicc-bits-and-pieces

# MAGICC binary
mkdir -p ${MAGICC_OUT_PATH}/magicc-v7.5.3
wget -O ${MAGICC_OUT_PATH}/magicc-v7.5.3.tar.gz ${MAGICC7_LINK}
tar -xf ${MAGICC_OUT_PATH}/magicc-v7.5.3.tar.gz -C ${MAGICC_OUT_PATH}/magicc-v7.5.3
cp -r ${MAGICC_OUT_PATH}/magicc-v7.5.3/run/defaults/* ${MAGICC_OUT_PATH}/magicc-v7.5.3/run/

# Probabilistic distribution
mkdir -p ${MAGICC_OUT_PATH}/magicc-ar6-0fd0f62-f023edb-drawnset
wget -O ${MAGICC_OUT_PATH}/magicc-ar6-0fd0f62-f023edb-drawnset.tar.gz ${MAGICC7_AR6_PARAMETER_SET}
tar -xf ${MAGICC_OUT_PATH}/magicc-ar6-0fd0f62-f023edb-drawnset.tar.gz -C ${MAGICC_OUT_PATH}/magicc-ar6-0fd0f62-f023edb-drawnset
