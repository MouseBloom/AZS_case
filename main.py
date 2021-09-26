# Developers: Marinkin O. (65%),
# Seledtsov A. (40%),
# Evdischenko M. (40%)
import random as rand
import math
import datetime as dt


gas_info = open('azs.txt', 'r', encoding='utf-8')
clients_info = open('input.txt', 'r', encoding='utf-8')
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

        def add_client(self, clients, ex_time):
            if len(self.clients)==0:
                self.clients.append(clients)
            else:
                self.clients.append(self.clients[-1] + ex_time)



        def gas_check(self, x):
            l = []
            for i in station._registry:
                if x in i.gas:
                     l.append(i)
            return l

        def check_place(self):
            if self.line < self.limit:
                return self
            else:
                None

        def clear_space(self, time):
            '''

            :param self: class station
            :param time: time now
            :return: returns nothing, just clear 'clients' attribute
            '''

            for obj in station._registry:
                for i in obj.clients:
                    if i < time:
                        print(f'{i} client left {obj.num}')
                        obj.clients.remove(i)
                        obj.line -= 1

    def min_line(x):
        '''

        :param x: list of objects
        :return: object with the minimal queue or 'No free space'
        '''
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
        '''

        :param x: txt file with azs info
        :purpose: fills class 'station' with objects
        '''
        for line in x.readlines():
            line = line.strip().split()
            station(f'station {line[0]}', int(line[1]), line[2:])

    def main(file, azs):
        fill_class(azs)
        for obj in station._registry:
            print(f'{obj.num}, max queue {obj.limit}, gas types:', end=' ')
            print(*obj.gas)
        print('')
        count = 0
        gas_price = {'АИ-80': 97.10, 'АИ-92': 45.03, 'АИ-95': 48.86, 'АИ-98': 56.16}  # gas price in rub, info from mimobaka.ru
        gas_sold = {'АИ-80': 0, 'АИ-92': 0, 'АИ-95': 0, 'АИ-98': 0}
        clients_missed = 0
        for line in file:
            #print()
            line = line.strip().split()
            h_m = line[0].split(':')
            gas_type = line[2]
            time_now = dt.timedelta(hours= int(h_m[0]), minutes = int(h_m[1]))
            amount = int(line[1])

            if amount <= 10:
                minut = int(h_m[1]) + math.ceil(amount/10) + rand.randint(0, 1)
            else:
                minut = int(h_m[1]) + math.ceil(amount / 10) + rand.randint(-1, 1)
            cl_time = dt.timedelta(hours = int(h_m[0]), minutes = minut )
            if amount <= 10:
                minut =  math.ceil(amount/10) + rand.randint(0, 1)
            else:
                minut = math.ceil(amount / 10) + rand.randint(-1, 1)
            minut = dt.timedelta(hours = 0, minutes= minut)
            station.clear_space(station, time_now)
            app_stations = station.gas_check(station, gas_type)
            new_cl = (min_line(app_stations))
            if type(new_cl) != str:
                station.add_client(new_cl, cl_time, minut)
                new_cl.line += 1
                print(f'{time_now} new client, {gas_type} {amount} in queue at {new_cl.num} ')
                gas_sold[gas_type] += amount
            else:
                print(f'New client {time_now} {gas_type} {amount} wasn`t able to stand in queue and left')
                clients_missed += 1
            for obj in station._registry:
                print(obj.num, 'queue', len(obj.clients))

        money_erned = 0
        for i in gas_sold.items():
            money_erned += gas_price[i[0]] * i[1]

        return gas_sold,money_erned, clients_missed
    a, b, c = main(clients_info, gas_info)
    #print('')
    for i, j in a.items():
        print(f'Sold {j} liters of {i}')
    print(f'Money erned {round(b, 2)}руб')
    print('Clients missed', c)

finally:
    gas_info.close()
    clients_info.close()
