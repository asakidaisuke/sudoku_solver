import itertools


def var(*args :int, alphabet = "x") -> str:
    if len(args) == 2:
        return alphabet + str(args[0]) + str(args[1])
    elif len(args) == 1:
        return alphabet + str(args[0])
    
def plus(input_list :list) -> list:
    return ["+"] + input_list

def equal(target1 :int, target2 :list) -> list:
    return ["=", str(target1), target2]

def morethan(target1 :int, target2 :str) -> list:
    return ["<=", str(target1), target2]

def lessthan(target1 :int, target2 :str) -> list:
    return ["<=", target2, str(target1),]

def distinct(input_list :list):
    return ["distinct"] + input_list

def show_distinct(input_list :list) -> str:
    state = "(distinct"
    for item in input_list:
        state += " " + item
    state = state + ")"
    return state

def sudoku_constraint(mesh_size :int) -> None:
    mesh_permutation = list(itertools.product(range(0,mesh_size**2, mesh_size), repeat=2))
    off_set_list = list(itertools.product(range(1, mesh_size + 1), repeat=2))
    dis_list = []
    for mesh in mesh_permutation:
        dis_list.append([var(mesh[0] + off_set[0], mesh[1] + off_set[1]) for off_set in off_set_list])
    return dis_list

def show_declare_int(variable :str) -> str:
    return "(declare-fun " + variable + " () Int)"

def show_get_value(input_list :list) -> str:
    return "(get-value  ( " + " ".join(input_list) + "))"

def show(formed_list :list) -> str:
    if type(formed_list) is int:
        return str(formed_list)
    elif type(formed_list) is str:
        return formed_list
    elif type(formed_list) is list:
        return "(" + " ".join([ show(y) for y in formed_list ]) + ")"

def cage_constraint(input_list :list) -> list:
    input_item_list = []
    for input_item in input_list:
        input_item_splited = list(map(
            lambda x: x.replace("\n", "") if "\n" in x else x, input_item.split(' ')
        ))
        input_item_splited = list(filter(lambda x: x != "", input_item_splited))
        input_item_list.append(input_item_splited)
    return form_input(input_item_list)

def form_input(cage_input_list :list) -> list:
    return [
        equal(cage_input[0], plus([var(cage_input[i]) for i in range(1,len(cage_input))])) 
        for cage_input in cage_input_list
    ]

def read_model(output :str) -> list:
    output_split_list = output.split('\n')
    
    read_output = []
    for output in output_split_list:
        if output == "sat":
            continue
        for out in output.split(')'):
            if out != '':
                output = out
                continue
        for out in output.split('('):
            if out != '':
                output = out
                continue
        if output == '':
            continue
        output = output.split(' ')
        read_output.append((output[0], int(output[1])))
    return read_output