class BibliotecaError(Exception):
  """Clase base para las excepciones personalizadas del sistema."""

  pass


class SinStockError(BibliotecaError):

  def __init__(self, titulo: str):
    super().__init__(
        f"Error de Stock: No hay ejemplares disponibles del material '{titulo}'."
    )


class UsuarioInhabilitadoError(BibliotecaError):

  def __init__(self, nombre: str):
    super().__init__(
        f"Error de Usuario: El profesor '{nombre}' se encuentra INHABILITADO"
        " para nuevos préstamos."
    )


class AlumnoConDeudaError(BibliotecaError):

  def __init__(self, nombre: str, monto: float):
    super().__init__(
        f"Error de Préstamo: El alumno '{nombre}' tiene un recargo acumulado en"
        f" su pensión de S/ {monto:.2f} (Supera el límite permitido)."
    )


class MaterialNoEncontradoError(BibliotecaError):

  def __init__(self, id_material: str):
    super().__init__(
        f"Error de Búsqueda: No se encontró ningún material con ID"
        f" '{id_material}'."
    )


class UsuarioNoEncontradoError(BibliotecaError):

  def __init__(self, dni: str):
    super().__init__(
        f"Error de Búsqueda: No se encontró ningún usuario con DNI '{dni}'."
    )
