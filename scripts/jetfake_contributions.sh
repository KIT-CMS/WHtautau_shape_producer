source utils/setup_root.sh
source utils/setup_python.sh
NTUPLE_TAG="29_05_24_alleras_allch"
SHAPE_TAG="31_05_24_control_shapes"
ERAS="2018" #"2016preVFP 2016postVFP 2017 2018"
CHANNELS="mmt"
FILENAME="nn_control_max_value.root"
for ERA in $ERAS
do
for CHANNEL in $CHANNELS
do
    echo $CHANNEL
    INPUT="output/shapes/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/${FILENAME}"
    OUTPUT="plots/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/"
    mkdir -p plots/${NTUPLE_TAG}/${ERA}/${CHANNEL}/${SHAPE_TAG}/
    python jetfake_contributions.py --input ${INPUT} --plot_output ${OUTPUT} --channel ${CHANNEL}
done
done