# -*- coding: utf-8 -*-
import logging
import os

from utils.datagenerationhelpers import generate_all_csv_with_avg_times

logging.basicConfig(level=logging.DEBUG, filename='retorchCostModel.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

path_output_avg = "./avg-datasets/"

# Comparing the returned list to empty list
listfiles = os.listdir(path_output_avg)
if len(listfiles) <= 1:
    generate_all_csv_with_avg_times(path_input="./raw-datasets/*", path_output=path_output_avg)