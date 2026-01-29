class EntityList(list):

    def filter(self, filter_lambda):
        filtered = filter(filter_lambda, self.__iter__())
        filtered = list(filtered)
        self[:] = filtered

    def sort(self, sort_lambda):
        super().sort(key=sort_lambda)

