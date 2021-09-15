import random as rand
import sys
import datetime as dt
import math
gas_info = open('azs.txt', 'r')
clients_info = open('input.txt', 'r')
try:
    class station(object):
        _registry = []

        def __init__(self, num, limit, gas, line = 0, clients = []):
            self._registry.append(self)
            self.num = num
            self.limit = int(limit)
            self.gas = gas
            self.line = int(line)
            self.clients = []

        def add_client(self, clients):

            self.clients.append(clients)

        def gas_check(self, x):
            l = []
            for i in station._registry:
                if x in i.gas:
                    #print(i.num)
                    l.append(i)
            #print(l)
            return l

        def check_place(self):
            if self.line < self.limit:
                return self
            else:
                None

        def clear_space(self, time):

            for obj in station._registry:
                for i in obj.clients:
                    if i < time:
                        print(f'{i} client left {obj.num}')
                        obj.clients.remove(i)
                        obj.line -= 1




    def min_line(x, time):
        l = []
        for obj in x:

            y = obj.check_place()
            if y != None:
                l.append(y)
        if len(l)>0:
            while len(l) > 1:
                if l[0].line < l[1].line:
                    l.pop(1)
                elif l[0].line > l[1].line:
                    l.pop(0)
                else:
                    r = rand.randint(0, 1)
                    l.pop(r)
            return l[0]
        else:
            return 'No space'
    def fill_class(x):
        for line in x.readlines():
            line = line.strip().split()
            line = station(f'station {line[0]}', int(line[1]), line[2:])

    '''line = gas_info.readline().split()
    st1 = station("station 1", int(line[1]), line[2:] )
    line = gas_info.readline().split()
    st2 = station("station 2", int(line[1]), line[2:])
    line = gas_info.readline().split()
    st3 = station("station 3", int(line[1]), line[2:])'''

    def main(file, azs):
        fill_class(azs)
        for obj in station._registry:
            print(f'{obj.num}, max queue {obj.limit}, gas types:', end=' ')
            print(*obj.gas)
        count = 0
        gas_price = {'АИ-80': 97.10, 'АИ-92': 45.03, 'АИ-95': 48.86, 'АИ-98': 56.16}  #info from mimobaka.ru
        gas_sold = {'АИ-80': 0, 'АИ-92': 0, 'АИ-95': 0, 'АИ-98': 0}
        clients_missed = 0
        for line in file:
            line = line.strip().split()
            h_m = line[0].split(':')
            gas_type = line[2]
            time_now = dt.timedelta(hours= int(h_m[0]), minutes = int(h_m[1]))
            amount = int(line[1])
            if amount < 15:
                minut = int(h_m[1]) + round(amount/10) + rand.randint(0, 1)
            else:
                minut = int(h_m[1]) + round(amount / 10) + rand.randint(-1, 1)
            cl_time = dt.timedelta(hours = int(h_m[0]), minutes = minut )
            #print(cl_time)
            station.clear_space(station, time_now)
            #print(gas_type)
            app_stations = station.gas_check(station, gas_type)
            new_cl = (min_line(app_stations, time_now))
            #print(new_cl)
            if type(new_cl) != str:
                station.add_client(new_cl, cl_time)
                new_cl.line += 1
                print(f'{time_now} new client, {gas_type} {amount} in line at {new_cl.num} ')
                gas_sold[gas_type] += amount
                #print(new_cl.num, end='  ')
                #print(new_cl.line)
            else:
                #print('No space')
                clients_missed += 1
        money_erned = 0

        for i in gas_sold.items():
            money_erned += gas_price[i[0]] * i[1]
        return gas_sold,money_erned, clients_missed
    a, b, c = main(clients_info, gas_info)
    for i, j in a.items():
        print(f'sold {j} liters of {i}')
    print(f'заработано {b}руб')
    print('Упущено клиентов', c)

finally:
    gas_info.close()
    clients_info.close()