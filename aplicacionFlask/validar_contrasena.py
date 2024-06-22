import re

def validar_contrasena(contrasena):
  """
  Función que valida una contraseña usando expresiones regulares.

  Args:
      contrasena (str): Contraseña a validar.

  Raises:
      ValueError: Si la contraseña no cumple con los requisitos.

  Returns:
      None: Si la contraseña es válida.
  """

  patron = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^\w\s]).{8,}$"

  if not re.match(patron, contrasena):
    raise ValueError("Contraseña no válida. Debe tener al menos 8 caracteres, contener una letra mayúscula, una minúscula, un número y un símbolo especial.")

  return None

# Ejemplo de uso
# try:
#   validar_contrasena("MiContraseña123!")
#   print("Contraseña válida")
# except ValueError as e:
#   print(e)
