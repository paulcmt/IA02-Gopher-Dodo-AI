# Module concernant la grille hexagonale de jeu
from typing import List

# Structures de données

# Types de base utilisés par l'arbitre
# que votre IA puisse jouer (objet, dictionnaire, autre...)
Player = int  # 1 ou 2
Grid = tuple[tuple[int, ...], ...]  # Array de Array en diagonal


# Exemples de Grid
GRID1 = (
    (-1, -1, -1, -1, -1, -1, 0, 0, 1, 0, 0, 0, 0),
    (-1, -1, -1, -1, -1, 0, 0, 1, 0, 0, 0, 0, 0),
    (-1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (-1, -1, -1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0),
    (-1, -1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 2, 2, 1, 0, 0, 0, 0, -1),
    (0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, -1, -1),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1),
    (0, 0, 0, 2, 0, 0, 0, 0, 0, -1, -1, -1, -1),
    (0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1),
    (0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1),
)

GRID2 = (
    ((-1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0), 
     (-1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0),
     (-1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0), 
     (-1, -1, -1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0),
     (-1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 
     (-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 
     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1),
     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1), 
     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1),
     (0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1),
     (0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1),
     (0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1))
)


# Exemple de grille initiale de taille 7
INIT_GRID = (
     (-1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1),
     (-1, -1, -1, -1, -1, 0, 1, 1, 1, 1, 1, 1, 1),
     (-1, -1, -1, -1, 0, 0, 0, 1, 1, 1, 1, 1, 1),
     (-1, -1, -1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1),
     (-1, -1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1),
     (-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1),
     (2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1),
     (2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1),
     (2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, -1, -1),
     (2, 2, 2, 2, 2, 0, 0, 0, 0, 0, -1, -1, -1),
     (2, 2, 2, 2, 2, 2, 0, 0, 0, -1, -1, -1, -1),
     (2, 2, 2, 2, 2, 2, 2, 0, -1, -1, -1, -1, -1),
     (2, 2, 2, 2, 2, 2, 2, -1, -1, -1, -1, -1, -1)
)


# Fonctions utilitaires

# Fonctions de coloration de texte
def coloration_red(text: str) -> str:
    return "\033[31m" + text + "\033[0m"


def coloration_blue(text: str) -> str:
    return "\033[34m" + text + "\033[0m"


# Fonctions de création de grille
def grid_tuple_to_grid_list(grid: Grid) -> list[list[int]]:
    return [list(i) for i in grid]


def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid:
    return tuple(tuple(i) for i in grid)


def display_neighbors(grid: Grid, q: int, r: int, directions: List[tuple[int, int]], n):
    neighbors: List[tuple[int, int]] = hex_neighbor(q, r, directions)

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            # Coloration en noir si == -1
            if cell == -1:
                print("\033[30m", end="")
            # Coloration en bleu si == 1
            elif cell == 1:
                print("\033[34m", end="")
            # Coloration en rouge si == 2
            elif cell == 2:
                print("\033[31m", end="")
            # Coloration en vert si c'est un voisin
            if (i, j) in neighbors:
                print("\033[92m", end="")
            # Coloration en rose element sélectionné
            if (i, j) == (q, r):
                print("\033[95m", end="")
            print(str(cell).rjust(2), end=" ")
            print("\033[0m", end="")
        print()


def grid_generation(n: int) -> Grid:
    # Création d'un tableau 2(n-1) * 2(n-1)
    m = n - 1
    grid = [[-1] * (2 * m) for _ in range(2 * m)]

    # Remplissage d'une grille vide
    # Remplissage de la première moitié de la grille
    for r in range(m):
        for q in range(m - r, 2 * m):
            grid[r][q] = 0
    # Remplissage de la seconde moitié de la grille
    for r in range(m):
        for q in range(2 * m - r - 1):
            grid[r + m][q] = 0
    # Ajout d'une colonne et d'une ligne de 0 au milieu de la grille
    grid.insert(m, [-0] * (2 * m))
    for ligne in grid:
        ligne.insert(m, 0)

    return grid_list_to_grid_tuple(grid)


def display_grid(grid: Grid):
    for row in grid:
        for cell in row:
            # Coloration en noir si == -1
            if cell == -1:
                print("\033[30m", end="")
            # Coloration en vert si == 4
            if cell == 4:
                print("\033[92m", end="")
            # Coloration en bleu si == 1
            if cell == 1:
                print("\033[34m", end="")
            # Coloration en rouge si == 2
            if cell == 2:
                print("\033[31m", end="")
            print(str(cell).rjust(2), end=" ")
            print("\033[0m", end="")
        print()


# Conversion de coordonnées allant de 0 à 2n à des coordonnées allant de -n à n
def convert(q: int, r: int, n) -> (int, int):
    return -q + n - 1, -n + r + 1


directions_case_neighbors: List[tuple[int, int]] = [
    (1, 0),
    (1, 1),
    (0, -1),
    (-1, 0),
    (-1, -1),
    (0, 1),
]


# Voisins d'une case selon certaines directions
def hex_neighbor(q, r, directions) -> List[tuple[int, int]]:

    return [(q - dq, r + dr) for dq, dr in directions]


def main():
    display_grid(INIT_GRID)
    pass


if __name__ == "__main__":
    main()

