from scipy import stats
import numpy as np

# Condiciones iniciales
NS = 0
N = 0
NT = 0
TPLL = 0
TPS = 0
TPSI = 0
T = 0

def establecer_condiciones_iniciales():
    print("Ingrese cantidad de puestos intermitentes:")
    N = int(input())
    TPS = [0 for _ in range(21)]
    TPSI = [0 for _ in range(N)]

def calcular_menor_tps(numeroPuesto, esIntermitente):
    #TODO
    return 0

def generar_intervalo_arribos():
    parametro_alpha = 0.68432
    parametro_beta = 0.67252
    valor_minimo = 10
    valor_maximo = 18

    valor = stats.beta.rvs(parametro_alpha, parametro_beta)
    return valor_minimo + valor * (valor_maximo - valor_minimo)


def procesar_llegada():
    T = TPLL
    IA = generar_intervalo_arribos()
    TPLL = T + IA
    NS = NS + 1
    NT = NT + 1
    
    return 0

# Programa principal
def main():
    numeroPuesto = 0
    esIntermitente = 0

    establecer_condiciones_iniciales()

    # Genero 58 eventos de llegada
    for i in range(58):
        MENOR_TPS = calcular_menor_tps(numeroPuesto, esIntermitente)
        
        if(TPLL <= MENOR_TPS):
            procesar_llegada()
        elif (esIntermitente == 0):
            # es una salida de un puesto fijo
            return 0
        else:
            # es una salida de un puesto intermitente
            return 0
    

if __name__ == "__main__":
    main()



    