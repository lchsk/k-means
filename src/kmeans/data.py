import random
from instance import Instance

class Data(object):

    def __init__(self, directory, data):

        # Directory in which data files are located
        self.dir = directory

        # Filenames of data files
        self.data = data

        self.instances = []

        # All training data

        # Separate lists for positive and negative training data

        # Test data (positive)

        # Test data (negative)

        # Dictionary that holds words (key) and weights (value)
        self.words = {}

        # we run loading of the data already in the constructor
        self.load()

    def get_weight(self, word):
        '''Simply returns weight of a given word'''

        return self.words[word]

    def update_weight(self, item):
        '''Update weights for all words in a given review.
            Review (item) is stored as a list which consists of two elements:
            1) all words from the review
            2) label (1 or -1)
        '''

        words = item[0]
        label = item[1]

        for word in words:
            self.words[word] = self.words[word] + label

    def _load(self, filename):
        '''Loads data. It might look a bit weird,
            but the point is that I wanted to have a structure like this:
            [words, label], where <words> is a list and label is a number, so it could
            be address by indexing (zeroth element: list of words, first element: label).
        '''

        f = open(self.dir + filename, 'r')

        for line in f:

            # Here <line> is essentially a review

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

    def shuffle(self):
        '''Shuffles a training list. Should be called after each iteration.'''

        random.shuffle(self.train_list)
