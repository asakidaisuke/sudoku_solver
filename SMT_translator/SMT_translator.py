class SMT_translator:
    def __init__(self, file_name :str = None,  
                 row :int = 9, column :int = 9):
        if row == 9 and column == 9:
            self.mesh = 3
        elif row == 16 and column == 16:
            self.mesh = 4
        else:
            raise ValueError("The number of row and column must be 9 or 16.")
            
        self.cage_input_list = []
        self.output_file = ""
        
        self.row = row
        self.column = column
        
        self.tab_space = "    "
        self.str_declaration_list = []
        self.str_max_min_constrain_list = []
        self.str_distinct_constrain_row_list = []
        self.str_distinct_constrain_column_list = []
        self.str_distinct_constrain_nonet_list = []
        self.str_cage_constrain_list = []
        self.show_result_list = []
        
    def set_output_file(self, output_file :str) -> None:
        self.output_file = output_file
    
    def set_cageinput(self, cage_list :list) -> None:
        self.cage_input_list = cage_list
        
    def __declaration(self) -> None:
        for r in range(1, self.row + 1):
            for c in range(1, self.column + 1):
                state = "(declare-fun x" + str(r) + str(c) + " () Int) \n"
                self.str_declaration_list.append(state)
                
    def __max_min_constrain(self) -> None:
        for r in range(1, self.row + 1):
            for c in range(1, self.column + 1):
                state = "(<= 1 x" + str(r) + str(c) + ") (<= x" + str(r) + str(c) + " 9) \n"
                self.str_max_min_constrain_list.append(self.tab_space + state)
        
    def __distinct_constrain_row(self) -> None:
        prefix = "(distinct "
        suffix = ")\n"
        for r in range(1, self.row + 1):
            state = ""
            for c in range(1, self.column + 1):
                state += " x" + str(r) + str(c)
            self.str_distinct_constrain_row_list.append(
                self.tab_space + prefix + state + suffix)
        
    def __distinct_constrain_column(self) -> None:
        prefix = "(distinct "
        suffix = ")\n"
        for c in range(1, self.column + 1):
            state = ""
            for r in range(1, self.row + 1):
                state += " x" + str(r) + str(c)
            self.str_distinct_constrain_column_list.append(
                self.tab_space + prefix + state + suffix)
            
    def __distinct_constrain_nonet(self) -> None:
        prefix = "(distinct "
        suffix = ")\n"
        for c_mesh in range(self.mesh):
            for r_mesh in range(self.mesh):
                state = ""
                for c_offset in range(1, self.mesh + 1):
                    for r_offset in range(1, self.mesh + 1):
                        r_base = r_mesh * self.mesh
                        c_base = c_mesh * self.mesh
                        state += " x" + str(r_base + r_offset) + str(c_base + c_offset)
                self.str_distinct_constrain_nonet_list.append(
                    self.tab_space + prefix + state + suffix)
    

    def __cage_constrain(self) -> None:
        pre_suffix = ") "
        suffix = ")\n"
        for cage_input in self.cage_input_list:
            state_middle = self.tab_space + "(= (+"
            state_post = ""
            for i in range(len(cage_input)):
                if i == 0:
                    state_post = pre_suffix + str(cage_input[i]) + suffix
                else:
                    state_middle += " " + "x" + str(cage_input[i])
            self.str_cage_constrain_list.append(state_middle + state_post)
    
    def __show_result(self) -> None:
        prefix = "(get-value  ("
        suffix = "))\n"
        for r in range(1, self.row + 1):
            state = ""
            for c in range(1, self.column + 1):
                state += " x" + str(r) + str(c)
            self.show_result_list.append(prefix + state + suffix)
    
    def __write_file(self):
        file1 = open(self.output_file,"w")
        file1.writelines(self.str_declaration_list)
        file1.writelines("(assert (and \n")
        file1.writelines(self.str_max_min_constrain_list)
        file1.writelines(self.str_distinct_constrain_row_list)
        file1.writelines(self.str_distinct_constrain_column_list)
        file1.writelines(self.str_distinct_constrain_nonet_list)
        file1.writelines(self.str_cage_constrain_list)
        file1.writelines(")) \n")
        file1.writelines("(check-sat) \n")
        file1.writelines(self.show_result_list)
        file1.close()
    
    
    def translate(self) -> None:
        """
        Make smt2 file.
        Each method creates constrain list.
        __write_file write smt2 file by reading each constrain list
        """
        self.__declaration()
        self.__max_min_constrain()
        self.__distinct_constrain_row()
        self.__distinct_constrain_column()
        self.__distinct_constrain_nonet()
        self.__cage_constrain()
        self.__show_result()
        self.__write_file()
        