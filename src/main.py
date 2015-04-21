from kmeans.data import Data
from kmeans.settings import Settings
from kmeans.kmeans import KMeans

if __name__ == '__main__':

    settings = Settings()
    settings.read_parameters()
    settings.print_parameters()

    data = Data(directory='../data/', data='data.txt')

    km = KMeans(data, settings)
    km.run()
