def import_map():
    '''imports a text file into an array to be used when generating the matrix'''
    f = open('sugar_map.txt', 'r')
    map_list = []
    for line in f:
        num_list = line.split(' ')
        for num in num_list:
            map_list.append(int(num[0]))

    return map_list

a = import_map()
print a