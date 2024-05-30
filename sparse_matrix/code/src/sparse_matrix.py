class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        self.matrix = {}
        if matrixFilePath:
            self.load_from_file(matrixFilePath)
        elif numRows is not None and numCols is not None:
            self.numRows = numRows
            self.numCols = numCols
    
    def load_from_file(self, matrixFilePath):
        with open(matrixFilePath, 'r') as file:
            self.numRows = int(file.readline().split('=')[1])
            self.numCols = int(file.readline().split('=')[1])
            for line in file:
                line = line.strip()
                if line:
                    row, col, value = map(int, line.strip('()').split(','))
                    if value != 0:
                        self.matrix[(row, col)] = value
    
    def get_element(self, row, col):
        return self.matrix.get((row, col), 0)
    
    def set_element(self, row, col, value):
        if value != 0:
            self.matrix[(row, col)] = value
        elif (row, col) in self.matrix:
            del self.matrix[(row, col)]
    
    def add(self, other):
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        for key, value in self.matrix.items():
            result.set_element(*key, value + other.get_element(*key))
        for key, value in other.matrix.items():
            if key not in result.matrix:
                result.set_element(*key, value)
        return result
    
    def subtract(self, other):
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        for key, value in self.matrix.items():
            result.set_element(*key, value - other.get_element(*key))
        for key, value in other.matrix.items():
            if key not in result.matrix:
                result.set_element(*key, -value)
        return result
    
    def multiply(self, other):
        result = SparseMatrix(numRows=self.numRows, numCols=other.numCols)
        for (i, j), value in self.matrix.items():
            for k in range(other.numCols):
                if (j, k) in other.matrix:
                    result.set_element(i, k, result.get_element(i, k) + value * other.get_element(j, k))
        return result

# Example usage:
# matrix1 = SparseMatrix('matrix1.txt')
# matrix2 = SparseMatrix('matrix2.txt')
# result = matrix1.add(matrix2)
# result = matrix1.subtract(matrix2)
# result = matrix1.multiply(matrix2)
