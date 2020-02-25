# -*- coding: utf-8 -*-
"""
Freecell Solver
Created on Thu Jan  9 22:10:31 2020

@author: Chris
"""

import Cards
import Freecell
import copy
import time

#%% Utility functions

def check_for_duplicates(game, d):
    """Returns True if any previous instance of the game is equal to the current instance."""
    equal = dict()
    for i in d:
        equal[i] = (game == d[i])
    return any(equal.values())   

def branches_from(tuple1, tuple2):
    """Takes two tuples as input and returns True if the first argument begins with the second
    argument."""
    if len(tuple1) >= len(tuple2):
        res = list()
        for j in range(len(tuple2)):
            res.append(tuple1[j] == tuple2[j])
        return all(res)
    return False

#%% Performance optimization

def perform_optimal_moves(game, key):
    """Performs the obvious moves in a game of Freecell. Returns an updated
    key, number of moves, and the list of legal moves."""
    cont = True
    while cont:
        cont_check = 0
        lengths = list()
        for j in range(4):
            lengths.append(len(game.Homecells[j].cards))
        minimum = min(lengths)
        for j in range(4):
            for i in range(8): #stacks to homecells
                if game.Stacks[i].cards != []:
                    if (game.Stacks[i].cards[-1].rank - 1) == \
                        minimum and \
                        game.Stacks[i].cards[-1].suit == j:
                            n = 4*i + j + 96
                            game.move(n)
                            key = key + (n,)
                            cont_check += 1
                    elif (game.Stacks[i].cards[-1].rank - 2) == \
                        minimum and \
                        game.Stacks[i].cards[-1].suit == j and \
                        (game.Stacks[i].cards[-1].rank - 1) == \
                        len(game.Homecells[j].cards):
                            n = 4*i + j + 96
                            game.move(n)
                            key = key + (n,)
                            cont_check += 1
            for i in range(4): #freecells to homecells
                if len(game.Freecell.cards) >= i + 1:
                    if (game.Freecell.cards[i].rank - 1) == \
                        minimum and \
                        game.Freecell.cards[i].suit == j:
                            n = 4*i + j + 128
                            game.move(n)
                            key = key + (n,)
                            cont_check += 1
                    elif (game.Freecell.cards[i].rank - 2) == \
                        minimum and \
                        game.Freecell.cards[i].suit == j and \
                        (game.Freecell.cards[i].rank - 1) == \
                        len(game.Homecells[j].cards):
                            n = 4*i + j + 128
                            game.move(n)
                            key = key + (n,)
                            cont_check += 1
        if cont_check == 0:
            cont = False
    legal_moves[key] = game.gather_legal_moves()
    return game, key
              
#%% Determines if a game of Freecell has a solution.
         
def build_tree(game, key = tuple()):
    """Builds the tree of a game of Freecell."""
    tic = time.time()
    print('Finding candidate...')
    game, key = perform_optimal_moves(game, key)
    if game.check_win():
        d[key] = game
    else:
        for n in range(760):
            if legal_moves[key][n]:
                game.move(n)
                if not check_for_duplicates(game, d): #checks if the game instance has appeared previously
                    game.undo_move(n)
                    iterkey = key + (n,)
                    d[iterkey] = copy.deepcopy(game)
                    d[iterkey].move(n)
                    legal_moves[iterkey] = d[iterkey].gather_legal_moves()
                else:
                    game.undo_move(n)
        if len(key) < 5:
            depth = 5
        if 5 <= len(key) < 15:
            depth = 4
        if 15 <= len(key) < 30:
            depth = 3
        if len(key) >= 30:
            depth = 2
        for j in range(depth):
            branches = list()
            for i in d:
                if branches_from(i, key) and len(i) == len(key) + j + 1:
                    branches.append(i)
            if j < depth - 1:
                for i in branches:
                    for n in range(760):
                        if legal_moves[i][n]:
                            game2 = copy.deepcopy(d[i])
                            game2.move(n)
                            if not check_for_duplicates(game2, d):
                                iterkey = i + (n,)
                                d[iterkey] = copy.deepcopy(game2)
                                legal_moves[iterkey] = d[iterkey].gather_legal_moves()
            else:
                candidate = branches[0]
                for i in branches:
                    if d[candidate].oracle() < d[i].oracle():
                        candidate = i
                indices = list(d.keys())
                for i in indices:
                    if len(i) <= len(candidate) - depth:
                        del d[i]
                        del legal_moves[i]
                game2 = copy.deepcopy(d[candidate])
                duration = time.time() - tic
                print('Complete. Time duration: %d \n' %(duration))
                print('Candidate: ', candidate)
                build_tree(game2, candidate)
    
def has_solution(game):
    """Determines if a game of Freecell has a solution."""
    key = tuple()
    legal_moves[key] = game.gather_legal_moves()
    build_tree(game)
    for i in d:
        is_win[i] = d[i].check_win()
    return any(is_win.values())
            
#%% Finds the solution to a game of Freecell

def solve(game):
    """Solves a game of Freecell. Attempts to returns a move order of shortest length to solve the
    game."""
    if has_solution(game):
        num_moves = dict()
        res = list() 
        for i in is_win:
            if is_win[i] == True:
                num_moves[i] = len(i)
        m = min(num_moves.values())
        for i in num_moves:
            if num_moves[i] == m:
                res.append(i)
        return res[0]
    return None
    
#%%
    
# game = Freecell.Game() #43306
# game.Stacks[0].cards = [Cards.Card(1, 10), Cards.Card(2, 12), Cards.Card(2, 3), Cards.Card(1, 6), Cards.Card(1, 11),\
#                         Cards.Card(0,2), Cards.Card(0,4)]
# game.Stacks[1].cards = [Cards.Card(1, 12), Cards.Card(2, 8), Cards.Card(0, 13), Cards.Card(1, 9), Cards.Card(3, 2),\
#                         Cards.Card(3, 7), Cards.Card(2, 6)]
# game.Stacks[2].cards = [Cards.Card(2, 9), Cards.Card(3, 4), Cards.Card(1, 3), Cards.Card(2, 7), Cards.Card(3, 9),\
#                         Cards.Card(2, 4), Cards.Card(0, 3)]
# game.Stacks[3].cards = [Cards.Card(3, 6), Cards.Card(3, 5), Cards.Card(3, 11), Cards.Card(2, 5), Cards.Card(0, 7),\
#                         Cards.Card(0, 5), Cards.Card(0, 1)]
# game.Stacks[4].cards = [Cards.Card(2, 2), Cards.Card(1, 8), Cards.Card(2, 11), Cards.Card(1, 13), Cards.Card(1, 2),\
#                         Cards.Card(3, 1)]
# game.Stacks[5].cards = [Cards.Card(3, 12), Cards.Card(0, 9), Cards.Card(3, 13), Cards.Card(1, 7), Cards.Card(2, 13),\
#                         Cards.Card(3, 8)]
# game.Stacks[6].cards = [Cards.Card(0, 11), Cards.Card(2, 10), Cards.Card(0, 10), Cards.Card(1, 4), Cards.Card(0, 6),\
#                         Cards.Card(0, 8)]
# game.Stacks[7].cards = [Cards.Card(3, 10), Cards.Card(3, 3), Cards.Card(0, 12), Cards.Card(1, 1), Cards.Card(1, 5),\
#                         Cards.Card(2, 1)]
    
game = Freecell.Game() #3983135
game.Stacks[0].cards = [Cards.Card(2, 2), Cards.Card(2, 1), Cards.Card(1, 5), Cards.Card(1, 13), Cards.Card(3, 9),\
                        Cards.Card(1, 9), Cards.Card(2, 4)]
game.Stacks[1].cards = [Cards.Card(2, 13), Cards.Card(0, 4), Cards.Card(0, 6), Cards.Card(3, 5), Cards.Card(2, 9),\
                        Cards.Card(1, 3), Cards.Card(2, 12)]
game.Stacks[2].cards = [Cards.Card(1, 1), Cards.Card(0, 1), Cards.Card(1, 4), Cards.Card(3, 12), Cards.Card(2, 7),\
                        Cards.Card(1, 11), Cards.Card(3, 1)]
game.Stacks[3].cards = [Cards.Card(2, 5), Cards.Card(3, 7), Cards.Card(0, 10), Cards.Card(1, 7), Cards.Card(2, 6),\
                        Cards.Card(3, 4), Cards.Card(1, 12)]
game.Stacks[4].cards = [Cards.Card(0, 3), Cards.Card(0, 8), Cards.Card(3, 6), Cards.Card(0, 12), Cards.Card(3, 8),\
                        Cards.Card(2, 11)]
game.Stacks[5].cards = [Cards.Card(0, 11), Cards.Card(3, 3), Cards.Card(0, 7), Cards.Card(3, 11), Cards.Card(0, 2),\
                        Cards.Card(0, 13)]
game.Stacks[6].cards = [Cards.Card(3, 10), Cards.Card(2, 3), Cards.Card(3, 13), Cards.Card(1, 6), Cards.Card(0, 9),\
                        Cards.Card(2, 10)]
game.Stacks[7].cards = [Cards.Card(1, 10), Cards.Card(3, 2), Cards.Card(0, 5), Cards.Card(2, 8), Cards.Card(1, 8),\
                        Cards.Card(1, 2)]
d = dict()
legal_moves = dict()
is_win = dict()


solution = solve(game)
