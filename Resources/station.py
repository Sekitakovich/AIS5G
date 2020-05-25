with open('./station.csv', 'rt', encoding='utf-8') as f:
    all = f.read()
    row = all.split('\n')
    for line in row:
        column = line.split(',')
        print('Location(name=\'%s\', lat=%f, lng=%f),' % (column[0], float(column[1]), float(column[2])))

