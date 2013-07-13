def apply_script(protocol, connection, config):
    class AutoReloadingConnection(connection):
        def on_shoot_set(self, fire):
            if not fire and self.weapon_object.current_ammo <= 0 and self.weapon_object.current_stock > 0:
                self.send_chat('Reloading...')
                self.weapon_object.reload()
            connection.on_shoot_set(self, fire)
    
    return protocol, AutoReloadingConnection