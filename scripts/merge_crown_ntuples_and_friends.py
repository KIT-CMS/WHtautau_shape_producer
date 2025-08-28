#!/usr/bin/env python3

import argparse
import os
import uproot
import ROOT as r
import pandas as pd
from natsort import natsorted
import logging
import datetime
from concurrent.futures import ProcessPoolExecutor
from queue import Queue

def parse_args():
    parser = argparse.ArgumentParser(description="Merge CROWN ntuples and friends.")
    parser.add_argument("--main_directory", required=True, help="Main directory containing ntuples and friends.")
    parser.add_argument("--filelist", required=True, help="File containing list of ROOT files.")
    parser.add_argument("--tree", required=True, help="Name of the tree to process.")
    parser.add_argument("--allowed_friends", nargs='*', help="List of allowed friend trees.")
    parser.add_argument("--n_threads", type=int, default=4, help="Number of parallel threads to be used for merging.")
    parser.add_argument("--logfile", type=str, default="logfile_merge.txt", help="Path to the logfile used by this script.")
    parser.add_argument("--remote_server", type=str, default="", help="Remote XRootD server URL to prepend to file paths.")
    parser.add_argument("--run_nevents_check", action="store_true", help="Run a check to ensure the number of events is consistent across filetypes.")
    return parser.parse_args()

def is_subpath(path, base):
    try:
        common_path = os.path.commonpath([path, base])
        return common_path == base
    except ValueError:
        return False

def get_files(filelist):
    with open(filelist, "r") as f:
        return natsorted([l.strip().split()[0] for l in f.readlines()])

def determine_job_from_file(f, main_ntuples_directory, friends_directory):
    if is_subpath(f, main_ntuples_directory):
        rel_file_path = os.path.relpath(f, main_ntuples_directory)
        job_dir, file_name = os.path.split(rel_file_path)
        return job_dir, "ntuples", f
    elif is_subpath(f, friends_directory):
        rel_file_path = os.path.relpath(f, friends_directory)
        friend_dir, file_name = os.path.split(rel_file_path)
        friend, job_dir = friend_dir.split("/", 1)
        return job_dir, friend, f
    else:
        return "UNKNOWN", "UNKNOWN", f

def check_event_consistency_across_filetypes(job_dict, tree, remote_server):
    logger = logging.getLogger()
    consistency_dict = {}
    for filetype, job_files in job_dict.items():
        consistency_dict[filetype] = 0
        for fname in job_files:
            if remote_server:
                fname = remote_server.rstrip('/') + '//' + fname.lstrip('/')
            logger.info(f"Main: Checking file {fname}")
            try:
                checkfile = r.TFile.Open(fname)
                checktree = checkfile.Get(tree)
                consistency_dict[filetype] += checktree.GetEntries()
                checkfile.Close()
            except Exception as e:
                logger.warning(f"Main: File {fname} does not contain the specified tree {tree} or is empty.")
                continue
    
    if len(set(consistency_dict.values())) != 1:
        print(f"Error: Inconsistent number of entries in files {f}")
        for filetype, entries in consistency_dict.items():
            print(f"\t{filetype}: {entries}")
        return False
    logger.info(f"Main: Found {set(consistency_dict.values()).pop()} consistent events")
    return True

def merge_ntuples(job, job_dict, tree, worker_id, remote_server):
    logger = logging.getLogger(f"worker_{worker_id}")
    logger.info(f"Worker {worker_id}: Starting merging process for job {job}")
    df_dict = {}
    output_file_name = job.replace("/", "_") + "_merged.root"
    for filetype, files in job_dict.items():
        logger.info(f"Worker {worker_id}: Merging {filetype} files for job {job}")
        if filetype not in df_dict:
            df_dict[filetype] = pd.DataFrame()
        for fname in files:
            if remote_server:
                fname = remote_server.rstrip('/') + '//' + fname.lstrip('/')
            logger.info(f"Worker {worker_id}: Merging file {fname}")
            try:
                with uproot.open(fname) as f:
                    if tree not in f:
                        logger.warning(f"Worker {worker_id}: File {fname} does not contain the specified tree {tree} or is empty.")
                        continue
                    t = f[tree]
                    df = t.arrays(library="pd")
                    df_dict[filetype] = pd.concat([df_dict[filetype], df])
            except Exception as e:
                logger.warning(f"Worker {worker_id}: Failed to open file {fname} with error: {e}")
                continue
    logger.info(f"Worker {worker_id}: Merging {job} DataFrames")
    merged_df = pd.concat(df_dict.values(), axis=1)

    # Write the merged DataFrame to a new ROOT file using uproot
    logger.info(f"Worker {worker_id}: Writing merged file for job {job}")
    with uproot.recreate(output_file_name) as f:
        f[tree] = merged_df

    logger.info(f"Worker {worker_id}: Merged file created for job {job}")

def main():
    args = parse_args()

    logging.getLogger("asyncio").setLevel(logging.NOTSET)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    infofile_handler = logging.FileHandler(
        filename=f"_{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}".join(
            os.path.splitext(args.logfile)
        )
    )
    infofile_handler.setFormatter(formatter)
    infofile_handler.setLevel(logging.INFO)

    logger.addHandler(stream_handler)
    logger.addHandler(infofile_handler)

    main_ntuples_directory = os.path.join(args.main_directory, "CROWNRun")
    friends_directory = os.path.join(args.main_directory, "CROWNFriends")

    flist = get_files(args.filelist)

    merge_jobs_dict = {}
    for f in flist:
        job, filetype, file_path = determine_job_from_file(f, main_ntuples_directory, friends_directory)
        if job not in merge_jobs_dict:
            merge_jobs_dict[job] = {}
        
        if filetype == "ntuples" or filetype in args.allowed_friends:
            if filetype not in merge_jobs_dict[job]:
                merge_jobs_dict[job][filetype] = []
            merge_jobs_dict[job][filetype].append(file_path)

    for job, job_dict in merge_jobs_dict.items():
        logger.info(f"Main: Job: {job}")
        for filetype, files in job_dict.items():
            merge_jobs_dict[job][filetype] = natsorted(files)
            logger.info(f"Main: \t{filetype}:")
            for f in merge_jobs_dict[job][filetype]:
                logger.info(f"Main: \t\t{f}")

    merge_task_queue = Queue()

    for job, job_dict in merge_jobs_dict.items():
        if args.run_nevents_check:
            if not check_event_consistency_across_filetypes(job_dict, args.tree, args.remote_server):
                logger.error(f"Main: Inconsistent number of events across filetypes for job {job}")
                exit(1)
            else:
                logger.info(f"Main: Job {job} is consistent in number of events across filetypes")
        merge_task_queue.put((job, job_dict))
    logger.info(f"Main: queue size: {merge_task_queue.qsize()}")

    worker_name_template = "merge_worker_{INDEX}"
    merge_workers = []
    nworkers = min(len(merge_jobs_dict), args.n_threads)

    logger.info(f"Main: maximum number of concurrent workers: {nworkers}")

    with ProcessPoolExecutor(max_workers=nworkers) as executor:
        while not merge_task_queue.empty():
            job, job_dict = merge_task_queue.get()
            worker_id = worker_name_template.format(INDEX=len(merge_workers))
            future = executor.submit(merge_ntuples, job, job_dict, args.tree, worker_id, args.remote_server)
            merge_workers.append(future)

    for future in merge_workers:
        future.result()  # Wait for all workers to complete

    logger.info(f"Main: Merging finished")

if __name__ == "__main__":
    main()