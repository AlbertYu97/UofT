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

This file contains the hierarchy of player classes.
"""
from __future__ import annotations
import random
import pygame

from block import Block
from goal import Goal, generate_goals

from actions import Action, KEY_ACTION, ROTATE_CLOCKWISE, \
    ROTATE_COUNTER_CLOCKWISE, \
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, PASS, PAINT, COMBINE


def create_players(num_human: int, num_random: int, smart_players: list[int]) \
        -> list[Player]:
    """Return a new list of Player objects.

    <num_human> is the number of human player, <num_random> is the number of
    random players, and <smart_players> is a list of difficulty levels for each
    SmartPlayer that is to be created.

    The list should contain <num_human> HumanPlayer objects first, then
    <num_random> RandomPlayer objects, then the same number of SmartPlayer
    objects as the length of <smart_players>. The difficulty levels in
    <smart_players> should be applied to each SmartPlayer object, in order.

    Player ids are given in the order that the players are created, starting
    at id 0.

    Each player is assigned a random goal.
    """
    # TODO: Implement this function
    # goals = generate_goals(1)  # FIXME
    # return [HumanPlayer(0, goals[0])]  # FIXME
    # Generate all goals first
    num_of_players = num_human + num_random + len(smart_players)
    goal_list = generate_goals(num_of_players)
    players = []
    player_id = 0
    # Generate human players
    for i in range(num_human):
        human_p = HumanPlayer(player_id, goal_list.pop())
        player_id += 1
        players.append(human_p)
    for j in range(num_random):
        random_p = RandomPlayer(player_id, goal_list.pop())
        player_id += 1
        players.append(random_p)
    for diff_lv in smart_players:
        smart_p = SmartPlayer(player_id, goal_list.pop(), diff_lv)
        player_id += 1
        players.append(smart_p)
    return players


def _get_block(block: Block, location: tuple[int, int], level: int) -> \
        Block | None:
    """Return the Block within <block> that is at <level> and includes
    <location>. <location> is a coordinate-pair (x, y).

    A block includes all locations that are strictly inside it, as well as
    locations on the top and left edges. A block does not include locations that
    are on the bottom or right edge.

    If a Block includes <location>, then so do its ancestors. <level> specifies
    which of these blocks to return. If <level> is greater than the level of
    the deepest block that includes <location>, then return that deepest block.

    If no Block can be found at <location>, return None.

    Preconditions:
        - block.level <= level <= block.max_depth
    """
    # TODO: Implement this function
    x_coord, y_coord = block.position
    width = block.size
    # Based case: location is not in block range
    if not (x_coord <= location[0] < x_coord + width and y_coord <= location[1] < y_coord + width):
        return None
    # Location is in block range
    else:
        # check current level
        # If the level match, we found the result
        if block.level == level:
            return block
        # If the current level is smaller than desired level, go deeper
        if block.level < level:
            # If the blcok has no child, current level is the deepest possible
            # level, return current block
            if not block.children:
                return block
            # If it has child, loop over all child and do recursion
            else:
                for child in block.children:
                    block = _get_block(child, location, level)
                    if block:
                        return block


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    Instance Attributes:
    - id: This player's number.
    - goal: This player's assigned goal for the game.
    - penalty: The penalty accumulated by this player through their actions.
    """
    id: int
    goal: Goal
    penalty: int

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.id = player_id
        self.penalty = 0

    def get_selected_block(self, board: Block) -> Block | None:
        """Return the block that is currently selected by the player.

        If no block is selected by the player, return None.
        """
        raise NotImplementedError

    def process_event(self, event: pygame.event.Event) -> None:
        """Update this player based on the pygame event.
        """
        raise NotImplementedError

    def generate_move(self, board: Block) -> \
            tuple[Action, Block] | None:
        """Return a potential move to make on the <board>.

        The move is a tuple consisting of an action and
        the block the action will be applied to.

        Return None if no move can be made, yet.
        """
        raise NotImplementedError


class HumanPlayer(Player):
    """A human player.

    Instance Attributes:
    - _level: The level of the Block that the user selected most recently.
    - _desired_action: The most recent action that the user is attempting to do.

    Representation Invariants:
    - self._level >= 0
    """
    _level: int
    _desired_action: Action | None

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        Player.__init__(self, player_id, goal)

        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._desired_action = None

    def get_selected_block(self, board: Block) -> Block | None:
        """Return the block that is currently selected by the player based on
        the position of the mouse on the screen and the player's desired level.

        If no block is selected by the player, return None.
        """
        mouse_pos = pygame.mouse.get_pos()
        block = _get_block(board, mouse_pos, self._level)

        return block

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant keyboard events made by the player based on
        the mapping in KEY_ACTION, as well as the W and S keys for changing
        the level.
        """
        if event.type == pygame.KEYUP:
            if event.key in KEY_ACTION:
                self._desired_action = KEY_ACTION[event.key]
            elif event.key == pygame.K_w:
                self._level -= 1
                self._desired_action = None
            elif event.key == pygame.K_s:
                self._level += 1
                self._desired_action = None

    def generate_move(self, board: Block) -> \
            tuple[Action, Block] | None:
        """Return the move that the player would like to perform. The move may
        not be valid.

        Return None if the player is not currently selecting a block.

        This player's desired action gets reset after this method is called.
        """
        block = self.get_selected_block(board)

        if block is None or self._desired_action is None:
            self._correct_level(board)
            self._desired_action = None
            return None
        else:
            move = self._desired_action, block

            self._desired_action = None
            return move

    def _correct_level(self, board: Block) -> None:
        """Correct the level of the block that the player is currently
        selecting, if necessary.
        """
        self._level = max(0, min(self._level, board.max_depth))


class ComputerPlayer(Player):
    """A computer player. This class is still abstract,
    as how it generates moves is still to be defined
    in a subclass.

    Instance Attributes:
    - _proceed: True when the player should make a move, False when the
                player should wait.
    """
    _proceed: bool

    def __init__(self, player_id: int, goal: Goal) -> None:
        Player.__init__(self, player_id, goal)

        self._proceed = False

    def get_selected_block(self, board: Block) -> Block | None:
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        if (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == pygame.BUTTON_LEFT):
            self._proceed = True

    # Note: this is included just to make pyTA happy; as it thinks
    #       we forgot to implement this abstract method otherwise :)
    def generate_move(self, board: Block) -> \
            tuple[Action, Block] | None:
        raise NotImplementedError

def get_random_block(board: Block) -> Block:
    """
    Go through the tree structure of a board and return a random sub-block.
    At each level, the prob of return the current block is 1 / max_depth,
    the prob of selecting a child of the current block is 1 - 1 / max_depth.
    The prob of selecting any of the 4 child is the same.
    """
    probability = 1 / board.max_depth
    random_number = random.random()
    # Base case the board has no children or the random number < prob
    if not board.children or random_number < probability:
        return board
    else:
        # board has children
        if random_number < 0.25:
            get_random_block(board.children[0])
        elif random_number < 0.5:
            get_random_block(board.children[1])
        elif random_number < 0.75:
            get_random_block(board.children[2])
        else:
            get_random_block(board.children[3])


def get_random_action(start: int, end: int) -> Action:
    random_number = random.randint(start,end)
    actions = [ROTATE_COUNTER_CLOCKWISE, ROTATE_CLOCKWISE, SWAP_VERTICAL, SWAP_HORIZONTAL, SMASH, COMBINE, PAINT]
    action = actions[random_number]
    return action


class RandomPlayer(ComputerPlayer):
    """A computer player who chooses completely random moves."""

    def generate_move(self, board: Block) -> \
            tuple[Action, Block] | None:
        """Return a valid, randomly generated move only during the player's
        turn.  Return None if the player should not make a move yet.

        A valid move is a move other than PASS that can be successfully
        performed on the <board>.

        This function does not mutate <board>.
        """
        # TODO: Implement this method
        # Return None if the player should not make a move yet
        if not self._proceed:
            return None
        # Create a copy of the board
        copy = board.create_copy()
        loop_continue = True
        sub_block, action = None, None
        # The while loop stops when a possible action is found on a block
        while loop_continue:
            # Create a random location and level
            rand_x = copy.position[0] + random.randint(0, copy.size)
            rand_y = copy.position[1] + random.randint(0, copy.size)
            rand_location = (rand_x, rand_y)
            rand_lv = random.randint(copy.level, copy.max_depth)
            # Get a random block
            sub_block = _get_block(copy, rand_location, rand_lv)
            # Get a random action
            action = get_random_action(0, 6)
            dict = {'colour': self.goal.colour}
            if sub_block:
                result = action.apply(sub_block, dict)
            # if action can be applied result return True
                if result:
                    self._proceed = False
                    loop_continue = False
        # Get the level and position of the copied block
        # Use the info to locate the original sub-block
        level = sub_block.level
        location = sub_block.position
        original_block = _get_block(board, location, level)
        return action, original_block


class SmartPlayer(ComputerPlayer):
    """A computer player who chooses moves by assessing a series of random
    moves and choosing the one that yields the best score.

    Private Instance Attributes:
    - _num_test: The number of moves this SmartPlayer will test out before
                 choosing a move.
    """
    _num_test: int

    def __init__(self, player_id: int, goal: Goal, difficulty: int) -> None:
        """Initialize this SmartPlayer with a <player_id> and <goal>.

        Use <difficulty> to determine and record how many moves this SmartPlayer
        will assess before choosing a move. The higher the value for
        <difficulty>, the more moves this SmartPlayer will assess, and hence the
        more difficult an opponent this SmartPlayer will be.

        Preconditions:
        - difficulty >= 0
        """
        # TODO: Implement this method
        ComputerPlayer.__init__(self, player_id, goal)
        self._num_test = difficulty

    def generate_move(self, board: Block) -> \
            tuple[Action, Block] | None:
        """Return a valid move only during the player's turn by assessing
        multiple valid moves and choosing the move that results in the highest
        score for this player's goal.  This score should also account for the
        penalty of the move.  Return None if the player should not make a move.

        A valid move is a move other than PASS that can be successfully
        performed on the <board>. If no move can be found that is better than
        the current score, this player will pass.

        This method does not mutate <board>.
        """
        # TODO: Implement this method
        # Return None if the player should not make a move yet
        if not self._proceed:
            return None
        # start_score is the score of the smart player before any move
        start_score = self.goal.score(board)
        best_score = start_score
        best_block, best_action = None, None
        # Create moves and find the one which adds most score
        for i in range(self._num_test):
            # Create a copy of the board
            copy = board.create_copy()
            loop_continue = True
        # The while loop stops when a possible action is found on a block
            while loop_continue:
                # Get a random block
                # Create a random location and level
                rand_x = copy.position[0] + random.randint(0, copy.size)
                rand_y = copy.position[1] + random.randint(0, copy.size)
                rand_location = (rand_x, rand_y)
                rand_lv = random.randint(copy.level, copy.max_depth)
                # Get a random block
                sub_block = _get_block(copy, rand_location, rand_lv)
                # Get a random action
                action = get_random_action(0, 6)
                dict = {'colour': self.goal.colour}
                if sub_block and action.apply(sub_block, dict):
                    # if action can be applied it return True
                    loop_continue = False
                    updated_score = self.goal.score(copy) - action.penalty
                    if updated_score > best_score:
                        best_score = updated_score
                        best_block = sub_block
                        best_action = action
        self._proceed = False
        # Decide return
        if best_score == start_score:
            return PASS, board
        # Get the level and position of the copied block
        # Use the info to locate the original sub-block
        original_block = _get_block(board, best_block.position, best_block.level)
        return best_action, original_block


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'actions', 'block',
            'goal', 'pygame', '__future__'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
