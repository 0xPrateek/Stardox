#! /usr/bin/python

black = '\033[30m'
red = '\033[31m'
green = '\033[32m'
orange = '\033[33m'
blue = '\033[34m'
purple = '\033[35m'
cyan = '\033[36m'
lightgrey = '\033[37m'
darkgrey = '\033[90m'
lightred = '\033[91m'
lightgreen = '\033[92m'
white ='\033[1;37m'
yellow = '\033[93m'
lightblue = '\033[94m'
pink = '\033[95m'
lightcyan = '\033[96m'
end = '\x1b[0m'

def error(message):
    message = str(message)
    initial =red + '[-] '
    print(initial + end + message)

def success(message,verbose):
    message = str(message)
    initial = lightgreen+'[+] '
    if verbose:
        print(initial + end + message)

def info(message,verbose):
    message = str(message)
    message = '[!] ' + message
    if verbose:
        print(initial + end + message)

def process(message,verbose):
    message=str(message)
    initial= white + '[~] '
    if verbose:
        print(initial + end + message)
