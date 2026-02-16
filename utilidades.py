import os
from datetime import datetime
from modelos.cliente import Cliente
from modelos.plan import PlanGratuito, PlanPremium, PlanEmpresa

# --- CONFIGURACIÓN ---
ARCHIVO_LOG = "datos/registro.txt"
clientes_en_memoria = []            # Lista que alamacena objetos Cliente durante la ejecución

# --- FUNCIONES UTILITARIAS ---

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def registrar_actividad(mensaje, es_error=False):
    fecha_hora = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    tipo = "[ERROR]" if es_error else "[INFO]"
    linea = f"{fecha_hora} - {tipo} - {mensaje}\n"

    if not os.path.exists("datos"):
        os.makedirs("datos")

    try:
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(linea)
    except Exception as e:
        print(f"Error crítico al guardar log: {e}")

# --- FUNCIONES DEL MENÚ ---

def crear_nuevo_cliente():
    limpiar_pantalla()
    print("\n--- REGISTRO DE NUEVO CLIENTE ---")

    nombre = input("\nNombre completo: \n>>> ")

    while True:
        rut = input("\nRUT con guión (ej: 12345678-9): \n>>> ")
        if "-" in rut:
            break
        print("Error: El RUT debe tener un guión. Inténtalo de nuevo.")

    while True:
        email = input("\nEmail: \n>>> ")
        if "@" in email and "." in email:
            break
        print("Error: Email inválido (falta @ o .). Inténtalo de nuevo.")

    try:
        nuevo_cliente = Cliente(nombre, rut, email)
        clientes_en_memoria.append(nuevo_cliente)

        print(f"\nCliente {nuevo_cliente.get_nombre()} creado exitosamente.")
        registrar_actividad(f"\nCliente creado: {nuevo_cliente.get_nombre()} (RUT: {rut})")

        input("\nPresione Enter para volver... ")

    except ValueError as e:
        print(f"\nError de validación interna: {e}")
        registrar_actividad(f"Fallo al crear cliente {rut}: {e}", es_error=True)

        input("\nPresione Enter para volver... ")

    except Exception as e:
        print(f"\nError inesperado: {e}")
        registrar_actividad(f"Error crítico: {e}", es_error=True)

def listar_clientes_registrados():
    print("\n--- LISTADO DE CLIENTES ---")

    if not clientes_en_memoria:
        print("No hay clientes registrados en memoria.")
        return
    
    for i, cliente in enumerate(clientes_en_memoria, 1):
        print(f"{i}. {cliente}")

def gestionar_planes():
    limpiar_pantalla()
    listar_clientes_registrados()

    if not clientes_en_memoria:
        input("\nPresione Enter para volver... ")
        return
    
    try:
        opcion_str = input("\nSeleccione el número de cliente a editar: \n>>> ")

        if not opcion_str.isdigit():
            print("\nDebe ingresar un número.")
            input("\nPresione Enter... ")
            return
        
        opcion = int(opcion_str) - 1

        if opcion < 0 or opcion >= len(clientes_en_memoria):
            print("Opción inválida.")
            input("\nPresione Enter... ")
            return
        
        cliente_seleccionado = clientes_en_memoria[opcion]

        print(f"\nEditando plan de: {cliente_seleccionado.get_nombre()}")
        print("1. Plan Gratuito")
        print("2. Plan Premium")
        print("3. Plan Empresa")

        tipo_plan = input("\nElija el nuevo plan (1-3): \n>>> ")

        nuevo_plan = None
        nombre_plan_log = ""

        if tipo_plan == "1":
            nuevo_plan = PlanGratuito()
            nombre_plan_log = "Gratuito"

        elif tipo_plan == "2":
            nuevo_plan = PlanPremium()
            nombre_plan_log = "Premium"

        elif tipo_plan == "3":
            print("\nConfiguración Plan Empresa")
            try:
                usuarios_input = input("Cantidad de usuarios (mín 3): \n>>> ")
                if not usuarios_input.isdigit():
                    raise ValueError("La cantidad de usuarios debe ser un número.")
                usuarios = int(usuarios_input)
                if usuarios < 3:
                    raise ValueError("El Plan Empresa requiere un mínimo de 3 usuarios.")
                
                while True:
                    dominio = input("Dominio personalizado (ej: miempresa.com): \n>>> ")

                    if "." in dominio:
                        break
                    print("\nError: El dominio debe tener una extensión (ej: .com, .cl).")

                nuevo_plan = PlanEmpresa(usuarios, dominio)
                nombre_plan_log = "Empresa"

            except ValueError as e:
                print(f"Error de validación: {e}")
                input("\nPresione Enter para volver... ")
                return
            
        else:
            print("Opción no válida.")
            input("\nPresione Enter... ")
            return
        
        if nuevo_plan:
            cliente_seleccionado.cambiar_plan(nuevo_plan)
            print(f"\nPlan actualizado correctamente a {nombre_plan_log}.")

            print("Beneficios activos:")
            for beneficio in nuevo_plan.listar_beneficios():
                print(f" • {beneficio}")

            registrar_actividad(f"Cambio de plan para {cliente_seleccionado.get_nombre()} (RUT: {cliente_seleccionado.get_rut()}): Ahora es {nombre_plan_log}")

            input("\nPresione Enter para volver... ")

    except ValueError:
        print("Error: Debe ingresar un número válido para seleccionar cliente.")
        input("\nPresione Enter... ")

def ver_logs():
    print("\n--- ÚLTIMOS REGISTROS ---")

    try:
        with open(ARCHIVO_LOG, "r", encoding="utf-8") as archivo:
            print(archivo.read())

    except FileNotFoundError:
        print("Aún no hay registros de actividad.")

def simular_uso_espacio():
    limpiar_pantalla()
    listar_clientes_registrados()

    if not clientes_en_memoria:
        input("\nPresione Enter para volver...")
        return
    
    try:
        print("\nSeleccione el cliente para subir archivos:")
        opcion_str = input(">>> ")

        if not opcion_str.isdigit():
            print("\nDebe ingresar un número entero.")
            input("Presione Enter... ")
            return
        
        opcion = int(opcion_str) - 1
        if opcion < 0 or opcion >= len(clientes_en_memoria):
            print("\nOpción inválida.")
            input("Presione Enter... ")
            return
        
        cliente = clientes_en_memoria[opcion]
        
        print(f"\nCliente: {cliente.get_nombre()}")
        print(f"Espacio actual: {cliente.get_gb_uso()} GB")
        
        print("\n¿Cuántos GB desea subir? (ej: 2.5):")
        gbs_str = input(">>> ")

        try:
            gbs = float(gbs_str)
            if gbs <= 0:
                raise ValueError
        except ValueError:
            print("\nDebe ingresar un número positivo (ej: 5 o 2.5).")
            input("Presione Enter...")
            return

        exito = cliente.subir_archivos(gbs)

        if exito:
            print(f"\nArchivos subidos exitosamente.")
            print(f"Nuevo uso: {cliente.get_gb_uso()} GB")
            registrar_actividad(f"Usuario {cliente.get_rut()} subió {gbs}GB.")
        else:
            print(f"\nError: Espacio insuficiente en el plan actual.")
            registrar_actividad(f"Usuario {cliente.get_rut()} falló al subir {gbs}GB (Espacio insuficiente).", es_error=True)
            
        input("\nPresione Enter para continuar...")

    except Exception as e:
        print(f"\nError inesperado: {e}")
        input("Presione Enter...")


