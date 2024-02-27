# from store import *
# config_file_name = 'input_files/config_111_01.json'
# with open(config_file_name) as config_file:
#     sim = GroceryStore(config_file)
#     config_file.close()
# print(sim.checkout_line)
# c1 = Customer('Belinda', [Item('cheese', 3)])
# c2 = Customer('Hamman', [Item('chips', 4), Item('gum', 1)])
# c3 = Customer('Hamman', [Item('chips', 4), Item('gum', 1)])
# c4 = Customer('Hamman', [Item('chips', 4), Item('gum', 1),
#                                      Item('chips', 4), Item('gum', 1),
#                                      Item('chips', 4), Item('gum', 1),
#                                      Item('chips', 4), Item('gum', 1),
#                                      Item('chips', 4), Item('gum', 1)])
#
# print(sim.enter_line(c1))
# print(sim.enter_line(c4))
# print(sim.close_line(1))
# print(sim.enter_line(c3))
# # # print(sim.next_checkout_time(0))
# # # print(sim.next_checkout_time(1))
# # # print(sim.next_checkout_time(2))
# # #
# # # print(sim.remove_front_customer(0))
from io import StringIO

# # # EVENT_SAMPLE = StringIO("""121 Arrive William Bananas 7
# # # 22 Arrive Trevor Flowers 22 Bread 3 Cheese 3 Cheese 3
# # # 41 Close 0""")
# # # event_lst = []
# # # for line in EVENT_SAMPLE:
# # #     sub = line.strip().split()
# # #     print(sub)
# # #     timestamp = sub[0]
# # #
# # #     if sub[1] == "Arrive":
# # #         name = sub[2]
# # #         items = []
# # #         i = 3
# # #         while i < len(sub):
# # #             item = Item(sub[i], sub[i+1])
# # #             items.append(item)
# # #             i += 2
# # #         customer = Customer(name, items)
# # #
# # #     if sub[1] == "Close":
# # #         line_number = sub[2]
# # #
from event import create_event_list
from simulation import GroceryStoreSimulation

# #
store_config_list = [
    # 'input_files/config_001_10.json',
    # 'input_files/config_010_10.json',
    # 'input_files/config_100_01.json',
    # 'input_files/config_100_10.json',
    # 'input_files/config_111_01.json',
    # 'input_files/config_111_10.json',
    'input_files/config_300_01.json',
    'input_files/config_300_10.json',
    # 'input_files/config_333_01.json',
    # 'input_files/config_333_10.json',
    # 'input_files/config_642_05.json',
]
# #
events_config_list = [
    'input_files/events_base.txt',
    'input_files/events_mixtures.txt',
    'input_files/events_no_express.txt',
    'input_files/events_one.txt',
    # 'input_files/events_one_test.txt',
    'input_files/events_one_at_a_time.txt',
    'input_files/events_one_close.txt',
    'input_files/events_two.txt',
]
# #
for store_name in store_config_list:
    for events_name in events_config_list:
        close_line_error = False
        store_config = open(store_name)
        events_config = open(events_name)
        gss = GroceryStoreSimulation(store_config)
        gss.run(create_event_list(events_config))
        print(gss.stats)
# # #
# # #         gss = GroceryStoreSimulation(store_config)
# # # print(gss._events)
# # # print(gss._store)
# # # initial_events = create_event_list(events_config)
# # # print(initial_events)
# # # for event in initial_events:
# # #     gss._events.add(event)
# # # while not gss._events.is_empty():
# # #     event = gss._events.remove()
# # #     new_event_lst = event.do(gss._store)
# # #     if new_event_lst is not None:
# # #         for new_event in new_event_lst:
# # #             gss._events.add(new_event)
# #
# #
# # def simulation_all_combinations() -> None:
# #     """Test two events and single checkout simulation."""
# #
# #     for store_name in store_config_list:
# #         for events_name in events_config_list:
# #             close_line_error = False
# #             store_config = open(store_name)
# #             events_config = open(events_name)
# #
# #             gss = GroceryStoreSimulation(store_config)
# #             gss.run(create_event_list(events_config))
# #             print(
# #                 f'{events_name[12:]} in store_{store_name[12:]} = {gss.stats}'
# #             )
# #
# #             store_config.close()
# #             events_config.close()
# #
# #
# # if __name__ == '__main__':
# #     simulation_all_combinations()
# # # line = SelfServeLine(1)
# # # line.accept(c1)
# # # print(line.next_checkout_time())
# # from io import StringIO
# #
# from assignments.a1.event import create_event_list
# from assignments.a1.simulation import GroceryStoreSimulation

# #
# # CONFIG_FILE = '''{
# #   "regular_count": 1,
# #   "express_count": 0,
# #   "self_serve_count": 0,
# #   "line_capacity": 1
# # }
# # '''
# #
# # EVENT_FILE = '''10 Arrive Tamara Bananas 7
# # 5 Arrive Jugo Bread 3 Cheese 3
# # '''
# # gss = GroceryStoreSimulation(StringIO(CONFIG_FILE))
# # d = create_event_list(StringIO(EVENT_FILE))
# # print(d)
# # gss.run(create_event_list(StringIO(EVENT_FILE)))
# #
# # print(gss.stats)

# CONFIG_FILE_demo = '''{
#   "regular_count": 1,
#   "express_count": 1,
#   "self_serve_count": 1,
#   "line_capacity": 3
# }
# '''
#
# EVENT_FILE_demo = '''0 Arrive Mia Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Milk 7 Cho 9
# 2 Arrive Pedro Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Bread 11
# 5 Arrive Leo Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1
# 8 Arrive Jasmine Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Milk 3 Milk 3
# 14 Arrive Xin Bread 8 Bread 8 Water 6
# 19 Arrive Sadia Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Banana 1 Milk 4
# 21 Close 0
# '''
#
# gss = GroceryStoreSimulation(StringIO(CONFIG_FILE_demo))
# initial_events = create_event_list(StringIO(EVENT_FILE_demo))
# # gss.run(d)
#
# from store import *
# from event import *
#
# for event in initial_events:
#     gss._events.add(event)
# max_wait_time = [0]
# print(max_wait_time)
# arrival_time = {}
# customers = []
# i = 0
# while not gss._events.is_empty():
#     event = gss._events.remove()
#     i += 1
#     if isinstance(event, CustomerArrival):
#         print(
#             f"{i} Handle the customer arrival event at {event.timestamp} with {event.customer.name}"
#         )
#         customer = event.customer.name
#         if customer not in customers:
#             customers.append(customer)
#         if customer not in arrival_time:
#             arrival_time[customer] = event.timestamp
#     if isinstance(event, CheckoutStarted):
#         print(
#             f"{i} Handle the checkout started event at {event.timestamp} with line number {event.line_number}"
#         )
#     if isinstance(event, CloseLine):
#         print(
#             f"{i} Handle the close line event at {event.timestamp} with line number {event.line_number}"
#         )
#     if isinstance(event, CheckoutCompleted):
#         print(
#             f"{i} Handle the checkout completed event at {event.timestamp} with line number {event.line_number} and {event.customer.name}"
#         )
#         max_wait_time.append(
#             event.timestamp - arrival_time[event.customer.name]
#         )
#     new_event_lst = event.do(gss._store)
#     if new_event_lst is not None:
#         for new_event in new_event_lst:
#             gss._events.add(new_event)
#             if isinstance(new_event, CustomerArrival):
#                 print(
#                     f"{i} Generate new the customer arrival event at {new_event.timestamp} with line number {new_event.customer.name}"
#                 )
#             if isinstance(new_event, CheckoutStarted):
#                 print(
#                     f"{i} Generate new the checkout started event at {new_event.timestamp} with line number {new_event.line_number}"
#                 )
#             if isinstance(new_event, CloseLine):
#                 print(
#                     f"{i} Generate new the close line event at {new_event.timestamp} with line number {new_event.line_number}"
#                 )
#             if isinstance(new_event, CheckoutCompleted):
#                 print(
#                     f"{i} Generate new the checkout completed event at {new_event.timestamp} with line number {new_event.line_number} and {new_event.customer.name}"
#                 )
# gss.stats['num_customers'] = len(customers)
# gss.stats['total_time'] = event.timestamp
# gss.stats['max_wait'] = max(max_wait_time)




# events = '''0 Arrive Alice Apples 2
# 1 Arrive Bob Bananas 3
# 3 Arrive Carol Carrots 1
# '''
#
# for line in EVENT_FILE_demo:
#     sub = line.strip().split()
#     print(sub)
# gss = GroceryStoreSimulation(StringIO(config))
# gss.run(create_event_list(StringIO(events)))
