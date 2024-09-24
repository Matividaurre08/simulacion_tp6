from scipy import stats
import numpy as np

# Condiciones iniciales
NS = 0
K = 0
NT = 0
TPLL = 0
TPS = []
HV = 9999999
TPSI = HV
T = 0
SPS = 0
NI = 0
STA = 0
PEC = 0
PPS = 0
PPSI = 0
TF = 1000

def establecer_condiciones_iniciales():
    global K, HV, TPS
    print("Ingrese cantidad de partidos en cola para agregar un puesto intermitente:")
    K = int(input())
    TPS = [HV for _ in range(21)]

def calcular_menor_tps():
    global HV, TPS
    menor = TPS[0]
    posicion = 0
    for i in range(21):
        if(TPS[i] < menor):
            menor = TPS[i]
            posicion = i
    return menor, posicion

def generar_intervalo_arribos():
    parametro_alpha = 0.68432
    parametro_beta = 0.67252
    valor_minimo = 10
    valor_maximo = 18

    valor = stats.beta.rvs(parametro_alpha, parametro_beta)
    return valor_minimo + valor * (valor_maximo - valor_minimo)

def generar_tiempo_atencion():
    k = -0.22959
    zigma = 33.969
    mu = 286.98

    while True:
        valor = stats.genextreme.rvs(k, loc=mu, scale=zigma)
        if 240 <= valor <= 400:
            return valor

def elegir_puesto_comun():
    global HV, TPS
    for i in range(21):
        if(TPS[i] == HV):
            return i
    return -1

def procesar_llegada():
    global T, TPLL, NT, NS, TPSI, SPS, STA, NI, HV

    SPS = SPS + ((TPLL - T) * NS)
    T = TPLL
    IA = generar_intervalo_arribos()
    TPLL = T + IA
    NT = NT + 1
    NS = NS + 1
    if((NS <= 21 and TPSI == HV) or (NS <= 20 and TPSI != HV)):
        # Hay un puesto fijo disponible
        POSICION = elegir_puesto_comun()
        TA = generar_tiempo_atencion()
        TPS[POSICION] = T + TA
        STA = STA + TA
    elif(NS == 21 + K and TPSI == HV):
        # Hay un puesto intermitente disponible
        TA = generar_tiempo_atencion()
        TPSI = T + TA
        NI = NI + 1
        STA = STA + TA
        
def procesar_salida(POSICION):
    global T, TPSI, NS, SPS, STA, NI, HV

    if(TPS[POSICION] <= TPSI):
        # Es una salida de un puesto fijo
        SPS += ((TPS[POSICION] - T) * NS)
        T = TPS[POSICION]
        NS -= 1
        if((NS>=21 and TPSI == HV) or (NS == 21 and TPS[POSICION] != HV)):
            TA = generar_tiempo_atencion()
            TPS[POSICION] = T + TA
            STA = STA + TA
        else:
            TPS[POSICION] = HV
    else:
        # Es una salida de un puesto intermitente
        SPS += ((TPSI - T) * NS)
        T = TPSI
        NS -= 1
        if(NS >= 21 + K):
            TA = generar_tiempo_atencion()
            TPSI = T + TA
            STA = STA + TA
            NI = NI + 1
        else:
            TPSI = HV

def calcular_resultados():
    global STA, SPS, PEC, PPS, PPSI, NT, NI

    PEC = (SPS - STA) / NT
    PPS = SPS / NT
    print(str(SPS))
    print(str(STA))
    print(str(NI))
    PPSI = (NI * 100) / NT

def imprimir_resultados():
    print("Promedio de espera en cola: " + str(PEC))
    print("Promedio de permanencia en el sistema: " + str(PPS))
    print("Porcentaje de uso del puesto intermitente: " + str(PPSI))
    print("Cantidad de partidos atendidos: " + str(NT))

# Programa principal
def main():
    global T, TF, TPLL, TPSI

    establecer_condiciones_iniciales()
    print (generar_tiempo_atencion())
    while(T <= TF):
        MENOR_TPS, POSICION = calcular_menor_tps()
        if(TPLL <= MENOR_TPS and TPLL <= TPSI):
            procesar_llegada()
        else:
            procesar_salida(POSICION)

    calcular_resultados()
    imprimir_resultados()
    

if __name__ == "__main__":
    main()



    