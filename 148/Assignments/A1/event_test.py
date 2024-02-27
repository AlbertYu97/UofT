from event import *
config_file_name = 'input_files/events_base.txt'
with open(config_file_name) as config_file:
    events = create_event_list(config_file)

print(len(events))
print(events[0].timestamp)
print(events[1].timestamp)
print(events[2].timestamp)
print(events[3].timestamp)
print(isinstance(events[0], CustomerArrival))
print(isinstance(events[5], CloseLine))

ls = [10, 20, 20, 30]
ls.insert(0, 99)
print(ls)
nm1 = 'anna'
nm2 = 'fred'
nm3 = 'sophia'
nm4 = 'mona'
print()
