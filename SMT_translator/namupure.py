import sys
from collections import defaultdict
import subprocess

from SMT_translator import SMT_translator
from sudoku import namurupe_constraint, read_model, print_matrix


def smt(cage_input :list, output_file_name :str = 'b.smt2') -> list:
    smt_translator = SMT_translator()
    smt_translator.set_output_file(output_file_name)
    smt_translator.set_cageinput(cage_input)
    smt_translator.translate()
    
    z3_output = subprocess.check_output(['z3 ' + output_file_name], shell=True)
    z3_output_str = z3_output.decode("utf-8")
    return read_model(z3_output_str)

if __name__ == "__main__":
    output_file_name = sys.argv[2]
    input_list = []
    with open(sys.argv[1], 'r') as my_file:
        input_list = my_file.readlines()
    input_item_list = namurupe_constraint(input_list)
    
    output = smt(input_item_list)
    print_matrix(output)