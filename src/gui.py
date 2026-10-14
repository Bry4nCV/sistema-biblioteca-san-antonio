import tkinter as tk
from tkinter import messagebox, ttk
from src.excepciones import BibliotecaError
from src.modelos import Alumno
from src.sistema import SistemaBibliotecaCompleto


class BibliotecaGUI:

  def __init__(self, root):
    self.root = root
    self.root.title(
        "Sistema de Gestión de Biblioteca - Colegio y Academia San Antonio"
    )
    self.root.geometry("800x550")

    self.sistema = SistemaBibliotecaCompleto()

    # Creación de Pestañas (Notebook)
    self.notebook = ttk.Notebook(self.root)
    self.notebook.pack(fill="both", expand=True)

    self.tab_inventario = ttk.Frame(self.notebook)
    self.tab_usuarios = ttk.Frame(self.notebook)
    self.tab_prestamo = ttk.Frame(self.notebook)
    self.tab_devolucion = ttk.Frame(self.notebook)

    self.notebook.add(self.tab_inventario, text="Inventario")
    self.notebook.add(self.tab_usuarios, text="Usuarios")
    self.notebook.add(self.tab_prestamo, text="Préstamos")
    self.notebook.add(self.tab_devolucion, text="Devoluciones")

    self.setup_inventario_tab()
    self.setup_usuarios_tab()
    self.setup_prestamo_tab()
    self.setup_devolucion_tab()

  def setup_inventario_tab(self):
    frame = ttk.Frame(self.tab_inventario, padding=10)
    frame.pack(fill="both", expand=True)

    self.tree_inv = ttk.Treeview(
        frame, columns=("ID", "Título", "Autor", "Stock"), show="headings"
    )
    self.tree_inv.heading("ID", text="ID")
    self.tree_inv.heading("Título", text="Título")
    self.tree_inv.heading("Autor", text="Autor / Editorial")
    self.tree_inv.heading("Stock", text="Stock")
    self.tree_inv.pack(fill="both", expand=True, pady=5)

    btn = ttk.Button(
        frame, text="Actualizar Inventario", command=self.actualizar_inventario
    )
    btn.pack(pady=5)
    self.actualizar_inventario()

  def actualizar_inventario(self):
    for row in self.tree_inv.get_children():
      self.tree_inv.delete(row)
    for m in self.sistema._catalogo:
      self.tree_inv.insert(
          "", "end", values=(m.id_material, m.titulo, m._autor, m.stock)
      )

  def setup_usuarios_tab(self):
    frame = ttk.Frame(self.tab_usuarios, padding=10)
    frame.pack(fill="both", expand=True)

    self.tree_usr = ttk.Treeview(
        frame,
        columns=("DNI", "Nombre", "Tipo", "Estado", "Deuda/Planilla"),
        show="headings",
    )
    self.tree_usr.heading("DNI", text="DNI")
    self.tree_usr.heading("Nombre", text="Nombre")
    self.tree_usr.heading("Tipo", text="Tipo / Modalidad")
    self.tree_usr.heading("Estado", text="Estado")
    self.tree_usr.heading("Deuda/Planilla", text="Extra Pensión / Planilla")
    self.tree_usr.pack(fill="both", expand=True, pady=5)

    btn = ttk.Button(
        frame, text="Actualizar Lista Usuarios", command=self.actualizar_usuarios
    )
    btn.pack(pady=5)
    self.actualizar_usuarios()

  def actualizar_usuarios(self):
    for row in self.tree_usr.get_children():
      self.tree_usr.delete(row)
    for u in self.sistema._usuarios:
      monto = (
          u.monto_pension_extra
          if isinstance(u, Alumno)
          else u.monto_descuento_planilla
      )
      self.tree_usr.insert(
          "",
          "end",
          values=(u.dni, u.nombre, u.obtener_tipo(), u.estado, f"S/ {monto:.2f}"),
      )

  def setup_prestamo_tab(self):
    frame = ttk.Frame(self.tab_prestamo, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="DNI del Usuario:").pack(anchor="w")
    self.entry_dni_p = ttk.Entry(frame, width=30)
    self.entry_dni_p.pack(anchor="w", pady=5)

    ttk.Label(frame, text="ID del Material:").pack(anchor="w")
    self.entry_mat_p = ttk.Entry(frame, width=30)
    self.entry_mat_p.pack(anchor="w", pady=5)

    btn_prestar = ttk.Button(
        frame, text="Registrar Préstamo", command=self.ejecutar_prestamo
    )
    btn_prestar.pack(anchor="w", pady=15)

  def ejecutar_prestamo(self):
    dni = self.entry_dni_p.get().strip()
    id_mat = self.entry_mat_p.get().strip()
    try:
      msg = self.sistema.realizar_prestamo(dni, id_mat)
      messagebox.showinfo("Éxito", msg)
      self.actualizar_inventario()
      self.actualizar_usuarios()
    except BibliotecaError as e:
      messagebox.showerror("Error de Negocio", str(e))
    except Exception as ex:
      messagebox.showerror("Error", str(ex))

  def setup_devolucion_tab(self):
    frame = ttk.Frame(self.tab_devolucion, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="ID del Préstamo:").pack(anchor="w")
    self.entry_id_p = ttk.Entry(frame, width=30)
    self.entry_id_p.pack(anchor="w", pady=5)

    ttk.Label(frame, text="Días de Retraso:").pack(anchor="w")
    self.entry_dias = ttk.Entry(frame, width=30)
    self.entry_dias.pack(anchor="w", pady=5)

    btn_dev = ttk.Button(
        frame, text="Procesar Devolución", command=self.ejecutar_devolucion
    )
    btn_dev.pack(anchor="w", pady=15)

  def ejecutar_devolucion(self):
    try:
      id_p = int(self.entry_id_p.get().strip())
      dias = int(self.entry_dias.get().strip())
      resultado = self.sistema.registrar_devolucion_por_id(id_p, dias)
      messagebox.showinfo("Devolución Procesada", resultado)
      self.actualizar_inventario()
      self.actualizar_usuarios()
    except ValueError:
      messagebox.showerror(
          "Error de Formato", "Ingrese números válidos para ID y días."
      )
    except BibliotecaError as e:
      messagebox.showerror("Error", str(e))
