import sys
from collections import defaultdict
import subprocess
import os

from SAT_translator import SAT_translator
from sudoku_bool import namurupe_constraint, print_matrix


def sat(cage_input :list, output_file_name :str = 'b.smt2') -> list:
    sat_translator = SAT_translator(length=length)
    sat_translator.set_output_file(output_file_name)
    sat_translator.set_cageinput(cage_input)
    sat_translator.translate()
    
#     subprocess.run(['minisat ' + output_file_name + ' ' + result_file], shell=True)
    subprocess.run(['python3 BCP_SAT_two_literal.py ' + output_file_name + ' ' + result_file], shell=True)
    return 0

if __name__ == "__main__":
    length=9
    output_file_name = sys.argv[2]
    result_file = sys.argv[3]
    input_list = []
    with open(sys.argv[1], 'r') as my_file:
        input_list = my_file.readlines()
    input_item_list = namurupe_constraint(input_list)
    
    output = sat(input_item_list, output_file_name)
    print_matrix(result_file, length)