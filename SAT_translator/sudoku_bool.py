import itertools
import math


def cell(column :int, row :int, num :int) -> str:
    return 'x' + str(column) + str(row) + str(num)

def negate(element :str) -> str:
    return '-' + element

def sudoku_constraint(mesh_size :int) -> list:
    mesh_permutation = list(itertools.product(range(0,mesh_size**2, mesh_size), repeat=2))
    off_set_list = list(itertools.product(range(1, mesh_size + 1), repeat=2))
    dis_list = []
    for mesh in mesh_permutation:
        dis_list.append(["x" + str(mesh[0] + off_set[0])+str(mesh[1] + off_set[1]) for off_set in off_set_list])
    return dis_list

def create_at_least(row :int, distinct_type :str) -> list:
    if distinct_type == "row":
        return [
            [[cell(j,i,num) for i in range(1, row + 1)] for j in range(1, row+ 1)]
            for num in range(1, row + 1)
        ]
    elif distinct_type == "column":
        return [
            [[cell(i,j,num) for i in range(1, row + 1)] for j in range(1, row+ 1)]
            for num in range(1, row + 1)
        ]
    elif distinct_type == "nonet":
        feed_list = sudoku_constraint(int(math.sqrt(row)))
        return [
            [
                [str(feed) + str(num) for feed in feeds]
                for feeds in feed_list
            ]
            for num in range(1, row + 1)
        ]
    elif distinct_type == "cell":
        return [
                    [[cell(i,j,num) for num in range(1, row + 1)] for i in range(1, row+ 1)]
                    for j in range(1, row + 1)
                ]
    
def create_at_most(row :int, distinct_type :str) -> list:
    combination = list(itertools.combinations(range(1, row+1),2))
    if distinct_type == "row":
        return [
                    [
                        [
                            [negate(cell(i, comb[0], num)),negate(cell(i, comb[1], num))]
                            for comb in combination
                        ]
                        for i in range(1, row + 1)
                    ]
                    for num in range(1, row + 1)
                ]
    elif distinct_type == "column":
        return [
                    [
                        [
                            [negate(cell(comb[0], i, num)),negate(cell(comb[1], i, num))]
                            for comb in combination
                        ]
                        for i in range(1, row + 1)
                    ]
                    for num in range(1, row + 1)
                ]
    elif distinct_type == "nonet":
        return [
                    [
                        [
                            [negate(cell(int(comb[0][1]), int(comb[0][2]), num)),
                             negate(cell(int(comb[1][1]), int(comb[1][2]), num))]
                            for comb in 
                            list(itertools.combinations(sudoku_constraint(int(math.sqrt(row)))[j], 2))
                        ]
                        for j in range(row)
                    ]
                    for num in range(1, row + 1)
                ]
    
def en_base_n(num :str, base :int):
    return (int(num[0]) -1) * (base ** 2) + (int(num[1]) -1) * base + int(num[2])

def de_base_n(num :str, base :int = 9):
    num_int = int(num)
    first_digit = num_int % base
    if first_digit == 0: first_digit = base
    num_int -= first_digit
    third_digit = num_int // (base**2)  + 1
    num_int -= (third_digit-1) * (base**2)
    second_digit = num_int // base  + 1
    num_int -= (second_digit-1) * base
    return str(third_digit) + str(second_digit) + str(first_digit)

def show_list(input_list :list, row :int=9) -> list:
    return [
        str(en_base_n(el[1:], row)) if el[0] =="x" else "-" + str(en_base_n(el[2:], row))
        for el in input_list
    ]

def namurupe_constraint(input_list :list) -> list:
    """
    [
       [3, 1, 2],
       [3, 1, 2],
       ....
    ]
    """
    judge_is_int = lambda x: True if x[0] != '.' else None
    mesh = len(input_list)
    constraint_list = []
    for i in range(mesh):
        constraint_list += [
            (str(i+1) + str(j+1), int(input_list[i].split(' ')[j][0]))
            for j in range(mesh) if judge_is_int(input_list[i].split(' ')[j])
        ]
    return namurupe_form_input(constraint_list)
        
def namurupe_form_input(input_list :list) -> list:
    """
    [
       ["=", 3, x12],
       ["=", 3, x12],
       ....
    ]
    """
    return [
        cell(item[0][0],item[0][1], item[1]) for item in input_list
    ]

def read_file(file :str) -> list:
    with open(file, 'r') as f:
        output = f.read()
    f.close()
    return output

def form_sat_output(output :list, length :int) -> list:
    output = [out for out in output.split(' ') if out[0] != '-']
    if output[0] == 'SAT\n1':
        output[0] = '1'
    else:
        output = output[1:]
    output = output[:-1]
    return [de_base_n(i, 9) for i in output]

def print_matrix(file :str, length :int) -> None:
    output = read_file(file)
    output = form_sat_output(output, length)
    output = [out[-1] for out in output]
    output = [output[i * length:i * length + length] for i in range(length)]
    for i in range(length):
        print(" ".join(output[i]))