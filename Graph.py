class Node:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight


class Vertex:
    def __init__(self, name):
        self.name = name
        self.Neighbour = []
        self.visited = 0
        self.cost = 0
        self.heuristic = 0
        self.predecessor = None


class Graph:
    explored = []

    def __init__(self):
        self.ListofVertices = []

    def insertVertex(self, name, hValue=0):
        for i in self.ListofVertices:
            if i.name == name:
                return -1
        v = Vertex(name)
        v.heuristic = hValue
        self.ListofVertices.append(v)
        return 1

    def insertEdge(self, v1, v2, weight=0):
        found2 = False
        x = None
        for i in self.ListofVertices:
            if i.name == v2:
                found2 = True
            if i.name == v1:
                x = i
                for j in i.Neighbour:
                    if j.name == v2:
                        return "Exist"

        if found2 is True and x is not None:
            nodev2 = Node(v2, weight)
            x.Neighbour.append(nodev2)
            return "Done"

        elif found2 is False:
            return "V2 ERR"
        return "V1 ERR"

    def deleteEdge(self, v1, v2):
        for i in self.ListofVertices:
            if i.name == v1:
                for j in i.Neighbour:
                    if j.name == v2:
                        i.Neighbour.remove(j)
                        return "deleted"
                return "edge doesn't exist"
        return "v doesn't exist"

    def deleteVertex(self, v):
        found = False
        x = None
        for i in self.ListofVertices:
            if i.name == v:
                x = i
                found = True
            for j in i.Neighbour:
                if j.name == v:
                    i.Neighbour.remove(j)
        if found:
            self.ListofVertices.remove(x)
            return "Done"
        else:
            return "Vertex Doesn't Exist"

    def DFS(self, start, goal):
        stack = []
        x = self.search(start)
        stack.insert(0, (x.name, None))

        while len(stack) != 0:
            x = self.search(stack[0][0])
            x.predecessor = stack[0][1]
            self.explored.append(x.name)
            x.visited = 1
            stack.pop(0)

            if x.name in goal:
                return self.path(x.name)

            for j in x.Neighbour:
                y = self.search(j.name)
                if y.visited == 0:
                    stack.insert(0, (y.name, x.name))

    def BFS(self, start, goal):
        Queue = []
        x = self.search(start)
        Queue.append((x.name, None))
        while len(Queue) != 0:
            x = self.search(Queue[0][0])

            if x.predecessor is None:
                x.predecessor = Queue[0][1]
            x.visited = 1
            self.explored.append(x.name)
            Queue.pop(0)

            if x.name in goal:
                return self.path(x.name)

            for j in x.Neighbour:
                y = self.search(j.name)
                if y.visited == 0:
                    Queue.append((y.name, x.name))

    def UCS(self, start, goal):
        priorityQ = []
        x = self.search(start)
        priorityQ.append((x.name, 0))

        while len(priorityQ) != 0:
            x = self.search(priorityQ[0][0])
            self.explored.append(x.name)
            x.visited = 1
            priorityQ.pop(0)

            if x.name in goal:
                return self.path(x.name)

            for j in x.Neighbour:
                y = self.search(j.name)
                z = x.cost + int(j.weight)
                if y.visited == 0:
                    if y.cost == 0:
                        y.cost = z
                        # priorityQ.append((j.name, y.cost))
                        y.predecessor = x.name
                    elif y.cost > z:
                        y.cost = z
                        # priorityQ.append((j.name, y.cost))
                        y.predecessor = x.name
                    priorityQ.append((j.name, z))
                priorityQ.sort(key=lambda x: x[1])

    def greedy(self, start, goal):
        priorityQ = []
        x = self.search(start)
        priorityQ.append((x.name, 0))

        while len(priorityQ) != 0:

            x = self.search(priorityQ[0][0])
            self.explored.append(x.name)
            x.visited = 1
            priorityQ.pop(0)

            if x.name in goal:
                return self.path(x.name)

            for j in x.Neighbour:
                y = self.search(j.name)
                if y.visited == 0:
                    priorityQ.append((j.name, y.heuristic))
                    y.predecessor = x.name
            priorityQ.sort(key=lambda x: x[1])

    def aStar(self, start, goal):
        priorityQ = []
        x = self.search(start)
        priorityQ.append((x.name, 0))

        while len(priorityQ) != 0:
            x = self.search(priorityQ[0][0])
            self.explored.append(x.name)
            x.visited = 1
            priorityQ.pop(0)

            if x.name in goal:
                return self.path(x.name)

            for j in x.Neighbour:
                y = self.search(j.name)
                g = x.cost + int(j.weight)
                z = g + y.heuristic
                if y.visited == 0:
                    if y.cost == 0:
                        y.cost = g
                        # priorityQ.append((j.name, z))
                        y.predecessor = x.name
                    elif y.cost > g:
                        y.cost = g
                        # priorityQ.append((j.name, z))
                        y.predecessor = x.name
                    priorityQ.append((j.name, z))
                priorityQ.sort(key=lambda x: x[1])

    def remove_pref(self):
        for i in self.ListofVertices:
            i.predecessor = None
            i.visited = 0
            i.cost = 0

    def path(self, goal):
        path = []
        x = self.search(goal)
        path.append(x.name)
        cost = 0

        while x.predecessor is not None:
            for i in self.search(x.predecessor).Neighbour:
                if i.name == x.name:
                    cost += int(i.weight)
            path.append(x.predecessor)
            x = self.search(x.predecessor)
        path.reverse()

        return path, cost

    def search(self, start):
        for i in self.ListofVertices:
            if i.name == start:
                return i
