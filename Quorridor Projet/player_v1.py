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

# Opening moves chosen at random
MOVES_PLAYER_1_RUSH = [('P', 1, 4), ('P', 2, 4), ('P', 3, 4), ('WV', 3, 3)]
MOVES_PLAYER_1_GAP = [('P', 1, 4), ('P', 2, 4), ('P', 3, 4), ('WH', 2, 3)]
MOVES_PLAYER_1_SHILLER = [('P', 1, 4), ('P', 2, 4), ('P', 3, 4), ('WV', 0, 3)]
MOVES_PLAYER_1_SIDEWALL = [('P', 1, 4), ('WV', 1, 3)]
MOVES_PLAYER_1_REED = [('WH', 5, 2)]
MOVES_PLAYER_1_SHATRANJ = [('WV', 0, 3)]


MOVES_OPENING = [MOVES_PLAYER_1_RUSH,
                 MOVES_PLAYER_1_GAP, MOVES_PLAYER_1_SHILLER, MOVES_PLAYER_1_SIDEWALL, MOVES_PLAYER_1_REED, MOVES_PLAYER_1_SHATRANJ]

SELECTED_OPENING = random.randint(0, 5)

# Function that returns an opening move depending on the selected opening and returns None if the opening is finished
# or if there is a wall placed in the game
def opening(board, player, step, opening):
    if(len(board.horiz_walls) == 0 and len(board.verti_walls) == 0 and step <= len(MOVES_OPENING[opening])):
        if player == 0 and MOVES_OPENING[opening][step-1] in board.get_actions(player):
            return MOVES_OPENING[opening][step-1]
    return None

# Heuristic that considers the distance of both players to their goal and the number of walls of both players.
def heuristic(board, player):
    try:
        distance = board.min_steps_before_victory(
            (player + 1) % 2) - board.min_steps_before_victory(player)

        # If the other player is near his goal, give a negative penalty.
        if(board.pawns[(player + 1) % 2][0] == abs(board.goals[(player + 1) % 2] - 1) and board.min_steps_before_victory((player + 1) % 2) <= 1):
            return (-(100 - board.min_steps_before_victory((player + 1) % 2)))

    except:
        try:
            distance = board.min_steps_before_victory(player)
        except:
            distance = 1

    walls = board.nb_walls[player] - board.nb_walls[(player + 1) % 2]

    # If the player has no walls, returns the distance to the goal
    if board.nb_walls[player] == 0:
        try:
            dist_to_goal = board.min_steps_before_victory(player)
        except:
            dist_to_goal = 1
        return -1*dist_to_goal

    return (5*distance + 2*walls)

# Function that returns -100 if the player has lost or 100 if he has won
def utility(board, player):
    if (board.pawns[player][0] == board.goals[player]):
        return 100
    elif (board.pawns[1-player][0] == board.goals[1-player]):
        return -100
    return 0


class MyAgent(Agent):

    """My Quoridor agent."""

    # Basic Minimax search algorithm with alpha beta pruning
    def minimax_search(self, board, player, cutoff=0):
        infinity = math.inf

        def max_value(board, player, alpha, beta, depth):
            if(board.is_finished()):
                value = utility(board, player)
                return(value, None)
            if(depth > cutoff):
                value = heuristic(board, player)
                return(value, None)
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
                    return (max_v, best_action)
            return (max_v, best_action)

        def min_value(board, player, alpha, beta, depth):
            if(board.is_finished()):
                value = utility(board, player)
                return(value, None)
            if(depth > cutoff):
                value = heuristic(board, player)
                return(value, None)
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
                    return (min_v, best_action)
            return (min_v, best_action)

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

        # Get opening moves
        o = opening(board, player, math.ceil(step/2), SELECTED_OPENING)
        if(o is not None):
            return o

        # Get the best action
        action = self.minimax_search(board, player)
        print(f"BEST ACTION AND VALUE : ", action)
        return action[1]


if __name__ == "__main__":
    agent_main(MyAgent())
