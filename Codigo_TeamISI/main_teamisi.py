import uasyncio  
import micro_monitoring
from  machine import ADC, Pin, PWM
import time

#relay = 0
#angulo_brazo = 0
#pos_panel_x = 0
#pos_panel_y = 0
# Definición de variables
datos_app = {
    "Relay": 0,
    "Brazo": 0,
    "Posicion_panel_eje_x": 0,
    "Posicion_panel_eje_y": 0
}

async def operations():
    #codigo base
    print("bucles de operations")
    button_pin = Pin(16, Pin.IN, Pin.PULL_UP)
    #relay_pin = digitalio.DigitalInOut(board.GP22)  # Pin GPIO para el relé
    #relay_pin.direction = digitalio.Direction.OUTPUT
    relay_pin = Pin(22,Pin.OUT)
    #definicion de variables para el manejo de los ejes
    ejeZ = 0 #almacena el angulo del brazo que sostiene el panel solar
    ejeX = 90 #almacena el angulo del panel solar en el eje X
    ejeY = 90 #almacena el angulo del panel solar en el eje Y

    modoUso = 0 #variable que nos permite manejar los dos lazos de control

    potentiometery = ADC(Pin(26))
    potentiometerx = ADC(Pin(27))

    led1 = PWM(Pin(21))  
    led1.freq(1000)     
    led1.duty_u16(0)

    led2 = PWM(Pin(20))  
    led2.freq(1000)     
    led2.duty_u16(0)

    led3 = PWM(Pin(19))  
    led3.freq(1000)     
    led3.duty_u16(0)

    led4 = PWM(Pin(18))  
    led4.freq(1000)     
    led4.duty_u16(0)

    led5px = PWM(Pin(13))  
    led5px.freq(1000)     
    led5px.duty_u16(0)

    led6nx = PWM(Pin(10))  
    led6nx.freq(1000)     
    led6nx.duty_u16(0)

    led7py = PWM(Pin(12))  
    led7py.freq(1000)     
    led7py.duty_u16(0)

    led8ny = PWM(Pin(11))  
    led8ny.freq(1000)     
    led8ny.duty_u16(0)

    ledlazo = PWM(Pin(14))  
    ledlazo.freq(1000)     
    ledlazo.duty_u16(0)



    def pos_led(anguloBrazo): #en funcion del angulo de brazo recibido asigna un valor de valor de brillo y llama a ajustar brillo

        if 0 <= anguloBrazo < 45: #ajustamos el brillo del led 1

            if anguloBrazo == 0:
                brillo = 0
            elif anguloBrazo <= 15:
                brillo = 33
            elif anguloBrazo <= 30:
                brillo = 66
            else:
                brillo = 100
            foco = led1
        elif anguloBrazo < 90: #ajustamos el brillo del led 2

            if anguloBrazo == 45:
                brillo = 0
            elif anguloBrazo <= 60:
                brillo = 33
            elif anguloBrazo <= 75:
                brillo = 66
            else:
                brillo = 100
            foco = led2


        elif anguloBrazo < 135: #ajustamos el brillo del led 3

            if anguloBrazo == 90:
                brillo = 0
            elif anguloBrazo <= 105:
                brillo = 33
            elif anguloBrazo <= 120:
                brillo = 66
            else:
                brillo = 100
            foco = led3


        else: #ajustamos el brillo del led 4

            if anguloBrazo == 135:
                brillo = 0
            elif anguloBrazo <= 150:
                brillo = 33
            elif anguloBrazo <= 165:
                brillo = 66
            else:
                brillo = 100
            foco = led4

        ajustar_brillo(brillo, foco) #se pasa el nivel de brillo y el led que debe ser ajustado


    def ajustar_brillo(porcentaje, led): # recibe un porcentaje de brillo y un led especifico a ajustar

        if porcentaje == 0:
            led.duty_u16(0)  # LED apagado
        elif porcentaje == 15:
            led.duty_u16(int((15 / 100) * 65535))
        # led.duty_cycle = int((15 / 100) * 65535)  # Brillo minimo
        elif porcentaje == 33:
            led.duty_u16(int((33 / 100) * 65535))
            #led.duty_cycle = int((33 / 100) * 65535)  # Brillo bajo
        elif porcentaje == 66:
            led.duty_u16(int((66 / 100) * 65535))
            #led.duty_cycle = int((66 / 100) * 65535)  # Brillo medio
        elif porcentaje == 100:
            led.duty_u16(65535)
            #led.duty_cycle = 65535  # Brillo máximo


    def pos_led2(anguloEje, Eje): #en funcion del angulo  y el eje recibido asigna un valor de valor de brillo y llama a ajustar brillo

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


    
    while True:    
        if modoUso == 0: #en este modo ajustamos el angulo del brazo que sostiene el panel solar

            if potentiometerx.read_u16() < 1000 and ejeZ < 180:  #se cumple cuando la palanca esta a la derecha
                ejeZ += 5 #incrementamos el angulo del brazo
                print("el brazo se encuentra en un angulo de " + str(ejeZ))

                pos_led(ejeZ) #llama a la funcion para que ajuste el brillo del led
                relay_pin.value(True)  # Activa el relé
                print("Relé activado")


            elif potentiometerx.read_u16() > 60000 and ejeZ > 0: ##se cumple cuando la palanca esta a la izquierda
                ejeZ -= 5 #decrementamos el angulo del brazo
                print("el brazo se encuentra en un angulo de " + str(ejeZ))

                pos_led(ejeZ) #llama a la funcion para que ajuste el brillo del led
                relay_pin.value(True)  # Activa el relé
                print("Relé activado")

            else:
                relay_pin.value(False)  # Desactiva el relé
                print("Relé desactivado")

            await uasyncio.sleep(0.3) #sirve para regular la velocidad con la que hacemos las lecturas de la palanca

        elif modoUso == 1: #en este modo ajustamos el angulo del panel solar en el eje X e Y

            if potentiometery.read_u16() > 60000 and potentiometerx.read_u16()< 300:

                print("palanca hacia abajo a la derecha")
                relay_pin.value(True)  # Activa el relé
                print("Relé activado")
                if ejeY > 0:
                    ejeY -= 5
                    pos_led2(ejeY, 1) #ajusta el brillo del led con un valor de eje y un 1 indicando que es el eje Y
                if ejeX < 180:
                    ejeX += 5
                    pos_led2(ejeX, 0) #ajusta el brillo del led con un valor de eje y un 0 indicando que es el eje X

            elif potentiometerx.read_u16() > 60000 and potentiometery.read_u16() < 300:

                print("palanca hacia arriba a la izquierda")
                relay_pin.value(True)  # Activa el relé
                print("Relé activado")
                if ejeY < 180:
                    ejeY += 5
                    pos_led2(ejeY, 1) #ajusta el brillo del led con un valor de eje y un 1 indicando que es el eje Y
                if ejeX > 0:
                    ejeX -= 5
                    pos_led2(ejeX, 0) #ajusta el brillo del led con un valor de eje y un 0 indicando que es el eje X

            elif potentiometery.read_u16() < 300 and potentiometerx.read_u16() < 300:

                print("palanca hacia arriba a la derecha")
                relay_pin.value(True)  # Activa el relé
                print("Relé activado")
                if ejeY < 180:
                    ejeY += 5
                    pos_led2(ejeY, 1) #ajusta el brillo del led con un valor de eje y un 1 indicando que es el eje Y
                if ejeX < 180:
                    ejeX += 5
                    pos_led2(ejeX, 0) #ajusta el brillo del led con un valor de eje y un 0 indicando que es el eje X

            elif potentiometery.read_u16() > 60000 and potentiometerx.read_u16() > 60000:

                print("palanca hacia abajo a la izquierda")
                relay_pin.value(True)  # Activa el relé
                print("Relé activado")

                if ejeY > 0:
                    ejeY -= 5
                    pos_led2(ejeY, 1) #ajusta el brillo del led con un valor de eje y un 1 indicando que es el eje Y
                if ejeX > 0:
                    ejeX -= 5
                    pos_led2(ejeX, 0) #ajusta el brillo del led con un valor de eje y un 0 indicando que es el eje X

            elif potentiometerx.read_u16() < 1000 and ejeX < 180:

                print("palanca a la derecha")
                relay_pin.value(True)  # Activa el relé
                print("Relé activado")
                ejeX += 5
                pos_led2(ejeX, 0) #ajusta el brillo del led con un valor de eje y un 0 indicando que es el eje X

            elif potentiometerx.read_u16() > 60000 and ejeX > 0:

                print("palanca a la izquierda")
                relay_pin.value(True)  # Activa el relé
                print("Relé activado")
                ejeX -= 5
                pos_led2(ejeX, 0) #ajusta el brillo del led con un valor de eje y un 0 indicando que es el eje X

            elif potentiometery.read_u16() < 1000 and ejeY < 180:
                print("palanca hacia arriba")
                relay_pin.value(True)  # Activa el relé
                print("Relé activado")
                ejeY += 5
                pos_led2(ejeY, 1) #ajusta el brillo del led con un valor de eje y un 1 indicando que es el eje Y

            elif potentiometery.read_u16() > 60000 and ejeY > 0:

                print("palanca hacia abajo")
                relay_pin.value(True)  # Activa el relé
                print("Relé activado")
                ejeY -= 5
                pos_led2(ejeY, 1) #ajusta el brillo del led con un valor de eje y un 1 indicando que es el eje Y

            else:

                print("valor eje x " + str(ejeX) + " valor eje y " + str(ejeY))
                relay_pin.value(False)  # Desactiva el relé
                print("Relé desactivado")
        
        else:
            print(potentiometerx.read_u16())
        # Actualizar datos de la aplicación
        datos_app["Relay"] = int(relay_pin.value())
        datos_app["Brazo"] = ejeZ
        datos_app["Posicion_panel_eje_x"] = ejeX
        datos_app["Posicion_panel_eje_y"] = ejeY

        await uasyncio.sleep(0.6)

        if not button_pin.value():  # Si el botón está presionado (estado bajo)

            if modoUso == 0:
                modoUso = 1 #se cambia al lazo que controla el penel solar
                print("se cambio a Control Panel")
            elif modoUso == 1:
                modoUso = 2 #se cambia al lazo que controla el angulo del brazo
            else:
                modoUso = 0
                print("se cambio a angulo brazo")
            await uasyncio.sleep(0.5)
            ajustar_brillo(100, ledlazo) #enciende un led indicando que se cambio de lazo de control

        else:
            ajustar_brillo(0, ledlazo) # apaga el led luego del cambio de lazo





async def main():
    # Funcionamiento del equipo y monitoreo con el maestro se ejecutan concurrentemente.
    await uasyncio.gather(
        operations(),
        micro_monitoring.monitoring(lambda: datos_app)   # Monitoreo del maestro
        
    )

uasyncio.run(main())



