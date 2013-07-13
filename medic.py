import commands
from pyspades.constants import SPADE_TOOL

@commands.alias('m')
def medic(connection, arg):
    if arg == "on":
        if connection.is_medic:
            connection.send_chat("You're already medic")
        else:
            connection.send_chat("You're medic now")
            connection.protocol.send_chat("%s (%s) is medic now" % (connection.name, connection.team.name))
            connection.is_medic = True
    elif arg == "off":
        if not connection.is_medic:
            connection.send_chat("You're not medic yet")
        else:
            connection.send_chat("You're no longer medic")
            connection.protocol.send_chat("%s (%s) is no longer medic" % (connection.name, connection.team.name))
            connection.is_medic = False
    else:
        connection.send_chat("Invalid argument - use 'on' or 'off' instead")
commands.add(medic)

def apply_script(protocol, connection, config):
    protocol.medic_heal_amount = config.get('medic_heal_amount', 25)

    class MedicConnection(connection):
        def on_login(self, name):
            self.is_medic = False
            connection.on_login(self, name)
	
        def on_hit(self, amount, victim, type, weapon):
            if self.is_medic:
                if self.tool == SPADE_TOOL and self.team == victim.team:
                    prev_hp = victim.hp
                    victim.set_hp(prev_hp + self.protocol.medic_heal_amount)
                    cur_hp = victim.hp
                    delta = cur_hp - prev_hp
                    if delta == 0:
                        self.send_chat("You don't need to heal %s anymore" % victim.name)
                    else:
                        self.send_chat("You've healed %s by %d hp. His current hp is %d" % (victim.name, delta, cur_hp))
                        victim.send_chat("You've been healed by %s for %d hp" % (self.name, delta))
                else:
                    self.send_chat("You can't kill anybody while you're medic")
                    return 0
            return connection.on_hit(self, amount, victim, type, weapon)
			
        def on_block_destroy(self, x, y, z, mode):
            if self.is_medic:
                self.send_chat("You can't destroy blocks while you're medic")
                return False
            return connection.on_block_destroy(self, x, y, z, mode)
            
        def on_position_update(self):
            if self.is_medic:
                x, y, z = self.get_location()
                for player in self.protocol.players.values():
                    xa, ya, za = player.get_location()
                    if self.team == player.team and 5 > xa-x > -5 and 5 > ya-y > -5 and 5 > za-z > -5:
                        if player.hp is None:
                            try:
                                player.spawn_call.cancel()
                            except AlreadyCancelled:
                                print("An error occurred while using function cancel - AlreadyCancelled")
                            except AlreadyCalled:
                                print("An error occurred while using function cancel - AlreadyCalled")
                            player.spawn(player.get_location())
                            pos = (xa, ya, za)
                            player.set_location(pos)
                            self.send_chat("You've revived %s!" % player.name)
                            player.send_chat("You've been revived by %s" % self.name)
            return connection.on_position_update(self)
            
    return protocol, MedicConnection
