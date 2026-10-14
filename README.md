Sistema de Gestión de Biblioteca - Colegio y Academia San Antonio

Sistema modular desarrollado en Python utilizando Programación Orientada a Objetos (POO), manejo de excepciones personalizadas, asociaciones de negocio e interfaz gráfica con Tkinter.

👥 Estructura del Equipo y Roles (Sincronizado con Trello)

El desarrollo del proyecto está distribuido entre 3 integrantes:

Integrante 1 - Almendra Freyre (src/excepciones.py y parte de src/modelos.py):

Implementación de excepciones personalizadas (BibliotecaError, SinStockError, UsuarioInhabilitadoError, AlumnoConDeudaError, etc.).

Jerarquía de materiales bibliográficos (MaterialBibliografico, TextoEscolar, CompendioPreuniversitario, ExamenAdmision) aplicando herencia y polimorfismo.

Integrante 2 - Felipe Oballe (src/modelos.py y src/sistema.py):

Jerarquía de usuarios (Usuario, Alumno, Profesor).

Lógica de asociación con la clase Prestamo.

Controlador central SistemaBibliotecaCompleto con datos de prueba y reglas de negocio.

Integrante 3 - Bryan Carlos Velasco (src/gui.py y main.py):

Construcción de la interfaz gráfica en Tkinter basada en pestañas (ttk.Notebook).

Integración de los componentes visuales (Treeview, formularios) con el controlador del backend.

Punto de entrada ejecutable de la aplicación.
