import pytest
from block import *


# def test_create_copy():
block = generate_board(3, 750)
copy = block.create_copy()
block == copy
# assert block == copy
