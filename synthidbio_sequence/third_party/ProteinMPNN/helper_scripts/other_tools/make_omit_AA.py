# Original code licensed under MIT License.
# Copyright (c) 2022 Justas Dauparas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import glob
import random
import numpy as np
import json
import itertools

#MODIFY this path
with open('/home/justas/projects/lab_github/mpnn/data/pdbs.jsonl', 'r') as json_file:
    json_list = list(json_file)

my_dict = {}
for json_str in json_list:
    result = json.loads(json_str)
    all_chain_list = [item[-1:] for item in list(result) if item[:9]=='seq_chain']
    fixed_position_dict = {}
    print(result['name'])
    if result['name'] == '5TTA':
        for chain in all_chain_list:
            if chain == 'A':
                fixed_position_dict[chain] = [
                    [[int(item) for item in list(itertools.chain(list(np.arange(1,4)), list(np.arange(7,10)), [22, 25, 33]))], 'GPL'],
                    [[int(item) for item in list(itertools.chain([40, 41, 42, 43]))], 'WC'],
                    [[int(item) for item in list(itertools.chain(list(np.arange(50,150))))], 'ACEFGHIKLMNRSTVWYX'],
                    [[int(item) for item in list(itertools.chain(list(np.arange(160,200))))], 'FGHIKLPQDMNRSTVWYX']]
            else:
                fixed_position_dict[chain] = []
    else:
        for chain in all_chain_list:
            fixed_position_dict[chain] = []
    my_dict[result['name']] = fixed_position_dict

#MODIFY this path   
with open('/home/justas/projects/lab_github/mpnn/data/omit_AA.jsonl', 'w') as f:
    f.write(json.dumps(my_dict) + '\n')


print('Finished')
#e.g. output
#{"5TTA": {"A": [[[1, 2, 3, 7, 8, 9, 22, 25, 33], "GPL"], [[40, 41, 42, 43], "WC"], [[50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149], "ACEFGHIKLMNRSTVWYX"], [[160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199], "FGHIKLPQDMNRSTVWYX"]], "B": []}, "3LIS": {"A": [], "B": []}}  
