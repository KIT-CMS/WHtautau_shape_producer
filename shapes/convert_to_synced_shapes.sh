#!/bin/bash

ERA=$1
CHANNEL=$2
NTUPLE_TAG=$3
SHAPE_TAG=$4
INPUT_FILE=$5
REGION=$6
source utils/bashFunctionCollection.sh
source utils/setup_root.sh

logandrun python shapes/convert_to_synced_shapes.py -e $ERA \
                                                    -i ${INPUT_FILE} \
                                                    -o output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/synced_shapes \
                                                    -n 12 \
                                                    --region ${REGION} \
                                                    --gof


