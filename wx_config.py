fn_config = 'config.txt'

def get_station_id():
    f = open(fn_config, 'r')
    lines = [x.split('\n') for x in f.readlines()]
    station_id = lines[1][0].split('\t')[0]
    return(station_id[1:])

def get_station_id_4code():
    f = open(fn_config, 'r')
    lines = [x.split('\n') for x in f.readlines()]
    station_id = lines[1][0].split('\t')[0]
    return(station_id)

def get_state_id():
    f = open(fn_config, 'r')
    lines = [x.split('\n') for x in f.readlines()]
    state_id = lines[0][0].split('\t')[0]
    return(state_id)



