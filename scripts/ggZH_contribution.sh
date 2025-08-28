source utils/setup_root.sh
source utils/setup_python.sh
NTUPLE_TAG_GGZH="28_11_24_2018_allch_ggzh"
SHAPE_TAG_GGZH="28_11_24_nn_shapes_ggZHtest"
NTUPLE_TAG="13_11_24_alleras_allch"
SHAPE_TAG="28_11_24_nn_shapes_ggZHtest"
ERAS="2018" #"2016preVFP 2016postVFP 2017 2018"
CHANNELS="llt ltt"
#FILENAME="nn_signal_minus.root"
for ERA in $ERAS
do
for CHANNEL in $CHANNELS
do
for CHARGE in plus minus
do
    FILENAME="nn_signal_${CHARGE}.root"
    echo $CHANNEL
    INPUT_GGZH="output/shapes/${NTUPLE_TAG_GGZH}/${ERA}/${CHANNEL}/${SHAPE_TAG_GGZH}/${FILENAME}"
    INPUT="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${FILENAME}"
    OUTPUT="plots/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${CHARGE}/"
    mkdir -p ${OUTPUT}
    python ggZH_contribution.py --input_ggzh ${INPUT_GGZH} --input ${INPUT} --plot_output ${OUTPUT} --channel ${CHANNEL}
done
done
done