import csv

filename = 'ortop.csv'
brand = 'benarti'

size_list_190 = ['70 X 190','80 X 190','90 X 190','120 X 190','140 X 190','160 X 190','180 X 190','200 X 190']
size_list_195 = ['70 X 195','80 X 195','90 X 195','120 X 195','140 X 195','160 X 195','180 X 195','200 X 195']
size_list = ['70 X 200','80 X 200','90 X 200','120 X 200','140 X 200','160 X 200','180 X 200','200 X 200',
             'D200','D210','D220']

filename_write = filename.split('.')[0] + '_ready.csv'
art_sym = 'PY' + brand.upper() + filename.split('.')[0].upper()


def get_price_list():
    lst = []
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            lst.append(row)
        return lst


i = 1
price = 0
art_num = 1
cnt = 0
line = ''

lst = get_price_list()
with open(filename_write, 'w', encoding='utf-8') as f:
    for row in lst:
        i = 1
        line = row[0].rstrip()
        line += ','
        line += art_sym + str(art_num)
        line += ','
        line += size_list_190[0]
        line += ','
        line += ','
        line += ''.join((filter(lambda x: x.isdigit(), row[5])))
        line += ','
        line += ','
        line += ','
        line += ''.join((filter(lambda x: x.isdigit(), row[4].split('/', maxsplit=1)[0])))
        line += ','
        line += ''.join((filter(lambda x: x.isdigit(), row[4].split('/', maxsplit=1)[1])))
        line += ','
        line += '100'
        line += '\n'
        # size 190 #
        i = 1
        while i < len(size_list_190):
            if i == 1:
                j = 6
            line += ','
            line += ','
            line += size_list_190[i]
            line += ','
            line += ','
            line += ''.join((filter(lambda x: x.isdigit(), row[j])))
            line += ','
            line += ','
            line += ','
            line += ','
            line += ','
            line += '100'
            line += '\n'
            j += 1
            i += 1
            # size 195 #
        i = 0
        while i < len(size_list_195):
            if i == 0:
                j = 5
            line += ','
            line += ','
            line += size_list_195[i]
            line += ','
            line += ','
            line += ''.join((filter(lambda x: x.isdigit(), row[j])))
            line += ','
            line += ','
            line += ','
            line += ','
            line += ','
            line += '100'
            line += '\n'
            j += 1
            i += 1
            # size 200 #
        i = 0
        while i < len(size_list):
            if i == 0:
                j = 5
            line += ','
            line += ','
            line += size_list[i]
            line += ','
            line += ','
            line += ''.join((filter(lambda x: x.isdigit(), row[j])))
            line += ','
            line += ','
            line += ','
            line += ','
            line += ','
            line += '100'
            line += '\n'
            j += 1
            i += 1
        f.write(line)
        art_num += 1
        cnt += 1

