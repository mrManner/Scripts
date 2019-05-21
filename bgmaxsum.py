# Sums up the transactions in a Bankgiroinbetalning transaction file

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("bgfile", help="File from Bankgirot")
args = parser.parse_args()

with open(args.bgfile, 'r') as f:
    l = f.readline()
    sum = 0
    i = 0
    while l:
        if l[:2] == "20":
            i+=1
            sum += int(l[38:55])
        l = f.readline()
    print("Sum: %d Transactions: %d" % (sum, i))