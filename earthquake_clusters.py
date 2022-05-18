"""
Module: earthquake_clusters

A program to create and visualize clusters of earthquakes.

Authors:
1) Galen Forbes - gforbesroberts@sandiego.edu
2) Alex Bae - abae@sandiego.edu
3) Josue Bautista - josuebautista@sandiego.edu
"""

import sys
import math
import matplotlib.pyplot as pp
import imageio
import csv


def euclidean_distance(point1, point2):
    """
    Returns the euclidean distance between point1 and point2.
    point1 and point2 are tuples of length 2.
    """
    return math.sqrt(((point2[0]-point1[0])**2) + (point2[1]-point1[1])**2)

def get_close_points(p, epsilon, data):
    """
    Returns a list of all the points in the dataset data 
    that are the within epsilon of p.
	"""
    points = []
    for point in data:
        if data[point] == None and point != p:
            distance = euclidean_distance(p,point)
            if distance <= epsilon:
                points.append(point)
    return points

def add_to_cluster(points, cluster_num, data, epsilon, min_pts):
    """
    This function loops through all of the given points and sees if they can be added 
    to the cluster with number cluster_num.
    If a point in points is  labeled as an outlier/noise (value is -1), it is ignored
    """
    for point in points:
        if data[point] == None or data[point] == -1:
            data[point] = cluster_num
            close_points = get_close_points(point,epsilon,data)
            if len(close_points) + 1 >= min_pts:
                add_to_cluster(close_points,cluster_num,data,epsilon,min_pts)

def dbscan(data, epsilon, min_pts):
    """
    As we loop through all points in our data, if the point hasn't been assigned a cluster, 
    we use close_points and add_to_cluster to find nearby points and to assign them to a cluster.
    Afterwards, we find a new set of points to assign. Outliers are ignored. 
    """
    cluster_num = 0
    for point in data:
        if data[point] == None:
            close_points = get_close_points(point, epsilon, data)
            if len(close_points) + 1 >= min_pts:
                add_to_cluster(close_points,cluster_num,data,epsilon,min_pts)
                cluster_num += 1
            else:
                data[point] = -1
    return cluster_num

def get_clusters(data, num_clusters):
    """
    As we loop through all points in data, we create a list of clusters, a list of lists.
    Each list within the parent list is a different cluster,
    """
    clusters, temp_cluster = [], [] 
    for i in range(num_clusters):
        temp_cluster = [point for point in data if data[point] == i]
        clusters.append(temp_cluster)
    return clusters

def plot_clusters(clusters):
    """
    For each cluster in clusters(list of all clusters), we plot the cluster 
    on a scatterplot. This is accomplished by storing the x,y values of each 
    cluster then using the pp.scatter method.
    """
    lst_x, lst_y = [], []
    for lst in clusters:
        lst_x = [point[0] for point in lst]
        lst_y = [point[1] for point in lst]
        pp.scatter(lst_x, lst_y)

def get_eq_locations(filename):
    """
    We create a list of earthquake locations given a csv file
    containing data of earthquakes.
    """
    locations = []
    f = open(filename, encoding = 'utf-8')
    f.readline()
    csv_reader = csv.reader(f, delimiter = ',')
    for line in csv_reader:
        point = float(line[2]),float(line[1])
        locations.append(point)
    return locations

def initialize_database(locations):
    """
    We create a dictionary with each point in locations list
    as a key. 
    """
    data = {}
    for point in locations:
        data.setdefault(point)
    return data

def plot_earthquakes(filename):
    """
    Creates clusters of earthquakes from the data contained in filename and
    displays them on a world map.
    """

    print("Creating and visualizing clusters from file: %s" % filename)

    # To Do: Use the functions you wrote above to complete the following 5
    # steps. Delete this comment when you are done.

    # Step 1: Gets a list of all of the earthquake locations.
    locations = get_eq_locations(filename)
    # Step 2: Initializes the data dictionary.
    data = initialize_database(locations)
    # Step 3: Use dbscan to create clusters.
    num_clusters = dbscan(data, 2.0, 4)
    # Step 4: Get the list of created clusters.
    clusters = get_clusters(data, num_clusters)
    # Step 5: Plot the clusters.
    plot_clusters(clusters)

    # Set the image background to be a world-map
    # Don't change anything after this point.
    img = imageio.imread("world-map-full.jpg")
    pp.imshow(img, zorder=0, extent=[-180, 180, -90, 90])
    pp.axis('off')
    pp.show()


if __name__ == "__main__":
    # Choose the input file
    choice = input("Enter 1 (for eq_day.csv) or 2 (for eq_week.csv): ")

    # Create the clusters and plot the data.
    if choice == '1':
        plot_earthquakes("eq_day.csv")
    elif choice == '2':
        plot_earthquakes("eq_week.csv")
    else:
        print("Invalid choice")