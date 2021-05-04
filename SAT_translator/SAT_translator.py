from sudoku_bool import *

class SAT_translator:
    def __init__(self, file_name :str = None,  
                 length :int = 9):
        if length == 9:
            self.mesh = 3
        elif length == 16:
            self.mesh = 4
        elif length == 4:
            self.mesh = 2
        else:
            raise ValueError("The number of row and column must be 9 or 16.")
            
        self.sudoku_input_list = []
        self.output_file = "myfile.smt2"

        self.length = length
        
    def set_output_file(self, output_file :str) -> None:
        self.output_file = output_file
        self.write_file = open(self.output_file,"w")
    
    def set_cageinput(self, cage_list :list) -> None:
        self.sudoku_input_list = cage_list
        
    def __distinct_constrain_cell(self) -> None:
        for cells in create_at_least(self.length, "cell"):
            for cell in cells:
                self.__write_file(" ".join(show_list(cell, self.length))+ " 0 \n")
        
    def __distinct_constrain_row(self) -> None:
        for rows in create_at_least(self.length, "row"):
            for row in rows:
                self.__write_file(" ".join(show_list(row, self.length))+ " 0 \n")
        
        for num_combination in create_at_most(self.length, "row"):
            for rows in num_combination:
                for row in rows:
                    self.__write_file(" ".join(show_list(row, self.length))+ " 0 \n")

    def __distinct_constrain_column(self) -> None:
        for columns in create_at_least(self.length, "column"):
            for column in columns:
                self.__write_file(" ".join(show_list(column, self.length))+ " 0 \n")
        
        for num_combination in create_at_most(self.length, "column"):
            for columns in num_combination:
                for column in columns:
                    self.__write_file(" ".join(show_list(column, self.length))+ " 0 \n")
            
    def __distinct_constrain_nonet(self) -> None:
        for nonets in create_at_least(self.length, "nonet"):
            for nonet in nonets:
                self.__write_file(" ".join(show_list(nonet, self.length))+ " 0 \n")
                
        for num_combination in create_at_most(self.length, "nonet"):
            for nonets in num_combination:
                for nonet in nonets:
                    self.__write_file(" ".join(show_list(nonet, self.length))+ " 0 \n")
    
    def __sudoku_constrain(self) -> None:
        for sudoku_input in self.sudoku_input_list:
            self.__write_file(str(en_base_n(sudoku_input[1:], self.length)) + " 0 \n")
    
    def __write_file(self, input_list :list) -> None:
        self.write_file.writelines(input_list)
    
    def translate(self) -> None:
        """
        Make smt2 file.
        Each method creates constrain list.
        __write_file write smt2 file by reading each constrain list
        """
        self.__distinct_constrain_cell()
        self.__distinct_constrain_row()
        self.__distinct_constrain_column()
        self.__distinct_constrain_nonet()
        self.__sudoku_constrain()
        self.write_file.close()
