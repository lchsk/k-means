# K-means

Tested with Python 2.7.6, Ubuntu 14.04.

Source code is available in the **src** directory.
Program can be run with default parameters by:
<code>python main.py</code>

**Default parameters are**

- clusters: 3
- method: 2 (1 - cluster means which are not instances of the clusters, 2 - cluster means which are instances of the clusters)
- iterations: 2 (number of iterations to run)

**Parameters are given as in any other program**

<code>-h        Prints help</code>

<code>-i int  Number of iterations</code>

<code>-m int  Method (1 - cluster means which are not instances of the clusters, 2 - cluster means which are instances of the clusters)</code>

<code>-c int  Number of clusters</code>

**Examples**

<code>python main.py -h</code>

Prints help information.

<code>python main.py -i 10 -m 1</code>

Runs the program (using method 1) once with 10 iterations.

<code>python main.py -m 2 -i 5 -c 4</code>

Runs the program using method two with 5 iterations and 4 clusters.
