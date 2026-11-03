import time

import serial
import serial.tools.list_ports

class ArduinoController:
    def __init__(self):
        self.serial_connection = None
        
    def listar_puertos(self):
        puertos = serial.tools.list_ports.comports()
        return [
            {
                "device": puerto.device,
                "description": puerto.description
            }
            for puerto in sorted(puertos, key=lambda p: p.device)
        ]
    
    def detectar_puerto_arduino(self):
        puertos = self.listar_puertos()
        
        if not puertos:
            return None
        for puerto in puertos:
            texto = f"{puerto['device']} {puerto['description']}".lower()
            
            if (
              "arduino" in texto
              or "usb serial" in texto
              or "ch340" in texto
              or "wch" in texto
              or "cp210" in texto  
            ):
                return puerto["device"]
            
        return puertos[0]["device"]
    
    def conectar(self, puerto: str, baudrate: int = 115200):
        self.cerrar()
        
        print(f"[ARDUINO] Conectando a {puerto} @ {baudrate}...")
        self.serial_connection = serial.Serial(
            port=puerto,
            baudrate=baudrate,
            timeout=0.2
        )
        self.serial_connection.reset_input_buffer()
        time.sleep(2)
        print(f"[ARDUINO] Conexion abierta: {self.serial_connection.is_open}")
        return self.serial_connection.is_open
    
    def leer_linea(self):
        if self.serial_connection is None or not self.serial_connection.is_open:
            return None
        
        if self.serial_connection.in_waiting > 0:
            linea = self.serial_connection.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()
            print(f"[ARDUINO] RX: {linea}")
            return linea
        return None
    
    def enviar_linea(self, texto: str):
        conexion = self.serial_connection

        if conexion is None or not conexion.is_open:
            raise RuntimeError("No hay conexion serial abierta.")

        texto = texto.strip()
        payload = (texto + "\n").encode("utf-8")

        if texto.startswith("al,") and len(payload) > 60:
            if len(payload) > 96:
                raise ValueError(
                    "Comando de alta demasiado largo."
                )

            # Pedir que Arduino esté listo para recibir el alta larga.
            conexion.write(b"preparar_alta24\n")

            limite = time.monotonic() + 8.0
            listo = False

            while time.monotonic() < limite:
                if not conexion.is_open:
                    raise RuntimeError(
                        "Se cerro la conexion con Arduino."
                    )

                if conexion.in_waiting:
                    respuesta = conexion.readline().decode(
                        "utf-8", errors="ignore"
                    ).strip()

                    print(f"[ARDUINO] RX: {respuesta}")

                    if respuesta == "ALTA24_LISTO":
                        listo = True
                        break
                else:
                    time.sleep(0.01)

            if not listo:
                raise RuntimeError(
                    "Arduino no confirmo ALTA24_LISTO. "
                    "Carga el inicializador actualizado."
                )

        print(f"[ARDUINO] TX: {texto}")

        enviados = conexion.write(payload)

        if enviados != len(payload):
            raise RuntimeError(
                "El comando no se envio completo."
            )

        return True
        
    
    def cerrar(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
