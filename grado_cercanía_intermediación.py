import csv
import networkx as nx
import pandas as pd

def load_graph_from_csv(csv_file):
    G = nx.Graph()
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ruta = row['Código CTP']
            inicio = row['Código Distrito Inicio']
            fin = row['Código Distrito Final']
            extension = float(row['Extensión (km)'])

            G.add_node(inicio, label=row['Cantón Inicio'])
            G.add_node(fin, label=row['Cantón Final'])
            G.add_edge(inicio, fin, weight=extension, label=ruta)
    return G

def calculate_centralities(G):
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    return degree_centrality, closeness_centrality, betweenness_centrality

csv_file = "Rutas.csv"
G = load_graph_from_csv(csv_file)

degree_centrality, closeness_centrality, betweenness_centrality = calculate_centralities(G)

# Create a pandas DataFrame to store the centrality measures
df = pd.DataFrame({
    'Nodo': list(degree_centrality.keys()),
    'Centralidad de Grado': list(degree_centrality.values()),
    'Centralidad de Cercanía': list(closeness_centrality.values()),
    'Centralidad de Intermediación': list(betweenness_centrality.values())
})

# Export the DataFrame to an Excel file
df.to_excel('Grado_Cercanía_Intermediación.xlsx', index=False)