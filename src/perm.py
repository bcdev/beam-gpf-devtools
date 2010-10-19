
class NestedFor:
    def get_dim_sizes(self, list_of_lists):
        dim_sizes = []
        for i in range(len(list_of_lists)):
            dim_sizes.append(len(list_of_lists[i]))
        return dim_sizes

    def do_element(self, indexes):
        pass

    def loop(self, dim_sizes):
        indexes = []
        for i in range(len(dim_sizes)):
            indexes.append(0)

        loop_index = len(dim_sizes) - 1
        while loop_index >= 0:
            self.do_element(indexes)
            for i in reversed(range(len(dim_sizes))):
                indexes[i] += 1
                if indexes[i] < dim_sizes[i]:
                    break
                else:
                    indexes[i] = 0
                    if i == loop_index:
                        loop_index -= 1
                        if loop_index < 0:
                            break