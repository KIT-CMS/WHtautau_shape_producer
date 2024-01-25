import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--era", help="Experiment era.")
    parser.add_argument("--global_path_ww", help="path to WW datacards")
    parser.add_argument("--global_path_tt", help="path to TT datacards")
    parser.add_argument("--output", help="path to the output datacard")
    parser.add_argument("--scaleWW", action="store_true", help="use WW datacards with signal scaled by 10")
    return parser.parse_args()

def main(args):
    global_ww = args.global_path_ww
    global_tt = args.global_path_tt

    # suffix_loose_bVeto         = "_DYflip_loose_bVeto"
    # suffix_WH3l_old_wz_scaling = "_old_wz_scaling"

    var_WHSS = 'BDTG6_TT_100_bins'
    var_SSSF = 'BDT_WH3l_SSSF_new_v9_more'
    var_OSSF = 'BDT_WH3l_OSSF_new_v9_more'

    # ---------
    # Full 2018
    # ---------
    print(global_ww)
    # 2018 datacards WW
    WHSS_2018_high_pt = "WH_SS_em_1j_minus_2018={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2ge20/{var}/datacard.txt         \
                        WH_SS_em_1j_plus_2018={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2ge20/{var}/datacard.txt           \
                        WH_SS_mm_1j_minus_2018={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2ge20/{var}/datacard.txt \
                        WH_SS_mm_1j_plus_2018={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2ge20/{var}/datacard.txt   \
                        WH_SS_ee_1j_minus_2018={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2ge20/{var}/datacard.txt         \
                        WH_SS_ee_1j_plus_2018={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2ge20/{var}/datacard.txt           \
                        WH_SS_em_2j_minus_2018={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2ge20/{var}/datacard.txt         \
                        WH_SS_em_2j_plus_2018={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2ge20/{var}/datacard.txt           \
                        WH_SS_mm_2j_minus_2018={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2ge20/{var}/datacard.txt \
                        WH_SS_mm_2j_plus_2018={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2ge20/{var}/datacard.txt   \
                        WH_SS_ee_2j_minus_2018={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2ge20/{var}/datacard.txt         \
                        WH_SS_ee_2j_plus_2018={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2ge20/{var}/datacard.txt     \
                        WH_SS_WZ_1j_2018={glob_ww}/Full2018/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_1j/events/datacard.txt                             \
                        WH_SS_WZ_2j_2018={glob_ww}/Full2018/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_2j/events/datacard.txt                             \
                        ".format(var=var_WHSS,glob_ww=global_ww)

    WHSS_2018_low_pt = "WH_SS_em_1j_minus_2018_low_pt={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2lt20/{var}/datacard.txt         \
                        WH_SS_em_1j_plus_2018_low_pt={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2lt20/{var}/datacard.txt           \
                        WH_SS_mm_1j_minus_2018_low_pt={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2lt20/{var}/datacard.txt \
                        WH_SS_mm_1j_plus_2018_low_pt={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2lt20/{var}/datacard.txt   \
                        WH_SS_ee_1j_minus_2018_low_pt={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2lt20/{var}/datacard.txt         \
                        WH_SS_ee_1j_plus_2018_low_pt={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2lt20/{var}/datacard.txt           \
                        WH_SS_em_2j_minus_2018_low_pt={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2lt20/{var}/datacard.txt         \
                        WH_SS_em_2j_plus_2018_low_pt={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2lt20/{var}/datacard.txt           \
                        WH_SS_mm_2j_minus_2018_low_pt={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2lt20/{var}/datacard.txt \
                        WH_SS_mm_2j_plus_2018_low_pt={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2lt20/{var}/datacard.txt   \
                        WH_SS_ee_2j_minus_2018_low_pt={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2lt20/{var}/datacard.txt         \
                        WH_SS_ee_2j_plus_2018_low_pt={glob_ww}/Full2018/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2lt20/{var}/datacard.txt           \
                        ".format(var=var_WHSS, glob_ww=global_ww)

    WH3l_2018 = "WH_3l_sssf_plus_2018={glob_ww}/Full2018/WH3l/datacards_original_signal_scale_opt/wh3l_13TeV_sssf_plus_pt2ge20/{var_ss}/datacard.txt   \
                WH_3l_sssf_minus_2018={glob_ww}/Full2018/WH3l/datacards_original_signal_scale_opt/wh3l_13TeV_sssf_minus_pt2ge20/{var_ss}/datacard.txt \
                WH_3l_ossf_plus_2018={glob_ww}/Full2018/WH3l/datacards_original_signal_scale_opt/wh3l_13TeV_ossf_plus_pt2ge20/{var_os}/datacard.txt   \
                WH_3l_ossf_minus_2018={glob_ww}/Full2018/WH3l/datacards_original_signal_scale_opt/wh3l_13TeV_ossf_minus_pt2ge20/{var_os}/datacard.txt                \
                WH_3l_WZ_CR_0j_2018={glob_ww}/Full2018/WH3l/datacards_original_signal_scale/wh3l_wz_13TeV/events/datacard.txt                    \
                ".format(var_ss=var_SSSF,var_os=var_OSSF,glob_ww=global_ww)
    
    # 2018 datacards tau tau

    EMT_2018 = "emt_1_2018={glob_tt}/2018_emt/emt/htt_emt_1_2018.txt \
                emt_2_2018={glob_tt}/2018_emt/emt/htt_emt_2_2018.txt \
                emt_3_2018={glob_tt}/2018_emt/emt/htt_emt_3_2018.txt \
                emt_4_2018={glob_tt}/2018_emt/emt/htt_emt_4_2018.txt    ".format(glob_tt=global_tt)

    MMT_2018 = "mmt_1_2018={glob_tt}/2018_mmt/mmt/htt_mmt_1_2018.txt \
                mmt_2_2018={glob_tt}/2018_mmt/mmt/htt_mmt_2_2018.txt \
                mmt_3_2018={glob_tt}/2018_mmt/mmt/htt_mmt_3_2018.txt \
                mmt_4_2018={glob_tt}/2018_mmt/mmt/htt_mmt_4_2018.txt     ".format(glob_tt=global_tt)
    
    MTT_2018 = "mtt_1_2018={glob_tt}/2018_mtt/mtt/htt_mtt_1_2018.txt \
                mtt_2_2018={glob_tt}/2018_mtt/mtt/htt_mtt_2_2018.txt \
                mtt_3_2018={glob_tt}/2018_mtt/mtt/htt_mtt_3_2018.txt \
                mtt_4_2018={glob_tt}/2018_mtt/mtt/htt_mtt_4_2018.txt    ".format(glob_tt=global_tt)
    
    ETT_2018 = "ett_1_2018={glob_tt}/2018_ett/ett/htt_ett_1_2018.txt \
                ett_2_2018={glob_tt}/2018_ett/ett/htt_ett_2_2018.txt \
                ett_3_2018={glob_tt}/2018_ett/ett/htt_ett_3_2018.txt \
                ett_4_2018={glob_tt}/2018_ett/ett/htt_ett_4_2018.txt    ".format(glob_tt=global_tt)
    

    # ---------
    # Full 2017
    # ---------

    # 2017 datacards
    WHSS_2017_high_pt = "WH_SS_em_1j_minus_2017={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2ge20/{var}/datacard.txt         \
                        WH_SS_em_1j_plus_2017={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2ge20/{var}/datacard.txt           \
                        WH_SS_mm_1j_minus_2017={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2ge20/{var}/datacard.txt \
                        WH_SS_mm_1j_plus_2017={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2ge20/{var}/datacard.txt   \
                        WH_SS_ee_1j_minus_2017={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2ge20/{var}/datacard.txt         \
                        WH_SS_ee_1j_plus_2017={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2ge20/{var}/datacard.txt           \
                        WH_SS_em_2j_minus_2017={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2ge20/{var}/datacard.txt         \
                        WH_SS_em_2j_plus_2017={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2ge20/{var}/datacard.txt           \
                        WH_SS_mm_2j_minus_2017={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2ge20/{var}/datacard.txt \
                        WH_SS_mm_2j_plus_2017={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2ge20/{var}/datacard.txt   \
                        WH_SS_ee_2j_minus_2017={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2ge20/{var}/datacard.txt         \
                        WH_SS_ee_2j_plus_2017={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2ge20/{var}/datacard.txt   \
                        WH_SS_WZ_1j_2017={glob_ww}/Full2017/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_1j/events/datacard.txt                            \
                        WH_SS_WZ_2j_2017={glob_ww}/Full2017/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_2j/events/datacard.txt                             \
                        ".format(var=var_WHSS,glob_ww=global_ww)

    WHSS_2017_low_pt = "WH_SS_em_1j_minus_2017_low_pt={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2lt20/{var}/datacard.txt         \
                        WH_SS_em_1j_plus_2017_low_pt={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2lt20/{var}/datacard.txt           \
                        WH_SS_mm_1j_minus_2017_low_pt={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2lt20/{var}/datacard.txt \
                        WH_SS_mm_1j_plus_2017_low_pt={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2lt20/{var}/datacard.txt   \
                        WH_SS_ee_1j_minus_2017_low_pt={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2lt20/{var}/datacard.txt         \
                        WH_SS_ee_1j_plus_2017_low_pt={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2lt20/{var}/datacard.txt           \
                        WH_SS_em_2j_minus_2017_low_pt={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2lt20/{var}/datacard.txt         \
                        WH_SS_em_2j_plus_2017_low_pt={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2lt20/{var}/datacard.txt           \
                        WH_SS_mm_2j_minus_2017_low_pt={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2lt20/{var}/datacard.txt \
                        WH_SS_mm_2j_plus_2017_low_pt={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2lt20/{var}/datacard.txt   \
                        WH_SS_ee_2j_minus_2017_low_pt={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2lt20/{var}/datacard.txt         \
                        WH_SS_ee_2j_plus_2017_low_pt={glob_ww}/Full2017/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2lt20/{var}/datacard.txt           \
                        ".format(var=var_WHSS,glob_ww=global_ww)

    WH3l_2017 = "WH_3l_sssf_plus_2017={glob_ww}/Full2017/WH3l/datacards_original_signal_scale_opt/wh3l_13TeV_sssf_plus_pt2ge20/{var_ss}/datacard.txt   \
                WH_3l_sssf_minus_2017={glob_ww}/Full2017/WH3l/datacards_original_signal_scale_opt/wh3l_13TeV_sssf_minus_pt2ge20/{var_ss}/datacard.txt \
                WH_3l_ossf_plus_2017={glob_ww}/Full2017/WH3l/datacards_original_signal_scale_opt/wh3l_13TeV_ossf_plus_pt2ge20/{var_os}/datacard.txt   \
                WH_3l_ossf_minus_2017={glob_ww}/Full2017/WH3l/datacards_original_signal_scale_opt/wh3l_13TeV_ossf_minus_pt2ge20/{var_os}/datacard.txt  \
                WH_3l_WZ_CR_0j_2017={glob_ww}/Full2017/WH3l/datacards_original_signal_scale/wh3l_wz_13TeV/events/datacard.txt                    \
                ".format(var_ss=var_SSSF,var_os=var_OSSF,glob_ww=global_ww)
    
    # 2017 datacards tau tau

    EMT_2017 = "emt_1_2017={glob_tt}/2017_emt/emt/htt_emt_1_2017.txt \
                emt_2_2017={glob_tt}/2017_emt/emt/htt_emt_2_2017.txt \
                emt_3_2017={glob_tt}/2017_emt/emt/htt_emt_3_2017.txt \
                emt_4_2017={glob_tt}/2017_emt/emt/htt_emt_4_2017.txt    ".format(glob_tt=global_tt)

    MMT_2017 = "mmt_1_2017={glob_tt}/2017_mmt/mmt/htt_mmt_1_2017.txt \
                mmt_2_2017={glob_tt}/2017_mmt/mmt/htt_mmt_2_2017.txt \
                mmt_3_2017={glob_tt}/2017_mmt/mmt/htt_mmt_3_2017.txt \
                mmt_4_2017={glob_tt}/2017_mmt/mmt/htt_mmt_4_2017.txt    ".format(glob_tt=global_tt)
    
    MTT_2017 = "mtt_1_2017={glob_tt}/2017_mtt/mtt/htt_mtt_1_2017.txt \
                mtt_2_2017={glob_tt}/2017_mtt/mtt/htt_mtt_2_2017.txt \
                mtt_3_2017={glob_tt}/2017_mtt/mtt/htt_mtt_3_2017.txt \
                mtt_4_2017={glob_tt}/2017_mtt/mtt/htt_mtt_4_2017.txt    ".format(glob_tt=global_tt)
    
    ETT_2017 = "ett_1_2017={glob_tt}/2017_ett/ett/htt_ett_1_2017.txt \
                ett_2_2017={glob_tt}/2017_ett/ett/htt_ett_2_2017.txt \
                ett_3_2017={glob_tt}/2017_ett/ett/htt_ett_3_2017.txt \
                ett_4_2017={glob_tt}/2017_ett/ett/htt_ett_4_2017.txt    ".format(glob_tt=global_tt)
    

    # ------------
    # 2016 no HIPM
    # ------------

    # 2016noHIPM datacards

    WHSS_2016noHIPM_high_pt = "WH_SS_em_1j_minus_2016noHIPM={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2ge20/{var}/datacard.txt         \
                            WH_SS_em_1j_plus_2016noHIPM={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2ge20/{var}/datacard.txt           \
                            WH_SS_mm_1j_minus_2016noHIPM={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2ge20/{var}/datacard.txt \
                            WH_SS_mm_1j_plus_2016noHIPM={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2ge20/{var}/datacard.txt   \
                            WH_SS_ee_1j_minus_2016noHIPM={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2ge20/{var}/datacard.txt         \
                            WH_SS_ee_1j_plus_2016noHIPM={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2ge20/{var}/datacard.txt           \
                            WH_SS_em_2j_minus_2016noHIPM={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2ge20/{var}/datacard.txt         \
                            WH_SS_em_2j_plus_2016noHIPM={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2ge20/{var}/datacard.txt           \
                            WH_SS_mm_2j_minus_2016noHIPM={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2ge20/{var}/datacard.txt \
                            WH_SS_mm_2j_plus_2016noHIPM={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2ge20/{var}/datacard.txt   \
                            WH_SS_ee_2j_minus_2016noHIPM={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2ge20/{var}/datacard.txt         \
                            WH_SS_ee_2j_plus_2016noHIPM={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2ge20/{var}/datacard.txt   \
                            WH_SS_WZ_1j_2016noHIPM={glob_ww}/2016noHIPM/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_1j/events/datacard.txt                             \
                            WH_SS_WZ_2j_2016noHIPM={glob_ww}/2016noHIPM/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_2j/events/datacard.txt                             \
                            ".format(var=var_WHSS,glob_ww=global_ww)


    WHSS_2016noHIPM_low_pt = "WH_SS_em_1j_minus_2016noHIPM_low_pt={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2lt20/{var}/datacard.txt         \
                            WH_SS_em_1j_plus_2016noHIPM_low_pt={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2lt20/{var}/datacard.txt           \
                            WH_SS_mm_1j_minus_2016noHIPM_low_pt={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2lt20/{var}/datacard.txt \
                            WH_SS_mm_1j_plus_2016noHIPM_low_pt={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2lt20/{var}/datacard.txt   \
                            WH_SS_ee_1j_minus_2016noHIPM_low_pt={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2lt20/{var}/datacard.txt         \
                            WH_SS_ee_1j_plus_2016noHIPM_low_pt={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2lt20/{var}/datacard.txt           \
                            WH_SS_em_2j_minus_2016noHIPM_low_pt={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2lt20/{var}/datacard.txt         \
                            WH_SS_em_2j_plus_2016noHIPM_low_pt={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2lt20/{var}/datacard.txt           \
                            WH_SS_mm_2j_minus_2016noHIPM_low_pt={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2lt20/{var}/datacard.txt \
                            WH_SS_mm_2j_plus_2016noHIPM_low_pt={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2lt20/{var}/datacard.txt   \
                            WH_SS_ee_2j_minus_2016noHIPM_low_pt={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2lt20/{var}/datacard.txt         \
                            WH_SS_ee_2j_plus_2016noHIPM_low_pt={glob_ww}/2016noHIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2lt20/{var}/datacard.txt           \
                            ".format(var=var_WHSS,glob_ww=global_ww)

    WH3l_2016noHIPM = "WH_3l_sssf_plus_2016noHIPM={glob_ww}/2016noHIPM/WH3l/datacards_original_signal_scale_opt/wh3l_13TeV_sssf_plus_pt2ge20/{var_ss}/datacard.txt   \
                    WH_3l_sssf_minus_2016noHIPM={glob_ww}/2016noHIPM/WH3l/datacards_original_signal_scale_opt/wh3l_13TeV_sssf_minus_pt2ge20/{var_ss}/datacard.txt \
                    WH_3l_ossf_plus_2016noHIPM={glob_ww}/2016noHIPM/WH3l/datacards_original_signal_scale_opt/wh3l_13TeV_ossf_plus_pt2ge20/{var_os}/datacard.txt   \
                    WH_3l_ossf_minus_2016noHIPM={glob_ww}/2016noHIPM/WH3l/datacards_original_signal_scale_opt/wh3l_13TeV_ossf_minus_pt2ge20/{var_os}/datacard.txt \
                    WH_3l_WZ_CR_0j_2016noHIPM={glob_ww}/2016noHIPM/WH3l/datacards_original_signal_scale/wh3l_wz_13TeV/events/datacard.txt                    \
                    ".format(var_ss=var_SSSF,var_os=var_OSSF,glob_ww=global_ww)
    
    # 2016postVFP datacards tau tau

    EMT_2016postVFP = "emt_1_2016postVFP={glob_tt}/2016postVFP_emt/emt/htt_emt_1_2016postVFP.txt \
                emt_2_2016postVFP={glob_tt}/2016postVFP_emt/emt/htt_emt_2_2016postVFP.txt   ".format(glob_tt=global_tt)

    MMT_2016postVFP = "mmt_1_2016postVFP={glob_tt}/2016postVFP_mmt/mmt/htt_mmt_1_2016postVFP.txt \
                mmt_2_2016postVFP={glob_tt}/2016postVFP_mmt/mmt/htt_mmt_2_2016postVFP.txt   ".format(glob_tt=global_tt)
    
    MTT_2016postVFP = "mtt_1_2016postVFP={glob_tt}/2016postVFP_mtt/mtt/htt_mtt_1_2016postVFP.txt \
                mtt_2_2016postVFP={glob_tt}/2016postVFP_mtt/mtt/htt_mtt_2_2016postVFP.txt   ".format(glob_tt=global_tt)
    
    ETT_2016postVFP = "ett_1_2016postVFP={glob_tt}/2016postVFP_ett/ett/htt_ett_1_2016postVFP.txt \
                ett_2_2016postVFP={glob_tt}/2016postVFP_ett/ett/htt_ett_2_2016postVFP.txt   ".format(glob_tt=global_tt)
    

    # ---------
    # 2016 HIPM
    # ---------

    # 2016HIPM datacards

    WHSS_2016HIPM_high_pt = "WH_SS_em_1j_minus_2016HIPM={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2ge20/{var}/datacard.txt         \
                            WH_SS_em_1j_plus_2016HIPM={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2ge20/{var}/datacard.txt           \
                            WH_SS_mm_1j_minus_2016HIPM={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2ge20/{var}/datacard.txt \
                            WH_SS_mm_1j_plus_2016HIPM={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2ge20/{var}/datacard.txt   \
                            WH_SS_ee_1j_minus_2016HIPM={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2ge20/{var}/datacard.txt         \
                            WH_SS_ee_1j_plus_2016HIPM={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2ge20/{var}/datacard.txt           \
                            WH_SS_em_2j_minus_2016HIPM={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2ge20/{var}/datacard.txt         \
                            WH_SS_em_2j_plus_2016HIPM={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2ge20/{var}/datacard.txt           \
                            WH_SS_mm_2j_minus_2016HIPM={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2ge20/{var}/datacard.txt \
                            WH_SS_mm_2j_plus_2016HIPM={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2ge20/{var}/datacard.txt   \
                            WH_SS_ee_2j_minus_2016HIPM={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2ge20/{var}/datacard.txt         \
                            WH_SS_ee_2j_plus_2016HIPM={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2ge20/{var}/datacard.txt   \
                            WH_SS_WZ_1j_2016HIPM={glob_ww}/2016HIPM/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_1j/events/datacard.txt                                     \
                            WH_SS_WZ_2j_2016HIPM={glob_ww}/2016HIPM/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_2j/events/datacard.txt  \
                            ".format(var=var_WHSS,glob_ww=global_ww)

    WHSS_2016HIPM_low_pt = "WH_SS_em_1j_minus_2016HIPM_low_pt={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2lt20/{var}/datacard.txt         \
                            WH_SS_em_1j_plus_2016HIPM_low_pt={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2lt20/{var}/datacard.txt           \
                            WH_SS_mm_1j_minus_2016HIPM_low_pt={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2lt20/{var}/datacard.txt \
                            WH_SS_mm_1j_plus_2016HIPM_low_pt={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2lt20/{var}/datacard.txt   \
                            WH_SS_ee_1j_minus_2016HIPM_low_pt={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2lt20/{var}/datacard.txt         \
                            WH_SS_ee_1j_plus_2016HIPM_low_pt={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2lt20/{var}/datacard.txt           \
                            WH_SS_em_2j_minus_2016HIPM_low_pt={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2lt20/{var}/datacard.txt         \
                            WH_SS_em_2j_plus_2016HIPM_low_pt={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2lt20/{var}/datacard.txt           \
                            WH_SS_mm_2j_minus_2016HIPM_low_pt={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2lt20/{var}/datacard.txt \
                            WH_SS_mm_2j_plus_2016HIPM_low_pt={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2lt20/{var}/datacard.txt   \
                            WH_SS_ee_2j_minus_2016HIPM_low_pt={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2lt20/{var}/datacard.txt         \
                            WH_SS_ee_2j_plus_2016HIPM_low_pt={glob_ww}/2016HIPM/WHSS/datacards_DYflip_original_signal_scale_opt/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2lt20/{var}/datacard.txt           \
                            ".format(var=var_WHSS,glob_ww=global_ww)

    WH3l_2016HIPM = "WH_3l_sssf_plus_2016HIPM={glob_ww}/2016HIPM/WH3l/datacards_original_signal_scale_opt/wh3l_13TeV_sssf_plus_pt2ge20/{var_ss}/datacard.txt   \
                    WH_3l_sssf_minus_2016HIPM={glob_ww}/2016HIPM/WH3l/datacards_original_signal_scale_opt/wh3l_13TeV_sssf_minus_pt2ge20/{var_ss}/datacard.txt \
                    WH_3l_ossf_plus_2016HIPM={glob_ww}/2016HIPM/WH3l/datacards_original_signal_scale_opt/wh3l_13TeV_ossf_plus_pt2ge20/{var_os}/datacard.txt   \
                    WH_3l_ossf_minus_2016HIPM={glob_ww}/2016HIPM/WH3l/datacards_original_signal_scale_opt/wh3l_13TeV_ossf_minus_pt2ge20/{var_os}/datacard.txt \
                    WH_3l_WZ_CR_0j_2016HIPM={glob_ww}/2016HIPM/WH3l/datacards_original_signal_scale/wh3l_wz_13TeV/events/datacard.txt                    \
                    ".format(var_ss=var_SSSF,var_os=var_OSSF,glob_ww=global_ww)
    
    # 2016preVFP datacards tau tau

    EMT_2016preVFP = "emt_1_2016preVFP={glob_tt}/2016preVFP_emt/emt/htt_emt_1_2016preVFP.txt \
                emt_2_2016preVFP={glob_tt}/2016preVFP_emt/emt/htt_emt_2_2016preVFP.txt  ".format(glob_tt=global_tt)

    MMT_2016preVFP = "mmt_1_2016preVFP={glob_tt}/2016preVFP_mmt/mmt/htt_mmt_1_2016preVFP.txt \
                mmt_2_2016preVFP={glob_tt}/2016preVFP_mmt/mmt/htt_mmt_2_2016preVFP.txt  ".format(glob_tt=global_tt)
    
    MTT_2016preVFP = "mtt_1_2016preVFP={glob_tt}/2016preVFP_mtt/mtt/htt_mtt_1_2016preVFP.txt \
                mtt_2_2016preVFP={glob_tt}/2016preVFP_mtt/mtt/htt_mtt_2_2016preVFP.txt  ".format(glob_tt=global_tt)
    
    ETT_2016preVFP = "ett_1_2016preVFP={glob_tt}/2016preVFP_ett/ett/htt_ett_1_2016preVFP.txt \
                ett_2_2016preVFP={glob_tt}/2016preVFP_ett/ett/htt_ett_2_2016preVFP.txt  ".format(glob_tt=global_tt)

    # Here we define the actual combine commands we want to use
    os.system("mkdir -p Combination")

    tmp_command = "combineCards.py "

    
    
    output_name_suffix = "_100_bins_original_signal_scale"
    print("run2")
    combine_command_FullRun2 = tmp_command + WHSS_2018_high_pt       + WHSS_2018_low_pt       + WH3l_2018 \
                                        + WHSS_2017_high_pt       + WHSS_2017_low_pt       + WH3l_2017 \
                                        + WHSS_2016noHIPM_high_pt + WHSS_2016noHIPM_low_pt + WH3l_2016noHIPM \
                                        + WHSS_2016HIPM_high_pt   + WHSS_2016HIPM_low_pt   + WH3l_2016HIPM \
                                        + EMT_2018 + EMT_2017 + EMT_2016postVFP + EMT_2016preVFP \
                                        + MMT_2018 + MMT_2017 + MMT_2016postVFP + MMT_2016preVFP \
                                        + MTT_2018 + MTT_2017 + MTT_2016postVFP + MTT_2016preVFP \
                                        + ETT_2018 + ETT_2017 + ETT_2016postVFP + ETT_2016preVFP \
                                         + " > Combination/WH_chargeAsymmetry_WH_FullRun2{0}.txt".format(output_name_suffix)
                                        
    print(combine_command_FullRun2)
    os.system(combine_command_FullRun2)
    print("run2 exe")
    print("")
    print("")
    print("")

    # WHSS and WH3l Full 2018
    combine_command_Full2018 = tmp_command + WHSS_2018_high_pt + WHSS_2018_low_pt + WH3l_2018 + EMT_2018 + MMT_2018 + MTT_2018 + ETT_2018 + " > Combination/WH_chargeAsymmetry_WH_Full2018{0}.txt".format(output_name_suffix)
    #print(combine_command_Full2018)
    os.system(combine_command_Full2018)
    print("")
    print("")
    print("")

    # WHSS and WH3l Full 2017
    combine_command_Full2017 = tmp_command + WHSS_2017_high_pt + WHSS_2017_low_pt + WH3l_2017 + EMT_2017 + MMT_2017 + MTT_2017 + ETT_2017 + " > Combination/WH_chargeAsymmetry_WH_Full2017{0}.txt".format(output_name_suffix)
    #print(combine_command_Full2017)
    os.system(combine_command_Full2017)
    print("")
    print("")
    print("")

    # WHSS and WH3l 2016noHIPM
    combine_command_2016noHIPM = tmp_command + WHSS_2016noHIPM_high_pt + WHSS_2016noHIPM_low_pt + WH3l_2016noHIPM + EMT_2016postVFP + MMT_2016postVFP + MTT_2016postVFP + ETT_2016postVFP + " > Combination/WH_chargeAsymmetry_WH_2016noHIPM{0}.txt".format(output_name_suffix)
    #print(combine_command_2016noHIPM)
    os.system(combine_command_2016noHIPM)
    print("")
    print("")
    print("")

    # WHSS and WH3l 2016HIPM
    combine_command_2016HIPM = tmp_command + WHSS_2016HIPM_high_pt + WHSS_2016HIPM_low_pt + WH3l_2016HIPM + EMT_2016preVFP + MMT_2016preVFP + MTT_2016preVFP + ETT_2016preVFP + " > Combination/WH_chargeAsymmetry_WH_2016HIPM{0}.txt".format(output_name_suffix)
    #print(combine_command_2016HIPM)
    os.system(combine_command_2016HIPM)
    print("")
    print("")
    print("")

if __name__ == "__main__":
    args = parse_args()
    main(args)