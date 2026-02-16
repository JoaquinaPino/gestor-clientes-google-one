class Plan:
    def __init__(self, nombre, precio, almacenamiento_gb):
        self._nombre = nombre
        self._precio = precio
        self._almacenamiento_gb = almacenamiento_gb
        self.__suscripcion = None

    # --- GETTERS Y SETTERS ---

    def get_precio(self):
        return self._precio
    
    def set_precio(self, nuevo_precio):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = nuevo_precio

    def get_nombre(self):
        return self._nombre
    
    def get_almacenamiento(self):
        return self._almacenamiento_gb
    
    # --- MÉTODOS DE RELACIÓN ---
    
    def asignar_suscripcion(self, suscripcion):
        self.__suscripcion = suscripcion

    def obtener_suscripcion(self):
        return self.__suscripcion
    
    # --- MÉTODOS DE LÓGICA ---

    def verificar_almacenamiento(self, gb_uso):
        return gb_uso <= self._almacenamiento_gb
    
    def calcular_costo_total(self):
        return self._precio
    
    def listar_beneficios(self):
        raise NotImplementedError("Este método debe ser implementado por las clases hijas")

class PlanGratuito(Plan):
    def __init__(self):
        super().__init__("Google Free", 0.0, 15)

    def listar_beneficios(self):
        return ["Google Free", "15GB Drive", "Google Photos"]
    
class PlanPremium(Plan):
    def __init__(self):
        super().__init__("Google One AI Premium", 19.99, 2048)
        self.__acceso_gemini = True

    def get_acceso_gemini(self):
        return self.__acceso_gemini
    
    def listar_beneficios(self):
        return [
            "2TB Almacenamiento",
            "Gemini Advanced",
            "Magic Eraser"
        ]
    
class PlanEmpresa(Plan):
    def __init__(self, cantidad_usuarios, dominio_personalizado):
        super().__init__("Google Enterprise", 10.0, 100000)

        if cantidad_usuarios < 3:
            raise ValueError("El Plan Empresa requiere un mínimo de 3 usuarios.")
        self.__cantidad_usuarios = cantidad_usuarios

        if "." not in dominio_personalizado:
            raise ValueError("El dominio no es válido (falta el punto, ej: .com).")
        self.__dominio_personalizado = dominio_personalizado

    # --- GETTERS Y SETTERS ESPECIFICOS EMPRESA ---
    def get_cantidad_usuarios(self):
        return self.__cantidad_usuarios
    
    def set_cantidad_usuarios(self, n):
        if n < 3:
            raise ValueError("Error: Deber haber al menos 3 usuarios.")
        self.__cantidad_usuarios = n

    def get_dominio(self):
        return self.__dominio_personalizado
    
    # --- Polimorfismo ---
    def calcular_costo_total(self):
        return self._precio * self.__cantidad_usuarios
    
    def listar_beneficios(self):
        return [
            f"Espacio compartido para {self.__cantidad_usuarios} usuarios",
            f"Dominio @{self.__dominio_personalizado}",
            "Soporte 24/7"
        ]
    
    

    
