def calcular_prioridad_despacho(peso, distancia, urgente, fragil):
    prioridad = 0

    if peso > 50:
        prioridad += 2
    elif peso > 20:
        prioridad += 1

    if distancia > 500:
        prioridad += 2
    elif distancia > 100:
        prioridad += 1

    if urgente:
        prioridad += 3

    if fragil:
        prioridad += 2

    if prioridad >= 6:
        return "alta"
    elif prioridad >= 3:
        return "media"
    else:
        return "baja"
