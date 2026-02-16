import os
from datetime import datetime
from modelos.cliente import Cliente
from modelos.plan import PlanGratuito, PlanPremium, PlanEmpresa
from modelos.suscripcion import Suscripcion

# --- CONFIGURACIÓN ---
DIRECTORIO_RAIZ = os.path.dirname(os.path.abspath(__file__))
CARPETA_DATOS = os.path.join(DIRECTORIO_RAIZ, "datos")
ARCHIVO_LOG = os.path.join(CARPETA_DATOS, "registro.txt")
clientes_en_memoria = []

# --- FUNCIONES UTILITARIAS ---

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def registrar_actividad(mensaje, es_error=False):
    fecha_hora = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    tipo = "[ERROR]" if es_error else "[INFO]"
    linea = f"{fecha_hora} - {tipo} - {mensaje}\n"

    if not os.path.exists(CARPETA_DATOS):
        os.makedirs(CARPETA_DATOS)

    try:
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(linea)
    except Exception as e:
        print(f"Error crítico al guardar log: {e}")

# --- FUNCIONES DEL MENÚ ---

def crear_nuevo_cliente():
    print("\n--- REGISTRO DE NUEVO CLIENTE ---")

    nombre = input("\nNombre completo: \n>>> ")

    while True:
        rut = input("\nRUT con guión (ej: 12345678-9): \n>>> ")
        if "-" in rut:
            break
        print("Error: El RUT debe tener un guión.")

    while True:
        email = input("\nEmail: \n>>> ")
        if "@" in email and "." in email:
            break
        print("Error: Email inválido.")

    try:
        nuevo_cliente = Cliente(nombre, rut, email)

        suscripcion_inicial = Suscripcion(duracion_meses=12)
        nuevo_cliente.get_plan().asignar_suscripcion(suscripcion_inicial)

        clientes_en_memoria.append(nuevo_cliente)

        print(f"\nCliente {nuevo_cliente.get_nombre()} creado exitosamente.")
        registrar_actividad(f"Cliente creado: {nuevo_cliente.get_nombre()} (RUT: {rut})")

        input("\nPresione Enter para volver... ")

    except ValueError as e:
        print(f"\nError de validación: {e}")
        registrar_actividad(f"Fallo al crear cliente {rut}: {e}", es_error=True)
        input("\nPresione Enter para volver... ")

    except Exception as e:
        print(f"\nError inesperado: {e}")
        registrar_actividad(f"Error crítico: {e}", es_error=True)
        input("\nPresione Enter para volver... ")

def listar_clientes_registrados():
    print("\n--- LISTADO DE CLIENTES  Y SUSCRIPCIONES ---")

    if not clientes_en_memoria:
        print("No hay clientes registrados en memoria.")
        return
    
    for i, cliente in enumerate(clientes_en_memoria, 1):
        plan = cliente.get_plan()
        susc = plan.obtener_suscripcion()

        precio = plan.calcular_costo_total()

        vence = "Sin suscripción"
        if susc:
            fecha_fin = susc.calcular_fecha_fin()
            vence = fecha_fin.strftime("%d/%m/%Y")

        print(f"{i}. {cliente.get_nombre()} | Plan: {plan.get_nombre()} (${precio}) | Vence: {vence} | Uso: {cliente.get_gb_uso()}GB")

def gestionar_planes():
    listar_clientes_registrados()

    if not clientes_en_memoria:
        return
    
    try:
        opcion_str = input("\nSeleccione el número de cliente a editar: \n>>> ")

        if not opcion_str.isdigit():
            print("\nDebe ingresar un número.")
            return
        
        opcion = int(opcion_str) - 1

        if opcion < 0 or opcion >= len(clientes_en_memoria):
            print("Opción inválida.")
            return
        
        cliente_seleccionado = clientes_en_memoria[opcion]

        print(f"\n--- CAMBIANDO PLAN A: {cliente_seleccionado.get_nombre()} ---")
        print("1. Plan Gratuito ($0.00)")
        print("2. Plan Premium ($19.99)")
        print("3. Plan Empresa (Desde $30.00)")

        tipo_plan = input("\nElija el nuevo plan (1-3): \n>>> ")

        nuevo_plan = None
        nombre_plan_log = ""
        duracion = 0

        if tipo_plan == "1":
            nuevo_plan = PlanGratuito()
            nombre_plan_log = "Gratuito"
            duracion = 12

        elif tipo_plan == "2":
            nuevo_plan = PlanPremium()
            nombre_plan_log = "Premium"
            duracion = 1

        elif tipo_plan == "3":
            print("\n--- CONFIGURACIÓN PLAN EMPRESA ---")
            try:
                usuarios = 0
                while True:
                    usuarios_input = input("Cantidad de usuarios (mín 3): \n>>> ")

                    if not usuarios_input.isdigit():
                        print("La cantidad de usuarios debe ser un número.")
                        continue

                    usuarios = int(usuarios_input)
                    if usuarios >= 3:
                        break

                    print("El Plan Empresa requiere mínimo 3 usuarios")
                
                dominio = ""
                while True:
                    dominio = input("Dominio personalizado (ej: miempresa.com): \n>>> ")

                    if "." in dominio:
                        break

                    print("\nError: El dominio debe tener una extensión (ej: .com).")

                nuevo_plan = PlanEmpresa(usuarios, dominio)
                nombre_plan_log = "Empresa"
                duracion = 12

            except Exception as e:
                print(f"\nError inesperado: {e}.")
                return
            
        else:
            print("Opción no válida.")
            return
        
        if nuevo_plan:
            
            nueva_susc = Suscripcion(duracion_meses=duracion)
            nuevo_plan.asignar_suscripcion(nueva_susc)

            cliente_seleccionado.cambiar_plan(nuevo_plan)
            print(f"\nPlan actualizado correctamente a {nombre_plan_log} (Vence: {nueva_susc.calcular_fecha_fin().strftime('%d/%m/%Y')}).")

            print("Beneficios activos:")
            for beneficio in nuevo_plan.listar_beneficios():
                print(f" • {beneficio}")

            registrar_actividad(f"Cambio de plan para {cliente_seleccionado.get_nombre()}: Ahora es {nombre_plan_log}")

    except ValueError:
        print("Error inesperado.")

def ver_logs():
    print("\n--- ÚLTIMOS REGISTROS ---")

    try:
        with open(ARCHIVO_LOG, "r", encoding="utf-8") as archivo:
            print(archivo.read())
    except FileNotFoundError:
        print("Aún no hay registros de actividad.")

def simular_uso_espacio():
    listar_clientes_registrados()

    if not clientes_en_memoria:
        return
    
    try:
        opcion_str = input("\nSeleccione el cliente para subir archivos: \n>>> ")

        if not opcion_str.isdigit():
            print("\nDebe ingresar un número entero.")
            return
        
        opcion = int(opcion_str) - 1
        if opcion < 0 or opcion >= len(clientes_en_memoria):
            print("\nOpción inválida.")
            return
        
        cliente = clientes_en_memoria[opcion]
        
        print(f"\nCliente: {cliente.get_nombre()}")
        print(f"Espacio actual: {cliente.get_gb_uso()} GB")
        
        gbs_str = input("\n¿Cuántos GB desea subir? (ej: 2.5): \n>>> ")

        try:
            gbs = float(gbs_str)
            if gbs <= 0:
                raise ValueError
        except ValueError:
            print("\nDebe ingresar un número positivo (ej: 5 o 2.5).")
            return

        exito = cliente.subir_archivos(gbs)

        if exito:
            print(f"\nArchivos subidos exitosamente.")
            print(f"Nuevo uso: {cliente.get_gb_uso()} GB")
            registrar_actividad(f"Usuario: {cliente.get_nombre()}, RUT:{cliente.get_rut()} subió {gbs}GB.")
        else:
            print(f"\nError: Espacio insuficiente en el plan actual.")
            registrar_actividad(f"Usuario: {cliente.get_nombre()}, RUT:{cliente.get_rut()} falló al subir {gbs}GB (Espacio insuficiente).", es_error=True)

    except Exception as e:
        print(f"\nError inesperado: {e}")


