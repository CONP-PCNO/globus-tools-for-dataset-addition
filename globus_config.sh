#!/usr/bin/env bash


# The following command is going to setup, initialize and connect with the globus special remote. The following operations are performed when launched:
# 1) Sets up connection with globus via authentication
# 2) Initializes the annex remote (if remote not initialized) or enables remote
# 3) Iterates through directories until all symlinks file are found, parses them and extract file keys for all files
# 4) Makes globus aware of the file keys
# 5) Builds globus urls for all files based on their location in globus and registers urls with corresponding file keys
# 6) Enable retrieving of file content by $git annex get path/to/file

pip install configparser
pip install git-annex-remote-globus==1.0

CURRENT_DIR=`pwd`

if [[ $# -eq 0 ]] ; then
    DATASET_ROOT_PATH=${CURRENT_DIR}
else
    DATASET_ROOT_PATH="$1"
fi


${CURRENT_DIR}/retrieve.py --path ${DATASET_ROOT_PATH} --endpoint frdr_prod_2 --fileprefix /5/published/publication_170/submitted_data --encryption none