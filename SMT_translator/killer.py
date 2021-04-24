import sys
from collections import defaultdict

from SMT_translator import SMT_translator


def create_input_list(input_list :list) -> list:
    """
    read input file and make input list
    """
    input_item_list = []
    for input_item in input_list:
        item_list = []
        input_item_splited = input_item.split(' ')
        for i in range(len(input_item_splited)):
            if "\n" in input_item_splited[i]:
                input_item_splited[i] = input_item_splited[i].replace("\n", "")
            if input_item_splited[i] == "":
                continue
            item_list.append(input_item_splited[i])
        input_item_list.append(item_list)
    return input_item_list

if __name__ == "__main__":
    output_file_name = sys.argv[2]
    input_list = []
    with open(sys.argv[1], 'r') as my_file:
        input_list = my_file.readlines()
    input_item_list = create_input_list(input_list)
    
    smt_translator = SMT_translator()
    smt_translator.set_output_file(output_file_name)
    smt_translator.set_cageinput(input_item_list)
    smt_translator.translate()
    print("")