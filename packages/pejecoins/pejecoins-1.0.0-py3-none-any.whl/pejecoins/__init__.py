#Suma sencilla
def suma(x,y):
    resultado = x + y
    return resultado

#Multiplicacion de matrices
def mxm(a,b):
    resultados = []

    c = 0
    i = 0
    j = 0
    n = 0
    p = 0
    print(f"Se realiza una multiplicación de las matices {a} y {b}: ")
    for i in range(len(a)):  # Iterar sobre las filas de a
        fila_resultante = []  # Inicializar una lista para la fila resultante actual
        for j in range(len(b[p])):  # Iterar sobre las columnas de b
            c = 0
            for k in range(len(a[n])):
                posicionA = a[i][k]
                posicionB = b[k][j]
                c += posicionA * posicionB
            fila_resultante.append(c)  # Agregar el resultado a la fila resultante actual
        resultados.append(fila_resultante)  # Agregar la fila resultante a resultados
    for row in resultados: #Itera para mostrar la matriz
        for element in row:
            print(f"({element}", end=")" ) 
        print()
    return resultados
    

#Multiplicacion de matris por escalar

def mxesc (a,b):
    c = 0
    iterar = len(a[0]) #Declaro en una varaiable la cantidad de columbas que tiens
    resultados = []
    for i in a: #Itero por las filas
        j = 0
        
        for columna in iterar:#Itero por las columnas
            lista = a[c][j]
            lista = lista * b
            print(f"({lista}", end=")")
            resultados.append(lista)
            j = j + 1 #Incrementeo para cambiar de columna
        print()    
        c = c + 1 #Incremento para cambiar de fila
    
    return resultados

#Prductocruz
def ProCruz (a, b):
    resultado = []
    P_1 = (a[1] * b[2]) - (a[2] * b[1])
    resultado.append(P_1)
    P_2 = (a[2] * b[0]) - (a[0] * b[2])
    resultado.append(P_2)
    P_3 = (a[0] * b[1]) - (a[1] * b[0])
    resultado.append(P_3)
    return resultado

#Determinate de matriz 3x3
def Det3x3(lista):
    resultado = 0

    for i in range(3):
        a1 = lista[0][i]
        a2 = lista[1][(i + 1) % 3]
        a3 = lista[2][(i + 2) % 3]

        resultado += (a1 * a2 * a3)

    for i in range(3):
        a1 = lista[0][i]
        a2 = lista[1][(i - 1) % 3]
        a3 = lista[2][(i - 2) % 3]

        resultado -= (a1 * a2 * a3)

    return resultado

def Det2x2(lista):
    primerResultado = lista[0][0] * lista[1][1]
    segundoResultado = lista[0][1] * lista[1][0]

    determinante = primerResultado - segundoResultado

    return determinante

def Transpuesta(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    
    transpuesta = []
    for i in range(columnas):
        filaTranspuesta = [0] * filas
        transpuesta.append(filaTranspuesta)  
    
    for i in range(filas):
        for j in range(columnas):
            transpuesta[j][i] = matriz[i][j]
    return transpuesta

def SumaVectores(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("Los vectores deben tener la misma longitud para ser sumados.")
    
    suma = []
    for i in range(len(v1)):
        suma.append(v1[i] + v2[i])
    
    return suma