import random
from instance import Instance

class Data(object):

    def __init__(self, directory, data):

        # Directory in which data files are located
        self.dir = directory

        # Filenames of data files
        self.data = data

        self.instances = []

        # we run loading of the data already in the constructor
        self.load()

    def _load(self, filename):

        f = open(self.dir + filename, 'r')

        for line in f:

            i = Instance()
            i.init_line(line)
            self.instances.append(i)

        f.close()

    def load(self):
        '''External method for loading the data.'''

        self._load(self.data)

        # All labels
        self.labels = list({ i.label for i in self.instances })

        # All features
        self.features = []
        for i in self.instances:
            self.features += i.features.keys()

        self.features = list(set(self.features))
