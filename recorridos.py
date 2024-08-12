import csv
import networkx as nx
from openpyxl import Workbook

def load_graph_from_csv(csv_file):
    G = nx.Graph()
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            inicio = row['Código Distrito Inicio']
            fin = row['Código Distrito Final']
            extension = int(round(float(row['Extensión (km)'])))
            G.add_node(inicio, label=row['Cantón Inicio'])
            G.add_node(fin, label=row['Cantón Final'])
            G.add_edge(inicio, fin, weight=extension, label=row['Código CTP'])
    return G

def find_all_paths(G, start_node):
    paths = {}
    for node in G.nodes():
        if node != start_node:
            try:
                path = nx.shortest_path(G, source=start_node, target=node, weight='weight')
                length = nx.shortest_path_length(G, source=start_node, target=node, weight='weight')
                paths[node] = (path, int(round(length)))
            except nx.NetworkXNoPath:
                paths[node] = ([], float('inf'))
    return paths

def export_paths_to_excel(paths, filename):
    wb = Workbook()
    ws = wb.active
    ws.title = "Recorridos"
    
    ws.append(["Destino", "Recorrido", "Distancia (km)"])
    
    for dest, (path, length) in paths.items():
        if path:
            path_str = " -> ".join(path)
            ws.append([dest, path_str, length])
        else:
            ws.append([dest, "No hay recorrido", "N/A"])
    
    wb.save(filename)

def main():
    csv_file = 'Rutas.csv'
    G = load_graph_from_csv(csv_file)
    start_node = '101'  # San José
    
    print("Calculando todos los recorridos posibles...")
    all_paths = find_all_paths(G, start_node)
    
    excel_file = 'Recorridos.xlsx'
    export_paths_to_excel(all_paths, excel_file)
    print(f"Se ha creado el archivo '{excel_file}' con todos los recorridos.")

if __name__ == '__main__':
    main()