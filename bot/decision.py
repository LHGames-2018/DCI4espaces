from bot.implementation import *

def PoidsDistance(distance_a_peser, longest_dist):
    return longest_dist / distance_a_peser

# Implémentation des décisions du bot à l'aide de poids
# C'est une fonction qui sert à ça

def decision(tile_list, player_info):
    NOMBRE_PROPRIETES = 3   # Nb de données importantes: item, poids, distance
    longest_dist = 0    # Important pour caller PoidsDistance

    w, h = NOMBRE_PROPRIETES, len(tile_list)

    data = [[None for x in range(w)] for y in range(h)]

    # Setup la première colonne en copiant les données dedans
    # et les données pour setuper la troisième qui contient la distance
    for i in range(len(tile_list)):
        data[i][0] = tile_list[i]

        dist = distance(tile_list[i].Position, player_info.Position)

        # pour setup la deuxième
        if dist > longest_dist:
            longest_dist = dist

    # On setup la deuxième colonne avec ce qu'on pèse
    for i in range(len(tile_list)):
        data[i][1] = PoidsDistance(data[i][2], longest_dist)

    # On évalue la décision à prendre. On cherche le plus grand poids.
    best = None
    biggest_poids = 0
    for i in range(len(tile_list)):
        if tile_list[1] > biggest_poids:
            best = tile_list[0]
            biggest_poids = tile_list[1]

    return best
