import json
from myos.tools import run
from myos.cloud import Cloud


class Project:
    def __init__(self, project_id=None, name=None, cloud=Cloud()):
        self._id = None
        self._name = None
        if project_id:
            self._id = project_id
        if name:
            self._name = name
        self._cloud = cloud
        self._data_d = {}

    def _get_data(self):
        if self._name:
            cmd = f'openstack --os-cloud {self._cloud.cloud} project show "{self._name}" -f json'
        else:
            cmd = f'openstack --os-cloud {self._cloud.cloud} project show {self._id} -f json'
        results = run(cmd)
        self._data_d = json.loads(results.out)

    @property
    def name(self):
        """
        returns the name associated to this Project
        """
        if not self._name:
            self._get_data()
            return self._data_d['name']
        else:
            return self._name

    @property
    def id(self):
        """
        returns the ID associated to this Project
        """
        if not self._id:
            self._get_data()
            return self._data_d['id']
        else:
            return self._id

    @property
    def parent(self):
        """
        returns the parent Project associated to this Project
        """
        if not self._id:
            self._get_data()
        parent_id = self._data_d['parent_id']
        if parent_id == None:
            return None
        else:
            return Project(project_id=parent_id)

    @property
    def tags(self):
        """
        returns the tags associated to this Project
        output is a list of strings
        """
        if not self._id:
            self._get_data()
        return self._data_d['tags']

    @property
    def servers(self):
        """
        get the list of Servers currently running on this Project
       
        $ openstack --os-cloud admin server list --project ncas-force-U
        +--------------------------------------+-----------------------------------+--------+-------------------------------+-------+----------+----------------------------------+
        | ID                                   | Name                              | Status | Networks                      | Image | Flavor   | Project ID                       |
        +--------------------------------------+-----------------------------------+--------+-------------------------------+-------+----------+----------------------------------+
        | 99333158-356a-41a5-9c64-84f9e8e881f9 | force-staging-control-plane-fb4sb | ACTIVE | portal-internal=192.168.3.77  |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | 3e447537-b525-4792-a277-e274963b02a2 | force-staging-control-plane-c5xnn | ACTIVE | portal-internal=192.168.3.254 |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | dd928a49-ac65-484c-95af-14bafc67404e | force-staging-staging-pljbm-fv7k9 | ACTIVE | portal-internal=192.168.3.58  |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | 28a58a54-9ffe-490c-8a37-ad331d6055c7 | force-staging-staging-pljbm-lhndq | ACTIVE | portal-internal=192.168.3.60  |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | fb231de3-2eee-4411-8cd6-8a404cf9476c | force-staging-staging-pljbm-rnxr9 | ACTIVE | portal-internal=192.168.3.180 |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | 27d111dc-1e2d-41b7-a19c-01ef0713c8c4 | force-staging-control-plane-kfcql | ACTIVE | portal-internal=192.168.3.26  |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | 2738bd95-50e0-40b1-80bc-5551a285507d | force-live-control-plane-mm5xz    | ACTIVE | portal-internal=192.168.3.43  |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | e5dfbdc1-e993-4138-80b1-bb73e9d5b3f4 | force-live-control-plane-pszdt    | ACTIVE | portal-internal=192.168.3.242 |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | e83b9437-1abd-4adb-a98b-43669594b187 | force-live-live-8wptz-dmfbh       | ACTIVE | portal-internal=192.168.3.84  |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | 5a915b61-2402-4463-9819-294c0a6d44e3 | force-live-live-8wptz-7qqr4       | ACTIVE | portal-internal=192.168.3.192 |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | f21978e5-99a5-4456-a6e7-219ec6410f96 | force-live-live-8wptz-2gbqp       | ACTIVE | portal-internal=192.168.3.63  |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | 23c7d1b6-ff4c-405b-b71c-42060ab22312 | force-live-control-plane-bk6dl    | ACTIVE | portal-internal=192.168.3.231 |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        +--------------------------------------+-----------------------------------+--------+-------------------------------+-------+----------+----------------------------------+

        $ openstack --os-cloud {self._cloud.cloud} server list --project Condor --format json
        [
          {
            "ID": "e2951a59-e290-430f-8f12-1fa4168c3024",
            "Name": "vwn-gpu-2025-12-17-07-17-16-0",
            "Status": "SHUTOFF",
            "Networks": {
              "Internal": [
                "172.16.112.122"
              ]
            },
            "Image": "rocky-8-aqml",
            "Flavor": "g-a100-80gb-2022.x1",
            "Project ID": "2d8252b430c2405da24d74df2004c24b"
          },
          ...
          ...
        """
        from myos.server import Server
        cmd = f'openstack --os-cloud {self._cloud.cloud} server list --project {self.name} --format json'
        results = run(cmd)
        servers_l = json.loads(results.out)
        out = []
        for server in servers_l:
            server_id = server["ID"]
            out.append(Server(server_id=server_id))
        return out

    @property
    def users(self):
        """
        returns the list of Users with access to this Project

        $ openstack --os-cloud admin role assignment list --project Condor  --names --format json
        [
          {
            "Role": "user",
            "User": "mfh49987@stfc",
            "Group": "",
            "Project": "Condor@default",
            "Domain": "",
            "System": "",
            "Inherited": false
          },
          ...
          ...
        ]
        """
        from myos.user import User
        cmd = f'openstack --os-cloud {self._cloud.cloud} role assignment list --project {self.name} --names --format json'
        results = run(cmd)
        users_l = json.loads(results.out)
        out = []
        for user in users_l:
            user_name = user['User']
            out.append(User(name=user_name))
        return out
       
    @property
    def fips(self):
        """
        returns the list of Floating IPs in this Project

        $ openstack --os-cloud admin floating ip list --project lsst-drp --format json
        [
          {
            "ID": "3b90998e-ab39-45b4-b56e-120e00d31fdb",
            "Floating IP Address": "130.246.83.113",
            "Fixed IP Address": null,
            "Port": null,
            "Floating Network": "5283f642-8bd8-48b6-8608-fa3006ff4539",
            "Project": "22547d0eef6445ff9febfedec9b4da4a"
          }
        ]        
        """
        from myos.ip import FloatingIP
        cmd = f'openstack --os-cloud {self._cloud.cloud} floating ip list --project {self.name} --format json'
        results = run(cmd)
        fip_l = json.loads(results.out)
        out = []
        for fip in fip_l:
            fip_id = fip['ID']
            out.append(FloatingIP(fip_id=fip_id))
        return out


    ####################################
    # BEGIN TEST 
    ####################################

    def add(self, entity):
        from myos.user import User
        if type(entity) is User:
            self._add_user(entity)

    def _add_user(self, user):
        # example: 
        #    openstack role add user 
        #    --user 69669657eb53642a96b6a03cf27fb47b9fef0f863da0e5ca285c724c91c50e47 
        #    --project f2ae44b03b3742d0808c6197b76b0e5e 
        #    --user-domain stfc
        cmd = f'openstack --os-cloud {self._cloud.cloud} role add user --user {user.id} --project {self.name} --user-domain {user.domain.name}'
        results = run(cmd)

    ####################################
    # END TEST 
    ####################################



if __name__ == '__main__':
    p = Project(name="lsst-drp")
    print(p.name)
    print(p.id)
    #ss = p.servers
    #for s in ss:
    #    print(s.id)
    #    print(s.name)
    #uu = p.users
    #for u in uu:
    #    print(u.name)
    fips = p.fips
    print(fips[0].ip)

