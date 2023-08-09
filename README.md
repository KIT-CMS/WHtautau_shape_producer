

# WH(tautau) analysis framework
In this repository all software necessary for the WH(tautau) charge asymmetry UL analysis starting from flat n-tuple level (see https://github.com/KIT-CMS/WHTauTauAnalysis-CROWN) is stored. The software uses the ntuple_processor code included as submodule of the main repository. The software is written in python3 and uses RDataFrames.
The repository provides code to produce friendtrees for xsec related quantities and fake factors and shapes for the fit. 

# 0. friendtree production
Script for friendtree production for crosssection related variables and fake factors is:
```
friendtree_production.sh
```
# 0.1 Crosssection friend
Based on the information provided in `KingMaker/sample_database/datasets.yaml` necessary variables like `crossSectionPerEventWeight` are written in a friend tree. 

# 0.2 Fake factors
Backgrounds that have at least on jet faking one of the objects in the final state (muon, electron, hadronic tau) are estimated via data driven fake faktors. Fake factors are calculated for each fakeable object. Precise selection criteria are written in https://cms.cern.ch/iCMS/jsp/db_notes/noteInfo.jsp?cmsnoteid=CMS%20AN-2020/089 and studies in https://indico.cern.ch/event/1313127/  <br>
The first step to calculate fake factors is to produce shapes for a tight and a loose phasespace. This is done via the scripts:
```
jet_to_tau_fakerate_shapes.sh
jet_to_lepton_fakerate_shapes.sh
```
In case of jet faking hadronic taus, the two regions are `VVVLoosevsJets && !VTightvsJets` and `VTightvsJets`. In case of jets faking leptons, the two regions are `iso<0.15&&mediumID` and `iso>0.15 || !mediumID` (same for electrons). With these shapes the fake rates are calculated via `jet_fakerate_calculation.sh` and stored in a json file. In this script you also have to specify the amount of the systematic uncertainty related to the uncertainty of backgrounds, that are estimated via simulation and subtracted before taking the ratio. 
The json file is than picked up by the `friendtree_production.sh` script.
# 1. configuration
Before you produce control or signal shapes you have to modify the configuration files in `config/shapes` to your needs.  <br>
In `config/shapes/channel_selection.py` the selection on plotting level takes place and also the difference between signal and control shapes. <br>
In `config/shapes/process_selection.py` correction factors are applied that correct the difference between data and MC. Those correction factors depend on working points and cuts defined in `config/shapes/channel_selection.py`. Therefore these two files have to be synchronized. Also pay attention to the fact, that if you are using extention files (filenames with ext_1 at the end) you have to modfiy the value of numberofgeneratedevents weight <br> 
In `config/shapes/control_binning.py` the quantities like `pt_1` are defined. <br>
In `config/shapes/file_names.py` the file names of the corresponding processes are defined. <br>
In `config/shapes/variations.py` the shape uncertainties (uncertainties that affect the shape of one or more quantities) are defined. Furthermore anti iso regions necessary for the jet fake rate estimation (also see `shapes/do_estimations.py`) are defined here. Anti iso regions are phase spaces in which leptons do not pass the tight ID/iso criterias. 

# 2. shape production

Once you have the friendtrees in place and configured the settings, you can start producing shapes. The top level script to do this is:
```
bash shape_production.sh
```
One of the arguments is the regions argument. Here you specify for which phasespace you want the shapes for. Options are `control`, `plus`, `minus`, while the latter are signal regions with cuts on the charge of the first lepton assigned to the W. In case of signal regions, the script produces all systematic variations. In `shape_production.sh` the following scripts are executed:
`shapes/produce_shapes.py`: here you specify which systematic variations you want to include for which process from `config/shapes/variations.py`. If you not further specify the processes you want to process, check the defaults that are used.  <br>
`shapes/do_estimations.sh`: in this script the estimation of jet faking taus and leptons take place. <br>
`shapes/convert_to_synced_shapes.sh`


and produces so called synced shapes, which are the same shapes but renamed for the fit with combine. 


For the production of analysis shape the submission script `submit/submit_shape_production.sh` is provided, which uses `shapes/produce_shapes_condor.py`. It is recommended to split up the signal shapes, since it takes a lot of memory to produce them in a single job and split up the channels and eras as well. The splitting of NMSSM processes can be found in `utils/setup_nmssm_samples.sh` and needs to be changed, depending which signal shapes you want to produce. The singlegraph argument remains fixed. The TAG you give to the script identifies the batch of shapes you are producing. This is just a string which ends up in the output filename. Choose 0 for control shapes and 1 for analysis shapes. The last argument is the path to the NN configuration file. 
The actual paths to your background and signal samples need to be specified. You will need to change the paths to the directories of your ntuples and friends in `utils/setup_samples` accordingly.
1. An example execution is:
```bash
TAG=mH1000
NN_config="/work/rschmieder/nmssm/nmssm_condor_analysis/sm-htt-analysis/output/ml/parametrized_nn_mH1000/all_eras_mt/dataset_config.yaml"

for ERA in 2016 2017 2018
do
 for CHANNEL in et mt tt
 do

   for PROCESSES in backgrounds nmssm_split1
   do
     bash submit/submit_shape_production.sh $ERA $CHANNEL $PROCESSES singlegraph $TAG 1 $NN_config
   done
 done
done
```
The logs of the shape production can be found under `log/condor_shapes/`. The shapes can be found in `output/shapes/`.

2. The different files we now have containing shapes for different proccesses are added together to a single root file with for example:
```
hadd output/YOUR_DIRECTORY/${ERA}-${CHANNEL}.root output/shapes/{YOUR_FILES}/*
```

3. We will now peform qcd estimations on the histograms in the root file you get in previous step To do this, execute: 
    ./shapes/do_estimations.sh ${ERA} ${pathtoyourrootfile} 0

4. The naming of the shapes needs to be converted to a format which combine (CMS fitting tool) is able to read. We call these 'synced shapes'
    To do this, execute: 
```
python shapes/convert_to_synced_shapes.py --era ${ERA} --input ${pathtoyourrootfile} --output output/YOUR_DIRECTORY/ -n 12
```
The output file name can be altered in the conver_to_synced_shapes.py file
 5. As the last step, the synced shapes, which are divided in the NN classes right now, need to added into a single file again again via: 
```
hadd output/YOUR_DIRECTORY/htt_${CHANNEL}.inputs-nmssm-${ERA}-${CHANNEL}_max_score_{heavy_mass}_{batch}.root output/YOUR_DIRECTORY/{ERA}-{CHANNELS}-synced-NMSSM*
```
These shapes you can use for combine.
