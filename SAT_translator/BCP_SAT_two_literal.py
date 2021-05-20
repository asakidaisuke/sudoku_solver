from collections import defaultdict
import time
import sys


def lister(nums: list) -> list:
    a = [[], []]
    for num in nums:
        if num > 0:
            a[0].append(num - 1)
        else:
            a[1].append(-num - 1)
    return a

def make_two_watched_table(
                CNF, watch_table
        ):
    for i in range(len(CNF)):
        vars = CNF[i][0] + CNF[i][1]
        if len(vars) > 1:
            watch_table[i] = vars[0:2]
        else:
            watch_table[i].append(vars[0])

def find_unit_clause(index: int, current_list: list, unit_clause: list):
    """
    新しく割り当てられた変数にtriggerされて、新しくunit状態となった
    clauseを探し、その過程でコンフリクトを見つけた場合はNoneを返す。
    """
    # 割り当てが何もなされていない場合、一個のliteralのclauseのみを返す。
    if index is None:
        for literal in (single_literals):
            unit_clause.append(literal)
        return True
    # 新しく割り当てられた変数をwatchしているclauseからunit状態のものを抽出。
    # コンフリクトがあった場合はNoneを返す。
    noConflict = filter_conflict_and_duplicate(index, current_list, unit_clause)
    return noConflict

def filter_conflict_and_duplicate(
                index: int, current_list: list, unit_clause: list
        ) -> list:
    """
    watching literalに新しくassignした変数によって生み出されたコンフリクト、
    unit状態のclauseを探し出す。
    """
    # watchリストに変数が入っていない場合、そのclauseは飛ばす。
    for clause, watch_literal_list in watch_table.items():
        if index not in watch_literal_list:
            continue
        # 既にそのclauseがunit状態と認識されていたら飛ばす。
        if clause in unit_clause:
            continue
        # 新しいassignでsatになった場合は飛ばす。
        if (current_list[index] and index in CNF[clause][0]) or \
                (not current_list[index] and index in CNF[clause][1]):
            continue
        # watching literalのもう片方のliteralを取得
        other_literal = list(set(watch_literal_list) - set([index]))[0]
        # watching literal以外のliteral
        not_watch_literal = list(set(CNF[clause][0] + CNF[clause][1]) - set(watch_literal_list))
        if len(not_watch_literal) > 0:
            # not Falseの変数を探す、あればそれを監視下に置換する
            assignable = [
                literal for literal in not_watch_literal
                if current_list[literal] is None or
                   (current_list[literal] and literal in CNF[clause][0]) or
                   (not current_list[literal] and literal in CNF[clause][1])
                    ]
        else:
            assignable = []

        if len(assignable) > 0:
            # not Falseの変数があればそれを監視下に置き換え
            watch_table[clause][watch_table[clause].index(index)] = assignable[0]
        else:
            # not Falseの変数がなくて片方の監視下literalがNoneならそれはunit状態
            if current_list[other_literal] is None:
                unit_clause.append(
                    (
                        clause,
                        other_literal
                    )
                )
                # もう一方のliteralが1の場合satなので飛ばす
            elif (current_list[other_literal] and other_literal in CNF[clause][0]) or \
                    (not current_list[other_literal] and other_literal in CNF[clause][1]):
                continue
            else:
                # もう一方のliteralも0の場合conflict
                return None
    return True

def two_watched(current_list: list, CNF: list, index: int) -> bool:
    X = current_list.copy()
    unit_clause = []
    # まず最初に新しく割り当てられてた変数からtriggerされるunit clauseを探索する。
    noConflict = find_unit_clause(index, X, unit_clause)
    # コンフリクトがある場合はNoneになる。
    if noConflict is None:
        return False
    # unit_clauseにはunit状態のclauseの番号と割り当て待ちの変数(番号)が入っている。
    # unit_clause -> [(clause番号, unitで割り当てられる変数番号),(,), ]
    while len(unit_clause) > 0:
        clause = unit_clause.pop()
        # unit状態のclauseを取り出す。
        P, N = CNF[clause[0]]
        # 変数に割り当てを行う。
        X[clause[1]] = clause[1] in P
        # 新しい割り当てでtriggerされたunit状態のclauseがあるかを調べる。
        noConflict = find_unit_clause(clause[1], X, unit_clause)
        # conflictがあればNoneが返ってくる。
        if noConflict is None:
            return False

    if index is None:
        # 一つだけのclauseで割り当てられる変数はその後変動がないので、
        # 決定の割り付けとして最初の段階でXを更新する。
        for i in range(len(X)):
            current_list[i] = X[i]
    return True

# def propagate(current_list: list, CNF: list) -> bool:
#     X = current_list.copy()
#     done = False
#     while not done:
#         done = True
#         for (P, N) in CNF:
#             I = [i for i in P if X[i] != False] + \
#                 [i for i in N if X[i] != True]
#             if I == []:
#                 # continue
#                 return False
#             i = I.pop()
#             if I == [] and X[i] == None:
#                 X[i] = i in P
#                 done = False
#     if current_list[0] is None:
#         for i in range(len(X)):
#             current_list[i] = X[i]
#     return True

def search(X, CNF, index=None):
    # print(X)
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

# def search(X, CNF):
#     # print(X)
#     if not propagate(X, CNF):
#         return None
#     if not None in X:
#         return X
#     i = X.index(None)
#     Y = X[:]
#     Y[i] = True
#     Z = search(Y, CNF)
#     if Z != None:
#         return Z
#     Y[i] = False
#     return search(Y, CNF)

def write_output(file_name: str, output: list) -> None:
    output = [str(i + 1) + ' ' if output[i] else str(-(i + 1)) + ' ' for i in range(len(output))] + ['0']
    with open(file_name, 'w') as f:
        f.writelines('SAT \n')
        f.writelines("".join(output))
    f.close()


if __name__ == '__main__':
    start = time.time()
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
    make_two_watched_table(CNF, watch_table)
    single_literals = [(key, value) for key, value in watch_table.items() if len(value) == 1]
    single_literals = [(clause[0], clause[1][0]) for clause in single_literals]


    output = search(none_list, CNF)
    write_output(output_file, output)
    print(time.time() - start)
