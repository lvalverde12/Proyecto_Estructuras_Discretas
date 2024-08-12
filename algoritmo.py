import csv
import networkx as nx
import matplotlib.pyplot as plt

def load_graph_from_csv(csv_file):
    G = nx.Graph()
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ruta = row['Código CTP']
            inicio = row['Código Distrito Inicio']
            fin = row['Código Distrito Final']
            extension = int(round(float(row['Extensión (km)'])))
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
    nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{v}" for k, v in labels.items()})
    nx.draw_networkx_nodes(G, pos, nodelist=['101'], node_color='red', node_size=500)
    if path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=2.5)
    plt.title(title)
    plt.show()

def find_shortest_path(G, start_node, end_node):
    try:
        path = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')
        length = nx.shortest_path_length(G, source=start_node, target=end_node, weight='weight')
        return path, length
    except nx.NetworkXNoPath:
        return [], float('inf')

def main():
    csv_file = 'Rutas.csv'
    G = load_graph_from_csv(csv_file)
    start_node = '101'
    total_distance = 0  

    while True:
        valid_input = False 

        while not valid_input:
            end_node = input("Introduce el código del nodo destino: ")
            if end_node not in G.nodes:
                print(f"El código del nodo destino '{end_node}' no existe en el grafo. Por favor, ingrese un código válido.")
            else:
                valid_input = True  

        path, length = find_shortest_path(G, start_node, end_node)
        if path:
            print(f"Camino más corto de {start_node} a {end_node}: {path}")
            print(f"Longitud del camino: {int(round(length))} km")
            total_distance += length  
            path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            draw_graph(G, 'Red de Rutas desde San José', path_edges=path_edges)
        else:
            print(f"No se encontró una ruta desde {start_node} a {end_node}.")

        user_choice = input("¿Desea consultar otra ruta? (1: Sí, 2: No): ")
        if user_choice == '2':
            print("Gracias por usar el programa.")
            print(f"Distancia total en kilómetros de las rutas consultadas: {int(round(total_distance))} km")
            break
        elif user_choice != '1':
            print("Opción no válida. Por favor, ingrese 1 o 2.")

if __name__ == '__main__':
    main()
