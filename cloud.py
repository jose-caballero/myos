import json
from myos.tools import run

class Cloud:
    def __init__(self, cloud="admin"):
        self.cloud = cloud

    @property
    def hypervisors(self):
        """
        returns the entire list of Hypervisor objects for this cloud instance
        """
        from myos.hypervisor import Hypervisor
        cmd = f'openstack --os-cloud {self.cloud} hypervisor list --format json'
        results = run(cmd)
        hv_l = json.loads(results.out)
        out = []
        for hv in hv_l:
            hostname = hv['Hypervisor Hostname']
            out.append( Hypervisor(hostname=hostname) )
        return out

    @property
    def flavors(self):
        """
        returns the entire list of Flavor objects for this cloud instance
        """
        from myos.flavor import Flavor
        cmd = f'openstack --os-cloud {self.cloud} flavor list --all --format json'
        results = run(cmd)
        flavor_l = json.loads(results.out)
        out = []
        for flavor in flavor_l:
            flavor_id = flavor['ID']
            out.append( Flavor(flavor_id=flavor_id) )
        return out

    @property
    def images(self):
        """
        returns the entire list of Image objects for this cloud instance
        """
        from myos.image import Image
        cmd = f'openstack --os-cloud {self.cloud} image list --all --format json'
        results = run(cmd)
        image_l = json.loads(results.out)
        out = []
        for image in image_l:
            image_id = image['ID']
            out.append( Image(image_id=image_id) )
        return out
    
    @property
    def projects(self):
        """
        returns the entire list of Project objects for this cloud instance
        """
        from myos.project import Project
        cmd = f'openstack --os-cloud {self.cloud} project list --format json'
        results = run(cmd)
        project_l = json.loads(results.out)
        out = []
        for project in project_l:
            project_id = project['ID']
            out.append( Project(project_id=project_id) )
        return out

    @property
    def fips(self):
        """
        returns the entire list of FloatingIP objects for this cloud instance
        """
        from myos.ip import FloatingIP
        cmd = f'openstack --os-cloud {self.cloud} floating ip list --format json'
        results = run(cmd)
        fip_l = json.loads(results.out)
        out = []
        for fip in fip_l:
            fip_id = fip['ID']
            out.append( FloatingIP(fip_id=fip_id) )
        return out


if __name__ == '__main__':
    cloud = Cloud("admin")
    #hv_l = cloud.hypervisors
    #print(len(hv_l))
    #flavor_l = cloud.flavors
    #print(len(flavor_l))
    #image_l = cloud.images
    #print(len(image_l))
    fip_l = cloud.fips
    print(len(fip_l))

