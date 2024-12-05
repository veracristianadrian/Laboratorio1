import asyncio
import circuit_monitoring
import board
import analogio
import pwmio
import digitalio


relay = 0
angulo_brazo = 0
pos_panel_x = 0
pos_panel_y = 0


async def operations():

    # Configura el pin donde está conectado el botón
    button_pin = digitalio.DigitalInOut(board.GP16)
    button_pin.direction = digitalio.Direction.INPUT

    button_pin.pull = digitalio.Pull.UP  # Activa la resistencia pull-up interna
    # Configuración de los pines
    relay_pin = digitalio.DigitalInOut(board.GP22)  # Pin GPIO para el relé
    relay_pin.direction = digitalio.Direction.OUTPUT
    # definicion de variables para el manejo de los ejes
    ejeZ = 0  # almacena el angulo del brazo que sostiene el panel solar
    ejeX = 90  # almacena el angulo del panel solar en el eje X
    ejeY = 90  # almacena el angulo del panel solar en el eje Y

    modoUso = 0  # variable que nos permite manejar los dos lazos de control

    # definicion de la entrada analogica para el eje X
    potentiometery = analogio.AnalogIn(board.GP26)
    # definicion de la entrada analogica para el eje Y
    potentiometerx = analogio.AnalogIn(board.GP27)

    # Definicion de cada uno de los leds a utilizar:
    # leds para indicar el angulo del brazo
    led1 = pwmio.PWMOut(board.GP21, frequency=1000, duty_cycle=0)
    led2 = pwmio.PWMOut(board.GP20, frequency=1000, duty_cycle=0)
    led3 = pwmio.PWMOut(board.GP19, frequency=1000, duty_cycle=0)
    led4 = pwmio.PWMOut(board.GP18, frequency=1000, duty_cycle=0)

    # leds para indicar el angulo del eje X e Y respectivamente
    led5px = pwmio.PWMOut(board.GP13, frequency=1000, duty_cycle=0)
    led6nx = pwmio.PWMOut(board.GP10, frequency=1000, duty_cycle=0)
    led7py = pwmio.PWMOut(board.GP12, frequency=1000, duty_cycle=0)
    led8ny = pwmio.PWMOut(board.GP11, frequency=1000, duty_cycle=0)
    ledlazo = pwmio.PWMOut(board.GP14, frequency=1000, duty_cycle=0)

    def pos_led(anguloBrazo):  # en funcion del angulo de brazo recibido asigna un valor de valor de brillo y llama a ajustar brillo

        if 0 <= anguloBrazo < 45:  # ajustamos el brillo del led 1

            if anguloBrazo == 0:
                brillo = 0
            elif anguloBrazo <= 15:
                brillo = 33
            elif anguloBrazo <= 30:
                brillo = 66
            else:
                brillo = 100
            foco = led1
        elif anguloBrazo < 90:  # ajustamos el brillo del led 2

            if anguloBrazo == 45:
                brillo = 0
            elif anguloBrazo <= 60:
                brillo = 33
            elif anguloBrazo <= 75:
                brillo = 66
            else:
                brillo = 100
            foco = led2

        elif anguloBrazo < 135:  # ajustamos el brillo del led 3

            if anguloBrazo == 90:
                brillo = 0
            elif anguloBrazo <= 105:
                brillo = 33
            elif anguloBrazo <= 120:
                brillo = 66
            else:
                brillo = 100
            foco = led3

        else:  # ajustamos el brillo del led 4

            if anguloBrazo == 135:
                brillo = 0
            elif anguloBrazo <= 150:
                brillo = 33
            elif anguloBrazo <= 165:
                brillo = 66
            else:
                brillo = 100
            foco = led4

        # se pasa el nivel de brillo y el led que debe ser ajustado
        ajustar_brillo(brillo, foco)

    # recibe un porcentaje de brillo y un led especifico a ajustar
    def ajustar_brillo(porcentaje, led):

        if porcentaje == 0:
            led.duty_cycle = 0  # LED apagado
        elif porcentaje == 15:
            led.duty_cycle = int((15 / 100) * 65535)  # Brillo minimo
        elif porcentaje == 33:
            led.duty_cycle = int((33 / 100) * 65535)  # Brillo bajo
        elif porcentaje == 66:
            led.duty_cycle = int((66 / 100) * 65535)  # Brillo medio
        elif porcentaje == 100:
            led.duty_cycle = 65535  # Brillo máximo

    # en funcion del angulo  y el eje recibido asigna un valor de valor de brillo y llama a ajustar brillo
    def pos_led2(anguloEje, Eje):

        if Eje == 0:
            if anguloEje == 180:
                ajustar_brillo(100, led5px)
            elif anguloEje > 150:
                ajustar_brillo(66, led5px)
            elif anguloEje > 120:
                ajustar_brillo(33, led5px)
            elif anguloEje > 90 and anguloEje < 120:
                ajustar_brillo(15, led5px)
            elif anguloEje == 90:
                ajustar_brillo(0, led5px)
                ajustar_brillo(0, led6nx)
        elif anguloEje < 90 and anguloEje > 60:
            ajustar_brillo(15, led6nx)
        elif anguloEje == 0:
            ajustar_brillo(100, led6nx)
        elif anguloEje < 30 and anguloEje > 0:
            ajustar_brillo(66, led6nx)
        elif anguloEje < 60 and anguloEje > 30:
            ajustar_brillo(33, led6nx)
        else:
            if anguloEje == 180:
                ajustar_brillo(100, led7py)
            elif anguloEje > 150:
                ajustar_brillo(66, led7py)
            elif anguloEje > 120:
                ajustar_brillo(33, led7py)
            elif anguloEje > 90 and anguloEje < 120:
                ajustar_brillo(15, led7py)
            elif anguloEje == 90:
                ajustar_brillo(0, led7py)
                ajustar_brillo(0, led8ny)
            elif anguloEje < 90 and anguloEje > 60:
                ajustar_brillo(15, led8ny)
            elif anguloEje == 0:
                ajustar_brillo(100, led8ny)
            elif anguloEje < 30 and anguloEje > 0:
                ajustar_brillo(66, led8ny)
            elif anguloEje < 60 and anguloEje > 30:
                ajustar_brillo(33, led8ny)

    

    if modoUso == 0:  # en este modo ajustamos el angulo del brazo que sostiene el panel solar
        if potentiometerx.value < 1000 and ejeZ < 180:  # se cumple cuando la palanca esta a la derecha
            ejeZ += 5  # incrementamos el angulo del brazo
            print("el brazo se encuentra en un angulo de " + str(ejeZ))
            # llama a la funcion para que ajuste el brillo del led
            pos_led(ejeZ)
            relay_pin.value = True  # Activa el relé
            print("Relé activado")
        elif potentiometerx.value > 60000 and ejeZ > 0:  # se cumple cuando la palanca esta a la izquierda
            ejeZ -= 5  # decrementamos el angulo del brazo
            print("el brazo se encuentra en un angulo de " + str(ejeZ))
            # llama a la funcion para que ajuste el brillo del led
            pos_led(ejeZ)
            relay_pin.value = True  # Activa el relé
            print("Relé activado")
        else:
            relay_pin.value = False  # Desactiva el relé
            print("Relé desactivado")
        # sirve para regular la velocidad con la que hacemos las lecturas de la palanca
        await asyncio.sleep(0.3)

    elif modoUso == 1:  # en este modo ajustamos el angulo del panel solar en el eje X e Y

        if potentiometery.value > 60000 and potentiometerx.value < 300:
            print("palanca hacia abajo a la derecha")
            relay_pin.value = True  # Activa el relé
            print("Relé activado")
            if ejeY > 0:
                ejeY -= 5
                # ajusta el brillo del led con un valor de eje y un 1 indicando que es el eje Y
                pos_led2(ejeY, 1)
            if ejeX < 180:
                ejeX += 5
                # ajusta el brillo del led con un valor de eje y un 0 indicando que es el eje X
                pos_led2(ejeX, 0)

        elif potentiometerx.value > 60000 and potentiometery.value < 300:

            print("palanca hacia arriba a la izquierda")
            relay_pin.value = True  # Activa el relé
            print("Relé activado")
            if ejeY < 180:
                ejeY += 5
                # ajusta el brillo del led con un valor de eje y un 1 indicando que es el eje Y
                pos_led2(ejeY, 1)
            if ejeX > 0:
                ejeX -= 5
                # ajusta el brillo del led con un valor de eje y un 0 indicando que es el eje X
                pos_led2(ejeX, 0)

        elif potentiometery.value < 300 and potentiometerx.value < 300:

            print("palanca hacia arriba a la derecha")
            relay_pin.value = True  # Activa el relé
            print("Relé activado")
            if ejeY < 180:
                ejeY += 5
                # ajusta el brillo del led con un valor de eje y un 1 indicando que es el eje Y
                pos_led2(ejeY, 1)
            if ejeX < 180:
                ejeX += 5
                # ajusta el brillo del led con un valor de eje y un 0 indicando que es el eje X
                pos_led2(ejeX, 0)

        elif potentiometery.value > 60000 and potentiometerx.value > 60000:

            print("palanca hacia abajo a la izquierda")
            relay_pin.value = True  # Activa el relé
            print("Relé activado")
            if ejeY > 0:
                ejeY -= 5
                # ajusta el brillo del led con un valor de eje y un 1 indicando que es el eje Y
                pos_led2(ejeY, 1)
            if ejeX > 0:
                ejeX -= 5
                # ajusta el brillo del led con un valor de eje y un 0 indicando que es el eje X
                pos_led2(ejeX, 0)

        elif potentiometerx.value < 1000 and ejeX < 180:

            print("palanca a la derecha")
            relay_pin.value = True  # Activa el relé
            print("Relé activado")
            ejeX += 5
            # ajusta el brillo del led con un valor de eje y un 0 indicando que es el eje X
            pos_led2(ejeX, 0)

        elif potentiometerx.value > 60000 and ejeX > 0:

            print("palanca a la izquierda")
            relay_pin.value = True  # Activa el relé
            print("Relé activado")
            ejeX -= 5
            # ajusta el brillo del led con un valor de eje y un 0 indicando que es el eje X
            pos_led2(ejeX, 0)

        elif potentiometery.value < 1000 and ejeY < 180:

            print("palanca hacia arriba")
            relay_pin.value = True  # Activa el relé
            print("Relé activado")
            ejeY += 5
            # ajusta el brillo del led con un valor de eje y un 1 indicando que es el eje Y
            pos_led2(ejeY, 1)

        elif potentiometery.value > 60000 and ejeY > 0:

            print("palanca hacia abajo")
            relay_pin.value = True  # Activa el relé
            print("Relé activado")
            ejeY -= 5
            # ajusta el brillo del led con un valor de eje y un 1 indicando que es el eje Y
            pos_led2(ejeY, 1)

        else:
            print("valor eje x " + str(ejeX) + " valor eje y " + str(ejeY))
            relay_pin.value = False  # Desactiva el relé
            print("Relé desactivado")
    else:
        print(potentiometerx.value)
        await asyncio.sleep(0.6)

    if not button_pin.value:  # Si el botón está presionado (estado bajo)
        if modoUso == 0:
            modoUso = 1  # se cambia al lazo que controla el penel solar
            print("se cambio a Control Panel")
        elif modoUso == 1:
            modoUso = 2  # se cambia al lazo que controla el angulo del brazo
        else:
            modoUso = 0
            print("se cambio a angulo brazo")
        await asyncio.sleep(1)
        # enciende un led indicando que se cambio de lazo de control
        ajustar_brillo(100, ledlazo)
    else:
        ajustar_brillo(0, ledlazo)  # apaga el led luego del cambio de lazo


def get_app_data():
    # Función que devuelve un `dict` con la data para el maestro.
    return {
        "Relay": relay,
        "Brazo": angulo_brazo,
        "Posicion_panel_eje_x": pos_panel_x,
        "Posicion_panel_eje_y": pos_panel_y
    }


async def main():
    # Funcionamiento del equipo y monitoreo con el maestro se ejecutan concurrentemente.
    await asyncio.gather(
        operations(),
        circuit_monitoring.monitoring(get_app_data)   # Monitoreo del maestro
    )

asyncio.run(main())
