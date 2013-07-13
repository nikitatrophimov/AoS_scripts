from pyspades.constants import CTF_MODE
from pyspades.collision import vector_collision

def apply_script(protocol, connection, config):
    class CTFImprovedConnection(connection):
        def on_flag_take(self):
            self.team.other.flag.at_start_pos = False
            return connection.on_flag_take(self)
		
        def on_flag_capture(self):
            self.team.other.flag.at_start_pos = True
            self.team.other.flag.start_pos = self.team.other.flag.get()
            return connection.on_flag_capture(self)
		
        def on_flag_drop(self):
            self.protocol.send_chat('%s intel was dropped!' % self.team.other.name)
            connection.on_flag_drop(self)
			
        def on_position_update(self):
            flag = self.team.flag
            if vector_collision(self.world_object.position, flag):
                if not flag.at_start_pos:
                    flag.set(*flag.start_pos)
                    flag.update()
                    flag.at_start_pos = True
                    self.protocol.send_chat('%s intel was returned to the initial position by %s!' % (self.team.name, self.name))
            return connection.on_position_update(self)
	
    class CTFImprovedProtocol(protocol):
        game_mode = CTF_MODE
		
        def __init__(self, *arg, **kw):
            protocol.__init__(self, *arg, **kw)
            for team in self.teams.itervalues():
                if team.spectator:
                    continue
                team.flag.at_start_pos = True
                team.flag.start_pos = team.flag.get()
    
    return CTFImprovedProtocol, CTFImprovedConnection