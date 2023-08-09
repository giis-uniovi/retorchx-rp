class ResourceInstance:
    def __init__(self, name, capacities):
        self.name = name
        self.capacities = capacities

    def __eq__(self, other):
        return isinstance(self, ResourceInstance) and self.name == other.name and self.capacities == other.capacities

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)

    def __hash__(self):
        return hash(tuple(self))

    def __iter__(self):
        # return iter(self.__stations[1:]) #uncomment this if you wanted to skip the first element.
        return iter(self.capacities)
