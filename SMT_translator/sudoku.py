def var(*args :int, alphabet = "x") -> str:
    if len(args) == 2:
        return alphabet + str(args[0]) + str(args[1])
    elif len(args) == 1:
        return alphabet + str(args[0])
    else:
        raise ValueError("input must be less than three digit")
    
def plus(input_list :list) -> list:
    symbol = "+"
    output_list = [symbol]
    for item in input_list:
        output_list.append(str(item))
    return output_list

def equal(target1 :int, target2 :list) -> list:
    symbol = "="
    output_list = [symbol, str(target1), target2]
    return output_list

def morethan(target1 :int, target2 :str) -> list:
    symbol = "<="
    output_list = [symbol, str(target1), target2]
    return output_list

def lessthan(target1 :int, target2 :str) -> list:
    symbol = "<="
    output_list = [symbol, target2, str(target1),]
    return output_list

def show_distinct(input_list :list) -> str:
    state = "(distinct"
    for item in input_list:
        state += " " + item
    state = state + ")"
    return state

def show_declare_int(variable :str) -> str:
    return "(declare-fun " + variable + " () Int)"

def show_get_value(input_list :list) -> str:
    state = "(get-value  ( "
    items = ""
    for item in input_list:
        items += item + " "
    state = state + items + "))"
    return state

def show(formed_list :list) -> str:
    if len(formed_list) != 3:
        raise ValueError("input list is invalid")
        
    if isinstance(formed_list[2], str):
        return "(" + formed_list[0] + " " + formed_list[1] + " " + formed_list[2] + ")"
    
    if isinstance(formed_list[2], list):
        pre_state = "(" + formed_list[0] + " " + formed_list[1] + " " + "("
        post_state = ""
        for formed in formed_list[2]:
            post_state += formed + " "
        post_state = post_state + "))"
        return pre_state + post_state
    
    
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
    return form_input(input_item_list)

def form_input(cage_input_list :list) -> list:
    formed_input_list = []
    for cage_input in cage_input_list:
        cage_items_list = []
        for i in range(1, len(cage_input)):
            cage_items_list.append(var(cage_input[i]))
        formed_input_list.append(equal(cage_input[0], plus(cage_items_list)))
    return formed_input_list

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