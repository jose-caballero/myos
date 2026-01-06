import json
from myos.tools import run
from myos.cloud import Cloud

class Server:
    def __init__(self, server_id=None, name=None, cloud=Cloud()):
        self._id = None
        self._name = None
        if server_id:
            self._id = server_id
        if name:
            self._name = name
        self._cloud = cloud
        self._data_d = {}


    def _get_data(self):
        if self._name:
            cmd = f'openstack --os-cloud {self._cloud.cloud} server show {self._name} -f json'
        if self._id:
            cmd = f'openstack --os-cloud {self._cloud.cloud} server show {self._id} -f json'
        results = run(cmd)
        self._data_d = json.loads(results.out)

    @property
    def name(self):
        """
        returns the name associated to this Server
        """
        if not self._name:
            self._get_data()
            return self._data_d['name']
        else:
            return self._name

    @property
    def id(self):
        """
        returns the server_id associated to this Server
        """
        if not self._id:
            self._get_data()
            return self._data_d['id']
        else:
            return self._id

    @property
    def flavor(self):
        """
        returns the Flavor of this Server
        """
        from myos.flavor import Flavor
        if not self._data_d:
            self._get_data()
        flavor_name = self._data_d['flavor']['name']
        return Flavor(name=flavor_name)

    @property
    def image(self):
        """
        returns the Image of this Server
        """
        from myos.image import Image
        if not self._data_d:
            self._get_data()
        image_name = self._data_d['image'].split('(')[0].strip()
        return Image(name=image_name)

    @property
    def user(self):
        """
        returns the User who created this Server
        """
        from myos.user import User
        if not self._data_d:
            self._get_data()
        user_id = self._data_d['user_id']
        return User(user_id=user_id)

    @property
    def hypervisor(self):
        """
        returns the Hypervisor where this Server is running
        """
        from myos.hypervisor import Hypervisor
        if not self._data_d:
            self._get_data()
        hostname = self._data_d['OS-EXT-SRV-ATTR:hypervisor_hostname']
        return Hypervisor(hostname=hostname)




if __name__ == '__main__':
    s = Server(server_id="79b3b46d-c7d8-47d2-a59d-ce5ded79b63b")
    print(s.id)
    print(s.name)
    #print(s.flavor.name)
    #print(s.flavor.id)
    #print(s.image.name)
    #print(s.image.id)
