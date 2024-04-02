"""CSC148 Assignment 2

CSC148 Winter 2024
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
Jaisie Sin, and Joonho Kim

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, Jaisie Sin, and Joonho Kim

Module Description:

This file contains the hierarchy of Goal classes and related helper functions.
"""
from __future__ import annotations
import math
import random
from block import Block
from settings import colour_name, COLOUR_LIST


def generate_goals(num_goals: int) -> list[Goal]:
    """Return a randomly generated list of goals with length <num_goals>.

    Each goal must be randomly selected from the two types of Goals provided
    and must have a different randomly generated colour from COLOUR_LIST.
    No two goals can have the same colour.

    Preconditions:
    - num_goals <= len(COLOUR_LIST)
    """
    # TODO: Implement this function
    # Create a copy of color list
    goal_list = []
    colors = COLOUR_LIST.copy()
    for i in range(num_goals):
        # chose a random color and remove it from color list
        chosen_color = random.choice(colors)
        index = colors.index(chosen_color)
        colors.pop(index)
        random_number = random.random()
        if random_number > 0.5:
            # Create a Perimerter goal
            goal = PerimeterGoal(chosen_color)
        else:
            goal = BlobGoal(chosen_color)
        goal_list.append(goal)
    return goal_list
    # return [PerimeterGoal(COLOUR_LIST[0])]  # FIXME


def flatten(block: Block) -> list[list[tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j].

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    # TODO: Implement this function
    list_length = 2 ** (block.max_depth - block.level)
    flatten_lst = [
        [() for _i in range(list_length)] for _j in range(list_length)
    ]
    result = _fill_color(block, 0, 0, list_length, flatten_lst)
    return result


def _fill_color(
        block: Block,
        x: int,
        y: int,
        size: int,
        flatten_list: list[list[tuple[int, int, int]]],
) -> list[list[tuple[int, int, int]]]:
    """Fill the board with corresponding color"""
    size_in_unit_cell = 2 ** (block.max_depth - block.level)
    if not block.children:
        for col in range(x, x + size_in_unit_cell):
            for row in range(y, y + size_in_unit_cell):
                flatten_list[col][row] = block.colour
    else:
        child_cell = size_in_unit_cell // 2
        _fill_color(
            block.children[0], x + child_cell, y, child_cell, flatten_list
        )
        _fill_color(block.children[1], x, y, child_cell, flatten_list)
        _fill_color(
            block.children[2], x, y + child_cell, child_cell, flatten_list
        )
        _fill_color(
            block.children[3],
            x + child_cell,
            y + child_cell,
            child_cell,
            flatten_list,
            )
    return flatten_list
    # create a copy of the block
    # block_copy = block.create_copy()
    # unit_length = block.size
    # level = block.level
    # # Get the length of unit cell, unit_length is the len of unit cell
    # while level < block.max_depth:
    #     unit_length = round(unit_length / 2.0)
    #     level += 1
    #
    # # create list_length * list_length emtpy nested list
    # list_length = int(math.pow(2, block.max_depth - block.level))
    # flatten_lst = [[None for _ in range(list_length)] for _ in range(list_length)]
    # initial_position = block.position
    #
    # # Base case: current block is leaf, return 2d color list
    # if block.colour:
    #     return _leaf_to_unit_blocks(flatten_lst, block, unit_length)
    # # Not leaf
    # # Get the block which all the cells are unit cell
    # for child in block.children:
    #
    #     # child is leaf
    #     if child.colour:
    #         flatten_lst = _leaf_to_unit_blocks(flatten_lst, child, list_length)
    #     # child is not leaf
    #     else:
    #         flatten_lst = flatten(child)
    # return flatten_lst


def _leaf_to_unit_blocks(nested_list: list[list[tuple[int, int, int]]], sub_block: Block, unit_length: float) -> list[list[tuple[int, int, int]]]:
        a, b = sub_block.position
        size = round(sub_block.size / unit_length)
        index_x_start = round(a / unit_length)
        index_y_start = round(b / unit_length)
        for i in range(index_x_start, index_x_start + size):
            for j in range(index_y_start, index_y_start + size):
                nested_list[i][j] = sub_block.colour
        # Recursion on children
        return nested_list

def _split_into_unit_cells(block: Block) -> None:
    """
    Split all leaf in a block into unit cells
    """
    if block.level != block.max_depth:
        # block has color, child has not reached max_depth.
        # Current block has no child, so create child and make color none
        if block.colour:
            children_position = block.children_positions()
            l = block.child_size()
            child_0 = Block(children_position[0], l, block.colour, block.level + 1, block.max_depth)
            child_1 = Block(children_position[1], l, block.colour, block.level + 1, block.max_depth)
            child_2 = Block(children_position[2], l, block.colour, block.level + 1, block.max_depth)
            child_3 = Block(children_position[3], l, block.colour, block.level + 1, block.max_depth)
            block.children = [child_0, child_1, child_2, child_3]
            block.colour = None
        # Block with no color have children. So call recursion on child for all.
        for child in block.children:
            _split_into_unit_cells(child)


def _fill_2d_list(sublist: list[list[tuple[int, int, int]]], block: Block, initial_position: tuple[int, int], unit_length: float) -> list[list[tuple[int, int, int]]]:
    if block.level == block.max_depth:
        x, y = block.position
        index_x = round((x - initial_position[0]) / unit_length)
        index_y = round((y - initial_position[0]) / unit_length)
        sublist[index_x][index_y] = block.colour
    # Recursion on children
    else:
        for child in block.children:
            _fill_2d_list(sublist, child, initial_position, unit_length)
    return sublist

class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    Instance Attributes:
    - colour: The target colour for this goal, that is the colour to which
              this goal applies.
    """
    colour: tuple[int, int, int]

    def __init__(self, target_colour: tuple[int, int, int]) -> None:
        """Initialize this goal to have the given <target_colour>.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given <board>.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    """A goal to maximize the presence of this goal's target colour
    on the board's perimeter.
    """

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.

        The score for a PerimeterGoal is defined to be the number of unit cells
        on the perimeter whose colour is this goal's target colour. Corner cells
        count twice toward the score.
        """
        # TODO: Implement this method
        # return 148  # FIXME
        score = 0
        nested_list = flatten(board)
        size = len(nested_list)
        # Special case for a unit cell
        if size == 1 and nested_list[0][0] == self.colour:
            return 4
        # Look over the nested loop
        for i in range(size):
            for j in range(size):
                if nested_list[i][j] == self.colour and i in [0, size - 1] and j in [0, size - 1]:
                    score += 2
                elif nested_list[i][j] == self.colour and i == 0 or i == size - 1 or j == 0 or j == size - 1:
                    score += 1
        print(f"total score {score}")
        return score

    def description(self) -> str:
        """Return a description of this goal.
        """
        # TODO: Implement this method
        # return 'DESCRIPTION'  # FIXME
        color = colour_name(self.colour)
        description = 'Perimeter Goal for color ' + color
        return description


class BlobGoal(Goal):
    """A goal to create the largest connected blob of this goal's target
    colour, anywhere within the Block.
    """

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.

        The score for a BlobGoal is defined to be the total number of
        unit cells in the largest connected blob within this Block.
        """
        # TODO: Implement this method
        # Call flatten to get 2 dimensional board
        twod_board = flatten(board)
        size = len(twod_board)
        # Created nested list filled with -1
        visited = [[-1 for _ in range(size)] for _ in range(size)]
        score = 0
        position = 0, 0
        # Loop over all positions and find the score at each position
        for i in range(size):
            for j in range(size):
                # Create a copy of visited since it needs to be reused
                visited_copy = visited.copy()
                score_i_j = self._undiscovered_blob_size((i, j), twod_board, visited_copy)
                if score_i_j > score:
                    score = score_i_j
                    position = i, j
        print(f"biggest blob {score}")
        print(f"position {position}")
        return score

    def _undiscovered_blob_size(self, pos: tuple[int, int],
                                board: list[list[tuple[int, int, int]]],
                                visited: list[list[int]]) -> int:
        """Return the size of the largest connected blob in <board> that (a) is
        of this Goal's target <colour>, (b) includes the cell at <pos>, and (c)
        involves only cells that are not in <visited>.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure (to <board>) that, in each cell,
        contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.

        If <pos> is out of bounds for <board>, return 0.
        """
        # TODO: Implement this method
        blob_size = 0
        x, y = pos[0], pos[1]
        # Base case the position is not inside the board
        if (x >= len(board)) or (y >= len(board)) or (x < 0) or (y < 0):
            return 0
        else:
            # The position is inside the board and not visited
            if visited[x][y] == -1:
                # Color match
                if board[x][y] == self.colour:
                    visited[x][y] = 1
                    # Call recursion on all neighbours
                    blob_size = blob_size + 1 + self._undiscovered_blob_size((x, y-1), board, visited) + self._undiscovered_blob_size((x, y+1), board, visited) + self._undiscovered_blob_size((x-1, y), board, visited) + self._undiscovered_blob_size((x+1, y), board, visited)
                    # Color does not match
                else:
                    visited[x][y] = 0
        return blob_size


    def description(self) -> str:
        """Return a description of this goal.
        """
        # TODO: Implement this method
        # return 'DESCRIPTION'  # FIXME
        color = colour_name(self.colour)
        description = 'Blob Goal for color ' + color
        return description


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
