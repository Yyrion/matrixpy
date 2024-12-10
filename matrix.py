import sys

class Matrix:

    def __init__(self, content):
        for row in content:
            if len(row)!=len(content[0]):
                print("Matrix rows must be the same size", file=sys.stderr)
                raise ValueError
        self.__content = [[content[i][j] for j in range(len(content[0]))] for i in range(len(content))]
        self.__row = len(content)
        self.__col = len(content[0])

    @classmethod
    def identity(cls, n:int):
        return Matrix([[1 if j == k else 0 for j in range(n)]for k in range(n)])
    
    @classmethod
    def nullMatrix(cls, n:int):
        return Matrix([[0 for _ in range(n)] for _ in range(n)])

    @classmethod
    def vandermondeMatrix(cls, n:int, *args:float):
        return Matrix([[args[k]**j for j in range(n)]for k in range(len(args))])

    def getContent(self):
        return self.__content

    def getRow(self):
        return self.__row
    
    def getCol(self):
        return self.__col
    
    def invert(self):
        if abs(self) != 0:
            if self.__col == self.__row:
                print(self)
                copy = [[self.__content[i][j] for j in range(len(self.__content[0]))] for i in range(len(self.__content))]
                print(Matrix(copy))
                inverse = Matrix.identity(len(copy)).getContent()

                pos = 0
                for rw in range(len(copy)):
                    minrw = rw
                    while copy[rw][pos] == 0:
                        minrw += 1
                        copy[rw], copy[minrw] = copy[minrw], copy[rw]
                        inverse[rw], inverse[minrw] = inverse[minrw], inverse[rw]
                    w = copy[rw][pos]
                    copy[rw] = [copy[rw][i]/w for i in range(len(copy[rw]))]
                    inverse[rw] = [inverse[rw][i]/w for i in range(len(copy[rw]))]

                    for k in range(rw, len(copy)):
                        if (k>rw):
                            w = copy[k][pos]/copy[rw][pos]

                            for i in range(len(copy[k])):
                                copy[k][i] = copy[k][i]-w*copy[rw][i]
                                inverse[k][i] = inverse[k][i]-w*inverse[rw][i]
                    pos += 1

                for rw in range(len(copy)-1, -1, -1):
                    for minrw in range(rw):
                        w = copy[minrw][rw]
                        copy[minrw] = [copy[minrw][j] - copy[rw][j]*w for j in range(len(copy[minrw]))]
                        inverse[minrw] = [inverse[minrw][j] - inverse[rw][j]*w for j in range(len(inverse[minrw]))]

                return Matrix(inverse)
            
            else:
                #Gestion des matrices non carrées
                print("Non squared matrix does not have an inverse.")
                raise ValueError
        else:
            #Gestion du cas où le déterminant est nul
            raise ZeroDivisionError

    def __abs__(self):
        if self.__col != self.__row:
            print("Matrix for det must have the same number of row and column", file=sys.stderr)
            raise ValueError
        if self.__col == 2:
            return self.__content[0][0]*self.__content[1][1] - self.__content[0][1]*self.__content[1][0]
        else:
            result = 0
            for i in range(len(self.__content[0])):
                if self.__content[0][i] != 0:
                    newMat = [[self.__content[k][j] for j in (tuple(range(i)) + tuple(range(i+1, self.__col)))] for k in range(1, self.__row)]
                    if (i%2 == 0):
                        pos = 1
                    else:
                        pos = -1
                    result += pos*self.__content[0][i] * abs(Matrix(newMat))
            return result

    def __str__(self):
        result = ""
        for row in self.__content:
            result += "[ "
            for e in row:
                result += f"{e} "
            result += "] \n"
        return result
    
    def __mul__(self, other): 
        if not isinstance(other, Matrix):
            if not isinstance(other, int) and not isinstance(other, float):
                print("You can only multiply a matrix by another matrix", file=sys.stderr)
                raise ValueError
            return Matrix([[self.__content[k][j]*other for j in range(self.__col)] for k in range(self.__row)])
        if self.__col != other.getRow():
            print("Matrix 1 must have the same number of col than the other has of row.", file=sys.stderr)
            raise ValueError

        def getElement(k, j, content1, content2):
            temp = 0
            for i in range(self.__col):
                temp += content1[k][i] * content2[i][j]
            return temp
        
        otherContent = other.getContent()
        resultContent = [[(getElement(k, j, self.__content, otherContent)) for j in range(other.getCol())] for k in range(self.__row)]

        return Matrix(resultContent)

    def __add__(self, other):
        if not isinstance(other, Matrix):
            print("You can only add a matrix by another matrix", file=sys.stderr)
            raise ValueError
        if self.__col != other.getCol() or self.__row != other.getRow():
            print("When adding one matrix by another, the two matrix must have the same size", file=sys.stderr)
            raise ValueError
        otherContent = other.getContent()
        resultContent = [[(otherContent[k][j] + self.__content[k][j] ) for j in range(self.__col)] for k in range(self.__row)]

        return Matrix(resultContent)
    
    def __sub__(self, other):
        if not isinstance(other, Matrix):
            print("You can only substract a matrix by another matrix", file=sys.stderr)
            raise ValueError
        if self.__col != other.getCol() and self.__row != other.getRow():
            print("When substracting one matrix by another, the two matrix must have the same size", file=sys.stderr)
            raise ValueError
        
        otherContent = other.getContent()
        resultContent = [[(self.__content[k][j] - otherContent[k][j]) for j in range(self.__col)] for k in range(self.__row)]

        return Matrix(resultContent)

    def __eq__(self, value):
        if not isinstance(value, Matrix):
            return False
            
        if value.getCol() != self.__col or value.getRow() != self.__row:
            return False
        
        otherContent = value.getContent()
        for k in range(self.__row):
            for j in range(self.__col):
                if otherContent[k][j] != self.__content[k][j]:
                    return False

        return True

