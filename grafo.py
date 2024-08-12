import csv
import networkx as nx
import matplotlib.pyplot as plt

def load_graph_from_csv(csv_file):
    G = nx.Graph()
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ruta = row['Código CTP']
            inicio = row['Código Cantón Inicio']
            fin = row['Código Distrito Final']
            extension = float(row['Extensión (km)'])
            G.add_node(inicio, label=row['Cantón Inicio'])
            G.add_node(fin, label=row['Cantón Final'])
            G.add_edge(inicio, fin, weight=extension, label=ruta)
    return G

def draw_graph(G, title, node_size=500, node_color='lightblue', font_size=10, path_edges=[]):
    pos = nx.spring_layout(G, k=10, seed=42)  
    pos['101'] = (0, 0)
    for node in pos:
        if node != '101':
            pos[node] = (pos[node][0] * 10, pos[node][1] * 30)
    plt.figure(figsize=(12, 10))

    nx.draw(G, pos, with_labels=True, node_size=node_size, node_color=node_color, font_size=font_size, edge_color='gray')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{int(v)}" for k, v in labels.items()})
    nx.draw_networkx_nodes(G, pos, nodelist=['101'], node_color='red', node_size=500)
    if path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=2.5)
    plt.title(title)
    plt.show()

def main():
    csv_file = 'Rutas.csv'
    G = load_graph_from_csv(csv_file)
    draw_graph(G, 'Red de Rutas desde San José')

if __name__ == '__main__':
    main()
