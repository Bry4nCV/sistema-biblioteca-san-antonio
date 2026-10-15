from abc import ABC, abstractmethod


class MaterialBibliografico(ABC):

  def __init__(self, id_material: str, titulo: str, autor: str, stock: int):
    self._id_material = id_material
    self._titulo = titulo
    self._autor = autor
    self._stock = stock

  @property
  def id_material(self):
    return self._id_material

  @property
  def titulo(self):
    return self._titulo

  @property
  def stock(self):
    return self._stock

  @stock.setter
  def stock(self, nuevo_stock: int):
    if nuevo_stock < 0:
      raise ValueError("El stock no puede ser negativo.")
    self._stock = nuevo_stock

  @abstractmethod
  def calcular_mora(self, dias_retraso: int) -> float:
    pass


class TextoEscolar(MaterialBibliografico):
  TARIFA_DIARIA = 2.0

  def calcular_mora(self, dias_retraso: int) -> float:
    return max(0.0, dias_retraso * self.TARIFA_DIARIA)


class CompendioPreuniversitario(MaterialBibliografico):
  TARIFA_DIARIA = 3.5

  def calcular_mora(self, dias_retraso: int) -> float:
    return max(0.0, dias_retraso * self.TARIFA_DIARIA)


class ExamenAdmision(MaterialBibliografico):
  TARIFA_DIARIA = 4.0

  def calcular_mora(self, dias_retraso: int) -> float:
    return max(0.0, dias_retraso * self.TARIFA_DIARIA)


class Usuario(ABC):

  def __init__(self, dni: str, nombre: str, email: str):
    self._dni = dni
    self._nombre = nombre
    self._email = email
    self._estado = "ACTIVO"

  @property
  def dni(self):
    return self._dni

  @property
  def nombre(self):
    return self._nombre

  @property
  def estado(self):
    return self._estado

  @estado.setter
  def estado(self, nuevo_estado: str):
    self._estado = nuevo_estado

  @abstractmethod
  def aplicar_sancion(self, monto_mora: float, dias_retraso: int) -> str:
    pass

  @abstractmethod
  def obtener_tipo(self) -> str:
    pass


class Alumno(Usuario):

  def __init__(
      self,
      dni: str,
      nombre: str,
      email: str,
      modalidad: str,
      grado_ciclo: str,
  ):
    super().__init__(dni, nombre, email)
    self._modalidad = modalidad
    self._grado_ciclo = grado_ciclo
    self._monto_pension_extra = 0.0

  @property
  def monto_pension_extra(self):
    return self._monto_pension_extra

  def aplicar_sancion(self, monto_mora: float, dias_retraso: int) -> str:
    if monto_mora > 0:
      self._monto_pension_extra += monto_mora
      return (
          f"Se añadió un recargo de S/ {monto_mora:.2f} a la pensión mensual.\n"
          f"(Total acumulado de mora en pensión: S/"
          f" {self._monto_pension_extra:.2f})"
      )
    return "Devolución a tiempo. No se genera recargo."

  def obtener_tipo(self) -> str:
    return f"Alumno ({self._modalidad} - {self._grado_ciclo})"


class Profesor(Usuario):

  def __init__(
      self, dni: str, nombre: str, email: str, area_academica: str
  ):
    super().__init__(dni, nombre, email)
    self._area_academica = area_academica
    self._monto_descuento_planilla = 0.0

  @property
  def monto_descuento_planilla(self):
    return self._monto_descuento_planilla

  def aplicar_sancion(self, monto_mora: float, dias_retraso: int) -> str:
    if dias_retraso > 0:
      self._estado = "INHABILITADO"
      self._monto_descuento_planilla += monto_mora
      return (
          f"El docente ha sido INHABILITADO.\nSe generó orden de descuento"
          f" por S/ {monto_mora:.2f}.\n(Total planilla: S/"
          f" {self._monto_descuento_planilla:.2f})"
      )
    return "Devolución a tiempo. Sin observaciones."

  def obtener_tipo(self) -> str:
    return f"Profesor (Área: {self._area_academica})"
