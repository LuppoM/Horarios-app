
operarios_ocupados = set()

def agregar_operario(operario):
    """
    Agrega un operario al conjunto de operarios ocupados.
    """
    operarios_ocupados.add(operario)

def quitar_operario(operario):
    """
    Elimina un operario del conjunto de operarios ocupados.
    """
    operarios_ocupados.discard(operario)

def esta_ocupado(operario):
    """
    Verifica si un operario está ocupado.
    """
    return operario in operarios_ocupados

def obtener_operarios_ocupados():
    """
    Retorna el conjunto de operarios ocupados.
    """
    return operarios_ocupados
