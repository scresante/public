#!/usr/bin/python
"""x """

from sys import argv
from datetime import datetime as dd, timedelta
import os
import json
import requests
import bs4
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# from matplotlib.ticker import (MultipleLocator, FuncFormatter)
# import ipdb

req = requests.get('http://192.168.1.254/cgi-bin/broadbandstatistics.ha')
soup = bs4.BeautifulSoup(req.content, features="lxml")

# class Modem():
    # """ provide a cleaner interface to get modem datapoints """
    # def __init__(self):
        # pass

# class Log():
    # """ better interface for logfiles """
    # def __init__(self, timestamp):
        # pass

qf = lambda x: dd.strftime(x, '%c')

def first_log(write=False):
    """ for now, give us what filename should be at 0, based on time since reboot """
    sysinforeq = requests.get('http://192.168.1.254/cgi-bin/sysinfo.ha')
    syssoup = bs4.BeautifulSoup(sysinforeq.content, features="lxml")
    last_reboot = syssoup.find('th', string="Time Since Last Reboot").parent()[1].text
    last_reboot = [int(_) for _ in last_reboot.split(':')]
    d, h, m, s = last_reboot
    td = timedelta(days=d, hours=h, minutes=m, seconds=s)
    last_reboot = dd.now() - td
    print(f'{qf(last_reboot)=}')
    last_reboot_name = dd.strftime(last_reboot, "%y.%m.%d.%H.%M.%S")
    if write:
        data = add_fields(get_data())
        for k in data:
            data[k] = 0
        data['timestamp'] = int(dd.timestamp(last_reboot))
        with open(last_reboot_name, 'w') as fd:
            print(f'writing {last_reboot_name} with {data}')
            fd.write(json.dumps(data))
    return last_reboot

def get_data():
    """ return """
    data = {}
    for datapoint in soup.find(summary="Ethernet IPv4 Statistics Table").find_all('th'):
        label = datapoint.text
        value = int(datapoint.find_next_sibling().text)
        data[label] = value
    return data

def add_fields(data):
    """ add timestamp and total """
    data['timestamp'] = int(dd.timestamp(dd.now()))
    data['total'] = data['Transmit Bytes'] + data['Receive Bytes']
    return data

def print_stats():
    """ print """
    print(f"Data Usage Report for {dd.strftime(dd.now(), '%c')}")
    data = add_fields(get_data())
    # for datapoint in soup.find(summary="Ethernet IPv4 Statistics Table").find_all('th'):
    for key in data:
        if key == 'timestamp':
            continue
        label = key
        value = int(data[key])
        suffix = ''
        if value > 10**12:
            value = value / 10**12
            suffix = ' T'
        elif value > 10**9:
            value = value / 10**9
            suffix = ' G'
        elif value > 10**6:
            value = value / 10**6
            suffix = ' M'
        elif value > 10**3:
            value = value / 10**3
            suffix = ' K'
        label += ':'
        if suffix:
            nf = str(round(value, 2)) + suffix
            print(f'{label:<19s} {nf:<10}')
        else:
            print(f'{label:<19s} {value:<10}')

def log_stats():
    """ log """
    os.chdir('/var/log/modem')
    latest_file = sorted(os.listdir('.'))[-1]
    fname = dd.strftime(dd.now(), "%y.%m.%d.%H.%M.%S")

    data = add_fields(get_data())
    with open(latest_file, 'r') as fd:
        last_data = json.loads(fd.read())
    if last_data != data:
        with open(fname, 'w') as fd:
            fd.write(json.dumps(data))

def add_fields_to_previous():
    """ add new fields to all previous data TODO:make better """
    os.chdir('/var/log/modem')
    def check_add(fname):
        with open(fname) as fd:
            data = json.loads(fd.read())
        # if 'timestamp' not in data.keys():
            # timestamp = dd.timestamp(dd.strptime(fname, "%y.%m.%d.%H.%M.%S"))
            # data['timestamp'] = timestamp
            # # print(f'added {data["timestamp"]=} to {fname}')
        # if 'total' not in data.keys():
            # data['total'] = data['Transmit Bytes'] + data['Receive Bytes']
            # # print(f'added {data["total"]=} to {fname}')
        return data
    for fname in sorted(os.listdir('.')):
        data = check_add(fname)
        with open(fname, 'w') as fd:
            print(f'modifying {fname}')
            fd.write(json.dumps(data))

def plot_usage():
    """."""
    fmt_ts = lambda x: dd.strftime(x, "%m-%d %H:%M")
    print('plot_usage()')
    os.chdir('/var/log/modem')
    x, y = [], []
    for fname in sorted(os.listdir('.')):
        with open(fname) as fd:
            data = json.loads(fd.read())
            x.append(dd.fromtimestamp(data['timestamp']))
            y.append(data['total'] / 10**9)
    start, end = fmt_ts(x[0]), fmt_ts(x[-1])
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title(f'Bandwidth usage for {start} - {end}')
    plt.xlabel('date')
    plt.ylabel('Total (GB)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    # its easier to just have GB data to plot to begin with...
    ax.format_ydata = lambda x: '%.2fGB' % x
    fig.autofmt_xdate()
    plt.show(block=True)

if __name__ == "__main__":
    if len(argv) > 1:
        if argv[1] == '-l':
            log_stats()
        # if argv[1] == '-f':
            # add_fields_to_previous()
        if argv[1] == '-0':
            first_log(write=True)
        if argv[1] == '-plot':
            plot_usage()
    else:
        print_stats()
        # plot_usage()
