"""Assignment 1 - Tests for class PriorityQueue  (Task 3a)

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory are
Copyright (c) Jonathan Calver, Diane Horton, Sophia Huynh, Joonho Kim and
Jacqueline Smith.

Module Description:
This module will contain tests for class PriorityQueue.
"""
from container import PriorityQueue

# TODO: Put your pytest test functions for class PriorityQueue here
# Add to empty pq
def test_add_none():
    pq = PriorityQueue()
    pq.add(1)
    assert pq._items == [1]

# Add at front
def test_add_at_font():
    pq = PriorityQueue()
    pq.add(1)
    pq.add(2)
    pq.add(0)
    assert pq._items == [0, 1, 2]

# Add in middle
def test_add_in_middle():
    pq = PriorityQueue()
    pq.add(2)
    pq.add(4)
    pq.add(3)
    pq.add(112)
    pq.add(85)
    pq.add(43)
    assert pq._items == [2, 3, 4, 43, 85, 112]

# Handle tie?


if __name__ == '__main__':
    import pytest

    pytest.main(['test_priority_queue.py'])
