from pyspades.collision import vector_collision

def apply_script(protocol, connection, config):
    class EnemyBaseHealConnection(connection):
        def on_position_update(self):
            if vector_collision(self.world_object.position, self.team.other.base):
                self.refill()
            return connection.on_position_update(self)
    
    return protocol, EnemyBaseHealConnection