ERAS="2016preVFP 2016postVFP 2017 2018"
CHANNELS="llt ltt"
TAG="10_05_25_nn_fitshapes"
source utils/setup_root.sh
for ERA in $ERAS 
do 
for CH in $CHANNELS
do
INPUT="/work/rschmieder/WH_analysis/WHtautau_shape_producer/output/datacard_output/14_04_25_alleras_allch3/10_05_25_nn_fitshapes_CA_RD/${ERA}_${CH}/cmb/prefitshape.root"
python postfit_yields_unc_pm.py --input $INPUT --era $ERA --channel $CH --tag $TAG
done 
done 