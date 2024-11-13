from random import randint

id_list = []


def find_last_id(id_list):
    try:
        return max(id_list)
    except ValueError:
        return False


# print(find_last_id(id_list))


# class Graph_list:
#     def __init__(self) -> None:
#         pass


class Graph:
    def __init__(self, data, connections):
        last_id = find_last_id(id_list)
        if last_id:
            self.id = last_id
        else:
            self.id = 0

        id_list.append(self.id)
        self.data = data
        self.connections = connections

    def find_random_next(self):
        return randint(0, max(self.connections))

    def cycle_random_points(self, n, start_point):
        for i in range(n):
            next_point = start_point.find_random_next()
            print(next_point)


graph_list = []
A0 = Graph("1a", [0, 1, 2])
A1 = Graph("2a", [0, 1, 2])
A2 = Graph("3z", [0, 1, 2])
A3 = Graph("4a", [0, 1, 2])
graph_list = [A0, A1, A2, A3]
graph_list.append(A0)
graph_list.append(A1)
graph_list.append(A2)
graph_list.append(A3)
print(A0.data, A0.connections)
print(A0.find_random_next())
print(graph_list)
