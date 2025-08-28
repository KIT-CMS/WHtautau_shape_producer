# arturs scripts to merge files on nrg or copy them to desy
MODE=$1
CHANNELS="emt met ett mtt" # mmt ett mtt"
ERAS="2016preVFP 2016postVFP 2017 2018"
if [[ $MODE == "COPY" ]]; then
    python copy_files.py --input-storage-prefix davs://cmsdcache-kit-disk.gridka.de:2880/pnfs/gridka.de/cms/disk-only --output-storage-prefix davs://dcache-cms-webdav.desy.de:2880/pnfs/desy.de/cms/tier2 --old-directory rschmieder --new-directory rschmieder --filelist rschmieder_13_11_24_alleras_allch_no_size.txt
fi
if [[ $MODE == "FILELIST" ]]; then
    python find_all_files_via_xrootd.py --server_url root://cmsdcache-kit-disk.gridka.de --directory /store/user/rschmieder/CROWN/ntuples/13_11_24_alleras_allch/ --filter_substring ".root" --output_file rschmieder_13_11_24_alleras_allch.txt
fi
if [[ $MODE == "CH_FILELIST" ]]; then
    for CHANNEL in $CHANNELS
    do
        python modify_txt_file.py --channel $CHANNEL --input_file rschmieder_13_11_24_alleras_allch.txt --output_file ${CHANNEL}_13_11_24_alleras_allch.txt
    done
fi
if [[ $MODE == "MERGE" ]]; then
    source /cvmfs/sft.cern.ch/lcg/views/LCG_106b/x86_64-el9-gcc14-opt/setup.sh
    for CHANNEL in $CHANNELS
    do
        if [[ "$CHANNEL" == "ett" ]] || [[ "$CHANNEL" == "mtt" ]] ; then
                FRIENDS="crosssection jetfakes_wpVSjet_Medium_30_08_24_MediumvsJetsvsL jetfakes_wpVSjet_Medium_11_10_24_MediumvsJetsvsL_measure_njetclosure jetfakes_wpVSjet_Medium_11_10_24_MediumvsJetsvsL_measure_metclosure met_unc_22_10_24 pt_1_unc_22_10_24 nn_friends_22_11_24_MediumvsJL_pruned"
        else
                FRIENDS="crosssection jetfakes_wpVSjet_Loose_30_08_24_LoosevsJetsvsL jetfakes_wpVSjet_Loose_11_10_24_LoosevsJetsvsL_measure_njetclosure jetfakes_wpVSjet_Loose_11_10_24_LoosevsJetsvsL_measure_metclosure met_unc_22_10_24 pt_1_unc_22_10_24 nn_friends_22_11_24_LoosevsJL_pruned"
        fi
        python merge_crown_ntuples_and_friends.py --main_directory /store/user/rschmieder/CROWN/ntuples/13_11_24_alleras_allch/ --filelist ${CHANNEL}_13_11_24_alleras_allch.txt --tree ntuple --allowed_friends ${FRIENDS} --n_threads 6 --remote_server root://cmsdcache-kit-disk.gridka.de 
    done
fi
if [[ $MODE == "NRG" ]]; then
    source /cvmfs/sft.cern.ch/lcg/views/LCG_106b/x86_64-el9-gcc14-opt/setup.sh
    for CHANNEL in $CHANNELS
    do
        for ERA in $ERAS
        do 
            for file in ${ERA}* 
            do 
            if [[ "$file" == *"${CHANNEL}_merged.root" ]]; then
                echo "Processing file: $file"
                SAMPLE="${file#*_}"  # Remove the prefix up to and including the first "_"
                SAMPLE="${SAMPLE%_${CHANNEL}_merged.root}"
                echo "$SAMPLE"
                xrdcp $file "root://cmsdcache-kit-disk.gridka.de:1094//store/user/rschmieder/CROWN/ntuples/13_11_24_alleras_allch_merged/CROWNRun/${ERA}/${SAMPLE}/${CHANNEL}/${SAMPLE}_0.root"
            fi
            done
        done
    done
fi