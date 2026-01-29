class UserList(list):

    def filter(self, filter_lamba):
        filtered = filter(filter_lamba, self.__iter__())
        filtered = list(filtered)
        self[:] = filtered

