import math
from math import sqrt
import numbers
import numpy as np

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
            
        if self.h <= 1 and self.w <= 1:
            return self.g[0][0]                       
        return self.g[0][0]*self.g[1][1] - self.g[0][1]*self.g[1][0]
    
    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """

        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")

        sum = 0

        # For loop within a for loop to iterate over the matrices
        for row in range(len(self.g)):
            sum += self.g[row][row]
    
        return sum
    
#     no idea what happened here. had this function done long back, seems like it wasn't saved, redid it Soon :)

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")

        # TODO - your code here
        inverse_matrix = self.g.copy()
        
        if len(self.g) == 1:
            inverse_matrix = []
            inverse_matrix.append(1 / self.g[0][0])
            return Matrix([inverse_matrix])
        elif len(self.g) == 2:
            # If the matrix is 2x2, check that the matrix is invertible
            if self.g[0][0] * self.g[1][1] == self.g[0][1] * self.g[1][0]:
                raise ValueError('The matrix is not invertible.')
            else:
                # Calculate the inverse of the square 1x1 or 2x2 matrix.
                a = self.g[0][0]
                b = self.g[0][1]
                c = self.g[1][0]
                d = self.g[1][1]

                factor = 1 / (a * d - b * c)

                inverse = [[d, -b],[-c, a]]

                for i in range(len(inverse)):
                    for j in range(len(inverse[0])):
                        inverse_matrix[i][j] = factor * inverse[i][j]
    
        return Matrix(inverse_matrix)
    
    # code taken from udacity lessons

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        # TODO - your code here
        
        gcopy = self.g        
        matrix_transpose = []
        # Loop through columns on outside loop
        for c in range(len(gcopy[0])):
            new_row = []
            # Loop through columns on inner loop
            for r in range(len(gcopy)):
                # Column values will be filled by what were each row before
                new_row.append(gcopy[r][c])
            matrix_transpose.append(new_row)
            
        # credit for code comes from udacity lessons

        return Matrix(matrix_transpose)
        
    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    
    def __len__(self): #overload len() as said in https://knowledge.udacity.com/questions/212390
        return self.h
    
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        
        else:
            matrixSum = []        

            # For loop within a for loop to iterate over the matrices
            for r in range(len(self.g)):
                row = [] # reset the list
                for c in range(len(self.g[0])):
                    row.append(self.g[r][c] + other[r][c]) # add the matrices
                matrixSum.append(row)

            return Matrix(matrixSum)
    
    # code taken from coding exercises
        

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        #   
        # TODO - your code here
        #
        
        neg_matrix = zeroes(self.h,self.w)
        
        for r in range(len(self.g)):
            row = [] # reset the list
            for c in range(len(self.g)):
                neg_matrix[r][c] = -self.g[r][c] 
        
        return Matrix(neg_matrix)

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        #   
        # TODO - your code here
        #
        
        matrixSum = []
    
        # matrix to hold a row for appending sums of each element
        row = []
        
        gcopy = self.g

        for r in range(len(gcopy)):
            row = [] # reset the list
            for c in range(len(gcopy[0])):
                row.append(gcopy[r][c] - other[r][c])
            matrixSum.append(row)
    
        return Matrix(matrixSum)
    
    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        #   
        # TODO - your code here
        #
        
        other_matrix = Matrix(other)
        result = zeroes(len(self.g),len(other_matrix[0]))
        
        for X_row in range(len(self.g)):                                  #grab idx of every single row in X            
            for Y_col in range(len(other_matrix[0])):                     #grab idx of every single column in y                
                for Y_row in range(len(other_matrix)):                    #want to grab idx of num. of rows in y so that we can add it
                    result[X_row][Y_col] += self.g[X_row][Y_row] * other_matrix[Y_row][Y_col] 

                    #what we want to do is grab X_row's indexx and multiply it by y_col (remember that # of X_cal = # of y_rows)

        return Matrix(result)
    
    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        matrix_rmul = []
        gcopy = self.g
        if isinstance(other, numbers.Number):
            for r in range(len(gcopy)):
                row = [] # reset the list
                for c in range(len(gcopy[0])):
                    row.append(gcopy[r][c] * other)
                matrix_rmul.append(row)
        return Matrix(matrix_rmul)
            