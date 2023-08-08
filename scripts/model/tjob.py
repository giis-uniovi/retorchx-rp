from scripts.model import capacitytypes
from scripts.model.capacity import Capacity


class Tjob:

    def __init__(self, name, resourceinstances):
        self.name = name
        self.resourceinstances = resourceinstances

    def get_capacities(self):

        memory = Capacity(name=capacitytypes.memory_name, quantity=0)
        processors = Capacity(name=capacitytypes.processor_name, quantity=0)
        slots = Capacity(name=capacitytypes.slots_name, quantity=0)
        storage = Capacity(name=capacitytypes.storage_name, quantity=0)
        for resource in self.resourceinstances:
            for capacities in resource:
                match capacities.name:
                    case str(capacitytypes.processor_name):
                        processors.add_quantity(capacities.quantity)
                    case str(capacitytypes.memory_name):
                        memory.add_quantity(capacities.quantity)
                    case str(capacitytypes.storage_name):
                        storage.add_quantity(capacities.quantity)
                    case str(capacitytypes.slots_name):
                        slots.add_quantity(capacities.quantity)
                    case _:
                        print("Capacity not found")
        return {memory, processors, slots, storage}
