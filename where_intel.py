import commands

X_COORDS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
Y_COORDS = ['1', '2', '3', '4', '5', '6', '7', '8']

MAP_SQUARE_SIZE = 64

def getSquareByCoordinates(coords):
    x, y, z = coords
    return X_COORDS[int(x / MAP_SQUARE_SIZE)] + Y_COORDS[int(y / MAP_SQUARE_SIZE)]

@commands.alias('w')
def whereintel(connection):
    enemy_flag = connection.team.other.flag
    player_with_flag = enemy_flag.player
    if player_with_flag is None:
        connection.send_chat("%s intel isn't hold by somebody. It is in %s" % (connection.team.other.name, getSquareByCoordinates((enemy_flag.x, enemy_flag.y, enemy_flag.z))))
    else:
        connection.send_chat("%s intel is hold by %s in %s" % (connection.team.other.name, player_with_flag.name, getSquareByCoordinates(player_with_flag.get_location())))
commands.add(whereintel)

def apply_script(protocol, connection, config):
    return protocol, connection