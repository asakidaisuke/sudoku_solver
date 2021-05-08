import sys


def lister(nums :list) -> list:
    a = [[],[]]
    for num in nums:
        if num > 0:
            a[0].append(num - 1)
        else:
            a[1].append(-num -1)
    return a

def propagate(current_list :list, CNF :list) -> bool: 
    X = current_list.copy()
    done = False
    while not done: 
        done = True
        for (P, N) in CNF:
            I = [ i for i in P if X[i] != False ] + \
             [ i for i in N if X[i] != True ]
            if I == []:
                return False 
            i = I.pop()
            if I == [] and X[i] == None: 
                X[i] = i in P
                done = False
    return True

def search(X :list, CNF :list) -> list:
    if not propagate(X, CNF): 
        return None
    if not None in X: 
        return X
    i = X.index(None)
    Y = X[:]
    Y[i] = True
    Z = search(Y, CNF)
    if Z != None:
        return Z 
    Y[i] = False
    return search(Y, CNF) 

def write_output(file_name: str, output: list) -> None:
    output = [str(i+1) + ' ' if output[i] else str(-(i+1)) + ' ' for i in range(len(output))] + ['0']
    with open(file_name,'w') as f:
        f.writelines('SAT \n')
        f.writelines("".join(output))
    f.close()

if __name__  == '__main__':
    cnf_file = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(cnf_file) as f:
        input_list = f.readlines()
    f.close()
    
    input_list = [[int(el) for el in clause.split(' ')[:-2]] for clause in input_list]
    CNF = [tuple(lister(el)) for el in input_list]
    none_list = [None] * 729
    
    output = search(none_list, CNF)
    write_output(output_file, output)
   