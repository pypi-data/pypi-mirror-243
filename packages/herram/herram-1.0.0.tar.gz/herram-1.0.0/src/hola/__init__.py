class Matrix():
    def _init_(self, m=3, n=3, matrix=None):
        self.matrix=[]
        self.m=m
        self.n=n

        if not matrix:
            for i in range(m):
                row_array=[]
                for j in range(n):
                    value=float(input(f"valor {i+1},{j+1}: "))
                    row_array.append(value)
                self.matrix.append(row_array)
        else:
            self.matrix=matrix

    def print_matrix(self, msg=""):
        print(f"\n Matrix: {msg}")
        for m in self.matrix:
            for n in m:
                print(n, end=", ")
            print("")
        print("")
    
    def sum_matrix(self, matrix):
        if self.m!=matrix.m or self.n!=matrix.n:
            return "No es posible "
        matrix_array=[]
        for m in range(self.m):
            h=[]
            for n in range(self.n):
                h.append(self.matrix[m][n]+matrix.matrix[m][n])
            matrix_array.append(h)
        sum_matrix=Matrix(self.m, self.n, matrix_array)
        return sum_matrix

    def rest_matrix(self, matrix):
        if self.m!=matrix.m or self.n!=matrix.n:
            return "No es posible "
        matrix_array=[]
        for m in range(self.m):
            h=[]
            for n in range(self.n):
                h.append(self.matrix[m][n]-matrix.matrix[m][n])
            matrix_array.append(h)
        sum_matrix=Matrix(self.m, self.n, matrix_array)
        return sum_matrix

    def multiplicate_scalar(self, num):
        result_matrix=self.matrix
        for m in range(self.m):
            for n in range(self.n):
                result_matrix[m][n]*=num
        result_matrix=Matrix(self.m, self.n, result_matrix)
        return result_matrix
    
    def multiplicate_matrix(self, matrix):
        if self.n!=matrix.m:
            return "It isn't possible"
        ans_matrix=[]
        for m in range(self.m):
            ans_row=[]
            for matrix_n in range(matrix.n):
                value=0
                for n in range(self.n):
                    first_number=self.matrix[m][n]
                    second_number=matrix.matrix[n][matrix_n]
                    value+=first_number*second_number
                ans_row.append(value)
            ans_matrix.append(ans_row)
        ans_matrix=Matrix(self.m, matrix.n, ans_matrix)
        return ans_matrix
        
    def gauss_jordan(self):
        gauss_jordan_fu=Matrix(self.m, self.n, self.matrix)
        gauss_jordan_fu.print_matrix("Inicializar gauss jordan")
        for i in range(len(gauss_jordan_fu.matrix)):
            div=gauss_jordan_fu.matrix[i][i]**-1
            for j in range(len(gauss_jordan_fu.matrix[i])):
                gauss_jordan_fu.matrix[i][j]*=div
                gauss_jordan_fu.print_matrix(f"Multiplicacion por {div} para pivote")

            for m in range(len(gauss_jordan_fu.matrix)):
                value_pivot=gauss_jordan_fu.matrix[i][i]
                if i==m:
                    continue
                else:
                    value_rest=gauss_jordan_fu.matrix[m][i]/value_pivot
                    for n in range(len(gauss_jordan_fu.matrix[m])):
                        gauss_jordan_fu.print_matrix(f"Resta de {m},{n}: {gauss_jordan_fu.matrix[m][n]} - {gauss_jordan_fu.matrix[i][n]*value_rest}")
                        gauss_jordan_fu.matrix[m][n]-=gauss_jordan_fu.matrix[i][n]*value_rest
        return gauss_jordan_fu
       
def inicializar():
    num_matrices=int(input("how many matrices?"))
    matrices=[]
    ans=None
    for i in range(num_matrices):
        m=int(input("m: "))
        n=int(input("n: "))
        matrix= Matrix(m,n)
        matrices.append(matrix)

    action=int(input("Choose action by number: (Scalar, Multiplicate matrix, Gauss-Jordan, Sum, rest): \n"))

    if action==1:
        for matrix in matrices:
            num=int(input("Scalar: "))
            matrix.multiplicate_scalar(num)
            matrix.print_matrix()
    elif action==2:
        ans=matrices[0]
        for i in range(len(matrices)-1):
            ans=ans.multiplicate_matrix(matrices[i+1])
            matrix.print_matrix()
    elif action==3:
        matrices[0].gauss_jordan().print_matrix("Gauss-Jordan")
        matrix.print_matrix()
    elif action==4:
        ans=matrices[0]
        for i in range(len(matrices)-1):
            ans=ans.sum_matrix(matrices[i+1]).print_matrix()
            matrix.print_matrix()
    elif action==5:
        matrices[0].rest_matrix(matrices[1]).print_matrix()
        matrix.print_matrix()