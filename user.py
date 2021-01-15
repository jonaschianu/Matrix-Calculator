################################################################################
 # Project:  Complex Number and Matrix Calculator                             #
 #                                                                            #
 # Name:          Jonas Chianu                                                #
 # File:          user.py                                                     #
 # Purpose:       Contains the user interface class                           #
 # Description:   Allows for user inputs and returns calculation results      #
################################################################################

import sys # importing system module
import main # Importing main.py file

class UI():
    ''' This class stores accepts and stores user input data,
     and displays requested output'''
    _matrices=[]
    _resultant_matrix = []

    def __init__(self):
        self._matrices=[]
        self._resultant_matrix = []

    def multiply_type(self):
        ''' Ask the user user what type of multiplication they want to perform
            Passed: None
            Returns: Multiplication type (Str)
        '''
        while True:
            __mul_type = input("Do you want to perform matrix or vector "
                               "multiplication (M or V) ").upper().strip()

            if __mul_type in ["M","MATRIX","V","VECTOR"]: break
            else: print("Invalid input, please choose (M/V)")

        return __mul_type

    def delete_matrix_prompt(self):
        ''' Ask the user user if they want to delete the matrix
            Passed: None
            Returns: Matrix Deletion Prompt Response (Str)
        '''
        delete_matrix = input("Do you want to delete the matrix (Y/N). If no, "
                              "choose a new matrix type ").upper().strip()
        while delete_matrix not in ['N', 'NO', 'Y', 'YES']:
            delete_matrix = input("Wrong input! Do you want to delete "
                                  "the matrix (Y/N) ").upper().strip()

        return delete_matrix

    def return_user_request(self):
        ''' Takes in inputs to create matrices and does calculations on them
            Passed: None
            Returns: None
        '''
        matrix_num = 0 # Tag for current matrix being created
        another_matrix = "Y"

        while another_matrix in ["Y","YES"]:
            print("Create matrix " + str(matrix_num + 1) + ":")

            # These variables keep track of rows and column of previous matrix,
            # to show user row and column that are needed for a successful
            # computation. M: Matrix multiplication ; V: Vector multiplication/division
            if matrix_num==0: newrow_V=1 ; newrow_M=1 ;newcol_V=1#default values

            numrow,numcol=self.input_dimension(matrix_num,newrow_M,
                                               newrow_V,newcol_V)

            # Creates and appends current matrix to list of previous matrices
            self.generate_user_matrices(numrow, numcol)

            print(self._matrices[matrix_num]) # Prints the current matrix

            if matrix_num == 0:  # Resultant matrix is set to first matrix
                self._resultant_matrix = self._matrices[0]

            else:
                # Calculate resultant matrix and check for errors
                resultant_is_valid=self.resultant_matrix_validation()

                if not resultant_is_valid:
                    continue


                print_current=self.print_current_result() # Print current result

                # Checks if user want to multiply another matrix to result
                another_matrix = self.mul_another_matrix(print_current)

            newrow_V = numrow ; newcol_V = numcol
            newrow_M = numcol

            matrix_num += 1

    def input_dimension(self,matrix_num,newrow_M,newrow_V,newcol_V):
        ''' Sets the dimensions based on user inputs
            Passed: Current matrix (int),
                    Required row for matrix multiplication (int),
                    Required row for matrix multiplication (int,
                    Required row for matrix multiplication (int)
            Returns: Number of rows (int), Number of columns(int)
        '''
        if matrix_num != 0:
            print("For matrix multiplication with previous matrix, you must use"
                  " a row of {}".format(newrow_M))
            print("For vector multiplication/division with previous matrix, you must use"
                  " a row of {} and col of {}".format(newrow_V, newcol_V))

        numrow=self.set_and_check_dimension_isdigit("row")

        # Checks that the input row is valid
        while matrix_num != 0 and numrow not in [newrow_M,newrow_V]:
            print("Error! For matrix multiplication and vector multiplication/division, "
                  "you must use a row of {} or {} respectively"\
                  .format(newrow_M, newrow_V))
            numrow = self.set_and_check_dimension_isdigit("row")

        numcol = self.set_and_check_dimension_isdigit("col")

        # If previously chosen rows is only possible with vector multiplication/division,
        # then the program checks that the input column is valid
        while matrix_num != 0 and newrow_M != newrow_V \
                and numrow!= newrow_M and numcol != newcol_V:
            print("Error! For vector multiplication/division, you must use "
                  "a col of {}".format(newcol_V))
            numcol = self.set_and_check_dimension_isdigit("col")

        return numrow,numcol

    def set_and_check_dimension_isdigit(self, type):
        ''' Checks if the user input for rows/columns is valid, and sets it
            Passed: dimension type (string)
            Returns: Number of row/col (int)
        '''
        num = input("How many " + type + "s do you want: ").strip()

        while True:
            if num.isdigit() and int(num) != 0:
                num = int(num)
                break

            else:
                print("Invalid number of " + type +"s")
                num = input("How many " + type + "s do you want: ").strip()

        return num

    def generate_user_matrices(self, numrow, numcol):
        ''' Creates and appends current matrix to list of previous matrices
            Passed: Number of rows (int), Number of columns (int)
            Returns: None
        '''
        matrix_list = []

        for row in range(numrow):
            matrix_list.append([])

            for col in range(numcol):
                fail = True
                while fail: # Loop continues the correct inputs are given
                    try:
                        real, imaginary = input("Enter real and imaginary "
                        "number on row " + str(row + 1) + " and col " + \
                        str(col + 1)+" (separated with space or tab): ").split()

                    except ValueError:
                        print("Error! Two numbers required")
                        continue

                    try:
                        if float(real) % 1 == 0:
                            real = int(float(real))
                        else:
                            real = float(real)

                        if float(imaginary) % 1 == 0:
                            imaginary = int(float(imaginary))
                        else:
                            imaginary = float(imaginary)

                        fail = False # Make fail equal false if no error

                    except ValueError:
                         print("Valid number was not given for real/imaginary")

                complexnum = [real, imaginary]
                matrix_list[row].append(complexnum)

        self._matrices.append(main.Matrix(matrix_list))

    def resultant_matrix_validation(self):
        ''' Calculate resultant matrix and check for errors
            Passed: None
            Returns: Valid resultant (bool)
        '''
        is_valid=True

        # Ask user if they want to multiply/divide current matrix by previous
        while True:
            mul_or_div = input("Do you want multiply or divide "
                               "(M or D) ").upper().strip()

            if mul_or_div in ["M","MULTIPLY","D","DIVIDE"]: break
            else: print("Invalid input, please choose (M/D)")

        # Calculations are performed on resultant_matrix_valid first in case
        # of an error.
        resultant_matrix_valid = self._resultant_matrix

        if mul_or_div in ["M", "MULTIPLY"]:
            resultant_matrix_valid *= self._matrices[-1]

        else:
            resultant_matrix_valid /= self._matrices[-1]

        # if there is a failure in calculating,
        # a custom message will return from Calculator class
        if type(resultant_matrix_valid) is str: # if not valid
            self._matrices.pop() # remove current matrix from matrices list

            print("Matrix has been removed. Please continue.\n")
            is_valid=False

        # If no error, assign resultant_matrix_valid to self.resultant_matrix
        else:
            self._resultant_matrix = resultant_matrix_valid

        return is_valid

    def print_current_result(self):
        ''' Check if user wants to print current result before continuing
            Passed: None
            Returns: If user has printed (str)
        '''
        print_current = " "
        while print_current not in ["N","NO","Y","YES"]:
            print_current = input("Do you want to print the current resultant "
            "matrix of previous matrices before you continue ").upper().strip()

            if print_current in ['Y','YES']:
                print("Resultant ", self._resultant_matrix)

            elif print_current not in ['N','NO']:
                print("Invalid input, please choose (Y/N) ")

        return print_current

    def mul_another_matrix(self, print_current):
        ''' Checks if user wants to multiply another matrix to the result.
            If not, return result if not already returned previously
            Passed: if user had previously printed the result (str)
            Returns: If user wants to multiply result by another matrix (str)
        '''
        another_matrix = " "
        while another_matrix not in ["N","NO","Y","YES"]:
            another_matrix = input("Do you want to add another matrix to the "
                                   "multiplication(Y/N) ").upper().strip()

            if another_matrix in ['N','NO']:
                if (print_current in ['N','NO']):
                    print("Resultant ", self._resultant_matrix)

            elif another_matrix not in ['Y','YES']:
                print("Invalid input, please choose (Y/N) ")

        return another_matrix

    if "pydevd" in sys.modules: # Run code only in debug mode
        def __del__(self):
            print('Destructor called, UI deleted.')