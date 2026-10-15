from datetime import datetime, timedelta
from src.excepciones import (
    AlumnoConDeudaError,
    BibliotecaError,
    MaterialNoEncontradoError,
    SinStockError,
    UsuarioInhabilitadoError,
    UsuarioNoEncontradoError,
)
from src.modelos import (
    Alumno,
    CompendioPreuniversitario,
    ExamenAdmision,
    MaterialBibliografico,
    Profesor,
    TextoEscolar,
    Usuario,
)


class Prestamo:

  def __init__(
      self,
      id_prestamo: int,
      usuario: Usuario,
      material: MaterialBibliografico,
      dias_prestamo: int = 7,
  ):
    self._id_prestamo = id_prestamo
    self._usuario = usuario
    self._material = material
    self._fecha_prestamo = datetime.now()
    self._fecha_limite = self._fecha_prestamo + timedelta(days=dias_prestamo)
    self._estado = "ACTIVO"
    self._mora_calculada = 0.0

  @property
  def id_prestamo(self):
    return self._id_prestamo

  @property
  def usuario(self):
    return self._usuario

  @property
  def material(self):
    return self._material

  @property
  def estado(self):
    return self._estado

  def registrar_devolucion(self, dias_retraso_simulado: int = 0) -> str:
    self._estado = "DEVUELTO"
    self._material.stock += 1
    self._mora_calculada = self._material.calcular_mora(dias_retraso_simulado)
    mensaje_sancion = self._usuario.aplicar_sancion(
        self._mora_calculada, dias_retraso_simulado
    )
    return (
        f"Devolución Exitosa (Préstamo #{self._id_prestamo})\n- Usuario:"
        f" {self._usuario.nombre}\n- Material: {self._material.titulo}\n- Mora:"
        f" S/ {self._mora_calculada:.2f}\n{mensaje_sancion}"
    )


class SistemaBibliotecaCompleto:

  def __init__(self):
    self._catalogo = []
    self._usuarios = []
    self._prestamos = []
    self._contador_prestamos = 1
    self._cargar_datos_prueba()

  def _cargar_datos_prueba(self):
    self._catalogo.append(
        TextoEscolar("ESC-01", "Matemática 4to Sec", "Santillana", 3)
    )
    self._catalogo.append(
        CompendioPreuniversitario("PRE-01", "Física Pre-UNI", "San Antonio", 2)
    )
    self._catalogo.append(
        ExamenAdmision("ADM-01", "Solucionario San Marcos", "Editorial", 1)
    )
    self._usuarios.append(
        Alumno(
            "73412589",
            "Renzo Farfán",
            "renzo@mail.com",
            "Academia",
            "Pre-UNI",
        )
    )
    self._usuarios.append(
        Profesor(
            "10452389",
            "Carlos Gutiérrez",
            "cgutierrez@colegio.edu.pe",
            "Ciencias",
        )
    )

  def agregar_material(self, material: MaterialBibliografico):
    self._catalogo.append(material)

  def registrar_usuario(self, usuario: Usuario):
    self._usuarios.append(usuario)

  def buscar_material(self, id_material: str):
    for mat in self._catalogo:
      if mat.id_material.upper() == id_material.upper():
        return mat
    raise MaterialNoEncontradoError(id_material)

  def buscar_usuario(self, dni: str):
    for usr in self._usuarios:
      if usr.dni == dni:
        return usr
    raise UsuarioNoEncontradoError(dni)

  def realizar_prestamo(self, dni_usuario: str, id_material: str, dias=7):
    usuario = self.buscar_usuario(dni_usuario)
    material = self.buscar_material(id_material)

    if isinstance(usuario, Profesor) and usuario.estado == "INHABILITADO":
      raise UsuarioInhabilitadoError(usuario.nombre)
    if isinstance(usuario, Alumno) and usuario.monto_pension_extra > 50.0:
      raise AlumnoConDeudaError(usuario.nombre, usuario.monto_pension_extra)
    if material.stock <= 0:
      raise SinStockError(material.titulo)

    material.stock -= 1
    nuevo_p = Prestamo(self._contador_prestamos, usuario, material, dias)
    self._prestamos.append(nuevo_p)
    self._contador_prestamos += 1
    return f"Préstamo #{nuevo_p.id_prestamo} registrado con éxito."

  def registrar_devolucion_por_id(self, id_prestamo: int, dias_retraso: int):
    for p in self._prestamos:
      if p.id_prestamo == id_prestamo and p.estado == "ACTIVO":
        return p.registrar_devolucion(dias_retraso)
    raise BibliotecaError(
        f"No se encontró un préstamo activo con ID #{id_prestamo}."
    )

