import sys
import getopt

class Settings(object):
    def __init__(self):

        # Parameters dictionary
        self.params = {}

        # Number of iterations to perform
        self.params['iterations'] = 2

        self.params['method'] = 2

        self.params['clusters'] = 3

    def help(self):
        '''Prints help information, explains all the parameters'''

        print 'This program implements the K-means algorithm.'
        print 'Usage:'
        print '\t-h\tfor help'
        print '\t-i <int>\tnumber of iterations'
        print '\t-m <int>\tmethod (1 - cluster means which are not instances of the clusters, 2 - cluster means which are instances of the clusters)'
        print '\t-c\t <int>\tnumber of clusters'

        sys.exit(0)

    def read_parameters(self):
        '''Reads parameters from the command line and sets corresponding variables'''

        opts, args = getopt.getopt(sys.argv[1:], "hi:m:c:", ['help', 'iterations', 'method', 'clusters'])

        try:
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    self.help()
                elif opt in ('-i', '--iterations'):
                    self.params['iterations'] = int(arg)
                elif opt in ('-m', '--method'):
                    self.params['method'] = int(arg)
                elif opt in ('-c', '--clusters'):
                    self.params['clusters'] = int(arg)
                else:
                    self.help()

        except getopt.GetoptError:
            self.help()

    def print_parameters(self):
        '''Prints parameters to the user to make sure that they were read properly'''

        print 'Parameters:'
        for k, v in self.params.iteritems():
            print '\t' + k + ': ' + str(v)

        print '*' * 50
