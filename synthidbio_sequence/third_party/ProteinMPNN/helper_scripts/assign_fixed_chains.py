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

import argparse

def main(args):
    import json

    with open(args.input_path, 'r') as json_file:
        json_list = list(json_file)
    
    global_designed_chain_list = []
    if args.chain_list != '':
        global_designed_chain_list = [str(item) for item in args.chain_list.split()]
    my_dict = {}
    for json_str in json_list:
        result = json.loads(json_str)
        all_chain_list = [item[-1:] for item in list(result) if item[:9]=='seq_chain'] #['A','B', 'C',...]
        if len(global_designed_chain_list) > 0:
            designed_chain_list = global_designed_chain_list
        else:
            #manually specify, e.g.
            designed_chain_list = ["A"]
        fixed_chain_list = [letter for letter in all_chain_list if letter not in designed_chain_list] #fix/do not redesign these chains 
        my_dict[result['name']]= (designed_chain_list, fixed_chain_list)
    
    with open(args.output_path, 'w') as f:
        f.write(json.dumps(my_dict) + '\n')


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argparser.add_argument("--input_path", type=str, help="Path to the parsed PDBs")
    argparser.add_argument("--output_path", type=str, help="Path to the output dictionary")
    argparser.add_argument("--chain_list", type=str, default='', help="List of the chains that need to be designed")    

    args = argparser.parse_args()
    main(args) 

# Output looks like this:
# {"5TTA": [["A"], ["B"]], "3LIS": [["A"], ["B"]]}

