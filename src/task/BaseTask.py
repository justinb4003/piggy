from abc import ABC, abstractmethod


class BaseTask(ABC):

    configured = False
    priority = 0
    name = ''
    uuid = ''

    def __init__(self):
        self.configured = False

    def get_name(self):
        return self.name

    def set_name(self, val):
        self.name = val

    def get_uuid(self):
        return self.uuid

    def set_uuid(self, val):
        self.uuid = val

    def get_priority(self):
        return self.priority

    def set_priority(self, val):
        self.priority = val

    def export_as_dict(self):
        # TODO: This is ugly.
        d = {}
        for key in self.prop_map.keys():
            v = getattr(self, key)
            if (isinstance(v, list)):
                d[key] = []
                for o in v:
                    ov = o
                    if hasattr(o, 'short_name'):
                        ov = o.short_name
                    d[key].append(ov)
            else:
                if hasattr(v, 'short_name'):
                    d[key] = v.short_name
                else:
                    d[key] = v
        return d

    def import_by_dict(self, valmap):
        # TODO: This is also ugly.
        for key, f in self.prop_map.items():
            if key in valmap:
                v = valmap[key]
                if isinstance(v, list):
                    newprop = []
                    for o in v:
                        newprop.append(f(o))
                    setattr(self, key, newprop)
                else:
                    setattr(self, key, f(valmap[key]))
        self.configured = True

    @abstractmethod
    def get_madlib(self):
        pass

    # Accepts a tuple of equipment allowed the task is allowed to maninpulate.
    # If the list of cleared equipment is not everything the task wanted
    # it will be up to the task to decide if partially proceeding works.
    @abstractmethod
    def take_action(self, eq_cleared):
        pass

    # Returns true or false then a list of equipment the task needs to
    # manipulate to carry out the action
    @abstractmethod
    def want_action(self):
        pass
