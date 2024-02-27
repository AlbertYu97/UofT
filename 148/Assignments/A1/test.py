from store import *
config_file_name = 'input_files/config_111_10.json'
with open(config_file_name) as config_file:
    sim = GroceryStore(config_file)
print(sim.customers)
print(sim.num_lines)
c1 = Customer('Belinda', [Item('cheese', 3)])
c2 = Customer('Hamman', [Item('chips', 4), Item('gum', 1)])
c3 = Customer('Hamman', [Item('chips', 4), Item('gum', 1)])
c4 = Customer('Hamman', [Item('chips', 4), Item('gum', 1),
                                     Item('chips', 4), Item('gum', 1),
                                     Item('chips', 4), Item('gum', 1),
                                     Item('chips', 4), Item('gum', 1),
                                     Item('chips', 4), Item('gum', 1)])

sim.enter_line(c1)
sim.enter_line(c4)
sim.enter_line(c3)
print(sim.next_checkout_time(0))
print(sim.next_checkout_time(1))
print(sim.next_checkout_time(2))
#
# print(sim.remove_front_customer(0))
# from io import StringIO
# EVENT_SAMPLE = StringIO("""121 Arrive William Bananas 7
# 22 Arrive Trevor Flowers 22 Bread 3 Cheese 3 Cheese 3
# 41 Close 0""")
# event_lst = []
# for line in EVENT_SAMPLE:
#     sub = line.strip().split()
#     print(sub)
#     timestamp = sub[0]
#
#     if sub[1] == "Arrive":
#         name = sub[2]
#         items = []
#         i = 3
#         while i < len(sub):
#             item = Item(sub[i], sub[i+1])
#             items.append(item)
#             i += 2
#         customer = Customer(name, items)
#
#     if sub[1] == "Close":
#         line_number = sub[2]
#
from event import create_event_list
from simulation import GroceryStoreSimulation

store_config_list = [
    'input_files/config_001_10.json',
    # 'input_files/config_010_10.json',
    # 'input_files/config_100_01.json',
    # 'input_files/config_100_10.json',
    # 'input_files/config_111_01.json',
    # 'input_files/config_111_10.json',
    # 'input_files/config_300_01.json',
    # 'input_files/config_300_10.json',
    # 'input_files/config_333_01.json',
    # 'input_files/config_333_10.json',
    # 'input_files/config_642_05.json',
]

events_config_list = [
    # 'input_files/events_base.txt',
    # 'input_files/events_mixtures.txt',
    # 'input_files/events_no_express.txt',
    'input_files/events_one.txt',
    # 'input_files/events_one_at_a_time.txt',
    # 'input_files/events_one_close.txt',
    # 'input_files/events_two.txt',
]


def simulation_all_combinations() -> None:
    """Test two events and single checkout simulation."""

    for store_name in store_config_list:
        for events_name in events_config_list:
            close_line_error = False
            store_config = open(store_name)
            events_config = open(events_name)

            gss = GroceryStoreSimulation(store_config)
            gss.run(create_event_list(events_config))
            print(f'{events_name[12:]} in store_{store_name[12:]} = {gss.stats}')

            store_config.close()
            events_config.close()

if __name__ == '__main__':
    simulation_all_combinations()
# line = SelfServeLine(1)
# line.accept(c1)
# print(line.next_checkout_time())
