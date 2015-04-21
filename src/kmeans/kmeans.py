import random
from instance import Instance
import math

class KMeans(object):
    def __init__(self, data, settings):
        self.data = data
        self.settings = settings

        # Cluster centres
        self.centres = []

        self.a = {}

    def run(self):
        '''
            Method 1: using cluster means which are not instances of the cluster.
            Method 2: using cluster means which are instances of the cluster.
        '''

        if self.settings.params['method'] == 1:
            self._method1()
        elif self.settings.params['method'] == 2:
            self._method2()

    def _method1(self):
        '''
        Method 1 - run. (cluster means)
        '''

        # Initial random centres
        for i in xrange(0, self.settings.params['clusters']):
            self.centres.append(self._generate_random_instance())

        self._assign_to_clusters()

        for i in xrange(0, self.settings.params['iterations']):
            print 'Iteration %s' % i

            self.centres = []

            self._find_centres()
            self.a = {}
            self._assign_to_clusters()
            self._evaluate()

        self._test()

    def _method2(self):
        '''
        Method 2 - run. (cluster means which are instances of the cluster)
        '''

        self._pick_random_clusters()
        self._assign_to_clusters()

        for i in xrange(0, self.settings.params['iterations']):
            print 'Iteration %s' % i
            self.centres = []
            self._find_centre_instances()
            self.a = {}
            self._assign_to_clusters()
            self._evaluate()

        self._test()

    def _find_centre_instances(self):
        '''
            Finds instances of each cluster which are centers of the clusters.
        '''
        for c, l in self.a.iteritems():
            ds = []

            # Compute distance between each instance pair (i1, i2)
            for i1 in l:
                for i2 in l:
                    if i1 != i2:
                        d = self.get_distance(i1, i2)
                        ds.append([i1, i2, d])

            stats = {}

            # ds is a list of pairs <i1, i2, distance_between i2 and i2>
            for i in self.data.instances:
                for triple in ds:
                    if i in triple:
                        stats[i] = stats.get(i, 0) + triple[2]

            new_c = None
            smallest_d = 0

            for k, v in stats.iteritems():
                if not new_c:
                    new_c, smallest_d = k, v

                if v < smallest_d:
                    new_c, smallest_d = k, v

            self.centres.append(new_c)

    def _find_centres(self):
        '''
            Finds mean of the cluster which is not an instance.
        '''

        for c, l in self.a.iteritems():
            _i = Instance()
            tmp = {}
            for i in l:
                for k, v in i.features.iteritems():
                    if k not in tmp:
                        tmp[k] = []

                    tmp[k].append(v)

            for k, v in tmp.iteritems():
                s = sum(v) / len(v)
                _i.features[k] = _i.features.get(k, 0) + s

            self.centres.append(_i)

    def _test(self):
        '''
            Calculates how many instances of each label are in all clusters.
        '''

        self.stats = {}

        for c, l in self.a.iteritems():

            if c not in self.stats:
                self.stats[c] = {}

            for i in l:
                label = i.label
                self.stats[c][label] = self.stats[c].get(label, 0) + 1

        for c, d in self.stats.iteritems():
            print c
            for k, v in d.iteritems():
                print '\t' + k + '\t' + str(v)

    def _generate_random_instance(self):
        '''
            Generates random instance (ie which is not an actual instance. (for method 1))
        '''

        _i = Instance()
        _i.label = random.choice(self.data.labels)
        n = random.randint(10, 30)

        for i in xrange(0, n):

            f = random.choice(self.data.features)
            _i.features[f] = 1

        _i.normalise()

        return _i

    def _pick_random_clusters(self):
        '''
            (for method 2)
            Picks random instances as initial cluster centres.
        '''

        for i in xrange(0, self.settings.params['clusters']):

            _instance = random.choice(self.data.instances)

            if _instance not in self.centres:
                self.centres.append(_instance)

    def get_distance(self, instance1, instance2):
        '''
            Computes distance between two instances.
        '''

        d = 0

        for k, v in instance1.features.iteritems():
            if instance1 and instance2 and k in instance1.features and k in instance2.features:
                d += math.pow(instance1.features[k] - instance2.features[k], 2)

        d = math.sqrt(d)

        return d

    def _evaluate(self):
        '''
            Computes evaluation measures:
            - precision
            - recall
            - f-score
        '''

        for c, l in self.a.iteritems():
            tmp = {}
            for i in l:
                tmp[i.label] = tmp.get(i.label, 0) + 1

            if len(tmp) and c > 0:
                # Dominant label in the cluster
                dominant = sorted(tmp, key=tmp.get, reverse=True)[0]
                c.label_centre = dominant


        # Precision, Recall, FScore
        prec = {}
        recall = {}
        labels = []
        for c, l in self.a.iteritems():
            if c and c.label_centre and c.label_centre not in labels:
                labels.append(c.label_centre)

        for c, l in self.a.iteritems():
            n = 0
            if len(l) and c > 0:
                for i in l:
                    if c and i.label == c.label_centre:
                        n += 1
                p = float(n) / len(l)
                r = float(n) / 51
                prec[c.label_centre] = prec.get(c.label_centre, 0.0) + p
                recall[c.label_centre] = recall.get(c.label_centre, 0.0) + r

        # Macro averages
        P = sum(prec.values()) / len(prec)
        R = sum(recall.values()) / len(recall)
        F = 2 * P * R / (P + R)

        print 'Macro-averaged precision: %s' % P
        print 'Macro-averaged recall: %s' % R
        print 'Macro-averaged F-score: %s' % F

    def _merge_dicts(self, d1, d2):
        '''
            Merge two dictionaries
        '''

        d = {}

        for k, v in d1.iteritems():
            d[k] = v

        for k, v in d2.iteritems():
            if k in d:
                d[k] = d[k] + v
            else:
                d[k] = v

    def _assign_to_clusters(self):
        '''
            (both method 1 & 2)
            Assigns all instances to their closest cluster centre.
        '''

        for i in self.data.instances:
            i.cluster = None
            i.distance = -1

        for c in self.centres:

            if c not in self.a:
                self.a[c] = []

            for i in self.data.instances:
                d = self.get_distance(i, c)

                if d > i.distance:
                    i.cluster = c
                    i.distance = d

        for i in self.data.instances:
            c = i.cluster

            self.a[c].append(i)
