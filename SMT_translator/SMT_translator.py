from sudoku import *

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
        self.output_file = "myfile.smt2"
        
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
                self.str_declaration_list.append(show_declare_int(var(r,c)) + "\n")
                
    def __max_min_constrain(self) -> None:
        for r in range(1, self.row + 1):
            for c in range(1, self.column + 1):
                first_state = show(morethan(1, var(r,c)))
                decond_state = show(lessthan(9, var(r,c)))
                state = first_state + " " +  decond_state
                self.str_max_min_constrain_list.append(self.tab_space + state + "\n")
        
    def __distinct_constrain_row(self) -> None:
        for r in range(1, self.row + 1):
            items = []
            for c in range(1, self.column + 1):
                items.append(var(r, c))
            self.str_distinct_constrain_row_list.append(
                self.tab_space + show_distinct(items) + "\n")
        
    def __distinct_constrain_column(self) -> None:
        for c in range(1, self.column + 1):
            items = []
            for r in range(1, self.row + 1):
                items.append(var(r, c))
            self.str_distinct_constrain_column_list.append(
                self.tab_space + show_distinct(items) + "\n")
            
    def __distinct_constrain_nonet(self) -> None:
        for c_mesh in range(self.mesh):
            for r_mesh in range(self.mesh):
                items = []
                for c_offset in range(1, self.mesh + 1):
                    for r_offset in range(1, self.mesh + 1):
                        r_base = r_mesh * self.mesh
                        c_base = c_mesh * self.mesh
                        items.append(var(r_base + r_offset, c_base + c_offset))
                self.str_distinct_constrain_nonet_list.append(
                    self.tab_space + show_distinct(items) + "\n")
    
    def __cage_constrain(self) -> None:
        for cage_input in self.cage_input_list:
            self.str_cage_constrain_list.append(
                self.tab_space + show(cage_input) + "\n")
    
    def __show_result(self) -> None:
        for r in range(1, self.row + 1):
            get_list = []
            for c in range(1, self.column + 1):
                get_list.append(var(r, c))
            self.show_result_list.append(show_get_value(get_list) + "\n")
    
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
