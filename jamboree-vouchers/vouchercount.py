import csv
import datetime
from dateutil.parser import parse


def get_groups():
    with open('vouchers_bestallda.csv','r') as groupfile:
        groups = {}
        reader = csv.reader(groupfile)
        for row in reader:
            groups[row[0]] = {'voucher_short' : row[2], 
                              'voucher_full' : row[3],
                              'whole_deregistered': 0,
                              'whole_period1' : 0,
                              'whole_period2' : 0,
                              'short_period1': 0,
                              'short_period2': 0,
                              'short_deregistered': 0,
                              'whole_credit': 0,
                              'short_credit': 0,
                              }
        return groups

def count_individuals(groups):
    with open('registrations.csv', 'r') as individualfile:
        reader = csv.reader(individualfile)

        for row in reader:
            group = row[0]
            registered = parse(row[2])
            if row[3] is not '-':
                deregistered = parse(row[3])
            else:
                deregistered = False
            participation = row[4]
            if (registered <= datetime.datetime(2017,02,07)):
                if not deregistered:
                    if participation == 'hela':
                        groups[group]['whole_period1'] = int(groups[group]['whole_period1'])+1
                    elif participation == 'kort':
                        groups[group]['short_period1'] = int(groups[group]['short_period1'])+1
                elif (deregistered > datetime.datetime(2017, 02, 07)):
                    if participation == 'hela':
                        groups[group]['whole_deregistered'] = int(groups[group]['whole_deregistered'])+1
                    elif participation == 'kort':
                        groups[group]['short_deregistered'] = int(groups[group]['short_deregistered'])+1

            if (registered > datetime.datetime(2017,02,07)):
                if not deregistered:
                    if participation == 'hela': 
                        groups[group]['whole_period2']= int(groups[group]['whole_period2'])+1
                    elif participation == 'kort':
                        groups[group]['short_period2'] = int(groups[group]['short_period2'])+1
                    elif participation == 'helvoucher':
                        groups[group]['voucher_full'] = int(groups[group]['voucher_full'])-1
                    elif participation == 'kortvoucher':
                        groups[group]['voucher_short'] = int(groups[group]['voucher_short'])-1
    return groups

def fix_groups(groups):
    ret=[]
    for group_number,group in groups.iteritems():
        # Deregistrations should qualify for a reregistration
        whole_net_deregistration = int(group['whole_deregistered']) - int(group['whole_period2'])
        if whole_net_deregistration > 0:
            whole_deregistration_voucher = whole_net_deregistration
            whole_deregistration_credit = int(group['whole_period2'])
        else:
            whole_deregistration_voucher = 0
            whole_deregistration_credit = int(group['whole_deregistered'])
        short_net_deregistration = int(group['short_deregistered']) - int(group['short_period2'])
        if short_net_deregistration > 0:
            short_deregistration_voucher = short_net_deregistration
            short_deregistration_credit = int(group['short_period2'])
        else:
            short_deregistration_voucher = 0
            short_deregistration_credit = int(group['short_deregistered'])
        
        


        ret = [({'group_number': group_number,
                      'whole_1': group['whole_period1'],
                      'whole_2': group['whole_period2'],
                      'whole_deregistered': group['whole_deregistered'],
                      'short_1': group['short_period1'],
                      'short_2': group['short_period2'],
                      'short_deregistered': group['short_deregistered'],
                      'short_voucher': int(group['voucher_short']) + short_deregistration_voucher,
                      'whole_voucher': int(group['voucher_full']) + whole_deregistration_voucher,
                      'whole_credit': whole_deregistration_credit,
                      'short_credit': short_deregistration_credit
                     })] + ret
    return ret

groups = get_groups()
groups = count_individuals(groups)

with open('outfile.csv', 'wb') as outfile:
    fieldnames = ['group_number',
                      'whole_1',
                      'whole_2',
                      'whole_deregistered',
                      'short_1',
                      'short_2',
                      'short_deregistered',
                      'short_voucher',
                      'whole_voucher',
                      'whole_credit',
                      'short_credit']

    writer = csv.DictWriter(outfile, fieldnames)
    rows = fix_groups(groups)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
