from hchocofindecontrolador import ControladorHchocoFinde


def abrir_modulo_finde_choco(root, conexion):
  """Función puente para instanciar la pantalla de Alistamiento / Fin de Semana."""
  return ControladorHchocoFinde(root, conexion)