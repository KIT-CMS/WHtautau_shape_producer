CHANNELS="emt met mmt ett mtt"
for CH in $CHANNELS
do
input="output/shapes/14_04_25_alleras_allch3/all_eras/${CH}/11_08_25_nncontrol_incl/nn_control.root"
python compare_normed_dists.py --input $input --channel $CH
done