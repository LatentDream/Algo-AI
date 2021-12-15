#!/usr/bin/env python3
"""
Quoridor agent.
Copyright (C) 2013, <<<<<<<<<<< YOUR NAMES HERE >>>>>>>>>>>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""

# Guillaume Thibault : 1948612
# Jacob Brisson : 1954091

from quoridor import *
import math
import random

# Opening moves
MOVES_PLAYER_1_RUSH = [('P', 1, 4), ('P', 2, 4), ('P', 3, 4), ('WV', 3, 3)]
MOVES_PLAYER_1_GAP = [('P', 1, 4), ('P', 2, 4), ('P', 3, 4), ('WH', 2, 3)]
MOVES_PLAYER_1_SHILLER = [('P', 1, 4), ('P', 2, 4), ('P', 3, 4), ('WV', 0, 3)]
MOVES_PLAYER_1_SIDEWALL = [('P', 1, 4), ('WV', 1, 3)]
MOVES_PLAYER_1_REED = [('WH', 5, 2)]
MOVES_PLAYER_1_SHATRANJ = [('WV', 0, 3)]

MOVES_OPENING = [MOVES_PLAYER_1_RUSH,
                 MOVES_PLAYER_1_GAP, MOVES_PLAYER_1_SHILLER, MOVES_PLAYER_1_SIDEWALL, MOVES_PLAYER_1_REED,
                 MOVES_PLAYER_1_SHATRANJ]

SELECTED_OPENING = random.randint(0, 5)


def opening(board, player, step, opening):
    """
    Function to get the opening move
    """
    if len(board.horiz_walls) == 0 and len(board.verti_walls) == 0 and step <= len(MOVES_OPENING[opening]):
        if player == 0 and MOVES_OPENING[opening][step - 1] in board.get_actions(player):
            return MOVES_OPENING[opening][step - 1]
    return None


def get_shortest_path_simplified(board, player, actual_pos=(-1, -1), end_pos=(-1, -1)):
    """
    Function adapted from get_shortest_path. It uses is_simplified_pawn_move_ok instead of is_pawn_move_ok to find the
      legal pawn moves, so that it wont crash because of a No_path exception. It also can find the shortest path between
      any inital position and final position, specified in the parameters
    """

    def get_pawn_moves(pos):
        (x, y) = pos
        positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
                     (x + 1, y + 1), (x - 1, y -
                                      1), (x + 1, y - 1), (x - 1, y + 1),
                     (x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
        moves = []
        for new_pos in positions:
            if board.is_simplified_pawn_move_ok(pos, new_pos):
                moves.append(new_pos)
        return moves

    if actual_pos == (-1, -1):
        actual_pos = board.pawns[player]
    if end_pos == (-1, -1):
        end_pos = (board.goals[player], [0, 1, 2, 3, 4, 5, 6, 7, 8])
    (a, b) = actual_pos
    if a == end_pos[0] and b in end_pos[1]:
        return []
    visited = [[False for i in range(board.size)] for i in range(board.size)]
    # Predecessor matrix in the BFS
    prede = [[None for i in range(board.size)] for i in range(board.size)]
    neighbors = [actual_pos]
    while len(neighbors) > 0:
        neighbor = neighbors.pop(0)
        (x, y) = neighbor
        visited[x][y] = True
        if x == end_pos[0] and y in end_pos[1]:
            succ = [neighbor]
            curr = prede[x][y]
            while curr is not None and curr != actual_pos:
                succ.append(curr)
                (x_, y_) = curr
                curr = prede[x_][y_]
            succ.reverse()
            return succ
        unvisited_succ = [(x_, y_) for (x_, y_) in
                          get_pawn_moves(neighbor) if not visited[x_][y_]]
        for n_ in unvisited_succ:
            (x_, y_) = n_
            if not n_ in neighbors:
                neighbors.append(n_)
                prede[x_][y_] = neighbor
    raise NoPath()


def number_of_paths(board, player):
    """
    Find the number of paths in front or behind the player. If the inv parameter is true, then it is the number of paths
    behind. A path is defined as a hole through a wall in front or behind the player
    """
    y_pawn = board.pawns[player][0]
    x_pawn = board.pawns[player][1]
    if player == 0:
        direction = 1
    else:
        direction = -1
    wall_found = False
    wall_pos = {}
    y = y_pawn
    while not wall_found and y != board.goals[player]:
        for i in range(9):
            if not board.is_simplified_pawn_move_ok((y, i), (y + direction, i)):
                wall_found = True
                if y in wall_pos:
                    wall_pos[y].append(i)
                else:
                    wall_pos[y] = [i]
        y += direction
    paths = 0
    keys = [key for key in wall_pos.keys()]

    if len(keys) > 0:
        if keys[0] == y_pawn and board.is_simplified_pawn_move_ok((y, x_pawn), (y + direction, x_pawn)):
            return 1
        pos_x = [x for x in wall_pos[keys[0]]]
        for i in range(10):
            if (i in pos_x or i == 9) and i - 1 not in pos_x and i - 1 >= 0:
                try:
                    new_path = get_shortest_path_simplified(
                        board=board, player=player, actual_pos=(keys[0] + direction, i - 1))
                    path_to_hole = get_shortest_path_simplified(
                        board=board, player=player, end_pos=(keys[0] + direction, [i - 1]))
                    y_pos = [v[0] for v in path_to_hole]
                    if player == 0:
                        not_a_path = keys[0] + \
                                     direction < max(y_pos) and (
                                         keys[0] + direction, i - 1) not in get_shortest_path_simplified(board, player)
                    else:
                        not_a_path = keys[0] + \
                                     direction > min(y_pos) and (
                                         keys[0] + direction, i - 1) not in get_shortest_path_simplified(board, player)
                    if (keys[0], i - 1) not in new_path and not_a_path is False and y_pos.count(
                            board.goals[player]) <= 1:
                        paths += 1
                except:
                    paths = paths

    else:
        return 1

    return max(1, paths)


def heuristic(board, player):
    """
    Heuristic using the distance to the goal of both players, the number of walls, the number of paths behind and in
    front of the player.
    """
    paths = number_of_paths(board, player)
    opp_paths = number_of_paths(board, (player + 1) % 2)
    path_heuristic = 0.5 * opp_paths - paths
    try:
        distance = board.min_steps_before_victory(
            (player + 1) % 2) - board.min_steps_before_victory(player)

        if board.pawns[(player + 1) % 2][0] == abs(
                board.goals[(player + 1) % 2] - 1) and board.min_steps_before_victory(
                (player + 1) % 2) <= 2 and board.min_steps_before_victory(player) > 1:
            return -(100 - board.min_steps_before_victory((player + 1) % 2))

    except:
        distance = len(get_shortest_path_simplified(
            board, (player + 1) % 2)) - len(get_shortest_path_simplified(board, player))

    walls = board.nb_walls[player] - board.nb_walls[(player + 1) % 2]

    if board.nb_walls == [0, 0]:
        return -1 * len(get_shortest_path_simplified(board, player))

    return 5 * distance + 2 * walls + 5 * path_heuristic


def utility(board, player):
    if board.pawns[player][0] == board.goals[player]:
        return 100
    elif board.pawns[(player + 1) % 2][0] == board.goals[(player + 1) % 2]:
        return -100
    return 0


class MyAgent(Agent):
    """My Quoridor agent."""

    def minimax_search(self, board, player, cutoff=0):
        infinity = math.inf

        def max_value(board, player, alpha, beta, depth):
            if board.is_finished():
                value = utility(board, player)
                return value, None
            if depth > cutoff:
                value = heuristic(board, player)
                return value, None
            max_v = -infinity
            best_action = None
            for action in board.get_actions(player):
                new_board = board.clone()
                next_state = new_board.play_action(action, player)
                (value, _) = min_value(next_state, player, alpha, beta, depth + 1)
                if value > max_v:
                    max_v = value
                    best_action = action
                    alpha = max(alpha, max_v)
                if max_v >= beta:
                    return max_v, best_action
            return max_v, best_action

        def min_value(board, player, alpha, beta, depth):
            if board.is_finished():
                value = utility(board, player)
                return value, None
            if depth > cutoff:
                value = heuristic(board, player)
                return value, None
            min_v = infinity
            best_action = None
            for action in board.get_actions(player):
                new_board = board.clone()
                next_state = new_board.play_action(action, player)
                (value, _) = max_value(next_state, player, alpha, beta, depth + 1)
                if value < min_v:
                    min_v = value
                    best_action = action
                    beta = min(beta, min_v)
                if min_v <= alpha:
                    return min_v, best_action
            return min_v, best_action

        return max_value(board, player, -infinity, +infinity, 0)

    def play(self, percepts, player, step, time_left):
        """
        This function is used to play a move according
        to the percepts, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        :param percepts: dictionary representing the current board
            in a form that can be fed to `dict_to_board()` in quoridor.py.
        :param player: the player to control in this step (0 or 1)
        :param step: the current step number, starting from 1
        :param time_left: a float giving the number of seconds left from the time
            credit. If the game is not time-limited, time_left is None.
        :return: an action
          eg: ('P', 5, 2) to move your pawn to cell (5,2)
          eg: ('WH', 5, 2) to put a horizontal wall on corridor (5,2)
          for more details, see `Board.get_actions()` in quoridor.py
        """
        board = dict_to_board(percepts)

        o = opening(board, player, math.ceil(step / 2), SELECTED_OPENING)
        if o is not None:
            return o
        cutoff = 0

        action = self.minimax_search(board, player, cutoff)
        print(f"BEST ACTION AND VALUE : ", action)

        return action[1]


if __name__ == "__main__":
    agent_main(MyAgent())
