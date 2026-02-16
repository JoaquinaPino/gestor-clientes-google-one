# PROYECTO MÓDULO 4: Gestor Inteligente de Clientes (GIC) - Google One

Sistema de consola desarrollado en Python para la administración eficiente de clientes, gestión de planes de servicio (Gratuito, Premium, Enterprise) y control de suscripciones.

## Sobre el proyecto
Este proyecto nace de la necesidad de administrar el registro de clientes y la gestión de sus servicios en una plataforma digital. El sistema se especializa en el alta de nuevos usuarios, la validación estricta de datos personales y la actualización dinámica de planes (upgrade/downgrade), asegurando que cada cliente cuente con el nivel de servicio adecuado (Free, Premium, Enterprise).

## Funciones Principales
El sistema GIC ofrece las siguientes capacidades operativas:

* **Registro de Clientes:** Alta de usuarios con validación en tiempo real de RUT y correo electrónico.
* **Gestión de Planes:** Capacidad para actualizar y modificar el servicio contratado entre tres niveles (Free, Premium, Enterprise), ajustando automáticamente beneficios y costos.
* **Control de Suscripciones:** Cálculo automático de fechas de vencimiento y costos asociados al plan seleccionado.
* **Simulación de Uso:** Módulo para simular la carga de archivos y validar si el almacenamiento disponible en el plan actual es suficiente.
* **Sistema de Logs:** Registro automático y persistente de todas las actividades críticas (altas, cambios de plan, errores) en un archivo de texto local.

## Instalación y Uso
Para ejecutar el sistema en un entorno local, siga estos pasos:

1.  Clonar el repositorio o descargar los archivos fuente.
2.  Asegurarse de tener Python 3.x instalado.
3. **Importante:** Entrar a la carpeta del proyecto antes de ejecutar:
   `cd PROYECTO_MODULO_4`
4. Ejecutar el programa:
   `python main.py`

### Formatos de Entrada
Para una correcta validación durante la ejecución, utilice los siguientes formatos:
* **RUT:** Debe incluir guion (Ej: `12345678-9`).
* **Email:** Debe contener '@' y '.' (Ej: `usuario@dominio.com`).
* **Dominio Empresa:** Debe incluir extensión (Ej: `miempresa.cl`).

## Estructura del Código
El proyecto sigue una arquitectura modular para facilitar el mantenimiento y la escalabilidad del software. Los componentes están organizados de la siguiente manera:

* **main.py:** Punto de entrada de la aplicación. Se encarga únicamente de orquestar el menú principal y el flujo de navegación.
* **utilidades.py:** Contiene la lógica operativa, validaciones de entrada por consola y la gestión de archivos (logs). Actúa como intermediario entre el usuario y los modelos.
* **modelos/**: Paquete que encapsula la lógica de negocio.
    * `cliente.py`: Clase que gestiona los datos personales y el estado del usuario.
    * `plan.py`: Jerarquía de clases (Herencia) para definir los diferentes niveles de servicio y sus beneficios.
    * `suscripcion.py`: Manejo de fechas, vigencia y renovación de servicios.
* **datos/**: Directorio generado automáticamente por el sistema para almacenar los registros de actividad (`registro.txt`).

## Salida de Datos
El sistema implementa persistencia de datos a través de archivos de texto.
* **Logs de Actividad:** Cada acción relevante genera una entrada en `datos/registro.txt` con fecha, hora, tipo de evento (INFO/ERROR) y descripción detallada. Esto permite una auditoría completa del uso del sistema incluso después de reiniciar la aplicación.

## Desafíos Técnicos
Durante el desarrollo se abordaron y resolvieron los siguientes retos:
* **Validación Bloqueante:** Implementación de bucles `while` para garantizar la integridad de los datos ingresados, impidiendo el avance del flujo hasta obtener inputs válidos.
* **Persistencia de Datos:** Manejo de rutas absolutas y modos de apertura de archivos (`append`) para asegurar que el historial de logs no se pierda entre ejecuciones.
* **Lógica de Negocio Temporal:** Cálculo preciso de fechas de vencimiento basado en la duración de la suscripción asignada a cada plan.

## Demostración
Puede ver una demostración funcional del sistema en el siguiente enlace:
[Enlace a YouTube]

---
**Autor:** Joaquina Pino
**Curso:** Python Full Stack - Módulo 4