# -*- coding: utf-8 -*-
"""
Freecell
Created on Wed Jan  8 15:42:16 2020

@author: Chris
"""
import Cards
import itertools
import copy
import numpy

#%%
class Freecell(Cards.Deck):
    """Represents a freecell in the game of Freecell."""
    
    def __init__(self):
        self.cards = []
        
    def to_stack(self, stack, i):
        """Moves a card from a freecell to the top of a stack, if the rules 
        allow."""
        # is_legal = False
        # if self.cards != []:
        #     if stack.cards == []:
        #         is_legal = True
        #     elif (stack.cards[len(stack.cards)-1].suit % 2) != \
        #         (self.cards[0].suit % 2) and \
        #         (self.cards[0].rank + 1) == stack.cards[len(stack.cards)-1].rank:
        #         is_legal = True
        # if is_legal:
        #     
        #self.move_cards(stack, 1)
        stack.cards.append(self.cards.pop(i))
        
    def to_homecell(self, cell, i):
        """Moves a card from a freecell to the top of a homecell, if the rules 
        allow."""
        # is_legal = False
        # if self.cards != []:
        #     if cell.cards == []:
        #         if self.cards[0].suit == cell.suit and \
        #             self.cards[0].rank == 1:
        #             is_legal = True
        #     else:
        #         if self.cards[0].suit == cell.suit and \
        #             (self.cards[0].rank - 1) \
        #             == cell.cards[len(cell.cards)-1].rank:
        #             is_legal = True
        # if is_legal:
        #     
        #self.move_cards(cell, 1)
        cell.cards.append(self.cards.pop(i))

#%% 
            
class Stack(Cards.Deck):
    """Represents a stack in the game of Freecell."""
    
    def __init__(self):
        self.cards = []
    
    def change_stack(self, stack):
        """Moves the top card of one stack to the top of another, if the rules 
        allow."""
        # is_legal = False
        # if self.cards != []:
        #     if stack.cards == []:
        #         is_legal = True
        #     elif (stack.cards[len(stack.cards)-1].suit % 2) != \
        #         (self.cards[len(self.cards)-1].suit % 2) and \
        #         (self.cards[len(self.cards)-1].rank + 1) == stack.cards[len(stack.cards)-1].rank:
        #         is_legal = True
        # if is_legal:
        #     
        self.move_cards(stack, 1)
            
    def to_freecell(self, cell):
        """Moves the top card of one stack to a freecell, if the rules allow.
        """
        # if self.cards != [] and cell.cards == []:
        #
        self.move_cards(cell, 1)
        
    def to_homecell(self, cell):
        """Moves the top card of a stack to the top of a homecell, if the rules 
        allow."""
        # is_legal = False
        # if self.cards != []:
        #     if cell.cards == []:
        #         if self.cards[len(self.cards)-1].suit == cell.suit and \
        #             self.cards[len(self.cards)-1].rank == 1:
        #             is_legal = True
        #     else:
        #         if self.cards[len(self.cards)-1].suit == cell.suit and \
        #             (self.cards[len(self.cards)-1].rank - 1) \
        #             == cell.cards[len(cell.cards)-1].rank:
        #             is_legal = True
        # if is_legal:
        #     
        self.move_cards(cell, 1)
    
    def is_sorted(self, n):
        """Determines if the top n cards of a stack are sorted."""
        if n <= len(self.cards):
            check = list()
            for i in range(1, n):
                j = len(self.cards) - i
                check.append(self.cards[j-1].suit % 2 != self.cards[j].suit % 2 \
                             and self.cards[j-1].rank == self.cards[j].rank + 1)
            if all(check):
                return True
        return False
        
#%%
            
class Homecell(Cards.Deck):
    """Represents a homecell in the game of Freecell."""
    
    def __init__(self, suit = 0):
        self.cards = []
        self.suit = suit
        
#%%
        
class Game:
    """Represents and initializes a game of Freecell."""
    
    def __init__(self):
        deck = Cards.Deck()
        deck.shuffle()
        self.Stacks = []
        self.Freecell = Freecell()
        self.Homecells = []
        for i in range(8):
            s = Stack()
            self.Stacks.append(s)
        for i in range(4):
            h = Homecell(i)
            self.Homecells.append(h)
        for i in range(4):
            deck.move_cards(self.Stacks[i], 7)
        for i in range(4,8):
            deck.move_cards(self.Stacks[i], 6)
            
    def __eq__(self, other):
        """Determines if two instances of Freecell are equal."""
        res = False
        equal = list()
        l = copy.copy(self.Freecell.cards)
        m = copy.copy(other.Freecell.cards)
        equal.append(l.sort() == m.sort())
        for i in range(8):
            equal.append(self.Stacks[i].cards == other.Stacks[i].cards)
        for i in range(4):
            equal.append(self.Homecells[i].cards == other.Homecells[i].cards)
        if all(equal):
            res = True
        return res
                        
    def move(self, n):
        """Performs a move according to an encoding. The input n should be an
        integer between 0 and 167."""
        if 0 <= n < 8: #stacks to freecells
            self.Stacks[n].to_freecell(self.Freecell)
        if 8 <= n < 40: #freecells to stacks 32
            i = (n - 8) // 4
            j = (n - 8) % 4
            self.Freecell.to_stack(self.Stacks[i], j)
        if 40 <= n < 96: #stacks to stacks 56
            i = n - 40
            self.Stacks[Game.perm[i][0]].change_stack(self.Stacks[Game.perm[i][1]])
        if 96 <= n < 128: #stacks to homecells 32
            i = (n - 96) // 4
            j = (n - 96) % 4
            self.Stacks[i].to_homecell(self.Homecells[j])
        if 128 <= n < 144: #freecells to homecells 16
            i = (n - 128) // 4
            j = (n - 128) % 4
            self.Freecell.to_homecell(self.Homecells[j], i) 
        if 144 <= n < 760: #stacked movement between stacks
            power_level = (n - 32) // 56
            i = (n - 144) % 56
            k = len(self.Stacks[Game.perm[i][0]].cards) - power_level
            for j in range(power_level):
                self.Stacks[Game.perm[i][1]].add_card(self.Stacks[Game.perm[i][0]].cards.pop(k))
            
    def undo_move(self, n):
        """Undoes a move according to the same encoding."""
        if 0 <= n < 8: #undoes stacks to freecells
            self.Freecell.move_cards(self.Stacks[n], 1)
        if 8 <= n < 40: #undoes freecells to stacks
            i = (n - 8) // 4
            j = (n - 8) % 4
            self.Freecell.cards.insert(j, self.Stacks[i].cards.pop())
        if 40 <= n < 96: #undoes a move between stacks
            i = n - 40
            self.Stacks[Game.perm[i][1]].move_cards(self.Stacks[Game.perm[i][0]], 1)
        if 96 <= n < 128: #undoes stacks to homecells
            i = (n - 96) // 4
            j = (n - 96) % 4
            self.Homecells[j].move_cards(self.Stacks[i], 1)
        if 128 <= n < 144: #undoes freecells to homecells
            i = (n - 128) // 4
            j = (n - 128) % 4
            self.Freecell.cards.insert(i, self.Homecells[j].cards.pop())
        if 144 <= n < 760: #undoes stacked movement between stacks
            power_level = (n - 32) // 56
            i = (n - 144) % 56
            k = len(self.Stacks[Game.perm[i][1]].cards) - power_level
            for j in range(power_level):
                self.Stacks[Game.perm[i][0]].add_card(self.Stacks[Game.perm[i][1]].cards.pop(k))
            
    def check_win(self):
        """Checks if a game of Freecell meets the winning conditions."""
        return len(self.Homecells[0].cards) == 13 and \
            len(self.Homecells[1].cards) == 13 and \
            len(self.Homecells[2].cards) == 13 and \
            len(self.Homecells[3].cards) == 13
    
    def gather_legal_moves(self):
        """Gathers all legal moves in an instance of a game of Freecell in an
        encoded list, including stacked movement."""
        legal_moves = list()
        num_empty_stacks = 0
        for i in range(8):
            if self.Stacks[i].cards == []:
                num_empty_stacks += 1
        power = 2**num_empty_stacks*(5-len(self.Freecell.cards)) #how many cards can be stack moved
        power = min(power, 12)
        for n in range(760):
            if 0 <= n < 8: #stacks to freecells
                res = False
                if self.Stacks[n].cards != [] and len(self.Freecell.cards) < 4:
                    res = True
                legal_moves.append(res)
            if 8 <= n < 40: #freecells to stacks
                res = False
                i = (n - 8) // 4
                j = (n - 8) % 4
                if len(self.Freecell.cards) >= j + 1:
                    if self.Stacks[i].cards == []:
                        res = True
                    elif (self.Stacks[i].cards[-1].suit % 2) != (self.Freecell.cards[j].suit % 2) and \
                        (self.Freecell.cards[j].rank + 1) == self.Stacks[i].cards[-1].rank:
                        res = True
                legal_moves.append(res)
            if  40 <= n < 96: #stacks to stacks
                res = False
                i = n - 40
                if self.Stacks[Game.perm[i][0]].cards != []:
                    if self.Stacks[Game.perm[i][1]].cards == []:
                        res = True
                    elif (self.Stacks[Game.perm[i][1]].cards[-1].suit % 2) != \
                        (self.Stacks[Game.perm[i][0]].cards[-1].suit % 2) and \
                        (self.Stacks[Game.perm[i][0]].cards[-1].rank + 1) == \
                        self.Stacks[Game.perm[i][1]].cards[-1].rank:
                        res = True
                legal_moves.append(res)
            if 96 <= n < 128: #stacks to homecells
                res = False
                i = (n - 96) // 4
                j = (n - 96) % 4
                if self.Stacks[i].cards != []:
                    if self.Homecells[j].cards == []:
                        if self.Stacks[i].cards[-1].suit == self.Homecells[j].suit and \
                            self.Stacks[i].cards[-1].rank == 1:
                            res = True
                    else:
                        if self.Stacks[i].cards[-1].suit == self.Homecells[j].suit and \
                            (self.Stacks[i].cards[-1].rank - 1) \
                            == self.Homecells[j].cards[-1].rank:
                            res = True
                legal_moves.append(res)
            if 128 <= n < 144: #freecells to homecells
                res = False
                i = (n - 128) // 4
                j = (n - 128) % 4
                if len(self.Freecell.cards) >= i + 1:
                    if self.Homecells[j].cards == []:
                        if self.Freecell.cards[i].suit == self.Homecells[j].suit and \
                            self.Freecell.cards[i].rank == 1:
                            res = True
                    else:
                        if self.Freecell.cards[i].suit == self.Homecells[j].suit and \
                            (self.Freecell.cards[i].rank - 1) \
                            == self.Homecells[j].cards[-1].rank:
                            res = True
                legal_moves.append(res)
            if 144 <= n < 760: #stacked movement between stacks
                res = False
                power_level = (n - 32) // 56 #determines how many cards will be stack moved
                i = (n - 144) % 56 #determines which stacks will be considered
                if power_level <= power:
                    if self.Stacks[Game.perm[i][0]].is_sorted(power_level):
                        if self.Stacks[Game.perm[i][1]].cards == []:
                            mod_power = power / 2
                            if power_level <= mod_power:
                                res = True
                        elif (self.Stacks[Game.perm[i][1]].cards[-1].suit % 2) != \
                            (self.Stacks[Game.perm[i][0]].cards[len(self.Stacks[Game.perm[i][0]].cards) - power_level].suit % 2) and \
                            (self.Stacks[Game.perm[i][0]].cards[len(self.Stacks[Game.perm[i][0]].cards) - power_level].rank + 1) == \
                            self.Stacks[Game.perm[i][1]].cards[-1].rank:
                            res = True
                legal_moves.append(res)        
        return legal_moves
    
    def oracle(self):
        """Returns a value which represents how good the position of the game is, e.g., how close
        it is to completion."""
        res = 0
        for i in range(4):
            res += len(self.Homecells[i].cards)
        res += 4 - len(self.Freecell.cards)
        for i in range(8):
            if self.Stacks[i].cards != []:
                if self.Stacks[i].is_sorted(len(self.Stacks[i].cards)):
                    if self.Stacks[i].cards[0].rank == 13:
                        res += len(self.Stacks[i].cards)
                    else:
                        res += len(self.Stacks[i].cards) // 2
            else:
                res += 2
        return res
    
    def vectorize(self):
        """Returns a vector (in the numpy.array format) which encodes the game state. The vector 
        will have dimension 156."""
        l = list()
        for n in range(156):
            if 0 <= n < 4:
                if n < len(self.Frecell.cards):
                    l.append(self.Freecell.cards[n].encode())
                else:
                    l.append(0)
            if 4 <= n < 80:
                i,j = divmod(n - 4, 19)
                if j < len(self.Stacks[i].cards):
                    l.append(self.Stacks[i].cards[j].encode())
                else:
                    l.append(0)              
            if 80 <= n < 152:
                i,j = divmod(n - 4, 18)
                i = i + 4
                if j < len(self.Stacks[i].cards):
                    l.append(self.Stacks[i].cards[j].encode())
                else:
                    l.append(0)
            if 152 <= n < 156:
                i = n - 152
                if self.Homecells[i].cards != []:
                    l.append(self.Homecells[i].cards[-1].encode())
                else:
                    l.append(0)
        v = numpy.array(l)
        return v
                                         
    perm = list(itertools.permutations([0,1,2,3,4,5,6,7],2))
            
        
    

        

            
            
            
#%%














