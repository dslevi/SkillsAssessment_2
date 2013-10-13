"""
Reservation finder

Along with this file, you'll find two files named units.csv and reservations.csv with fields in the following format

location_id, unit_size
location_id, reservation_start_date, reservation_end_date

You will write a simple application that manages a reservation system. It will have two commands, 'available' and 'reserve' with the following behaviors:

available <date> <number of occupants> <length of stay>
This will print all available units that match the criteria. Any unit with capacity equal or greater to the number of occupants will be printed out.

Example:
SeaBnb> available 10/10/2013 2 4
Unit 10 (Size 3) is available
Unit 20 (Size 2) is available

reserve <unit number> <start date> <length of stay>
This creates a record in your reservations that indicates the unit has been reserved. It will print a message indicating its success.

A reservation that ends on any given day may be rebooked for the same evening, ie:
    
    If a reservation ends on 10/10/2013, a different reservation may be made starting on 10/10/2013 as well.

Example:
SeaBnb> reserve 10 10/11/2013 3 
Successfully reserved unit 10 for 3 nights

Reserving a unit must make the unit available for later reservations. Here's a sample session:

SeaBnb> available 10/10/2013 2 4
Unit 10 (Size 3) is available
Unit 20 (Size 2) is available
SeaBnb> reserve 10 10/11/2013 3 
Successfully reserved unit 10 for 3 nights
SeaBnb> available 10/10/2013 2 4
Unit 20 (Size 2) is available
SeaBnb> reserve 10 10/11/2013 3 
Unit 10 is unavailable during those dates
SeaBnb> quit

Notes:
Start first by writing the functions to read in the csv file. These have been stubbed for you. 
Then write the availability function, then reservation. 
Test your program at each step (it may be beneficial to write tests in a separate file.) 
Use the 'reservations' variable as your database. 
Store all the reservations in there, including the ones from the new ones you will create.

The datetime and timedelta classes will be immensely helpful here, as will the strptime function.
"""

import sys
import datetime, time

def read_units():
    """Read in the file units.csv and returns a list of all known units."""
    f = open("units.csv")
    units = []
    while True:
        line = f.readline()
        if line == "":
            break
        line = line.split(",")
        units.append((int(line[0].strip()), int(line[1].strip())))
    f.close()
    return units

def parse_one_record(line):
    """Take a line from reservations.csv and return a dictionary representing that record. (hint: use the datetime type when parsing the start and end date columns)"""
    tokens = line.split(",")
    return {"unit_id":int(tokens[0]), "start_date": (tokens[1].strip()), "end_date": tokens[2].strip()}

def read_existing_reservations():
    """Reads in the file reservations.csv and returns a list of reservations."""
    f = open("reservations.csv")
    reservations = []
    while True:
        line = f.readline()
        if line == "":
            break
        reservations.append(parse_one_record(line))
    return reservations

def make_date(d):
    m_date = time.strptime(d, "%m/%d/%Y")
    date = datetime.date(m_date[0], m_date[1], m_date[2])
    return date

def find_end_date(start_date, stay_length):
    start = time.strptime(start_date, "%m/%d/%Y")
    date = datetime.date(start[0], start[1], start[2])
    delta = datetime.timedelta(days = stay_length)
    return (date + delta)

def find_stay_length(start_date, end_date):
    start = time.strptime(start_date, "%m/%d/%Y")
    str_date = datetime.date(start[0], start[1], start[2])
    end = time.strptime(end_date, "%m/%d/%y")
    end_date = datetime.date(end[0], end[1], end[2])
    return (end_date - str_date)

def available(units, reservations, start_date, occupants, stay_length):
    for unit in units:
        if unit[1] >= occupants:
            if if_available(unit[0], start_date, stay_length, reservations):
                print "Unit %s (Size %s) is available" % (unit[0], unit[1])

def make_list(start_date, stay_length):
    l = []
    count = 0
    for i in range(stay_length):
        add_day = datetime.timedelta(days = count)
        l.append(start_date + add_day)
        count += 1
    return l

def if_available(unit_id, start_date, stay_length, reservations):
    user_days = make_list(make_date(start_date), stay_length)
    for unit in reservations:
        if unit["unit_id"] == unit_id:
            reserv_start = make_date(unit["start_date"])
            reserv_end = make_date(unit["end_date"])
            length = reserv_end - reserv_start
            res_days = make_list(reserv_start, (length.days + 1))
            for x in range(len(res_days)):
                for y in range(len(user_days)):
                    if res_days[x] == user_days[y]:
                        print res_days[x], user_days[y]
                        if (x == (len(res_days) - 1) and y == 0) or (x == 0 and y == (len(user_days) - 1)):
                            print "Unit %d is available during the evening." % unit_id    
                        else:
                            return False
    return True

def reserve(units, reservations, unit_id, start_date, stay_length):
    possible_units = []
    for unit in units:
        possible_units.append(unit[0])
        if unit[0] == unit_id:
            if if_available(unit_id, start_date, stay_length, reservations):
                end_date = find_end_date(start_date, stay_length)
                end = "%d/%d/%d" % (end_date.month, end_date.day, end_date.year)
                night = "night"
                if stay_length > 1:
                    night += "s"
                print "Successfully reserved Unit %s for %s %s." % (unit_id, stay_length, night)
                f = open("reservations.csv", "a")
                f.write("\n%s, %s, %s" % (unit_id, start_date, end))
                f.close()
            else:
                print "Unit %s is unavailable during this time." %unit_id
    if unit_id not in possible_units:
        print "This is not a valid unit choice."

def main():
    while True:
        command = raw_input("SeaBnb> ")
        cmd = command.split()

        units = read_units()
        reservations = read_existing_reservations() 

        if cmd[0] == "available":
            available(units, reservations, cmd[1], int(cmd[2]), int(cmd[3]))
        elif cmd[0] == "reserve":
            reserve(units, reservations, int(cmd[1]), cmd[2], int(cmd[3]))
        elif cmd[0] == "quit":
            sys.exit(0)
        else:
            print "Unknown command"

if __name__ == "__main__":
    main()