class Matrix:

    def __init__(self, content):
        for row in content:
            assert len(row)==len(content[0]), "Matrix rows must be the same size"
        self.__content = content
        self.__row = len(content)
        self.__col = len(content[0])

    def getContent(self):
        return self.__content

    def getRow(self):
        return self.__row
    
    def getCol(self):
        return self.__col
    
    def det(self):
        assert self.__col == self.__row, "Matrix for det must have the same number of row and column"
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
                    result += pos*self.__content[0][i] * Matrix(newMat).det()
            return result

    def diagonal(self):
        assert False, "Method not finished"
        p = 0
        d = 0
        q = 0
        return (p, d, q)

    def __str__(self):
        result = ""
        for row in self.__content:
            result += "[ "
            for e in row:
                result += f"{e} "
            result += "] \n"
        return result
    
    def __mul__(self, other):
        assert type(other)==Matrix, "You can only multiply a matrix by another matrix"
        assert self.__col == other.getRow(), "Matrix 1 must have the same number of col than the other has of row."

        def getElement(k, j, content1, content2):
            temp = 0
            for i in range(self.__col):
                temp += content1[k][i] * content2[i][j]
            return temp
        
        otherContent = other.getContent()
        resultContent = [[(getElement(k, j, self.__content, otherContent)) for j in range(other.getCol())] for k in range(self.__row)]

        return Matrix(resultContent)

    def __add__(self, other):
        assert type(other)==Matrix, "You can only multiply a matrix by another matrix"
        assert self.__col == other.getCol() and self.__row == other.getRow(), "When adding one matrix by another, the two matrix must have the same size"
        otherContent = other.getContent()
        resultContent = [[(otherContent[k][j] + self.__content[k][j] ) for j in range(self.__col)] for k in range(self.__row)]

        return Matrix(resultContent)
    
    def __sub__(self, other):
        assert type(other)==Matrix, "You can only multiply a matrix by another matrix"
        assert self.__col == other.getCol() and self.__row == other.getRow(), "When substracting one matrix by another, the two matrix must have the same size"
        otherContent = other.getContent()
        resultContent = [[(self.__content[k][j] - otherContent[k][j]) for j in range(self.__col)] for k in range(self.__row)]

        return Matrix(resultContent)

    def __eq__(self, value):
        assert type(value)==Matrix, "You can only multiply a matrix by another matrix"
        if value.getCol != self.__col or value.getRow != self.__row:
            return False
        
        otherContent = value.getContent()
        for k in range(self.__row):
            for j in range(self.__col):
                if otherContent[k][j] != self.__content[k][j]:
                    return False

        return Matrix(True)
    
m = Matrix([[1,2,3], [2,6,5], [9,1,2]])
print(m)
print(m.det())