#! python
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from time import time
import csv
from tqdm import tqdm
import traceback
from threading import BoundedSemaphore, Thread
import json

IDLE = False
METRICS = ['psnr', 'ssim', 'vmaf', 'niqe']

DATASET = '../2019'
DISTORTED = f'{DATASET}/seq'
REFERENCES = f'{DATASET}/ref'
RESULTS = 'results_06-05/raw.csv'
MASKS = f'{DATASET}/masks'
ERRORS = 'errors.txt'
VQMT = '../vqmt'
HEADERS = 'Name,Reference,Distorted,Metric,Metric_val,Mask,Time'.split(',')


def folder2name(folder):
    name = os.path.basename(os.path.normpath(folder))
    name = "_".join(name.split("_")[:-1])
    return name


class CommandHandler:
    def __init__(self, max_processes):
        self.maxp = max_processes
        self.sem = BoundedSemaphore(self.maxp)
    def run(self, target, args):
        def func_with_end(args):
            target(*args)
            self.sem.release()
            # print('end')
            
        # print('waiting')
        self.sem.acquire()
        # print('started')
        thread = Thread(target=func_with_end, args=(args,))        
        thread.start()


def compute(seq_name, ref: str, dis: str, metric: str, writer_results, mask_path=None) -> float:
    try:
        tmp_file = f"/tmp/2019dataset_{os.getpid()}_{time()}.json"
        time_start_video = time()

        cmd = f"{VQMT} "
        if ref is not None:
            cmd += f"-orig {ref} 1920x1080 YUV420p "
        cmd += f"-in {dis} "
        if mask_path is not None:
            cmd += f"-mask {mask_path}  -mask-type 8bit black "
        cmd += f"-metr {metric} over Y -resize to orig -json-file {tmp_file} > /dev/null"

        if not IDLE:
            os.system(cmd)
            with open(tmp_file) as f:
                j = json.load(f)
                metric_value = j['accumulated']['mean']['A']
            os.remove(tmp_file)
        else:
            metric_value = 123.45678

        time_calc = int(time() - time_start_video)

        row = [seq_name, ref, dis, metric, round(metric_value, 3), mask_mode, time_calc]
        writer_results.write_row(row)
        print("%-70s%s   %s   %s   %s" % (dis.split('/')[-1], metric, mask_mode, round(metric_value, 3), f'{time_calc // 60} min, {time_calc % 60} sec'))
    except:
        print(traceback.format_exc())
        writer_errors.write_text(f'ERROR:  seq: {seq_name}, ref: {ref}, dis: {dis}, mask: {mask_path}, metric: {metric}, mask_mode: {mask_mode}')

class MyWriter:
    def __init__(self, f):
        self.filename = f
        if not os.path.exists(self.filename):
            os.open(self.filename, os.O_CREAT)

    def write_row(self, row):
        with open(self.filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def write_text(self, text):
        with open(self.filename, 'a') as f:
            f.write(text)
            print(text)


writer_results = MyWriter(RESULTS)
writer_errors = MyWriter(ERRORS)
writer_results.write_row(HEADERS)

command_handler = CommandHandler(2)

# assumed, that files in folders DISTORTED, REFERENCES, MASKS follow in the same order
dis_sequences = [x for x in os.listdir(DISTORTED) if os.path.isdir(f'{DISTORTED}/{x}')]
dis_sequences.sort()

references = [x for x in os.listdir(REFERENCES)]
references.sort()

masks_map = [x for x in os.listdir(MASKS)]
masks_map.sort()


total_files = sum([len(os.listdir(os.path.join(DISTORTED, sequence))) for sequence in os.listdir(DISTORTED)]) * 4
print('Total files:', total_files)

file_index = 0
testing_start = time()
for folder, ref, mask_map in [*zip(dis_sequences, references, masks_map)][3:]:  # !!!
    seq_name = folder2name(folder)
    for metric in METRICS:
        for mask_mode in [True]:
                distorted_seq = f'{DISTORTED}/{folder}'
                videos = os.listdir(distorted_seq)
                
                dis_list = [x for x in os.listdir(distorted_seq)]
                dis_list.sort()

                time_start_sequence = time()
                for dis in dis_list[:]:
                        ref_path = f'{REFERENCES}/{ref}'
                        dis_path = f'{distorted_seq}/{dis}'
                        mask_path = f'{MASKS}/{mask_map}' if mask_mode is True else None

                        if metric == 'niqe':
                            ref_path = None                      
                        
                        command_handler.run(target=compute, args=(seq_name, ref_path, dis_path, metric, writer_results, mask_path))
                        # print('>>> time for video:', f'{int(time() - time_start_video)} sec')
                        print(f'Progress: {round(file_index / total_files * 100, 1)}%')
                        file_index += 1
                time_for_seq = int(time() - time_start_sequence)
                print('>>> time for sequence:', f'{time_for_seq // 60} min, {time_for_seq % 60} sec')
