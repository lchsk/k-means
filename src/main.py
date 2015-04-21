from kmeans.data import Data
from kmeans.settings import Settings
from kmeans.kmeans import KMeans

if __name__ == '__main__':

    settings = Settings()
    settings.read_parameters()
    settings.print_parameters()

    # initiate data object
    # and set filesnames to the ones given
    data = Data(directory='../data/', data='data.txt')
    # print data.instances[0].features
    # print data.instances[1].features
    # print data.instances[2].features

    # create a Perceptron object and run it!
    km = KMeans(data, settings)
    km.run()
