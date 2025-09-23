# EJERCICIO 1

# Datos iniciales - NO MODIFICAR
estudiantes = ["Rodriguez", "Gonzalez", "Martinez", "Lopez", "Silva", "Vargas", "Torres"]
notas_parcial = [14, 16, 12, 18, 15, 13, 17]
notas_final = [16, 15, 14, 17, 16, 12, 18]

print("=== REGISTRO DE NOTAS ACTUAL ===")
print("Estudiante\t\tParcial\tFinal")
for i in range(len(estudiantes)):
    print(f"{estudiantes[i]}\t\t{notas_parcial[i]}\t{notas_final[i]}")


# a)
nueva_nota_parcial = [notas + 1 for notas in notas_parcial]
print(nueva_nota_parcial)

print("\n")

# b) y c) Versión optimizada
promedios_finales = [(nueva_nota_parcial[i] * 0.4 + notas_final[i] * 0.6) for i in range(len(estudiantes))]

# Esto reemplaza todas las asignaciones individuales de promedios

print("\n")


# d)

promedio_alto = max(promedios_finales)
estudiante_promedio_alto = estudiantes[promedios_finales.index(promedio_alto)]
promedio_bajo = min(promedios_finales)
estudiante_promedio_bajo = estudiantes[promedios_finales.index(promedio_bajo)]


print(f"Calificación más alta: {estudiante_promedio_alto} con {promedio_alto} puntos.")
print(f"Calificación más baja: {estudiante_promedio_bajo} con {promedio_bajo} puntos.")


# EJERCICIO 2

# Datos iniciales - NO MODIFICAR
dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
destinos = ["Laguna 69", "Pastoruri", "Chavín", "Santa Cruz"]

# Matriz de visitantes [día][destino]
visitantes = [
    [45, 30, 25, 40],   # Lunes
    [50, 35, 30, 45],   # Martes
    [40, 25, 20, 35],   # Miércoles
    [55, 40, 35, 50],   # Jueves
    [65, 45, 40, 60],   # Viernes
    [85, 70, 65, 80],   # Sábado
    [90, 75, 70, 85],   # Domingo
]

print("=== FLUJO TURÍSTICO SEMANAL EN HUARAZ ===")
print("Día\t\tLaguna 69\tPastoruri\tChavín\t\tSanta Cruz")
for i in range(len(dias_semana)):
    print(f"{dias_semana[i]}\t\t{visitantes[i][0]}\t\t{visitantes[i][1]}\t\t{visitantes[i][2]}\t\t{visitantes[i][3]}")



# a) Versión corregida
total_por_destino = [sum(dia[i] for dia in visitantes) for i in range(len(destinos))]
destino_mas_visitado = destinos[total_por_destino.index(max(total_por_destino))]
print(f"El destino más visitado fue {destino_mas_visitado} con {max(total_por_destino)} visitantes")

# b)
sumas_diarias = [sum(dias_semana) for dias_semana in visitantes]
suma_maxima = max(sumas_diarias)
indice_dia_maximo = sumas_diarias.index(suma_maxima)
dia_con_maxima_suma = dias_semana[indice_dia_maximo]


print(f"b) El día con la mayor suma de visitantes fue: {dia_con_maxima_suma} (Suma total: {suma_maxima}")


# c) 

max_visitantes_semana = 0
dia_pico = ""
destino_pico = ""

for i, dia_visitantes in enumerate(visitantes):
    for j, num_visitantes in enumerate(dia_visitantes):
        if num_visitantes > max_visitantes_semana:
            max_visitantes_semana = num_visitantes
            dia_pico = dias_semana[i]
            destino_pico = destinos[j]

print(f"El mayor número de visitantes fue {max_visitantes_semana} el día {dia_pico} en {destino_pico}.\n")


# d) Versión corregida
promedios_destino = [sum(dia[i] for dia in visitantes) / len(dias_semana) for i in range(len(destinos))]