from datetime import datetime, timedelta

class Suscripcion:
    def __init__(self, duracion_meses, fecha_inicio=None, renovacion_auto=True):

        if fecha_inicio is None: 
            self.__fecha_inicio = datetime.now()
        else:
            self.__fecha_inicio = fecha_inicio

        self.__duracion_meses = duracion_meses          # Define si es mensual, semestral o anual, (1, 6, 12 meses)
        self.__renovacion_auto = renovacion_auto
        self.__activa = True

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio

    def calcular_fecha_fin(self):                       # Calcula fecha vencimiento de plan
        dias_totales = self.__duracion_meses * 30       # Meses de 30 días, por simplificación
        return self.__fecha_inicio + timedelta(days=dias_totales)

    def es_valida(self):
        if not self.__activa:
            return False
            
        fecha_actual = datetime.now()
        fecha_vencimiento = self.calcular_fecha_fin()

        # Caso 1: Ya venció y tiene renovación automática, reseteamos fecha inicio
        if fecha_actual > fecha_vencimiento and self.__renovacion_auto:
            self.__fecha_inicio = datetime.now()
            return True
            
        # Caso 2: Si no ha vencido = True. Si venció sin auto-renovación = False.
        return fecha_actual < fecha_vencimiento

    def cancelar_suscripcion(self):
        self.__activa = False
        self.__renovacion_auto = False # Al cancelar, quitamos la renovación