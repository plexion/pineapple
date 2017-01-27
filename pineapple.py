# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import itertools
import random
import pickle
import time
 
# data
SUITS = ('c', 'd', 'h', 's')
RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
 
DECK = tuple(''.join(card) for card in itertools.product(RANKS, SUITS))
 
ORDER_LOOKUP = dict(zip(DECK, range(52)))
RANK_LOOKUP = dict(zip(RANKS, range(13)))
SUIT_LOOKUP = dict(zip(SUITS, range(4)))
 
# utility functions
def cmp_cards(a, b):
    return ((ORDER_LOOKUP[a] > ORDER_LOOKUP[b]) - (ORDER_LOOKUP[a] < ORDER_LOOKUP[b]))
   
def cmp_tuples(a, b):
    n1 = len(a)
    n2 = len(b)
    if n1 != n2:
        return ((n1 > n2) - (n1 < n2))
    return ((a > b) - (a < b))
   
def suit(card):
    return card[1]
   
def suit_int(card):
    return SUIT_LOOKUP[card[1]]
   
def rank(card):
    return card[0]
   
def rank_int(card):
    return RANK_LOOKUP[card[0]]
   
def card_int(card):
    s = 1 << suit_int(card)
    r = rank_int(card)
    c = (s << 4) | r
    return c
   
# test functions
def is_straight(cards):
    cards=sorted(cards)
    previous = rank_int(cards[0]) - 1
    for card in cards:
        r = rank_int(card)
        if r != previous + 1:
            if not (r == 12 and previous == 3):
                return False
        previous = r
    return True
   
def is_flush(cards):
    s = suit(cards[0])
    return all(suit(card) == s for card in cards)
   
def same_rank(cards):
    r = rank(cards[0])
    return all(rank(card) == r for card in cards)
   
def split_ranks(cards, indexes):
    for index in indexes:
        a, b = cards[:index], cards[index:]
        if same_rank(a) and same_rank(b):
            return True
    return False
   
def is_full_house(cards):
    cards=sorted(cards)
    return split_ranks(cards, (2, 3))
    
   
def is_four(cards):
    cards=sorted(cards)
    return split_ranks(cards, (1, 4))
   
def is_pat(cards):
    return is_straight(cards) or is_flush(cards) or is_full_house(cards) or is_four(cards)
   
def is_straight_flush(cards):
    return is_straight(cards) and is_flush(cards)
   
def rank_count(cards):
    result = {}
    for card in cards:
        r = rank_int(card)
        result[r] = result.get(r, 0) + 1
    return result
   
def is_three(cards):
    counts = rank_count(cards)
    return ((3 in counts.values()) and len(counts.values())==2)
   
def is_two_pair(cards):
    counts = rank_count(cards)
    return ((2 in counts.values()) and len(counts.values())==3)
   
def is_pair(cards):
    counts = rank_count(cards)
    return ((1 in counts.values()) and len(counts.values())==4)
   
   
def get_straight_rank(cards):
    cards=sorted(cards)
    top = rank_int(cards[-1])
    bottom = rank_int(cards[0])
    if top == 12 and bottom == 0:
        return 3
    return top
   
def evaluate_hand(cards):
    flush = is_flush(cards)
    straight = is_straight(cards)
    ranks=[0]
    counts = rank_count(cards)
    if straight:
        ranks = [get_straight_rank(cards)]
    if straight and flush:
        value = 9
    elif is_four(cards):
        value = 8
    elif is_full_house(cards):
        value = 7
    elif flush:
        value = 6
    elif straight:
        value = 5
    elif is_three(cards):
        value = 4
    elif is_two_pair(cards):
        value = 3
    elif is_pair(cards):
        value = 2
    else:
        value = 1
    ranks.insert(0, value)
    return tuple(ranks)

def deal_hands():
    i=0
    while (i < 1000):
        hand=random.sample(DECK,5)
        evaluate_hand(hand)
        
    
    
    