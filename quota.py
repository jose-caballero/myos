class Quota:
    def __init__(self, data):
        self._data = data
        # self._data is list that looks like this
        #
        # [
        #  {
        #    "Resource": "cores",
        #    "Limit": 10
        #  },
        #  {
        #    "Resource": "instances",
        #    "Limit": 10
        #  },
        #  {
        #    "Resource": "ram",
        #    "Limit": 51200
        #  },
        #  {
        #    "Resource": "fixed_ips",
        #    "Limit": null
        #  },
        #  ...
        #  ...
        #  {
        #    "Resource": "backup-gigabytes",
        #    "Limit": 1000
        #  },
        #  {
        #    "Resource": "per-volume-gigabytes",
        #    "Limit": -1
        #  }
        # ]
        #

    @property
    def cores(self):
        return self._get_value("cores")

    @property
    def instances(self):
        return self._get_value("instances")

    @property
    def ram(self):
        return self._get_value("ram")

    @property
    def fixed_ips(self):
        return self._get_value("fixed_ips")

    @property
    def networks(self):
        return self._get_value("networks")

    @property
    def volumes(self):
        return self._get_value("volumes")

    @property
    def snapshots(self):
        return self._get_value("snapshots")

    @property
    def gigabytes(self):
        return self._get_value("gigabytes")

    @property
    def backups(self):
        return self._get_value("backups")

    @property
    def volumes___DEFAULT__(self):
        return self._get_value("volumes___DEFAULT__")

    @property
    def gigabytes___DEFAULT__(self):
        return self._get_value("gigabytes___DEFAULT__")

    @property
    def snapshots___DEFAULT__(self):
        return self._get_value("snapshots___DEFAULT__")

    @property
    def volumes_rbd(self):
        return self._get_value("volumes_rbd")

    @property
    def gigabytes_rbd(self):
        return self._get_value("gigabytes_rbd")

    @property
    def snapshots_rbd(self):
        return self._get_value("snapshots_rbd")

    @property
    def groups(self):
        return self._get_value("groups")

    @property
    def check_limit(self):
        return self._get_value("check_limit")

    @property
    def health_monitors(self):
        return self._get_value("health_monitors")

    @property
    def listeners(self):
        return self._get_value("listeners")

    @property
    def load_balancers(self):
        return self._get_value("load_balancers")

    @property
    def l7_policies(self):
        return self._get_value("l7_policies")

    @property
    def pools(self):
        return self._get_value("pools")

    @property
    def ports(self):
        return self._get_value("ports")

    @property
    def project_id(self):
        return self._get_value("project_id")

    @property
    def rbac_policies(self):
        return self._get_value("rbac_policies")

    @property
    def routers(self):
        return self._get_value("routers")

    @property
    def subnets(self):
        return self._get_value("subnets")

    @property
    def subnet_pools(self):
        return self._get_value("subnet_pools")

    @property
    def injected_file_size(self):
        return self._get_value("injected-file-size")

    @property
    def injected_path_size(self):
        return self._get_value("iinjected-path-size")

    @property
    def injected_files(self):
        return self._get_value("injected-files")

    @property
    def key_pairs(self):
        return self._get_value("key-pairs")

    @property
    def properties(self):
        return self._get_value("properties")

    @property
    def server_group_members(self):
        return self._get_value("server-group-members")

    @property
    def server_groups(self):
        return self._get_value("server-groups")

    @property
    def floating_ips(self):
        return self._get_value("floating-ips")

    @property
    def secgroup_rules(self):
        return self._get_value("secgroup-rules")

    @property
    def secgroups(self):
        return self._get_value("secgroups")

    @property
    def backup_gigabytes(self):
        return self._get_value("backup-gigabytes")

    @property
    def per_volume_gigabytes(self):
        return self._get_value("per-volume-gigabytes")

    def _get_value(self, variable_name):
        for resource in self._data:
            if resource["Resource"] == variable_name:
                return resource["Limit"]
        else:
            return None

