#
# Copyright (c) 2016 Qualcomm Technologies, Inc.
# All Rights Reserved.
# Confidential and Proprietary - Qualcomm Technologies, Inc.
#

import argparse
import heapq
import numpy as np
import os


def main():
    parser = argparse.ArgumentParser(description='Display alexnet classification results.')
    parser.add_argument('-i', '--input_list',
                        help='File containing input list used to generate output_dir.', required=True)
    parser.add_argument('-o', '--output_dir',
                        help='Output directory containing Result_X/SUFFIX/prob.raw files matching input_list.', required=True)
    parser.add_argument('-s', '--suffix_path',
                        help='Suffix to output directory containing Result_X/SUFFIX/prob.raw files matching input_list.', required=True)
    parser.add_argument('-l', '--labels_file',
                        help='Path to ilsvrc_2012_labels.txt', required=True)
    parser.add_argument('-v', '--verbose_results',
                        help='Display top 5 classifications', action='store_true')
    args = parser.parse_args()

    num_labels = 5

    input_list = os.path.abspath(args.input_list)
    output_dir = os.path.abspath(args.output_dir)
    suffix_path = args.suffix_path
    labels_file = os.path.abspath(args.labels_file)
    display_top5 = args.verbose_results

    if not os.path.isfile(input_list):
        raise RuntimeError('input_list %s does not exist' % input_list)
    if not os.path.isdir(output_dir):
        raise RuntimeError('output_dir %s does not exist' % output_dir)
    if not os.path.isfile(labels_file):
        raise RuntimeError('labels_file %s does not exist' % labels_file)
    with open(labels_file, 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    if len(labels) != num_labels:
        raise RuntimeError('Invalid labels_file: need num_labels categories')
    with open(input_list, 'r') as f:
        input_files = [line.strip() for line in f.readlines()]

    if len(input_files) <= 0:
        print('No files listed in input_files')
    else:
        print('Classification results')
        max_filename_len = max([len(file) for file in input_files])

        total = 0
        wrong = 0
        for idx, val in enumerate(input_files):
            cur_results_dir = 'Result_' + str(idx)
            cur_results_file = os.path.join(output_dir, cur_results_dir, suffix_path) + '0.raw'
            if not os.path.isfile(cur_results_file):
                raise RuntimeError('missing results file: ' + cur_results_file)

            float_array = np.fromfile(cur_results_file, dtype=np.float32)
            if len(float_array) != num_labels:
                raise RuntimeError(str(len(float_array)) + ' outputs in ' + cur_results_file)

            if not display_top5:
                max_prob = max(float_array)
                max_prob_index = np.where(float_array == max_prob)[0][0]
                max_prob_category = labels[max_prob_index]

                if not max_prob_category in val:
                   wrong += 1
                total += 1

                display_text = '%s %f %s %s [%s]' % (
                val.ljust(max_filename_len), max_prob, str(max_prob_index).rjust(3), max_prob_category, max_prob_category in val)
            else:
                top5_prob = heapq.nlargest(5, xrange(len(float_array)), float_array.take)
                for i, idx in enumerate(top5_prob):
                    prob = float_array[idx]
                    prob_category = labels[idx]
                    display_text = '%s %f %s %s' % (
                        val.ljust(max_filename_len), prob, str(idx).rjust(3), prob_category)

            print(display_text)
        print(total, wrong, 100*(total-wrong)/total)


if __name__ == '__main__':
    main()
