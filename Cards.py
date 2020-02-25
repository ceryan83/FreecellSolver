# -*- coding: utf-8 -*-
"""
Cards
Created on Mon Dec 16 15:28:28 2019

@author: Chris
"""
import random

#%%

class Card:
    
    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return '%s of %s' %(Card.rank_names[self.rank], Card.suit_names[self.suit])
    
    def __lt__(self, other):
        if self.suit != other.suit:
            return self.suit < other.suit
        return self.rank < other.rank
    
    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank
    
    def encode(self):
        """Encodes a card with an integer from 1 to 52."""
        num = self.suit*13 + self.rank
        return num
    
    suit_names = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
    rank_names = [None, 'Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 
                  'Jack', 'Queen', 'King']
    
    

#%%
    
class Deck:
    
    def __init__(self):
        self.cards = []
        for i in range(4):
            for j in range(1,14):
                card = Card(i,j)
                self.cards.append(card)
                
    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)
    
    def pop_card(self):
        return self.cards.pop()
    
    def add_card(self, card):
        self.cards.append(card)
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def sort(self):
        self.cards.sort()
        
    def move_cards(self, hand, num):
        for i in range(num):
            hand.add_card(self.pop_card())
        
class Hand(Deck):
    """Represents a hand of playing cards."""
    
    def __init__(self, label = ''):
        self.cards = []
        self.label = label
        
