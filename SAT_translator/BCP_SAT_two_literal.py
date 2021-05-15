import sys
from collections import defaultdict


def lister(nums :list) -> list:
    a = [[],[]]
    for num in nums:
        if num > 0:
            a[0].append(num - 1)
        else:
            a[1].append(-num -1)
    return a

def make_two_watched_table(
            CNF, watch_tabl, all_table
        ):
    for i in range(len(CNF)):
        vars = CNF[i][0] + CNF[i][1]
        if len(vars) > 1:
            watch_table[i] = vars[0:2]
        else:
            watch_table[i].append(vars[0])
        all_table[i] = vars


def find_implication_from_table(index: int, current_list: list, first_look=False):
    if index is None:
        return single_literals
    implied_clause = [key for key, value in watch_table.items() if index in value]
    implied_clause = find_true_implication(implied_clause, index, current_list)
    if first_look:
        for i in range(index):
            implied_clause += find_true_implication(
                [key for key, value in watch_table.items() if i in value],
                i,
                current_list
            )
        implied_clause = list(set(implied_clause))
        implied_clause += single_literals
    return implied_clause


def find_true_implication(
        implied_clause: list, index: int, current_list: list
) -> list:
    truely_implied_clause = []
    for clause in implied_clause:
        # satになった場合は除外
        if (current_list[index] and index in CNF[clause][0]) or \
                (not current_list[index] and index in CNF[clause][1]):
            continue
        # implication状態になったclauseのwatch listを取得
        watch_literal = watch_table[clause]
        # implication状態になったclauseのwatch list以外をリスト化
        not_watch_literal = [literal for literal in all_table[clause] if literal not in watch_literal]
        # unassigned状態の変数があればそれを監視下に置換する
        not_assinged = [literal for literal in not_watch_literal if current_list[literal] is None]
        if len(not_assinged) > 0:
            watch_table[clause][watch_table[clause].index(index)] = not_assinged[0]
        elif len(watch_table[clause]) == 1:
            truely_implied_clause.append(clause)
        else:
            truely_implied_clause.append(clause)
    return truely_implied_clause


def two_watched(current_list: list, CNF: list, index: int) -> bool:
    X = current_list.copy()
    new_implied_clause = find_implication_from_table(index, X, first_look=True)
    while len(new_implied_clause) > 0:
        implied_clause = new_implied_clause
        new_implied_clause = []
        for clause in implied_clause:

            P, N = CNF[clause]
            I = [i for i in P if X[i] != False] + \
                [i for i in N if X[i] != True]

            if I == []:
                return False
            i = I.pop()
            if I == [] and X[i] == None:
                X[i] = i in P
                new_implied_clause += find_implication_from_table(i, X)
                new_implied_clause = list(set(new_implied_clause))
    return True


def search(X, CNF, index=None):
    print(X)
    if not two_watched(X, CNF, index):
        return None
    if not None in X:
        return X
    i = X.index(None)
    Y = X[:]
    Y[i] = True
    Z = search(Y, CNF, i)
    if Z != None:
        return Z
    Y[i] = False
    return search(Y, CNF, i)


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

    watch_table = defaultdict(list)
    watch_table_reverse = defaultdict(list)
    all_table = defaultdict(list)
    make_two_watched_table(CNF, watch_table, all_table)
#     make_two_watched_table_reverse(watch_table_reverse, watch_table)
    single_literals = [key for key, value in watch_table.items() if len(value) == 1]


    output = search(none_list, CNF)
    write_output(output_file, output)
   