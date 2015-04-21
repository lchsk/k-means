import random
from instance import Instance
import math

class KMeans(object):
    def __init__(self, data, settings):
        self.data = data
        self.settings = settings

        # Cluster centres
        self.centres = []
        # self._get_random_clusters

        self.a = {}


    def run(self):

        if self.settings.params['method'] == 1:
            self._method1()
        elif self.settings.params['method'] == 2:
            self._method2()

    def _method1(self):
        # Ver 1

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

        self._pick_random_clusters()
        self._assign_to_clusters()

        for c, l in self.a.iteritems():
            print '1: ', c, len(l)

        for i in xrange(0, self.settings.params['iterations']):
            print 'Iteration %s' % i
            self.centres = []
            self._find_centre_instances()
            self.a = {}
            self._assign_to_clusters()

        print self._test()

    def _find_centre_instances(self):

        print 'find-centre-instances'

        for c, l in self.a.iteritems():
            print 'c: ', c, len(l)
            ds = []

            for i1 in l:
                for i2 in l:
                    if i1 != i2:
                        d = self.get_distance(i1, i2)
                        ds.append([i1, i2, d])

            print 'ds ', len(ds)
            stats = {}

            for i in self.data.instances:
                for triple in ds:
                    if i in triple:
                        stats[i] = stats.get(i, 0) + triple[2]

            print 'stats ', len(stats)

            new_c = None
            smallest_d = 0

            for k, v in stats.iteritems():
                if not new_c:
                    new_c, smallest_d = k, v

                if v < smallest_d:
                    new_c, smallest_d = k, v

            # print new_c, smallest_d

            self.centres.append(new_c)
            # print self.centres

    def _find_centres(self):

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
                    # _i.features[k] = _i.features.get(k, 0) + v


            # i = 0
            # for word in sorted(_i.features, key=_i.features.get, reverse=True):
                # if i >= 120:
                    # del _i.features[word]
                # i += 1

            # print len(_i.features)
            # print 'c: ', _i.features
            self.centres.append(_i)

    def _test(self):

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

        _i = Instance()
        _i.label = random.choice(self.data.labels)
        n = random.randint(10, 30)

        for i in xrange(0, n):

            f = random.choice(self.data.features)
            _i.features[f] = 1

        _i.normalise()

        return _i

    def _pick_random_clusters(self):

        for i in xrange(0, self.settings.params['clusters']):

            _instance = random.choice(self.data.instances)

            if _instance not in self.centres:
                self.centres.append(_instance)

    def get_distance(self, instance1, instance2):

        d = 0

        for k, v in instance1.features.iteritems():
            if k in instance1.features and k in instance2.features:
                d += math.pow(instance1.features[k] - instance2.features[k], 2)
                # d += math.pow(instance1.features[k] - instance2.features.get(k, 0), 2)

        d = math.sqrt(d)

        if d == 1.0:
            print '1.0: ', instance1.features, 'ins2: ', instance2.features

        return d

    def _evaluate(self):

        for c, l in self.a.iteritems():
            tmp = {}
            for i in l:
                tmp[i.label] = tmp.get(i.label, 0) + 1

            if len(tmp) > 0:
                # Dominant label in the cluster
                dominant = sorted(tmp, key=tmp.get, reverse=True)[0]
                c.label_centre = dominant


        # Precision, Recall, FScore
        prec = {}
        recall = {}
        labels = []
        for c, l in self.a.iteritems():
            if c.label_centre and c.label_centre not in labels:
                labels.append(c.label_centre)

        for c, l in self.a.iteritems():
            n = 0
            if len(l) > 0:
                for i in l:
                    if i.label == c.label_centre:
                        n += 1
                p = float(n) / len(l)
                r = float(n) / 51
                prec[c.label_centre] = prec.get(c.label_centre, 0.0) + p
                recall[c.label_centre] = recall.get(c.label_centre, 0.0) + r

        # Macro averages
        P = sum(prec.values()) / len(prec)
        R = sum(recall.values()) / len(recall)
        F = 2 * P * R / (P + R)

        print P, R, F

    def _merge_dicts(self, d1, d2):

        d = {}

        for k, v in d1.iteritems():
            d[k] = v

        for k, v in d2.iteritems():
            if k in d:
                d[k] = d[k] + v
            else:
                d[k] = v

    def _assign_to_clusters(self):

        for i in self.data.instances:
            i.cluster = None
            i.distance = -1

        for c in self.centres:

            if c not in self.a:
                self.a[c] = []

            for i in self.data.instances:
                # print c, i
                d = self.get_distance(i, c)
                # print c, i, d

                if d > i.distance:
                    # print 'change: ', d, i.distance
                    i.cluster = c
                    i.distance = d
                else:
                    print 'nochange: ', d, i.distance
                    # print i.features
                    pass

        for i in self.data.instances:
            c = i.cluster

            self.a[c].append(i)
