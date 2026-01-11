# Librerías necesarias para generar datos, manejarlos y graficarlos
from faker import Faker
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Inicializa Faker y define cuántos registros se van a generar
fake = Faker()
NUM_REGISTROS = 10000

# Lista donde se guardarán todos los registros simulados
datos = []

# Bucle principal para generar los datos sintéticos
for _ in range(NUM_REGISTROS):
    
    # Genera datos demográficos y de contexto
    fecha = fake.date_between(start_date='-3M', end_date='today')
    edad = random.randint(18, 60)
    genero = random.choice(['Masculino', 'Femenino'])
    horas_sueno = round(random.uniform(4, 10), 2)
    cafeina = random.choice([0, 1])
    pasos = random.randint(1000, 15000)

    # Modelo base del nivel de energía según horas de sueño
    # Se basa en ciclos de sueño y en la inercia del despertar
    if horas_sueno < 5:
        energia_base = 3
    elif 5 <= horas_sueno <= 6.5:
        energia_base = 8
    elif 6.5 < horas_sueno <= 8:
        energia_base = 9
    elif 8 < horas_sueno <= 9:
        energia_base = 6
    else:
        energia_base = 4

    # Se agrega ruido para simular variabilidad humana y errores de percepción
    ruido = np.random.normal(0, 1.2)
    energia = energia_base + ruido

    # Ajuste leve del nivel de energía si hubo consumo de cafeína
    if cafeina == 1:
        energia += np.random.uniform(0.3, 1)

    # Se limita el nivel de energía al rango válido de 1 a 10
    energia = round(min(max(energia, 1), 10), 2)

    # Clasificación simple de buen o mal sueño
    buen_sueno = 6 <= horas_sueno <= 8

    # Se guarda el registro completo
    datos.append([
        fecha,
        edad,
        genero,
        horas_sueno,
        buen_sueno,
        cafeina,
        pasos,
        energia
    ])

# Se convierte la lista de registros en un DataFrame
df = pd.DataFrame(datos, columns=[
    'Fecha',
    'Edad',
    'Genero',
    'Horas_sueno',
    'Buen_sueno',
    'Cafeina',
    'Pasos',
    'Nivel_energia'
])

# Muestra una vista rápida de los primeros datos generados
print("Primeros registros:")
print(df.head())

# Agrupa las horas de sueño en intervalos de 0.5 horas
df['Intervalo_sueno'] = pd.cut(
    df['Horas_sueno'],
    bins=np.arange(4, 10.5, 0.5)
)

# Calcula el nivel de energía promedio por intervalo de sueño
energia_promedio = (
    df.groupby('Intervalo_sueno')['Nivel_energia']
    .mean()
    .reset_index()
)

print("\nDatos sin ruido (promedios por intervalo):")
print(energia_promedio)

# Ordena los datos por horas de sueño para aplicar suavizado
df_ordenado = df.sort_values('Horas_sueno')

# Aplica una media móvil para reducir el ruido y ver la tendencia general
df_ordenado['Energia_suavizada'] = (
    df_ordenado['Nivel_energia']
    .rolling(window=200, center=True)
    .mean()
)

# Gráfica de dispersión con los datos originales (con ruido)
plt.figure()
plt.scatter(
    df['Horas_sueno'],
    df['Nivel_energia'],
    alpha=0.25
)
plt.xlabel('Horas de sueño')
plt.ylabel('Nivel de energía')
plt.title('Nivel de energía vs horas de sueño (con ruido)')
plt.show()

# Gráfica de energía promedio por intervalo (sin ruido)
plt.figure()
plt.plot(
    energia_promedio['Intervalo_sueno'].astype(str),
    energia_promedio['Nivel_energia'],
    marker='o'
)
plt.xlabel('Intervalos de horas de sueño')
plt.ylabel('Nivel de energía promedio')
plt.title('Nivel de energía vs horas de sueño (sin ruido)')
plt.xticks(rotation=45)
plt.show()

# Gráfica suavizada usando media móvil
plt.figure()
plt.plot(
    df_ordenado['Horas_sueno'],
    df_ordenado['Energia_suavizada']
)
plt.xlabel('Horas de sueño')
plt.ylabel('Nivel de energía (suavizado)')
plt.title('Relación sueño–energía (media móvil)')
plt.show()

# Selección de variables numéricas para análisis de correlación
df_corr = df[
    ['Horas_sueno', 'Nivel_energia', 'Edad', 'Cafeina', 'Pasos']
]

# Cálculo de la matriz de correlación
corr_matrix = df_corr.corr()
print("Matriz de correlación:")
print(corr_matrix)

# Visualización de la matriz de correlación
plt.figure()
plt.imshow(corr_matrix)

plt.xticks(
    range(len(corr_matrix.columns)),
    corr_matrix.columns,
    rotation=45
)
plt.yticks(
    range(len(corr_matrix.columns)),
    corr_matrix.columns
)

# Se muestran los valores numéricos dentro de la matriz
for i in range(len(corr_matrix.columns)):
    for j in range(len(corr_matrix.columns)):
        plt.text(
            j,
            i,
            round(corr_matrix.iloc[i, j], 2),
            ha='center',
            va='center'
        )

plt.title('Matriz de correlación entre variables')
plt.colorbar()
plt.tight_layout()
plt.show()