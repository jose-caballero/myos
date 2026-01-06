import json
from myos.tools import run
from myos.cloud import Cloud

class Hypervisor:
    def __init__(self, hypervisor_id=None, name=None, cloud=Cloud()):
        self._id = None
        self._name = None
        if hypervisor_id:
            self._id = hypervisor_id
        if name:
            self._name = name
        self._cloud = cloud
        self._data_d = {}


    def _get_data(self):
        if self._name:
            cmd = f'openstack --os-cloud {self._cloud.cloud} hypervisor show {self._name} --format json'
        if self._id:
            cmd = f'openstack --os-cloud {self._cloud.cloud} hypervisor show {self._id} --format json'
        results = run(cmd)
        self._data_d = json.loads(results.out)


    @property
    def hostname(self):
        """
        returns the hostname associated to this Hypervisor
        """
        if not self._name:
            self._get_data()
            return self._data_d['hypervisor_hostname']
        else:
            return self._name

    @property
    def name(self):
        """
        returns the hostname associated to this Hypervisor
        name and hostname are the same thing for this class
        """
        return self.hostname

    @property
    def id(self):
        """
        returns the hypervisor_id associated to this Hypervisor
        """
        if not self._id:
            self._get_data()
            return self._data_d['id']
        else:
            return self._id

    @property 
    def status(self):
        """
        returns the status of this Hypervisor
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['status']

    @property 
    def state(self):
        """
        returns the state of this Hypervisor
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['state']

    @property
    def servers(self):
        """
        returns the list of Servers running on this Hypervisor

        $ openstack --os-cloud admin server list --host hv-a100x8-8.nubes.rl.ac.uk --all-projects --format json
        [
          {
            "ID": "79b3b46d-c7d8-47d2-a59d-ce5ded79b63b",
            "Name": "vwn-gpu-2025-12-05-21-03-17-0",
            "Status": "ACTIVE",
            "Networks": {
              "Internal": [
                "172.16.112.77"
              ]
            },
            "Image": "rocky-8-aqml",
            "Flavor": "g-a100-80gb-2022.x1",
            "Project ID": "2d8252b430c2405da24d74df2004c24b"
          },
          ...
          ...
        ]
        """
        from myos.server import Server
        cmd = f'openstack --os-cloud {self._cloud.cloud} server list --host {self.name} --all-projects --format json'
        results = run(cmd)
        servers_l = json.loads(results.out)
        out = []
        for server in servers_l:
            server_id = server['ID']
            out.append(Server(server_id=server_id))
        return out


if __name__ == '__main__':
    hv = Hypervisor(name='hv300.nubes.rl.ac.uk')
    hv = Hypervisor(name='hv-a100x8-8.nubes.rl.ac.uk')
    print(hv.id)
    print(hv.status)
    print(hv.state)
    print(len(hv.servers))
