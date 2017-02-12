from models.Droplet import Droplet


class DropletParser:
    def __init__(self):
        pass

    def __create_droplet(self, droplet_obj):
        return Droplet(droplet_obj.get('name'), droplet_obj.get('status'), droplet_obj.get('memory'))

    def parse(self, droplets):
        return [self.__create_droplet(droplet) for droplet in droplets]
