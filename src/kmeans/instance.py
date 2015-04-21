import math
import random

class Instance(object):
    def __init__(self):
        self.label = '<instance' + str(random.randint(1, 100)) + '>'
        self.features = {}
        self.label_centre = ''

        self.cluster = None
        self.distance = None

    def __repr__(self):
        return self.label

    def init(self, label, features):
        self.label = label
        self.features = features

    def init_line(self, line):
        self.array = line.split()

        if len(self.array) > 0:
            self.label = self.array[0]
            self.features = { e: 1 for e in self.array[1:]}

            self.normalise()
        else:
            self.label = self.features = False

    def _get_L2norm(self):

        self.L2norm = 0

        for k, v in self.features.iteritems():
            self.L2norm += v * v

        self.L2norm = math.sqrt(self.L2norm)

    def normalise(self):

        self._get_L2norm()

        for k, v in self.features.iteritems():
            self.features[k] = v / self.L2norm
