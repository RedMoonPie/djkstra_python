import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

my_nodes_list = []
conexiones = []
weights = []
fin = 0
final_result = {}
temporal = {}
Final = {}
acomulado, ac2 = 0, 0
origin = ""
lista_origen = []
path = []
path2 = []

def main():
    global my_nodes_list, fin, ttl, conexiones, izq, der, weights, temporal,final_result,path
    pltct = 0


    G = nx.DiGraph()

    # numero nodos
    n = input()

    # numero conexiones
    m = input()

    for i in range(0, int(m)):
        conexion = input()
        separar_nodos(conexion)
    ruta = input()
    rt = ruta.split(" ")
    my_nodes_list.sort(key=int)
    # --------------------------------------------------- graficar nodos -------------------------------------------
    G.add_nodes_from(my_nodes_list)
    k = 0

    for conexion in conexiones:

        tmp = conexion.split(" ")

        G.add_edge(tmp[0], tmp[1],weight=weights[k])

        k += 1



    matriz = asignar_valor(my_nodes_list)

    #print(matriz)
    no_v = calcular(rt[0], [rt[1]], matriz)
    #print(no_v)
    path.append(rt[0])
    for camino in Final:
        if Final[camino] != -1:
            tp = Final[camino].split(" ")
            if tp[0] in path and tp[1] not in path:
                path.append(tp[1])
    # pintar
    for e in G.edges():
        G[e[0]][e[1]]['color'] = 'gray'
    # poner aristas del camino corto a verde


    node_pos = nx.planar_layout(G, scale=1, center=None, dim=2)

    arc_weight = nx.get_edge_attributes(G, 'weight')

    red_edges = list(zip(path, path[1:]))

    node_col = ['gray' if not node in path else 'red' for node in G.nodes()]
    # si esta en el camino corto poner en rojo, sino en blanco
    edge_col = ['black' if not edge in red_edges else 'red' for edge in G.edges()]

    nx.draw_networkx(G,node_pos, node_color=node_col, node_size = 450)

    nx.draw_networkx_edges(G, node_pos,edge_color=edge_col)

    nx.draw_networkx_edge_labels(G, node_pos, edge_color=edge_col,edge_labels=arc_weight)
    plt.axis('off')

    plt.show()


    plt.savefig(f'plots/Grafo#{pltct}.png')
    plt.clf()
    G.clear()
    pltct += 1

    if rt[1] in no_v:
        img = Image.open(f'plots/elbromas.png')
        img.show()
        print("El grupo de los perdedores ha muerto prepárate a sufrir.")
    else:
        print(f"La distancia es de {temporal[rt[1]]} para llegar a casa.")
        img = Image.open(f'plots/georgie.jpg')
        img.show()
    #for camino in temporal:
    #    print(temporal[camino])


def calcular(nodo_origen, nodo_destino, matriz):
    global temporal, Final, vertice, my_nodes_list, acomulado, lista_origen
    tt = matriz.loc[matriz.loc[nodo_origen] != 0].index.tolist()
    lista_origen = tt
    for node in my_nodes_list:
        temporal[node] = -1
        Final[node] = -1

    mynodes = my_nodes_list.copy()
    mynodes.remove(nodo_origen)
    return recursiva(tt, matriz, mynodes, nodo_origen, nodo_destino, 0)


def recursiva(list, matriz, nodes, nodo_origen, nodo_destino, acomulador):
    global temporal, Final, ac2, origin, lista_origen,path2

    for nodo in list:

        if nodo in nodes:
            nodes.remove(nodo)
        if nodo_origen == origin:
            acomulador = ac2

        if len(list) > 1 or list == lista_origen:
            ac2 = acomulador
            origin = nodo_origen

        if nodo_origen == origin and list == lista_origen:
            acomulador = 0

        tt = matriz.loc[matriz.loc[nodo] != 0].index.tolist()

        if temporal[nodo] == -1:

            temporal[nodo] = int((matriz.at[nodo_origen, nodo])) + acomulador
            acomulador = acomulador + int((matriz.at[nodo_origen, nodo]))
            Final[nodo_origen] = (f"{nodo_origen} {nodo}")




        else:

            if temporal[nodo] > int((matriz.at[nodo_origen, nodo]) + acomulador):
                temporal[nodo] = int((matriz.at[nodo_origen, nodo])) + acomulador
                acomulador = acomulador + int((matriz.at[nodo_origen, nodo]))

                Final[nodo_origen] = (f"{nodo_origen} {nodo}")


            else:
                acomulador = acomulador + int((matriz.at[nodo_origen, nodo]))
                #Final[nodo_origen] = (f"{nodo} {nodo_origen}")



        if nodo == nodo_destino[0]:
            break

        recursiva(tt, matriz, nodes, nodo, nodo_destino, acomulador)

    return nodes


def asignar_valor(node_list):
    global conexiones, weights
    matrix = pd.DataFrame(0, index=node_list, columns=node_list)
    for i in range(0, len(conexiones)):
        tmp = conexiones[i].split(" ")

        matrix.at[tmp[0], tmp[1]] = weights[i]

    return matrix


def separar_nodos(cnx):
    global my_nodes_list, izq, der, conexiones, weights
    tmp = cnx.split(" ")

    if tmp[0] not in my_nodes_list:
        my_nodes_list.append(tmp[0])
    if tmp[1] not in my_nodes_list:
        my_nodes_list.append(tmp[1])

    conexiones.append(tmp[0] + " " + tmp[1])
    weights.append(tmp[2])


if __name__ == "__main__":
    main()
