import csv
import networkx as nx
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from networkx.algorithms.community import greedy_modularity_communities

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

def calculate_centrality(G):
    return nx.degree_centrality(G)

def detect_communities(G):
    communities = list(greedy_modularity_communities(G))
    if len(communities) > 1:
        print(f"Se detectaron {len(communities)} comunidades.")
        for i, community in enumerate(communities, 1):
            print(f"Comunidad {i} tiene {len(community)} nodos: {community}")
    else:
        print("No se detectaron comunidades, o el grafo no tiene una estructura comunitaria clara.")
    return communities

def export_to_excel(centrality, communities, filename='centralidades_o_comunidades.xlsx'):
    wb = Workbook()
    
    # Hoja de Centrality
    ws1 = wb.active
    ws1.title = "Centrality"
    ws1.append(["Node", "Centrality"])
    
    for cell in ws1["1:1"]:
        cell.font = Font(bold=True)
    
    for node, cent_value in centrality.items():
        ws1.append([node, cent_value])
    
    # Hoja de Comunidades
    ws2 = wb.create_sheet(title="Communities")
    ws2.append(["Community", "Nodes"])
    
    for cell in ws2["1:1"]:
        cell.font = Font(bold=True)
    
    for i, community in enumerate(communities, 1):
        community_str = ", ".join(sorted(community))  # Ordenar nodos para mejor lectura
        ws2.append([f"Community {i}", community_str])
    
    # Ajustar el ancho de las columnas para mejor visibilidad
    ws2.column_dimensions['A'].width = 15
    ws2.column_dimensions['B'].width = 100

    wb.save(filename)
    print(f"Datos exportados a {filename}")

def draw_graph(G, title, node_size=500, font_size=10):
    centrality = calculate_centrality(G)
    communities = detect_communities(G)
    
    pos = nx.spring_layout(G, k=10, seed=42)
    pos['101'] = (0, 0)
    for node in pos:
        if node != '101':
            pos[node] = (pos[node][0] * 10, pos[node][1] * 30)
    
    plt.figure(figsize=(12, 10))

    # Ajustar tamaño y color de los nodos según la centralidad y comunidad
    node_sizes = [5000 * centrality[node] for node in G.nodes()]
    node_colors = []
    community_map = {}
    for i, community in enumerate(communities):
        for node in community:
            community_map[node] = i
    for node in G.nodes():
        node_colors.append(plt.cm.rainbow(community_map.get(node, 0) / len(communities)))

    nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors, font_size=font_size, edge_color='gray')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{int(v)}" for k, v in labels.items()})
    nx.draw_networkx_nodes(G, pos, nodelist=['101'], node_color='red', node_size=500)
    
    plt.title(title)
    plt.show()

def main():
    csv_file = 'Rutas.csv'
    G = load_graph_from_csv(csv_file)
    draw_graph(G, 'Red de Rutas desde San José')
    centrality = calculate_centrality(G)
    communities = detect_communities(G)
    export_to_excel(centrality, communities)

if __name__ == '__main__':
    main()
