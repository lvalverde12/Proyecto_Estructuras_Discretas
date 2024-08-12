import pandas as pd

ruta_csv = 'Rutas.csv'
datos = pd.read_csv(ruta_csv)

adyacencia = {}

for _, fila in datos.iterrows():
    nodo_inicio = str(fila['Código Distrito Inicio'])
    nodo_final = str(fila['Código Distrito Final'])
    
    if nodo_inicio not in adyacencia:
        adyacencia[nodo_inicio] = []
    adyacencia[nodo_inicio].append(nodo_final)
    if nodo_final not in adyacencia:
        adyacencia[nodo_final] = []
    adyacencia[nodo_final].append(nodo_inicio)

# Crear un DataFrame con la lista de adyacencias
adyacencia_df = pd.DataFrame({
    'nodo': list(adyacencia.keys()),
    'adyacentes': list(adyacencia.values())
})

# Convertir los valores numéricos a cadenas
adyacencia_df['nodo'] = adyacencia_df['nodo'].astype(str)
adyacencia_df['adyacentes'] = adyacencia_df['adyacentes'].apply(lambda x: '[' + ', '.join(x) + ']')

ruta_excel = 'listas_adyacencia.xlsx'
adyacencia_df.to_excel(ruta_excel, index=False)

print(f'Archivo {ruta_excel} creado con éxito.')