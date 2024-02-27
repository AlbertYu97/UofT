"""Assignment 1 - Grocery Store Models (Task 1)

CSC148 Winter 2024
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory are
Copyright (c) Jonathan Calver, Diane Horton, Sophia Huynh, Joonho Kim and
Jacqueline Smith.

Module Description:

This file contains all the classes necessary to model the relevant entities
in a grocery store.
"""
from __future__ import annotations
from typing import TextIO
import json

# The maximum number of items a customer can have if they use an express line.
EXPRESS_LIMIT = 7


class NoAvailableLineError(Exception):
    """Represents a situation in which a customer has arrived at the checkout
    area and there is no line available for them to join.
    """

    def __str__(self) -> str:
        return 'No line available'


class GroceryStore:
    """A grocery store.

    A grocery store consists of checkout lines, customers, number of regular
    lines / express / self-serve lines.

    TODO: Add one or more attributes to store the checkout lines.
        Include documentation, a type contract, and appropriate Representation
        Invariants for any attribute(s) you add.

    Attributes:
    - num_lines: How many lines this grocery store has.
    - customers: Stores the customer in each of the lines.
    - reg_lines: Number of regular lines
    - express_lines
    - self_lines
    - line_capacity: Max number of customers in every of the lines

    Representation Invariants:
    - self.num_lines > 0
    - len(customers) == self.num_lines
    - self.reg_lines + self.express_lines + self.self_lines == self.num_lines
    """
    num_lines: int
    customers: list[CheckoutLine]

    def __init__(self, config_file: TextIO) -> None:
        """Initialize a GroceryStore from a configuration file <config_file>.

        Preconditions:
        - config_file is a valid JSON configuration file with the keys
          regular_count, express_count, self_serve_count, and line_capacity
        - config_file is open
        - All values in config_file are >= 0
        """
        config = json.load(config_file)
        line_capacity = config["line_capacity"]
        reg_lines = config["regular_count"]
        express_lines = config["express_count"]
        self_lines = config["self_serve_count"]
        num_lines = reg_lines + express_lines + self_lines
        self.num_lines = num_lines
        lines = []
        # Add each of the line to lines list
        for i in range(reg_lines):
            line = RegularLine(line_capacity)
            lines.append(line)
        for j in range(express_lines):
            line = ExpressLine(line_capacity)
            lines.append(line)
        for k in range(self_lines):
            line = SelfServeLine(line_capacity)
            lines.append(line)
        self.customers = lines


    def enter_line(self, customer: Customer) -> int:
        """Pick a new line for <customer> to join, using the algorithm from
        the handout and add <customer> to that line.

        Return the index of the line that the customer joined.

        Raise a NoAvailableLineError if there is no line available for the
        customer to join.

        Preconditions:
        - customer is not currently in any line in this GroceryStore
        """
        chosen_line = -1
        capacity = self.customers[0].capacity
        least_number_of_cx = capacity
        # Loop over lines and find the line that can accept the cx
        for i in range(self.num_lines):
            if self.customers[i].can_accept(customer):
                number_of_cx_in_line = len(self.customers[i])
                if number_of_cx_in_line < least_number_of_cx:
                    least_number_of_cx = number_of_cx_in_line
                    chosen_line = i
        # Raise an error if all lines are full
        if least_number_of_cx == capacity:
            raise NoAvailableLineError
        # Add customer to the line
        self.customers[chosen_line].accept(customer)
        return chosen_line

    def next_checkout_time(self, line_number: int) -> int:
        """Return the time it will take to check out the customer at the front
        of line <line_number>.

        Preconditions:
        - 0 <= line_number < self.num_lines
        """
        line = self.customers[line_number]
        return line.next_checkout_time()


    def remove_front_customer(self, line_number: int) -> int:
        """If there is any customer (or customers) in checkout line
        <line_number>, remove the front customer.

        Return the number of customers remaining in line <line_number>.

        Preconditions:
        - 0 <= line_number < self.num_lines
        """
        # TODO: Implement this method
        return self.customers[line_number].remove_front_customer()

    def close_line(self, line_number: int) -> list[Customer]:
        """Close checkout line <line_number> by updating its status to indicate
        that it is closed and removing from it all customers after the first
        one.

        Return a new list with these removed customers, in the same order as
        they appeared in the line before it closed.

        Preconditions:
        - 0 <= line_number < self.num_lines
        """
        # TODO: Implement this method
        return self.customers[line_number].close()

    def first_in_line(self, line_number: int) -> Customer | None:
        """Return the first customer in line <line_number>, or None if there
        are no customers in line.

        Do not change the line, however.

        Preconditions:
        - 0 <= line_number < self.num_lines
        """
        return self.customers[line_number].first_in_line()


class Customer:
    """A grocery store customer.

    Attributes:
    - name: A unique identifier for this customer.
    - arrival_time: The first time this customer arrived at the checkout area
      and attempted to join a line, or None if they have not yet arrived.
    - _items: The items this customer has.

    Representation Invariants:
    - self.arrival_time is None or self.arrival_time >= 0
    """
    name: str
    arrival_time: int | None
    _items: list[Item]

    def __init__(self, name: str, items: list[Item]) -> None:
        """Initialize a customer with the given <name> and a copy of the
        list <items>.

        The customer's arrival_time is initially None.

        >>> item_list = [Item('bananas', 7)]
        >>> belinda = Customer('Belinda', item_list)
        >>> belinda.name
        'Belinda'
        >>> belinda._items == item_list
        True
        >>> belinda._items is item_list
        False
        >>> belinda.arrival_time is None
        True
        """
        self.name = name
        self._items = []
        self.arrival_time = None
        for item in items:
            self._items.append(item)
    def num_items(self) -> int:
        """Return the number of items this customer has.

        >>> c = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
        >>> c.num_items()
        2
        """
        return len(self._items)

    def item_time(self) -> int:
        """Return the number of seconds it takes for a cashier to check out
        this customer, that is, the time it takes to check out this customer
        at a regular or express line.

        >>> c = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
        >>> c.item_time()
        10
        """
        # TODO: Implement this method
        checkout_time = 0
        for item in self._items:
            checkout_time += int(item.time)
        return checkout_time

class Item:
    """An item to be checked out.

    Attributes:
    - name: the name of this item
    - time: the amount of time it takes a cashier to check out this item

    Representation Invariants:
    - self.time > 0
    """
    name: str
    time: int

    def __init__(self, name: str, time: int) -> None:
        """Initialize a new item with <name> and <time>.

        Preconditions:
        - time > 0

        >>> item = Item('bananas', 7)
        >>> item.name
        'bananas'
        >>> item.time
        7
        """
        self.name = name
        self.time = time


class CheckoutLine:
    """A checkout line in a grocery store.

    This is an abstract class and should not be instantiated.

    Attributes:
    - capacity: The maximum number of customers allowed in this CheckoutLine.
    - is_open: True iff the line is open.
    - _queue: Customers in this line in order by arrival time, with the
                earliest arrival at the front of the list.

    Representation Invariants:
    - len(self) <= self.capacity
    - capacity > 0
    """
    capacity: int
    is_open: bool
    _queue: list[Customer]

    def __init__(self, capacity: int) -> None:
        """Initialize an open and empty CheckoutLine, with the given <capacity>.

        Preconditions:
        - capacity > 0

        >>> line = CheckoutLine(1)
        >>> line.capacity
        1
        >>> line.is_open
        True
        >>> line._queue
        []
        """
        self.capacity = capacity
        self.is_open = True
        self._queue = []

    def __len__(self) -> int:
        """Return the length of this CheckoutLine.

        >>> line = CheckoutLine(10)
        >>> len(line)
        0
        """
        return len(self._queue)

    def can_accept(self, customer: Customer) -> bool:
        """Return True iff this CheckoutLine can accept <customer>.

        >>> line = CheckoutLine(1)
        >>> line.can_accept(Customer('Sophia', []))
        True
        >>> line1 = CheckoutLine(0)
        >>> line1.can_accept(Customer('Sophia', []))
        False
        """
        """
        Return true when capacity is greater than the number of cx in the
        queue and line is open 
        """
        return (self.capacity > len(self._queue)) and (self.is_open)

    def accept(self, customer: Customer) -> bool:
        """Accept <customer> into the end of this CheckoutLine if possible.

        Return True iff the customer is accepted.

        >>> line = CheckoutLine(1)
        >>> c1 = Customer('Belinda', [Item('cheese', 3)])
        >>> c2 = Customer('Hamman', [Item('chips', 4), Item('gum', 1)])
        >>> line.accept(c1)
        True
        >>> line.accept(c2)
        False
        >>> len(line)
        1
        >>> line.first_in_line() is c1
        True
        """
        # call can_accept function
        if self.can_accept(customer):
            self._queue.append(customer)
            return True
        return False

    def next_checkout_time(self) -> int:
        """Return the time it will take to check out the customer at the front
        of this line.

        Preconditions:
        - self.first_in_line() is not None

        No doctests provided, since this method is abstract.
        """
        raise NotImplementedError

    def remove_front_customer(self) -> int:
        """If there is any customer (or customers) in this checkout line,
        remove the front customer.

        Return the number of customers remaining in the line.

        >>> line = CheckoutLine(1)
        >>> line.accept(Customer('Sophia', [Item('red snapper', 21)]))
        True
        >>> line.remove_front_customer() # No one is left in line.
        0
        >>> line.remove_front_customer() # It's still okay to call the method.
        0
        """
        # check if customer list is empty
        if len(self._queue) == 0:
            return 0
        self._queue.pop(0)
        return len(self._queue)

    def close(self) -> list[Customer]:
        """Close this line by updating its status to indicate that it is closed
        and removing from it all customers after the first one.

        Return a new list with these removed customers, in the same order as
        they appeared in the line before it closed.

        >>> line = CheckoutLine(2)
        >>> line.close()
        []
        >>> line.is_open
        False
        >>> line2 = CheckoutLine(2)
        >>> line2.accept(Customer('Sophia', [Item('red snapper', 21)]))
        True
        >>> line2.close()
        []
        """
        self.is_open = False
        if len(self) == 0:
            return []
        first_customer = self._queue[0]
        # Keep first customer, return the rest
        list_copy = self._queue[:]
        list_copy.remove(first_customer)
        self._queue = [first_customer]
        return list_copy

    def first_in_line(self) -> Customer | None:
        """Return the first customer in this line, or None if there are no
        customers in line.

        Do not change the line, however.

        >>> line = CheckoutLine(1)
        >>> line.first_in_line() is None
        True
        >>> line1 = CheckoutLine(1)
        >>> line1.accept(Customer('Sophia', [Item('red snapper', 21)]))
        True
        >>> line1.first_in_line() is not None
        True

        """
        if not self._queue:
            return None
        return self._queue[0]


# TODO: create subclasses for the different types of events below.
class RegularLine(CheckoutLine):
    """A regular CheckoutLine.
    """
    def next_checkout_time(self) -> int:
        next_customer = self.first_in_line()
        return next_customer.item_time()

class ExpressLine(CheckoutLine):
    """An express CheckoutLine.
    """
    def next_checkout_time(self) -> int:
        next_customer = self.first_in_line()
        if next_customer:
            return next_customer.item_time()
        return 0

    def can_accept(self, customer: Customer) -> bool:
        # Number of items < 8
        return customer.num_items() <= EXPRESS_LIMIT and super().can_accept(customer)

class SelfServeLine(CheckoutLine):
    """A self-serve CheckoutLine.
    """
    def next_checkout_time(self) -> int:
        next_customer = self.first_in_line()
        return 2 * next_customer.item_time()

if __name__ == '__main__':
    import doctest

    doctest.testmod()

    check_pyta = True
    if check_pyta:
        import python_ta

        python_ta.check_all(config={
            'allowed-import-modules': ['__future__', 'typing', 'json',
                                       'python_ta', 'doctest'],
            'disable': ['W0613']})
