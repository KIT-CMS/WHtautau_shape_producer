#!/bin/bash

ERA=$1
CHANNEL=$2
NTUPLE_TAG=$3
SHAPE_TAG=$4
INPUT_FILE=$5

source utils/bashFunctionCollection.sh
source utils/setup_root.sh

logandrun python shapes/convert_to_synced_shapes.py -e $ERA \
                                                    -i ${INPUT_FILE} \
                                                    -o output/shapes/${NTUPLE_TAG}/${CHANNEL}/${SHAPE_TAG}/synced_shapes \
                                                    -n 12 \
                                                    --gof

OUTFILE=output/shapes/${NTUPLE_TAG}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/htt_${CHANNEL}.inputs-sm-Run${ERA}.root
echo "[INFO] Adding written files to single output file $OUTFILE..."
logandrun hadd -f $OUTFILE output/shapes/${NTUPLE_TAG}/${CHANNEL}/${SHAPE_TAG}/synced_shapes/*.root
