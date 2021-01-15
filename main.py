################################################################################
 # Project:  Complex Number and Matrix Calculator                             #
 #                                                                            #
 # Name:          Jonas Chianu                                                #
 # File:          main.py                                                     #
 # Purpose:       Contains the main function and the complex number classes.  #
 # Description:   Entry for the program, including the main function.         #
 #                Creates complex numbers and matrices, and performs          #
 #                arithmetic operations on them.                              #
################################################################################

import sys # Importing system module
import math # Importing math module to access mathematical functions
import user # Importing user.py file

def main():
    ''' This is the main function
    Passed: None
    Returns: None
    '''

    # Creating matrix of complex numbers. [real, imaginary]
    #                                     -> ComplexNumber(real, imaginary)
    # matrix_1 = Matrix([ [ [1, 1] , [2, 0] ] ,
    #                   [ [0, 0] , [2, 5] ] ])
    # matrix_2 = Matrix([ [ [5, -5]  , [0, -2]    ] ,
    #                   [ [0, 4.2] , [-11.1, 0] ] ])

    # Resulting matrix from multiplication of two matrices.
    # matrix_1x2 = matrix_1 * matrix_2 # matrix_1x2 = matrix_1 X matrix_2

    # Printing out matrix for easy reading
    # print(matrix_1x2)

    # Creating matrix of complex numbers. [real, imaginary]
    #                                     -> ComplexNumber(real, imaginary)
    matrix_1 = Matrix([ [ [3, 4] , [2, 0] , [5, 3] ] ,
                      [ [0, 1] , [2, 5], [2, 1] ] ])
    matrix_2 = Matrix([ [ [8, -2]  , [0, -2], [4, -2] ] ,
                      [ [2, 3] , [-11.1, 0], [2, 3] ] ])

    # Resulting matrix from multiplication of two matrices.
    matrix_12 = matrix_1 / matrix_2 # matrix_12 = matrix_1 / matrix_2

    print(matrix_12) # Printing out matrix for easy reading

    another_calc = "Y"
    # Ask the user if that want to do another set of calculation.
    # If so, the program is restarted.
    while another_calc in ['Y','YES']:
        # Take in user request and generate requested output
        user.UI().return_user_request()

        # If user inputs an invalid response for another calculation,
        # ask the user again
        while True:
            another_calc = input("Do you want to do another calculation "
                                 "(Y/N) ").upper().strip()

            if another_calc in ['N','NO','Y','YES']:
                break

            print("Invalid input, please choose (Y/N)")

        print('---------------------------------------------------------------')

    # For pausing executable window
    input("Press Enter to continue...")

class Calculator():
    ''' This class stores calculator methods for complex number and matrices '''
    _real=0
    _imaginary=0
    _matrix=[]

    @property
    def polar_mag(self):
        ''' Returns the polar magnitude of the complex number
            Passed: None
            Returns: Polar magnitude of complex numbers (number)
        '''
        polar_mag = math.sqrt(self._real ** 2 + self._imaginary ** 2)
        return polar_mag

    @property
    def polar_phase(self):
        ''' Returns the polar phase of the complex number
            Passed: None
            Returns: Polar phase of complex numbers (number)
        '''
        polar_phase = math.atan2(self._imaginary, self._real)
        return polar_phase

    def __add__(self, other):
        ''' Returns the sum of two complex number
            Passed: self (ComplexNumber), other (ComplexNumber)
            Returns: Sum of complex numbers (ComplexNumber)
        '''
        real_add = self._real + other._real
        imaginary_add = self._imaginary + other._imaginary

        return ComplexNumber(real_add, imaginary_add)

    def __sub__(self, other):
        ''' Returns the difference of two complex number
            Passed: self (ComplexNumber), other (ComplexNumber)
            Returns: Difference of complex numbers (ComplexNumber)
        '''

        real_add = self._real - other._real
        imaginary_add = self._imaginary - other._imaginary

        return ComplexNumber(real_add, imaginary_add)

    def __mul__(self, other):
        ''' Method is able to do complex numbers multiplication,
            matrices multiplication and vector multiplication
            Passed: self (ComplexNumber), other (ComplexNumber);
                    or self (Matrix), other (Matrix)
            Returns: Error message (str);
                     or Multiplication of two complex numbers (ComplexNumber);
                     or Multiplication of two matrices (Matrices)
        '''

        # Checks to see if method arguments are of class ComplexNumber
        # or class Matrix
        if type(self) == ComplexNumber:
            result = self.complex_mul(other)
            return result

        else:
            result = self.matrix_mul(other)
            return result

    def complex_mul(self,other):
        ''' Method is able to do complex numbers multiplication
            Passed: self (ComplexNumber), other (ComplexNumber)
            Returns: Multiplication of two complex numbers (ComplexNumber);
        '''
        # Complex multiplication: (a + bi)(c + di) = (ac - bd) + (bc + ad)i
        real_multiply = (self._real * other._real) \
                        - (self._imaginary * other._imaginary)
        imaginary_multiply = (self._imaginary * other._real) \
                             + (self._real * other._imaginary)

        return ComplexNumber(real_multiply, imaginary_multiply)

    def matrix_mul(self,other):
        ''' Method is able to do matrices multiplication
            and vector multiplication
            Passed: self (Matrix), other (Matrix)
            Returns: Error message (str); or Multiplication of two matrices (Matrices)
        '''
        # Ask the user for their chosen multiplication type (Matrix or Vector)
        multiply_type = user.UI().multiply_type()

        # For matrix multiplication, checks that the first matrix is a
        # mxn matrix and the second matrix is a nxp matrix
        while multiply_type in ['M', 'MATRIX'] and \
                len(self._matrix[0]) != len(other._matrix):
            print("Not possible! The number of columns in the first matrix is "
                  "not the same as the number of rows in the second matrix.")

            # Ask the user if they want to delete the matrix
            delete_matrix = user.UI().delete_matrix_prompt()
            if delete_matrix in ['Y', 'YES']: return ''

            multiply_type = user.UI().multiply_type()

        # For vector multiplication,
        # checks that both matrices have the same rows and columns
        while multiply_type in ['V', 'VECTOR'] and \
                ((len(self._matrix) != len(other._matrix)) or
                 (len(self._matrix[0]) != len(other._matrix[0]))):
            print("Error! The number of rows and columns in the first matrix "
                   "has to be equal to the number of rows and columns " 
                   "in the second matrix.")

            delete_matrix=user.UI().delete_matrix_prompt()
            if delete_matrix in ['Y', 'YES']: return ''

            multiply_type = user.UI().multiply_type()

        result = [] #Contain matrix in List form

        for row in range(len(self._matrix)):
            result.append([])

            for col in range(len(other._matrix[0])):
                result[row].append([])

                # creating a complex object for each position
                # in new matrix
                compform = ComplexNumber()

                if multiply_type in ['M', 'MATRIX']:  # Matrix multiplication
                    # k is used for iterating through additions of two
                    # complex numbers products in order to get the complex
                    # number at position [row][col] for the new matrix
                    for k in range(len(self._matrix[0])):
                        compform += self._matrix[row][k] * other._matrix[k][col]

                else:  # Vector multiplication
                    compform = self._matrix[row][col] * other._matrix[row][col]

                # converting compform to a list of real and imaginary
                result[row][col].extend([compform.get_real(),
                                         compform.get_imaginary()])

        return Matrix(result)

    def __truediv__(self, other):
        ''' The method is able to do complex numbers division,
            and vector multiplication
            Passed: self (ComplexNumber), other (ComplexNumber);
                    or self (Matrix), other (Matrix)
            Returns: Error message (str);
                     or Division of two complex numbers (ComplexNumber);
                     or Division of two matrices (Matrices)
        '''

        # Checks to see if method arguments are of class ComplexNumber
        # or class Matrix
        if type(self) == ComplexNumber:
            result = self.complex_div(other)
            return result

        else:
            result = self.matrix_div(other)
            return result

    def complex_div(self,other):
        ''' Method is able to do complex numbers division
            Passed: self (ComplexNumber), other (ComplexNumber)
            Returns: Division of two complex numbers (ComplexNumber);
        '''
        other._imaginary *= -1

        new_numerator = self*other
        new_denominator=(other._real)**2 + (other._imaginary)**2

        try:
            # Complex division:
            # (a + bi)/(c + di) = (ac + bd)/(c^2+d^2) + (bc + ad)i/(c^2+d^2)
            real_div = new_numerator._real/new_denominator
            imaginary_div = new_numerator._imaginary /new_denominator

            return ComplexNumber(real_div, imaginary_div)

        except:
            return "Error! You can't divide by zero"

    def matrix_div(self,other):
        ''' Method is able to do  vector division
            Passed: self (Matrix), other (Matrix)
            Returns: Error message (str); or Division of two matrices (Matrices)
        '''
        result = [] #Contain matrix in List form

        if len(self._matrix)!=len(other._matrix) or len(self._matrix[0])!=len(other._matrix[0]):
            print("Error! Matrices don't have the same row or the same column")
            return ""

        for row in range(len(self._matrix)):
            result.append([])

            for col in range(len(other._matrix[0])):
                result[row].append([])

                # creating a complex object for each position
                # in new matrix
                compform = ComplexNumber()
                compform = self._matrix[row][col] / other._matrix[row][col]

                try:
                    # converting compform to a list of real and imaginary
                    result[row][col].extend([compform.get_real(),
                                         compform.get_imaginary()])

                except:
                    print("Error! You can't divide by zero")
                    return ""

        return Matrix(result)

    if "pydevd" in sys.modules: # Run code only in debug mode
        def __del__(self):
            print('Destructor called, Calculator deleted.')

class Matrix(Calculator):
    ''' This class is used to represent matrices '''

    def __init__(self, matrix_list):
        ''' Initializes the matrix with a matrix_list (Constructor)
            Passed: Matrix list (List)
            Returns: None
        '''

        invalid_matrix=False

        # Checks that the len of each row are the same
        for row in range(len(matrix_list)-1):
            if len(matrix_list[row]) != len(matrix_list[row+1]):
                invalid_matrix=True
                break

        if invalid_matrix:
            print("Error: Invalid Matrix! Rows have different sizes\n")

        else:
            self._matrix=[]
            k=0 # Used to access the numbers in inner most list [a,b]

            for row in range(len(matrix_list)):
                self._matrix.append([])

                for col in range(len(matrix_list[0])):
                    self._matrix[row].append(ComplexNumber(
                        matrix_list[row][col][k], matrix_list[row][col][k+1]))

    def get_matrix(self):
        ''' Returns the matrix
            Passed: None
            Returns: matrix (List)
        '''
        return self._matrix

    def __repr__(self):
        ''' Return a string representation of matrix.
            Passed: None
            Returns: String representation of matrix (String)
        '''
        if len(self._matrix[0]) == 1:
            # If you want to multiply a matrix and a vector, the vector must be
            # defined as a one column matrix and must be listed vertically
            print('Vector = \n') # A matrix with one column
        else:
            print('Matrix = \n')

        return_str = ''

        for row in self._matrix:

            for col in row:
                return_str += "{:^20}".format(col.__repr__())

            return_str += "\n\n"

        return return_str

    if "pydevd" in sys.modules:
        def __del__(self):
            print('Destructor called, Matrix deleted.')

class ComplexNumber(Calculator):
    ''' This class is used to represent complex numbers '''
    _complex_number=[]

    def __init__(self, real=0, imaginary=0):
        ''' Initializes the complex number with real and imaginary numbers
            (Constructor)
            Passed: Real number (number); Imaginary numbers (number)
            Returns: None
        '''
        self._real=real
        self._imaginary=imaginary
        self._complex_number=[real,imaginary]

    def set_complex_number(self, real, imaginary):
        ''' Writes the real and imaginary numbers to the complex number
            Passed: Real number (number); Imaginary numbers (number)
            Returns: None
        '''
        self._complex_number=[real,imaginary]
        self._real = real
        self._imaginary = imaginary

    def get_complex_Number(self):
        ''' Returns the complex number
            Passed: None
            Returns: Complex number (List)
        '''
        return self._complex_number

    def get_real(self):
        ''' Returns the real part of the complex number
            Passed: None
            Returns: Real number (number)
        '''
        return self._real

    def get_imaginary(self):
        ''' Returns the imaginary part of the complex number
            Passed: None
            Returns: Imaginary number (number)
        '''
        return self._imaginary

    def __repr__(self):
        ''' Return a string representation of the complex number.
            Passed: None
            Returns: String representation of complex number (String)
        '''
        real_round = round(self._real,4)
        imaginary_round = round(self._imaginary, 4)

        if self._real==0 and self._imaginary==0:
            return '0'

        elif self._real==0:
            return str(imaginary_round)+'i'

        elif self._imaginary==0:
            return str(real_round)

        elif self._imaginary < 0:
            return str(real_round) + ' - ' + str(abs(imaginary_round))+'i'

        else:
            return str(real_round) + ' + ' + str(imaginary_round)+'i'

    if "pydevd" in sys.modules:
        def __del__(self):
            print('Destructor called, ComplexNumber deleted.')

# Main function call
if __name__ == '__main__':
    main()