

# WH(tautau) analysis framework
In this repository all software necessary for the WH(tautau) charge asymmetry UL analysis starting from flat n-tuple level (see https://github.com/KIT-CMS/WHTauTauAnalysis-CROWN) is stored. The software uses the ntuple_processor code included as submodule of the main repository. The software is written in python3 and uses RDataFrames.
The repository provides code to produce friendtrees for xsec related quantities and fake factors and shapes for the fit. 

# 0. friendtree production
Script for friendtree production for crosssection related variables and fake factors is:
```
friendtree_production.sh
```
# 0.1 Crosssection friend
Based on the information provided in `bash KingMaker/sample_database/datasets.yaml` necessary variables like `crossSectionPerEventWeight` are written in a friend tree. 

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

The code used for the 2018 gridpack generation using the NMSSM model is below. The masses are set in the script `create_gridpack_for_mass_2018.sh` in which also further NMSSM parameters or the decay modes of the Higgs bosons can be changed. 

```bash
 https://launchpad.net/mg5amcnlo/2.0/2.6.x/+download/MG5_aMC_v2.6.7.tar.gz
wget https://launchpad.net/mg5amcnlo/2.0/2.6.x/+download/MG5_aMC_v2.6.7.tar.gz
tar xf MG5_aMC_v2.6.7.tar.gz
rm MG5_aMC_v2.6.7.tar.gz
cd MG5_aMC_v2_6_7
rm -rf models/hgg_plugin
git clone https://github.com/janekbechtel/NMSSM-madgraph
cp -r NMSSM-madgraph/models/* models/.
rm -rf NMSSM-madgraph
wget https://raw.githubusercontent.com/janekbechtel/NMSSM-madgraph/master/create_gridpack_for_mass_2018.sh
mkdir models/custom
git clone https://github.com/cms-sw/genproductions/ -b mg265
sh create_gridpack_for_mass_2018.sh
```
The gridpacks can be used in standard CMS simulation config (GEN-SIM -> PU-mixing -> AOD -> miniAOD)


## 1. Skimming from miniAOD

Set up the code
```bash
wget https://raw.githubusercontent.com/KIT-CMS/Kappa/dictchanges/Skimming/scripts/checkoutCmssw102xPackagesForSkimming.sh
source checkoutCmssw102xPackagesForSkimming.sh

cd Kappa/Skimming/
rm -rf data/
git clone https://github.com/KIT-CMS/datasets -b nmssm data

# to test
cmsRun higgsTauTau/kSkimming_run2_cfg_KappaOnly.py testfile=file:///PATH/TO/MINIAOD_FILE.root nickname=NMSSMM500h1M125tautauh2M100_RunIIAutumn18MiniAOD_102X_13TeV_MINIAOD_madgraph-pythia8_v1 mode=local maxevents=10 usePostMiniAODSequences=True


```

## 2. Creation of ntuples

**You probably do not need to produce new ntuple currently** and can use the ones I used for the analysis. They are located in 
```
/ceph/jbechtel/nmssm/ntuples/201?/?t/
```
in which `201?` can be 2016, 2017 or 2018 and stands for the CMS run period the sample describes, and `?t` stands for the final state of the di-tau pair: et, mt or tt.

In each folder lies a collection of root files, one for each physical process which is of interest for the analysis.
To create ntuples, we use https://github.com/KIT-CMS/KITHiggsToTauTau/. To set up the code, use the checkout script:
```bash
wget https://raw.githubusercontent.com/KIT-CMS/KITHiggsToTauTau/reduced_trigger_objects/scripts/checkout_packages_CMSSW102X.sh
chmod u+x checkout_packages_CMSSW102X.sh
./checkout_packages_CMSSW102X.sh
```
The default branch is `reduced_trigger_objects` and works for all analyses we do, so also the NMSSM analysis. 
After the checkout and compilation is complete, you can set up the software by these commands. This needs to be done in every new shell, so best create a script of an alias. Also change `/PATH/TO/` to the path where you cloned the repository. For the last two commands you will need a valid grid certificate and voms-proxy, necessary for grid submission. If you don't have this (yet) you can still use the software locally.
```bash
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
cd /PATH/TO/CMSSW_10_2_18/src/
source /cvmfs/grid.cern.ch/emi3ui-latest/etc/profile.d/setup-ui-example.sh
cmsenv
export PATH=$PATH:$CMSSW_BASE/src/grid-control
export PATH=$PATH:$CMSSW_BASE/src/grid-control/scripts
source ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/scripts/ini_KITHiggsToTauTauAnalysis.sh
export X509_USER_PROXY=/home/${USER}/.globus/x509up
voms-proxy-init --voms cms:/cms/dcms --valid 192:00 --out ${X509_USER_PROXY}
```
Afterwards, you can create an example ntuple from a skimmed file:
```bash
cd HiggsAnalysis/KITHiggsToTauTau/
HiggsToTauTauAnalysis.py -a legacy --nmssm -c tt -i data/Samples/Run2Legacy_bjetRegression/Run2018/Tau_Run2018A_17Sep2018v1_13TeV_MINIAOD.txt  -f 1
```
The option `-a legacy` is used for all legacy analyses on Run2 data. `--nmssm` is needed for the NMSSM analysis to apply a cut on the number of b-jets and to write out additional information. `-c tt` specifies that only the `tt` final state will be considered. `-i ` specifies the input file, for a complete set of ntuples, all files in the lists in `data/Samples/Run2Legacy_bjetRegression` need to be used. `-f 1` just tells the program to stop after one file (for testing).
The command creates an output file called `output.root`. You can see the content of the file via 
```
root -l output.root 
.ls # to see the content directly in the command line
TBrowser g
```
Opening the `TBrowser` is  a nice way of seeing the file content, however not recommended for remote file access. Another way of seeing the file content is 
```
rootls -t output.root:tt_nominal/ntuple
```
The most important TTree in each file is located in the folder `?t_nominal`, where `?t` is again mt, et or tt depending on the final state. 
The names of the variables can be cryptic, they correspond to event information such as pT of the particles, invariant masses, correction factors, etc. To actually see the data in some distribution, you can also do
```
root -l output.root 
.ls # to see the content directly in the command line
tt_nominal->cd()
ntuple->Draw("m_vis") # Creates a histogram of the visible di-tau mass 
```
As you can see, only very few events are in the file. To produce the events, we require a CPU batch system to parallelize the tasks.
```
HiggsToTauTauAnalysis.py -a legacy --pipelines auto --nmssm -i data/Samples/Run2Legacy_bjetRegression/SAMPLES_TO_PRODUCE  -b etp7 --dry-run --files-per-job 10 -c tt -w ${PWD}/workbase --se-path srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/${USER}/ntuple_testing/
```
`-b etp7` specifies that we will use the CentOS7 batch system of the ETP. `-w` specifies the working directory where grid control stores the job information. It is important that an absolute path is used here. 
`--se-path ` specifies the remote disk where the output is written to. 
Note that now also the option ` --pipelines auto` is used. In simulated samples, these create additional folders in the root file, in which systematic variations are propagated through  the analysis. An example is the folder `tt_btagEffDown`, in which the b-tagging efficiency is lowered within its uncertainty, and the effect on the analysis evaluated. These additional folders only exists for simulated or embedded events.

After running the command above, you will get a command of the form `go.py ...` returned. By running this command, the task is sent to the batch system via the tool grid-control.
After the task is complete, you will need to merge the outputs of the individual jobs using 
```
artusMergeOutputs.py -n 8 /storage/gridka-nrg/${USER}/ntuple_testing/ --output-dir /ceph/${USER}/YOUR/PATH/TO/OUTPUT
```


The submission of jobs can alternatively be very conveniently be run on the NAF cluster at DESY, which is where I always did it. The advantages are that usually many CPU cores are available, and the files will be stored on a mount with local read AND write access, compared to the ETP where the files are stored at a mount with only read access locally.

The code can be set up the same way on the NAF, by logging in using `ssh USER@naf-cms-el7.desy.de`.
The command changes to
```
HiggsToTauTauAnalysis.py -a legacy --pipelines auto --nmssm -i data/Samples/Run2Legacy_bjetRegression/SAMPLES_TO_PRODUCE  -b naf7 --dry-run --files-per-job 10 -c tt 
```
Note that you do not need to set the workdir and the se-path anymore. These will be automatically set to the disks mounted at `/nfs/dust/cms/user/`. 
After the task is complete, you can merge on NAF using the command
```
artusMergeOutputs.py -b naf7 /nfs/dust/cms/user/PATH/TO/WORKDIR/
```
and then again submitting the grid-control command that is output from the command line. 




## 3. Create friends trees

Friend trees need to be created for the FakeFactors, SVFit and HHKinFit. For this we use https://github.com/KIT-CMS/friend-tree-producer.

In this case I had to create a separate branch as the treatment of the FakeFactors is a bit different from the other analyses we do. The branch is not the default branch and is called `nmssm_analysis`.
There also exists a checkout script:
```bash
wget https://raw.githubusercontent.com/KIT-CMS/friend-tree-producer/nmssm_analysis/scripts/checkout.sh
chmod u+x checkout.sh
./checkout.sh
```
To set up the code in a new shell, use
```bash
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
cd /PATH/TO/CMSSW_10_2_14/src/
cmsenv
export PATH=$PATH:$CMSSW_BASE/src/grid-control
export PATH=$PATH:$CMSSW_BASE/src/grid-control/scripts
export X509_USER_PROXY=/home/${USER}/.globus/x509up
voms-proxy-info
voms-proxy-init --voms cms:/cms/dcms --valid 192:00 --out ${X509_USER_PROXY}
```
To set up a task of producing new friend trees, you first need the ntuples from the previous step. An example command is then
```
job_management.py --command submit --executable HHKinFit --custom_workdir_path /ceph/${USER}/nmssm/friends/2016/tt  --input_ntuples_directory /ceph/jbechtel/nmssm/ntuples/2016/tt/   --batch_cluster etp7 --events_per_job 20000 --cores 24 --restrict_to_channels tt
```
The executable can be either `HHKinFit`, `SVFit`, `FakeFactors` or (later)  `NNScore`. The four executables have very different run times. I usually set 20,000 events per job for HHKinFit, 5000 for SVFit and 100,000 for NNScore and FakeFactors, but this is up to you. Usually jobs with take on average ~15 minutes are very manageable.

Again, after running the command above, you will get a command of the form `go.py ...` returned. By running this command, the task is sent to the batch system.

When the command is complete, run the command from above again, only change `--command submit` to `--command collect`. This will merge the outputs of the individual tasks to single files.

## 4. Train machine learning methods

For this, you will need to check out the following software:
```bash
git clone https://github.com/KIT-CMS/sm-htt-analysis -b nmssm_analysis
cd sm-htt-analysis
git submodule init
git submodule update
```
Before, setting up an ssh agent before is often useful to avoid entering the password every time:
```bash
eval `ssh-agent -s` 
ssh-add
```
In this repository, the ntuples and friends produced in the previous steps need to be added in the file `utils/setup_samples.sh`. Please note that the programs will automatically replace the string `"+CH+" with the respective channel (mt, et or tt) that is selected for the training.

The top-level script to run the machine learning training and testing is the script `run_ml.sh`. It consist of many individual steps, and it is worthwhile to check and understand the individual steps, which are: 
1. Creation of training datasets
2. Summation of training weights -> In the current implementation, training weights are automatically chosen such that each process has the same importance to the training. This is done to avoid the neural network to learn that rare processes (which are among the most interesting) anyhow never occur.
3. Training of the network.
4. Exporting the final network to a json file, to be used for application.
5. "Testing" of the network, i.e. creation of performance metrics such as efficiency, purity but also a Taylor expansion of the NN response with respect to the input variables.
```bash
ERA="2016" #choices are 2016, 2017, 2018, or "all"
CHANNEL="tt" # other possibilities: mt, et
MASS=500 # other possibilities: 240 280 320 360 400 450 500 550 600 700 800 900 1000 1200
BATCH=2 # check ml/get_nBatches.py for possibilites
./run_ml.sh $ERA $CHANNEL $MASS $BATCH
```
If you look into the run_ml script, you will see that currently a specific set of signal masses are set, in which the training is performed. For testing / playing around with the network it is sufficient to train on one of these masses. For the full NMSSM analysis, 68 trainings were used. Whether this can be done in a smarter way, using only one training is an interesting point of study. The answer is probably yes. 


After running the script, a folder should be created in `output/ml/...`, containing json files of the form `fold*_lwtnn.json`. This contain the full description of the neural network function (all weights and biases), and are used to apply the model on the data. 

The parameters of the trainings are set in the template files, found by 
```
ls ml/templates/*training*.yaml
```
The important parameters you can also play around with are
```yaml
model:
  eventsPerClassAndBatch: 30 # how many events per batch are used before weights are updated
  early_stopping: 50 # after how many epochs is the training considered converged
  epochs: 100000 # Max number of epochs (is never reached)
  name: smhtt_dropout_tanh # NN layout, defined in htt-ml/training/keras_models.py
  save_best_only: true # saves best only
  steps_per_epoch: 100 # After how many weight updates is the model compared to the validation sample
```
Furthermore, the variables that were used to train on are defined as
```
- pt_1 : pT of first tau decay product (electron, muon oder had. tau for et, mt tt)
- pt_2 : pT of second (had. tau in all final states)
- m_vis : invariant visible di-tau mass
- ptvis : visible di-tau pT
- m_sv_puppi : SVFit di-tau mass (consideres also neutrinos / MET)
- nbtag : Number of b-jets
- jpt_1 : pT of pT-leading jet
- njets :  Number of non-b-jets
- jdeta : Difference in eta between two non-b-jets 
- mjj : Invariant mass of two non-b-jets
- dijetpt : pT of two non-b-jets
- bpt_bReg_1 : pT of leading b-jet
- bpt_bReg_2 : pT of subleading b-jet
- bm_bReg_1 : mass of leading b-jet
- bm_bReg_2 : mass of subleading b-jet
- bcsv_1 : B-jet discriminator score of leading b-jet
- bcsv_2 : B-jet discriminator score of subleadig b-jet
- jpt_2 : pT of subleading non-b-jet
- mbb_highCSV_bReg : Invariant mass of two b-jets 
- pt_bb_highCSV_bReg : pT of two b-jets
- m_ttvisbb_highCSV_bReg : Invariant mass of two b-jets plus visible taus
- kinfit_mH : bb+tautau mass (including neutrinos / MET using kinematic fit)
- kinfit_mh2 : bb mass used for the fit
- kinfit_chi2 : quality of the fit 
- highCSVjetUsedFordiBJetSystemCSV : B-jet discriminator score of non-b-jet jet with highest of such scores
```




## 5. Apply ML model
First of all we need to update the datasets.json file via:
```bash
cp -r /work/rschmieder/friendtree_producer/CMSSW_10_2_14/src/HiggsAnalysis/friend-tree-producer/data/input_params/datasets.json PATH_TO_YOUR_FRIENDTREE_PRODUCER/CMSSW_10_2_14/src/HiggsAnalysis/friend-tree-producer/data/input_params/datasets.json
```
To apply it we use the friend tree producer from step 2, and run e.g. the command
```bash
job_management.py --command submit --executable NNScore --custom_workdir_path /ceph/${USER}/nmssm/temp  --input_ntuples_directory /ceph/jbechtel/nmssm/ntuples/2016/tt/   --batch_cluster etp7 --events_per_job 20000 --cores 24 --restrict_to_channels tt  --friend_ntuples_directories /ceph/jbechtel/nmssm/ntuples/2016/tt/FakeFactors_nmssm/ /ceph/jbechtel/nmssm/ntuples/2016/tt/HHKinFit/ /ceph/jbechtel/nmssm/ntuples/2016/tt/SVFit/  --conditional --extra-parameters "--lwtnn_config /PATH/TO/ML/OUTPUT/FOLDER/"
```
Compared to the command of step 2, now also the options `--friend_ntuples_directories` (friend trees of step 2), `--conditional` (if all eras are used, remove flag if only 2016,2017 or 2018 is used) and `--extra-parameters "--lwtnn_config ..."` (with the path to the output folder of the training) need to be set.

After creating these friend trees, they can be added to the `utils/setup_samples.sh` and the full information of the NN response to each event is available.

## 6. Produce analysis histograms (shapes)
Before cloning the new analysis framework start the ssh agent:
```bash
eval $(ssh-agent)
ssh-add
```
Àfterwards checkout the new analysis framework:
```bash
git clone --recursive git@github.com:KIT-CMS/NMSSM_analysis.git
cd NMSSM_analysis
git submodule init
git submodule update
```

Now you are ready to produce shapes. This can be done locally or on the cluster. A local production of analysis shapes is not recommended, since signal processes  and also systematic variations need to be processed. The relevant file for the shape production is ```shapes/produce_shapes.py```. Consider all arguments of this file. For producting control shapes, enable the arguments ```--control-plots```, ```--skip-systematic-variations``` and depending on the quantities (see all possibilities in the variables list) you want to plot ```--control-plot-set pt_1,pt_2```. Local execution:
1. setup the environment
```bash
source utils/setup_root.sh
```
2. For producing control shapes for ```pt1, pt2``` an example command is:
```bash
python shapes/produce_shapes.py --channels mt --output-file output/parametrized_nn_mH1000/2016-mt --directory /ceph/jbechtel/nmssm/ntuples/2018/mt/ --mt-friend-directory /ceph/rschmieder/nmssm/friends/2018/mt/SVFit/ /ceph/rschmieder/nmssm/friends/2018/mt/FakeFactors_nmssm/ /ceph/rschmieder/nmssm/friends/2018/mt/HHKinFit/ /ceph/rschmieder/nmssm/friends/2018/mt/NNScore_train_all/parametrized_nn_mH1000/NNScore_workdir/NNScore_collected/ --era 2018 --num-processes 4 --num-threads 3 --optimization-level 1 --process-selection emb,data --control-plots --control-plot-set pt_1,pt_2 --skip-systematic-variations --NN_config /work/rschmieder/nmssm/nmssm_condor_analysis/sm-htt-analysis/output/ml/parametrized_nn_mH1000/all_eras_mt/dataset_config.yaml
```
3. For plotting the control shapes use the script ```plotting/plot_shapes_control.py``` with the according arguments.

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
