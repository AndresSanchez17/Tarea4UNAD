# =========================
# ARCHIVO: main.py
# =========================

from abc import ABC, abstractmethod
from datetime import datetime


# =====================================================
# LOGGER
# =====================================================

def registrar_log(mensaje):

    with open("logs.txt", "a", encoding="utf-8") as archivo:

        archivo.write(
            f"{datetime.now()} -> {mensaje}\n"
        )


# =====================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================

class ReservaError(Exception):
    pass


class ClienteInvalidoError(Exception):
    pass


class ServicioNoDisponibleError(Exception):
    pass


# =====================================================
# CLASE ABSTRACTA ENTIDAD
# =====================================================

class Entidad(ABC):

    @abstractmethod
    def mostrar_info(self):
        pass


# =====================================================
# CLASE CLIENTE
# =====================================================

class Cliente(Entidad):

    def __init__(self, nombre, documento, correo):

        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo

        self.validar_cliente()

    # =========================
    # VALIDACIONES
    # =========================

    def validar_cliente(self):

        if not self.__nombre.strip():

            raise ClienteInvalidoError(
                "El nombre no puede estar vacío"
            )

        if len(self.__documento) < 5:

            raise ClienteInvalidoError(
                "Documento inválido"
            )

        if "@" not in self.__correo:

            raise ClienteInvalidoError(
                "Correo electrónico inválido"
            )

    # =========================
    # GETTERS
    # =========================

    def get_nombre(self):
        return self.__nombre

    def get_documento(self):
        return self.__documento

    def get_correo(self):
        return self.__correo

    # =========================
    # MOSTRAR INFORMACIÓN
    # =========================

    def mostrar_info(self):

        return (
            f"Cliente: {self.__nombre} | "
            f"Documento: {self.__documento} | "
            f"Correo: {self.__correo}"
        )


# =====================================================
# CLASE ABSTRACTA SERVICIO
# =====================================================

class Servicio(ABC):

    def __init__(self, nombre, tarifa):

        self.nombre = nombre
        self.tarifa = tarifa

    @abstractmethod
    def calcular_costo(self, horas):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# =====================================================
# SERVICIO: RESERVA DE SALAS
# =====================================================

class ReservaSala(Servicio):

    def calcular_costo(self, horas, descuento=0):

        if horas <= 0:

            raise ValueError(
                "Las horas deben ser mayores a cero"
            )

        total = self.tarifa * horas

        total -= total * descuento

        return total

    def descripcion(self):

        return (
            f"Servicio de Reserva de Sala: {self.nombre}"
        )


# =====================================================
# SERVICIO: ALQUILER DE EQUIPOS
# =====================================================

class AlquilerEquipo(Servicio):

    def calcular_costo(self, horas):

        if horas <= 0:

            raise ValueError(
                "Las horas deben ser mayores a cero"
            )

        if horas > 24:

            raise ServicioNoDisponibleError(
                "No se permiten alquileres mayores a 24 horas"
            )

        return self.tarifa * horas

    def descripcion(self):

        return (
            f"Servicio de Alquiler de Equipos: {self.nombre}"
        )


# =====================================================
# SERVICIO: ASESORÍA ESPECIALIZADA
# =====================================================

class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, horas, impuesto=0.19):

        if horas <= 0:

            raise ValueError(
                "Las horas deben ser mayores a cero"
            )

        subtotal = self.tarifa * horas

        total = subtotal + (subtotal * impuesto)

        return total

    def descripcion(self):

        return (
            f"Servicio de Asesoría Especializada: {self.nombre}"
        )


# =====================================================
# CLASE RESERVA
# =====================================================

class Reserva:

    def __init__(self, cliente, servicio, horas):

        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "Pendiente"

    # =========================
    # CONFIRMAR RESERVA
    # =========================

    def confirmar(self):

        try:

            if self.horas <= 0:

                raise ReservaError(
                    "La duración debe ser mayor a cero"
                )

            costo = self.servicio.calcular_costo(
                self.horas
            )

            self.estado = "Confirmada"

            registrar_log(
                f"Reserva confirmada para "
                f"{self.cliente.get_nombre()}"
            )

            return costo

        except Exception as e:

            registrar_log(
                f"ERROR EN RESERVA: {str(e)}"
            )

            raise ReservaError(
                "Error al confirmar la reserva"
            ) from e

        finally:

            registrar_log(
                "Proceso de reserva finalizado"
            )

    # =========================
    # CANCELAR RESERVA
    # =========================

    def cancelar(self):

        self.estado = "Cancelada"

        registrar_log(
            f"Reserva cancelada para "
            f"{self.cliente.get_nombre()}"
        )

    # =========================
    # MOSTRAR RESERVA
    # =========================

    def mostrar_reserva(self):

        return (
            f"Cliente: {self.cliente.get_nombre()} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Horas: {self.horas} | "
            f"Estado: {self.estado}"
        )


# =====================================================
# LISTAS INTERNAS
# =====================================================

clientes = []
servicios = []
reservas = []


# =====================================================
# CREACIÓN DE SERVICIOS
# =====================================================

sala = ReservaSala(
    "Sala Ejecutiva",
    50000
)

equipo = AlquilerEquipo(
    "Portátil Gamer",
    30000
)

asesoria = AsesoriaEspecializada(
    "Asesoría Python",
    80000
)

servicios.append(sala)
servicios.append(equipo)
servicios.append(asesoria)


# =====================================================
# SIMULACIÓN DE OPERACIONES
# =====================================================

print("\n========== INICIO DEL SISTEMA ==========\n")


# =====================================================
# OPERACIÓN 1 - CLIENTE VÁLIDO
# =====================================================

try:

    cliente1 = Cliente(
        "Andres Sanchez",
        "123456",
        "andres@gmail.com"
    )

    clientes.append(cliente1)

    print(cliente1.mostrar_info())

except Exception as e:

    print("Error:", e)


# =====================================================
# OPERACIÓN 2 - CLIENTE INVÁLIDO
# =====================================================

try:

    cliente2 = Cliente(
        "",
        "12",
        "correo_malo"
    )

    clientes.append(cliente2)

except Exception as e:

    registrar_log(str(e))

    print("Error:", e)


# =====================================================
# OPERACIÓN 3 - CLIENTE VÁLIDO
# =====================================================

try:

    cliente3 = Cliente(
        "Maria Lopez",
        "987654",
        "maria@gmail.com"
    )

    clientes.append(cliente3)

    print(cliente3.mostrar_info())

except Exception as e:

    print("Error:", e)


# =====================================================
# OPERACIÓN 4 - RESERVA EXITOSA
# =====================================================

try:

    reserva1 = Reserva(
        cliente1,
        sala,
        5
    )

    costo = reserva1.confirmar()

    reservas.append(reserva1)

    print(
        "\nReserva exitosa"
    )

    print(
        reserva1.mostrar_reserva()
    )

    print(
        f"Costo Total: ${costo}"
    )

except Exception as e:

    print("Error:", e)


# =====================================================
# OPERACIÓN 5 - RESERVA FALLIDA
# =====================================================

try:

    reserva2 = Reserva(
        cliente1,
        equipo,
        30
    )

    costo = reserva2.confirmar()

    reservas.append(reserva2)

except Exception as e:

    print(
        "\nReserva fallida:"
    )

    print(e)


# =====================================================
# OPERACIÓN 6 - HORAS NEGATIVAS
# =====================================================

try:

    reserva3 = Reserva(
        cliente1,
        asesoria,
        -5
    )

    costo = reserva3.confirmar()

    reservas.append(reserva3)

except Exception as e:

    print(
        "\nError en reserva:"
    )

    print(e)


# =====================================================
# OPERACIÓN 7 - ASESORÍA EXITOSA
# =====================================================

try:

    reserva4 = Reserva(
        cliente3,
        asesoria,
        3
    )

    costo = reserva4.confirmar()

    reservas.append(reserva4)

    print(
        "\nReserva exitosa"
    )

    print(
        reserva4.mostrar_reserva()
    )

    print(
        f"Costo Total: ${costo}"
    )

except Exception as e:

    print(e)


# =====================================================
# OPERACIÓN 8 - CANCELAR RESERVA
# =====================================================

try:

    reserva4.cancelar()

    print(
        "\nReserva cancelada correctamente"
    )

    print(
        reserva4.mostrar_reserva()
    )

except Exception as e:

    print(e)


# =====================================================
# OPERACIÓN 9 - DESCUENTO
# =====================================================

try:

    costo_descuento = sala.calcular_costo(
        4,
        descuento=0.10
    )

    print(
        "\nCosto con descuento:"
    )

    print(
        f"${costo_descuento}"
    )

except Exception as e:

    print(e)


# =====================================================
# OPERACIÓN 10 - IMPUESTO
# =====================================================

try:

    costo_impuesto = asesoria.calcular_costo(
        2,
        impuesto=0.19
    )

    print(
        "\nCosto con impuesto:"
    )

    print(
        f"${costo_impuesto}"
    )

except Exception as e:

    print(e)


# =====================================================
# TRY / EXCEPT / ELSE
# =====================================================

print("\n========== EJEMPLO ELSE ==========\n")

try:

    resultado = 10 / 2

except ZeroDivisionError:

    print(
        "No se puede dividir entre cero"
    )

else:

    print(
        "Operación correcta:",
        resultado
    )


# =====================================================
# TRY / EXCEPT / FINALLY
# =====================================================

print("\n========== EJEMPLO FINALLY ==========\n")

try:

    archivo = open(
        "archivo_inexistente.txt"
    )

except FileNotFoundError:

    print(
        "Archivo no encontrado"
    )

finally:

    print(
        "Proceso finalizado"
    )


# =====================================================
# RESUMEN FINAL
# =====================================================

print("\n========== RESUMEN ==========\n")

print(
    f"Clientes registrados: {len(clientes)}"
)

print(
    f"Servicios registrados: {len(servicios)}"
)

print(
    f"Reservas procesadas: {len(reservas)}"
)

print("\n========== FIN DEL SISTEMA ==========\n")