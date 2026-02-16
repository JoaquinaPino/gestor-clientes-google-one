from utilidades import (
    limpiar_pantalla, 
    registrar_actividad, 
    crear_nuevo_cliente, 
    listar_clientes_registrados, 
    gestionar_planes,
    ver_logs,
    simular_uso_espacio
)

def main():
    registrar_actividad("Sistema GIC iniciado.")
    
    while True:
        limpiar_pantalla()
        print("========================================")
        print("   GESTOR INTELIGENTE DE CLIENTES (GIC)")
        print("         Solution Tech v1.0")
        print("========================================")
        print("1. Registrar Nuevo Cliente")
        print("2. Listar Clientes")
        print("3. Actualizar Plan de Cliente")
        print("4. Simular Subida de Archivos")
        print("5. Ver Log de Actividad")
        print("6. Salir")
        
        opcion = input("\nIngrese una opción: \n>>> ")

        if opcion == "1":
            crear_nuevo_cliente()

        elif opcion == "2":
            listar_clientes_registrados()
            input("\nPresione Enter para continuar... ") 

        elif opcion == "3":
            gestionar_planes()
            input("\nPresione Enter para continuar...")

        elif opcion == "4":
            simular_uso_espacio()

        elif opcion == "5":
            ver_logs()
            input("\nPresione Enter para continuar...")

        elif opcion == "6":
            print("\nCerrando sistema... ¡Hasta pronto!")
            registrar_actividad("Sistema cerrado correctamente.")
            break
        
        else:
            print("\nOpción no válida. Intente nuevamente.")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()