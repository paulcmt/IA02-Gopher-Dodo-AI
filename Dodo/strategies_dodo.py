""" Module contenant les différentes stratégies pour le jeu Dodo """
import random
from Game_playing.structures_classes import *

Strategy = Callable[[Environment, Player, Grid], Action]


def strategy_first_legal_dodo(env: Environment, player: Player, grid: Grid) -> Action:
    return env.legals_dodo(grid, player)[0]


def strategy_random_dodo(env: Environment, player: Player, grid: Grid) -> Action:
    return random.choice(env.legals_dodo(grid, player))


# Fonction d'évaluation sommaire pour le jeu Dodo
def is_near_edge(cell: Cell, grid: Grid) -> bool:
    return cell[0] == 0 or cell[0] == len(grid) - 1 or cell[1] == 0 or cell[1] == len(grid[0]) - 1


def evaluate(env: Environment, grid: Grid, player: Player) -> int:
    if player == env.max_player:
        opponent = env.min_player
    else:
        opponent = env.max_player

    player_moves = len(env.legals_dodo(grid, player))
    opponent_moves = len(env.legals_dodo(grid, opponent))

    player_score = 0
    opponent_score = 0

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == player:
                player_score -= 10  # Penalty for having a piece, to encourage blocking oneself
                player_score -= 5 * len(env.legals_dodo(grid, player))  # Penalty for mobility
                if is_near_edge((i, j), grid):
                    player_score += 5  # Reward for being near edge (easier to block oneself)
            elif cell == opponent:
                opponent_score += 10  # Reward for having a piece
                opponent_score += 5 * len(env.legals_dodo(grid, opponent))  # Reward for mobility
                if is_near_edge((i, j), grid):
                    opponent_score -= 5  # Penalty for opponent being near edge

    return player_score - opponent_score


# Minimax Strategy (sans cache)
def minmax_action(env: Environment, player: Player, grid: Grid, depth: int = 0) -> tuple[float, Action]:
    if depth == 0 or env.final_dodo(grid) != 0:
        return env.final_dodo(grid), (-1, -1)  # On retourne le score de la grille

    if player == env.max_player:  # maximizing player
        best = (float("-inf"), (-1, -1))
        for item in env.legals_dodo(grid, player):
            tmp = env.play_dodo(player, grid, item)
            returned_values = minmax_action(env, env.min_player, tmp, depth - 1)
            if max(best[0], returned_values[0]) == returned_values[0]:
                best = (returned_values[0], item)
        return best

    if player == env.min_player:  # minimizing player
        best = (float("inf"), (-1, -1))
        for item in env.legals_dodo(grid, player):
            tmp = env.play_dodo(player, grid, item)
            returned_values = minmax_action(env, env.max_player, tmp, depth - 1)
            if min(best[0], returned_values[0]) == returned_values[0]:
                best = (returned_values[0], item)
        return best


def minmax_action_alpha_beta_pruning(env: Environment, player: Player, grid: Grid, depth: int = 0) -> tuple[float, Action]:
    memo = {}  # Dictionary to store the memoized results

    def minmax_alpha_beta_pruning(env: Environment, player: Player, grid: Grid, depth: int, alpha: float, beta: float) -> tuple[float, Action]:
        # Convert grid to a tuple so it can be used as a key in the dictionary
        grid_key = tuple(map(tuple, grid))
        player_id = player.id  # Use a unique identifier for the player
        
        if (grid_key, player_id, depth) in memo:
            return memo[(grid_key, player_id, depth)]

        if env.final_dodo(grid) != 0:
            score = env.final_dodo(grid)
            memo[(grid_key, player_id, depth)] = (score, (-1, -1))
            return score, (-1, -1)
        if depth == 0:
            score = evaluate(env, grid, player)
            memo[(grid_key, player_id, depth)] = (score, (-1, -1))
            return score, (-1, -1)

        if player == env.max_player:  # Maximizing player
            best = (float("-inf"), (-1, -1))
            for item in env.legals_dodo(grid, player):
                tmp = env.play_dodo(player, grid, item)
                returned_values = minmax_alpha_beta_pruning(env, env.min_player, tmp, depth - 1, alpha, beta)
                if max(best[0], returned_values[0]) == returned_values[0]:
                    best = (returned_values[0], item)
                alpha = max(alpha, best[0])
                if beta <= alpha:
                    break
            memo[(grid_key, player_id, depth)] = best
            return best

        if player == env.min_player:  # Minimizing player
            best = (float("inf"), (-1, -1))
            for item in env.legals_dodo(grid, player):
                tmp = env.play_dodo(player, grid, item)
                returned_values = minmax_alpha_beta_pruning(env, env.max_player, tmp, depth - 1, alpha, beta)
                if min(best[0], returned_values[0]) == returned_values[0]:
                    best = (returned_values[0], item)
                beta = min(beta, best[0])
                if beta <= alpha:
                    break
            memo[(grid_key, player_id, depth)] = best
            return best

    return minmax_alpha_beta_pruning(env, player, grid, depth, float("-inf"), float("inf"))


def strategy_minmax(env: Environment, player: Player, grid: Grid) -> Action:
    # return minmax_action(env, player, grid, 4)[1]
    return minmax_action_alpha_beta_pruning(env, player, grid, 4)[1]
