# =====================================================================
#  Control del robot Unitree Go2 en simulador (MuJoCo)
#
#  La rutina verifica la bateria, saluda, avanza, gira y se detiene.
#  Despues hace tres ejercicios extra: un cuadrado, un giro de 180
#  grados y el mismo movimiento con el orden invertido.
#
#  Antes de ejecutar:
#    1. Abrir INICIAR_SIMULADOR y elegir el robot (2 = Go2)
#    2. Esperar a que aparezca la ventana con el robot
#    3. Ejecutar este archivo
#
# =====================================================================

from robot import Robot

# ---------------------------------------------------------------------
#  Valores de los movimientos
#    distancia = velocidad x tiempo
#    angulo    = velocidad x tiempo (en radianes)
# ---------------------------------------------------------------------
VELOCIDAD_AVANCE = 0.2   # m/s (maximo permitido por el robot)
TIEMPO_AVANCE = 2.0      # s -> 0.2 x 2 = 0.4 m = 40 cm
VELOCIDAD_GIRO = 0.5     # rad/s (maximo permitido por el robot)
TIEMPO_GIRO_90 = 3.14    # s -> 0.5 x 3.14 = 1.57 rad = 90 grados
BATERIA_MINIMA = 20      # por debajo de este porcentaje no se mueve


def mostrar_posicion(robot):
    # Pide el estado actual del robot y muestra su posicion (x, y)
    estado = robot.verificar_estado()
    print(f"   Posicion del robot: x = {estado.x} | y = {estado.y}")


def avanzar_40_cm(robot):
    # Avanza 40 cm (0.2 m/s durante 2 s) y muestra la posicion
    print("Avanzando 40 cm...")
    robot.avanzar(velocidad=VELOCIDAD_AVANCE, tiempo=TIEMPO_AVANCE)
    mostrar_posicion(robot)


def girar_90_izquierda(robot):
    # Gira 90 grados a la izquierda (0.5 rad/s durante 3.14 s)
    # y muestra la posicion
    print("Girando 90 grados hacia la izquierda...")
    robot.girar(velocidad=VELOCIDAD_GIRO, tiempo=TIEMPO_GIRO_90)
    mostrar_posicion(robot)


def rutina_basica(robot):
    # Saludo, avance, giro y frenado, en ese orden
    print("Bateria suficiente. Comienza la rutina.")
    mostrar_posicion(robot)

    print("El robot esta saludando...")
    robot.saludar()
    mostrar_posicion(robot)

    avanzar_40_cm(robot)
    girar_90_izquierda(robot)

    print("Deteniendo el robot...")
    robot.detenerse()
    print("Robot detenido.")
    mostrar_posicion(robot)


def ejercicios_extra(robot):
    # --- Cuadrado de 40 cm de lado ---
    # Cuatro veces: avanzar 40 cm y girar 90 grados.
    # Asi el robot vuelve (casi exactamente) al punto de partida.
    print("--- Dibujando un cuadrado de 40 cm de lado ---")
    for lado in range(1, 5):
        print("Lado", lado, "de 4:")
        avanzar_40_cm(robot)
        girar_90_izquierda(robot)
    print("Cuadrado terminado.")

    # --- Giro de 180 grados ---
    # A 0.5 rad/s harian falta 6.28 s, pero el maximo por orden es 5 s.
    # Por eso se parte en dos giros de 90 grados.
    print("--- Girando 180 grados (en dos giros de 90) ---")
    girar_90_izquierda(robot)
    girar_90_izquierda(robot)

    # --- Orden invertido: primero girar, despues avanzar ---
    # Comparar la posicion final con la de la rutina basica.
    print("--- Experimento: primero girar, despues avanzar ---")
    girar_90_izquierda(robot)
    avanzar_40_cm(robot)

    # Nota: pedir una velocidad mayor al maximo (por ejemplo 0.3 m/s)
    # corta el programa con un error de limite, en lugar de ir mas lento.


def main():
    # Conexion
    robot = Robot()
    print("Conectando al robot...")
    robot.conectar()
    print("Robot conectado.")

    # Verificacion de bateria (valor de 0 a 100)
    print("Verificando el estado del robot...")
    estado = robot.verificar_estado()
    print("Bateria actual:", estado.bateria, "%")

    if estado.bateria < BATERIA_MINIMA:
        # Con bateria insuficiente se avisa y el robot no se mueve
        print("ADVERTENCIA: bateria insuficiente (menos del 20%).")
        print("La rutina no continua y el robot no se movio.")
    else:
        rutina_basica(robot)
        ejercicios_extra(robot)

    # Desconexion (se hace siempre, haya o no bateria suficiente)
    print("Desconectando del robot...")
    robot.desconectar()
    print("Robot desconectado. Fin del programa.")


if __name__ == "__main__":
    main()