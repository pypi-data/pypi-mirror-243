from pejecoins import suma, mxm, mxesc, ProCruz, Det3x3, Det2x2, Transpuesta, SumaVectores
import __init__ as test

print("""
Que prueba va a realizar:
-----
1) Suma => suma
2) Multiplicacion de matrices => MxM
3) Multiplicacion de matriz por vector => MxE
4) Producto Cruz    =>  ProCruz
5) Determinante 3x3  =>  Det3x3
6) Determinante 2x2  =>  Det2x2
7) Matriz Transpuesta   => Transpuesta
8) Suma de Vectores    => SumaVectores
-----
      
""")

while True: #Bucle para realizar varias prubas con control
    
    usuario = str(input("Prueba: "))

    if usuario == "suma": #Simple de suma
        resultado = test.suma(2,3)
        print(resultado)
         
    elif usuario == "MxM": #Multiplicacion de matrices
        a = [[-1, 0, 1], [7, 3, -(13/2)], [3, (1/2), -(5/2)]]
        b = [[2, 4, 5], [2, 3, 4], [3, 4, 6]]

        multiplicacion = test.mxm(a, b)
        print(multiplicacion)

    elif usuario == "MxE": #Matriz por escalar
        a = [[-1, 0, 3, 4], [7, 3, 5, 6], [3, 2, 4, 3]]
        b = 2
        resultado = test.mxesc(a,b)
        print(resultado)

    elif usuario == "ProCruz": #Matriz por vector
        a = [3, -1, 1]
        b = [1, 2, -1]
        resultado = test.ProCruz(a, b)
        print(resultado)
        print(f"{resultado[0]}i {resultado[1]}j {resultado[2]}k")

    elif usuario == "Det3x3":
        a = [[1, -2, 1], [4, 2, 1], [3, -1, 2]]
        resultado = test.Det3x3(a)
        print(resultado)

    elif usuario == "Det2x2":
        a = [[3, 3], [3, 5]]
        resultado = test.Det2x2(a)
        print(resultado)
    
    elif usuario == "Transpuesta":
        a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        resultado = test.Transpuesta(a)
        print(resultado)
    
    elif usuario == "SumaVectores":
        a = [1, 2, 3]
        b = [4, 5, 6]
        resultado = test.SumaVectores(a,b)
        print(resultado)
    
    else:
        print("Comando Equivocado. Intenta de nuevo.")