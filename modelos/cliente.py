from modelos.plan import PlanGratuito

class Cliente:
    def __init__(self, nombre, rut, email):
        self.__nombre = nombre.title()

        if "-" not in rut:
            raise ValueError(f"El RUT '{rut}' no es válido. Debe tener guión (Ej: 12345678-9)")
        self.__rut = rut
        
        self.set_email(email.lower())                   # Validación inicial
        self.__gb_uso = 0.0                     # Iniciamos con 0 GB de espacio usado

        self.__plan_actual = PlanGratuito()     # Se asigna el plan gratuito por defecto al crear cliente

    # --- GETTERS Y SETTERS ---

    def get_nombre(self):
        return self.__nombre
    
    def get_rut(self):
        return self.__rut
    
    def get_email(self):
        return self.__email
    
    def set_email(self, nuevo_email):
        email_procesado = nuevo_email.lower()

        if "@" not in email_procesado or "." not in email_procesado:
            raise ValueError(f"El correo '{nuevo_email}' no es válido.")
        self.__email = email_procesado

    def get_plan(self):
        return self.__plan_actual
    
    def get_gb_uso(self):
        return self.__gb_uso
    
    # --- MÉTODOS DE NEGOCIO ---
    def cambiar_plan(self, nuevo_plan):
        self.__plan_actual = nuevo_plan         # Recibe un objeto de tipo Plan y reemplaza el actual

    def subir_archivos(self, peso_gb):          # Simula la subida de archivos. Verifica con el plan si hay espacio.
        if self.__plan_actual.verificar_almacenamiento(self.__gb_uso + peso_gb):
            self.__gb_uso += peso_gb
            return True
        else:
            return False
        
    def __str__(self):
        return f"{self.__nombre} (RUT: {self.__rut}) - Plan: {self.__plan_actual.get_nombre()} - Uso: {self.__gb_uso}GB"
        

    

    