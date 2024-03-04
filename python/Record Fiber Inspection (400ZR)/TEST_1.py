import csv

csv_path = '\\\\fbn-fs-bu5\\acacia$\\Test Module\\Utility for FIR Program\\HW_PN_Mixing_400ZR_FCAL.csv'

data = []

with open(csv_path, 'r') as f:
    for row in csv.reader(f):
        data.append(row)

print(data)

# with open(csv_path, 'a', newline='') as f:
#     csv.writer(f).writerow(['a','b','c'])
