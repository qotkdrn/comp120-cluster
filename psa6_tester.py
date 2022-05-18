"""
Module: earthquake_clusters_tester

Test cases for earthquake_clusters module.
"""

import unittest
from unittest.mock import Mock, MagicMock, mock_open, patch, call
import earthquake_clusters
import io

import sys
import math
import matplotlib.pyplot as pp
from imageio import imread
import random

class PA6Test(unittest.TestCase):
    """ 
    For testing the neighbor_count and one_step methods of the LifeModel class.
    Run test_neighbor_count and test_one_step by typing
    python3 -m unittest psa6_tester.py 
    from the command line.
    """
    def setUp(self):
        """ Set up testing of functions. """
        print("In setup")

        # Test data

        # For testing get_eq_locations
        self.file_contents_mock = """time,latitude,longitude,depth,mag,magType,nst,gap,dmin,rms,net,id,updated,place,type,horizontalError,depthError,magError,magNst,status,locationSource,magSource
2018-11-08T22:35:24.300Z,36.0548333,-117.5971667,1.97,0.89,ml,9,109,0.0877,0.08,ci,ci38354672,2018-11-08T22:38:52.029Z,"31km ENE of Little Lake, CA",earthquake,0.31,0.58,0.147,9,automatic,ci,ci
2018-11-08T22:32:32.680Z,33.4818333,-116.5031667,16.26,0.88,ml,21,133,0.07897,0.27,ci,ci38354664,2018-11-08T22:36:06.013Z,"18km ESE of Anza, CA",earthquake,0.72,1.04,0.269,19,automatic,ci,ci
2018-11-08T22:25:24.100Z,60.1567,-141.4784,0,1.8,ml,,,,1.17,ak,ak20336006,2018-11-08T22:28:00.728Z,"53km E of Cape Yakataga, Alaska",earthquake,,0.7,,,automatic,ak,ak
2018-11-08T22:23:36.060Z,19.4058342,-155.290329,-0.21,1.73,md,13,82,0.009167,0.1,hv,hv70679846,2018-11-08T22:26:47.240Z,"6km WSW of Volcano, Hawaii",earthquake,0.15,0.32,0.17,8,automatic,hv,hv
2018-11-08T22:15:12.120Z,38.7903328,-122.7626648,0.94,0.48,md,7,92,0.01973,0.02,nc,nc73108491,2018-11-08T22:29:02.760Z,"2km NNW of The Geysers, CA",earthquake,0.34,0.69,0.03,2,automatic,nc,nc
2018-11-08T22:09:25.630Z,33.511,-116.7968333,3.94,0.1,ml,14,139,0.00324,0.12,ci,ci38354656,2018-11-08T22:21:54.452Z,"10km NE of Aguanga, CA",earthquake,0.36,0.46,0.096,8,reviewed,ci,ci
2018-11-08T22:07:38.780Z,34.1531667,-117.4748333,7.51,0.88,ml,27,66,0.0556,0.12,ci,ci38354648,2018-11-08T22:17:54.897Z,"6km NNW of Fontana, CA",earthquake,0.23,0.42,0.084,11,reviewed,ci,ci
2018-11-08T21:58:50.720Z,38.7733345,-122.7713318,9.08,1.55,md,9,175,0.02937,0.07,nc,nc73108486,2018-11-08T22:13:03.670Z,"1km WSW of The Geysers, CA",earthquake,1.41,4.46,0.52,2,automatic,nc,nc
2018-11-08T21:19:47.340Z,45.8603333,-111.345,4.03,1.76,ml,15,89,0.304,0.17,mb,mb80322894,2018-11-08T21:30:26.300Z,"1km WNW of Manhattan, Montana",earthquake,0.44,12.3,0.085,6,reviewed,mb,mb
2018-11-08T21:17:27.180Z,38.7874985,-122.7433319,1.34,1.19,md,10,85,0.006691,0.02,nc,nc73108481,2018-11-08T21:32:03.492Z,"2km NE of The Geysers, CA",earthquake,0.25,0.57,0.15,2,automatic,nc,nc
2018-11-08T21:07:01.580Z,-34.3517,116.87,10,5,mb,,66,1.453,1.08,us,us1000hpej,2018-11-08T22:43:06.888Z,"63km SSW of Kojonup, Australia",earthquake,8,1.9,0.085,45,reviewed,us,us
2018-11-08T21:06:13.228Z,63.8402,-149.3208,128.5,1.9,ml,,,,0.32,ak,ak20335898,2018-11-08T21:10:02.309Z,"17km W of Healy, Alaska",earthquake,,1.1,,,automatic,ak,ak
2018-11-08T20:55:33.770Z,36.0908333,-117.6595,1.56,1.15,ml,15,51,0.1017,0.09,ci,ci38354576,2018-11-08T21:12:14.120Z,"26km E of Coso Junction, CA",earthquake,0.14,0.26,0.212,11,reviewed,ci,ci
2018-11-08T20:20:35.330Z,38.7888336,-122.7444992,1.21,1.79,md,14,56,0.008255,0.03,nc,nc73108466,2018-11-08T20:52:03.215Z,"2km NE of The Geysers, CA",earthquake,0.24,0.49,0.17,5,automatic,nc,nc
2018-11-08T20:16:17.330Z,45.9081667,-111.4148333,-2,1.49,ml,7,176,0.281,0.05,mb,mb80322844,2018-11-08T21:59:24.410Z,"8km NW of Manhattan, Montana",quarry blast,0.54,31.61,0.323,5,reviewed,mb,mb
2018-11-08T20:14:45.710Z,33.6603333,-116.7336667,14.51,0.87,ml,22,94,0.05066,0.07,ci,ci38354528,2018-11-08T20:26:31.352Z,"9km S of Idyllwild, CA",earthquake,0.18,0.31,0.164,21,reviewed,ci,ci
2018-11-08T19:45:34.140Z,33.8203333,-117.6656667,5.56,0.8,ml,7,230,0.05334,0.16,ci,ci38354488,2018-11-08T20:04:05.261Z,"11km WSW of Corona, CA",earthquake,0.67,0.89,0.015,3,reviewed,ci,ci
2018-11-08T19:29:57.447Z,61.7518,-151.3002,29,1.9,ml,,,,1.29,ak,ak20335892,2018-11-08T19:34:34.824Z,"66km W of Willow, Alaska",earthquake,,0.4,,,automatic,ak,ak
2018-11-08T19:03:42.849Z,57.3909,-153.4153,3.7,2.1,ml,,,,0.53,ak,ak20335889,2018-11-08T19:06:44.004Z,"37km ESE of Larsen Bay, Alaska",earthquake,,0.3,,,automatic,ak,ak
2018-11-08T18:56:38.354Z,37.0682,-117.7838,13.2,1,ml,5,215.71,0.198,0.0873,nn,nn00664745,2018-11-08T19:17:16.340Z,"46km ESE of Big Pine, California",earthquake,,11,0.51,4,reviewed,nn,nn
2018-11-08T18:52:18.010Z,18.1781,-64.8718,29,2.27,md,5,344,0.9776,0.21,pr,pr2018312004,2018-11-08T21:45:46.579Z,"19km SSE of Charlotte Amalie, U.S. Virgin Islands",earthquake,6.26,17.04,0.11,3,reviewed,pr,pr
2018-11-08T18:49:20.657Z,64.3487,-151.028,15,1.5,ml,,,,0.59,ak,ak20335885,2018-11-08T18:53:35.761Z,"75km SSW of Manley Hot Springs, Alaska",earthquake,,0.2,,,automatic,ak,ak
2018-11-08T18:33:04.292Z,69.6218,-144.2639,0,2.9,ml,,,,0.77,ak,ak20335879,2018-11-08T18:44:46.147Z,"61km SSW of Kaktovik, Alaska",earthquake,,0.8,,,automatic,ak,ak
2018-11-08T18:28:33.590Z,44.0826666666667,-122.836166666667,12.74,1.22,ml,7,101,,0.08,uw,uw61503147,2018-11-08T19:16:28.640Z,"15km ENE of Springfield, Oregon",explosion,0.42,0.95,0.267963955368372,5,reviewed,uw,uw
2018-11-08T18:28:29.340Z,33.4956667,-116.7908333,4.5,0.4,ml,19,96,0.01846,0.09,ci,ci38354432,2018-11-08T19:33:30.290Z,"9km NE of Aguanga, CA",earthquake,0.21,0.27,0.192,11,reviewed,ci,ci
2018-11-08T18:17:02.619Z,56.0588,-149.9913,12.6,3.4,ml,,,,0.72,ak,ak20335871,2018-11-08T19:36:18.748Z,"242km SE of Kodiak, Alaska",earthquake,,9.1,,,reviewed,ak,ak
2018-11-08T18:14:00.463Z,61.0576,-147.5786,41.5,1.9,ml,,,,1.06,ak,ak20335869,2018-11-08T18:18:30.288Z,"66km W of Valdez, Alaska",earthquake,,1,,,automatic,ak,ak
2018-11-08T18:11:53.979Z,68.649,-147.3513,0,2.3,ml,,,,0.57,ak,ak20335867,2018-11-08T18:23:31.009Z,"94km NW of Arctic Village, Alaska",earthquake,,0.4,,,automatic,ak,ak
2018-11-08T18:04:24.190Z,36.0861667,-117.6491667,2.15,0.37,ml,9,89,0.1073,0.06,ci,ci38354424,2018-11-08T19:36:23.095Z,"27km E of Coso Junction, CA",earthquake,0.17,0.33,0.118,4,reviewed,ci,ci"""

        self.eq_locations = [(-117.5971667, 36.0548333), 
            (-116.5031667, 33.4818333), (-141.4784, 60.1567), 
            (-155.290329, 19.4058342), (-122.7626648, 38.7903328), 
            (-116.7968333, 33.511), (-117.4748333, 34.1531667), 
            (-122.7713318, 38.7733345), (-111.345, 45.8603333), 
            (-122.7433319, 38.7874985), (116.87, -34.3517), 
            (-149.3208, 63.8402), (-117.6595, 36.0908333), 
            (-122.7444992, 38.7888336), (-111.4148333, 45.9081667), 
            (-116.7336667, 33.6603333), (-117.6656667, 33.8203333), 
            (-151.3002, 61.7518), (-153.4153, 57.3909), 
            (-117.7838, 37.0682), (-64.8718, 18.1781), 
            (-151.028, 64.3487), (-144.2639, 69.6218), 
            (-122.836166666667, 44.0826666666667), (-116.7908333, 33.4956667), 
            (-149.9913, 56.0588), (-147.5786, 61.0576), 
            (-147.3513, 68.649), (-117.6491667, 36.0861667)]

        # For testing get_close_points
        self.index_test_location = 19
        self.test_distance = 7.0
        self.close_points = [(-117.5971667, 36.0548333), 
                    (-116.5031667, 33.4818333), (-122.7626648, 38.7903328), 
                    (-116.7968333, 33.511), (-117.4748333, 34.1531667), 
                    (-122.7713318, 38.7733345), (-122.7433319, 38.7874985), 
                    (-117.6595, 36.0908333), (-122.7444992, 38.7888336), 
                    (-116.7336667, 33.6603333), (-117.6656667, 33.8203333), 
                    (-116.7908333, 33.4956667), (-117.6491667, 36.0861667)]
        self.close_points.sort()

        # For testing euclidean_distance
        self.point1 = self.eq_locations[0]
        self.point2 = self.eq_locations[1]
        self.distance_point1_point2 = 2.7959193479068776
        self.tolerance = 1.0e-6

        # For testing initialize_database
        self.eq_locations_database = {(-117.5971667, 36.0548333): None, 
            (-116.5031667, 33.4818333): None, (-141.4784, 60.1567): None, 
            (-155.290329, 19.4058342): None, (-122.7626648, 38.7903328): None, 
            (-116.7968333, 33.511): None, (-117.4748333, 34.1531667): None, 
            (-122.7713318, 38.7733345): None, (-111.345, 45.8603333): None, 
            (-122.7433319, 38.7874985): None, (116.87, -34.3517): None, 
            (-149.3208, 63.8402): None, (-117.6595, 36.0908333): None, 
            (-122.7444992, 38.7888336): None, (-111.4148333, 45.9081667): None, 
            (-116.7336667, 33.6603333): None, (-117.6656667, 33.8203333): None, 
            (-151.3002, 61.7518): None, (-153.4153, 57.3909): None, 
            (-117.7838, 37.0682): None, (-64.8718, 18.1781): None, 
            (-151.028, 64.3487): None, (-144.2639, 69.6218): None, 
            (-122.836166666667, 44.0826666666667): None, 
            (-116.7908333, 33.4956667): None, (-149.9913, 56.0588): None, 
            (-147.5786, 61.0576): None, (-147.3513, 68.649): None, 
            (-117.6491667, 36.0861667): None}

        # For testing add_to_cluster
        self.cluster_num = 1
        self.max_distance = 1.01
        self.min_pts = 3
        self.p1 = [(0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1),
                    (3,0), (4,0), (5,0), (6,0), (3,2), (3,3), (4,3), (2,3)]

        self.p2 = [self.p1[2], self.p1[4], self.p1[8], self.p1[12], 
                    self.p1[13], self.p1[14], self.p1[15]]
        self.d2 = {self.p1[2]:-1, self.p1[3]:self.cluster_num, self.p1[4]:-1, 
                self.p1[8]:-1, self.p1[12]:-1, self.p1[13]:None, 
                self.p1[14]:None, self.p1[15]:None}
        self.d2_after = {(2, 1): 1, (3, 1): 1, (4, 1): 1, (3, 0): 1, 
                    (3, 2): 1, (3, 3): 1, (4, 3): 1, (2, 3): 1}

        self.p3 = [self.p1[2], self.p1[8], self.p1[12], self.p1[4]]
        self.d3 = {self.p1[2]:2, self.p1[3]:self.cluster_num, self.p1[4]:2, 
                    self.p1[8]:2, self.p1[12]:2}
        self.d3_after = {(2, 1): 2, (3, 1): 1, (4, 1): 2, (3, 0): 2, (3, 2): 2}

        self.p4 = [self.p1[2], self.p1[4], self.p1[8], self.p1[12]]
        self.d4 = {self.p1[0]:None, self.p1[1]:None, self.p1[2]:None, 
                self.p1[3]:self.cluster_num, self.p1[4]:None, self.p1[5]:None,
                self.p1[6]:None, self.p1[7]:None, self.p1[8]:None, self.p1[9]:None, 
                self.p1[10]:None, self.p1[11]:None, self.p1[12]:None,
                self.p1[13]:None, self.p1[14]:None, self.p1[15]:None}

        self.d4_after = {(0, 1): None, (1, 1): None, (2, 1): 1, 
                        (3, 1): 1, (4, 1): 1, (5, 1): 1, (6, 1): 1, 
                        (7, 1): 1, (3, 0): 1, (4, 0): 1, (5, 0): 1, 
                        (6, 0): 1, (3, 2): 1, (3, 3): None, 
                        (4, 3): None, (2, 3): None}

        # For testing dbscan
        self.eq_locations_database_after = {(-117.5971667, 36.0548333): 0, 
        (-116.5031667, 33.4818333): 0, (-141.4784, 60.1567): -1, 
        (-155.290329, 19.4058342): -1, (-122.7626648, 38.7903328): 1, 
        (-116.7968333, 33.511): 0, (-117.4748333, 34.1531667): 0, 
        (-122.7713318, 38.7733345): 1, (-111.345, 45.8603333): -1, 
        (-122.7433319, 38.7874985): 1, (116.87, -34.3517): -1, 
        (-149.3208, 63.8402): 2, (-117.6595, 36.0908333): 0, 
        (-122.7444992, 38.7888336): 1, (-111.4148333, 45.9081667): -1, 
        (-116.7336667, 33.6603333): 0, (-117.6656667, 33.8203333): 0, 
        (-151.3002, 61.7518): 2, (-153.4153, 57.3909): -1, 
        (-117.7838, 37.0682): 0, (-64.8718, 18.1781): -1, 
        (-151.028, 64.3487): 2, (-144.2639, 69.6218): -1, 
        (-122.836166666667, 44.0826666666667): -1, 
        (-116.7908333, 33.4956667): 0, (-149.9913, 56.0588): -1, 
        (-147.5786, 61.0576): 2, (-147.3513, 68.649): -1, 
        (-117.6491667, 36.0861667): 0}
        self.max_distance_2 = 4.0
        self.num_clusters = 3

        # For testing get_clusters
        self.clusters = [[(-117.5971667, 36.0548333), (-116.5031667, 33.4818333), 
            (-116.7968333, 33.511), (-117.4748333, 34.1531667), 
            (-117.6595, 36.0908333), (-116.7336667, 33.6603333), 
            (-117.6656667, 33.8203333), (-117.7838, 37.0682), 
            (-116.7908333, 33.4956667), (-117.6491667, 36.0861667)], 
            [(-122.7626648, 38.7903328), (-122.7713318, 38.7733345), 
            (-122.7433319, 38.7874985), (-122.7444992, 38.7888336)], 
            [(-149.3208, 63.8402), (-151.3002, 61.7518), (-151.028, 64.3487), 
            (-147.5786, 61.0576)]]

        # For testing plot_clusters
        self.clusters_for_plot = [[(1,2), (3,4), (5,6)], [(7, 8), (9, 10)]] 
        self.expected_calls_for_plot=[call([1,3,5],[2,4,6]), call([7, 9], [8, 10])]

    def test_all(self):
        """ Tests all functions in the earthquake_clusters program """

        # Track number of tests, and number of incorrect tests
        num_incorrect = 0
        num_tests = 0

        # Test euclidean_distance
        num_tests += 1
        try:
            self.euclidean_distance_test()
        except Exception as e:
            print("\nTest of euclidean_distance failed")
            print(f"Exception: {e}")
            num_incorrect += 1

        # Test get_eq_locations
        num_tests += 1
        try:
            self.get_eq_locations_test()
        except Exception as e:
            print("\nTest of get_eq_locations failed")
            print(f"Exception: {e}")
            num_incorrect += 1

        # Test initialize_database
        num_tests += 1
        try:
            self.initialize_database_test()
        except Exception as e:
            print("\nTest of initialize_data failed")
            print(f"Exception: {e}")
            num_incorrect += 1

        # Test get_close_points
        num_tests += 1
        try:
            self.get_close_points_test()
        except Exception as e:
            print("\nTest of get_close_points failed")
            print(f"Exception: {e}")
            num_incorrect += 1

        # Test add_to_cluster
        num_tests += 1
        try:
            self.add_to_cluster_test_a()
        except Exception as e:
            print("\nTest of add_to_cluster failed")
            print(f"Exception: {e}")
            num_incorrect += 1

        num_tests += 1
        try:
            self.add_to_cluster_test_b()
        except Exception as e:
            print("\nTest of add_to_cluster failed")
            print(f"Exception: {e}")
            num_incorrect += 1

        num_tests += 1
        try:
            self.add_to_cluster_test_c()
        except Exception as e:
            print("\nTest of add_to_cluster failed")
            print(f"Exception: {e}")
            num_incorrect += 1

        # Test dbscan
        num_tests += 1
        try:
            self.dbscan_test()
        except Exception as e:
            print("\nTest of dbscan failed")
            print(f"Exception: {e}")
            num_incorrect += 1

        # Test get_clusters
        num_tests += 1
        try:
            self.get_clusters_test()
        except Exception as e:
            print("\nTest of get_clusters failed")
            print(f"Exception: {e}")
            num_incorrect += 1

        # Test plot_clusters
        num_tests += 1
        try:
            self.plot_clusters_test()
        except Exception as e:
            print("\nTest of plot_clusters failed")
            print(f"Exception: {e}")
            num_incorrect += 1

        # Test plot_earthquakes
        num_tests += 1
        try:
            self.plot_earthquakes_test()
        except Exception as e:
            print("\nTest of plot_earthquakes failed")
            print(f"Exception: {e}")
            num_incorrect += 1

        print(f"Num tests completed = {num_tests}")
        print(f"Num correct = {num_tests - num_incorrect}")
        if num_incorrect == 0:
            print("All correct.  Make sure the final test of your program looks good")
            print("by running your program on both 'eq_day.csv'")
            print("and 'eq_week.csv' and making sure the plots look as shown")
            print("in the problem statement")
        else:
            print("Not all functions are correct.  Keep working on it.")

    def euclidean_distance_test(self):
        """ Tests euclidean_distance """
        print("\n**************\nTesting euclidean_distance function.")
        distance = earthquake_clusters.euclidean_distance(self.point1, self.point2)
        self.assertTrue(abs(distance - self.distance_point1_point2) <= self.tolerance)
            
        print("Test of euclidean_distance passed")

    def get_eq_locations_test(self):
        """ Tests get_eq_locations function. """
        print("\n**************\nTesting get_eq_locations function.")

        fake_file_path = 'file/path/mock'

        #with patch('earthquake_clusters.get_eq_locations.open'.format(__name__),
        with patch('builtins.open',
                    new=mock_open(read_data=self.file_contents_mock)) as _file:
            actual = earthquake_clusters.get_eq_locations(fake_file_path)
            print(actual)
            self.assertEqual(self.eq_locations, actual)

        print("Test of get_eq_locations passed")
        
    def initialize_database_test(self):
        """ Tests initialize database """
        print("\n**************\nTesting initialize_database function.")

        database = earthquake_clusters.initialize_database(self.eq_locations)
        self.assertEqual(database, self.eq_locations_database)
            
        print("Test of initialize_database passed")

    def get_close_points_test(self):
        """ Tests get_close_points """
        print("\n**************\nTesting get_close_points function.")

        close_points = earthquake_clusters.get_close_points(
            self.eq_locations[self.index_test_location], self.test_distance, 
                            self.eq_locations_database)
        close_points.sort()
        self.assertEqual(close_points, self.close_points)
            
        print("Test of initialize_database passed")


    def add_to_cluster_test_a(self):
        """ Tests add_to_cluster """
        print("\n**************\nTesting add_to_cluster function.")

        print("  Testing handling of points already labeled as outliers:")
        d2_copy = dict(self.d2)
        earthquake_clusters.add_to_cluster(self.p2, self.cluster_num, d2_copy, 
                            self.max_distance, self.min_pts)
        self.assertEqual(d2_copy, self.d2_after)
            
        print("Test a) of add_to_cluster passed")

    def add_to_cluster_test_b(self):
        """ Tests add_to_cluster """
        print("\n**************\nTesting add_to_cluster function.")

        print("\nTesting handling of points already assigned to cluster:")
        d3_copy = dict(self.d3)
        earthquake_clusters.add_to_cluster(self.p3, self.cluster_num, d3_copy, 
                            self.max_distance, self.min_pts)
        self.assertEqual(d3_copy, self.d3_after)
            
        print("Test b) of add_to_cluster passed")

    def add_to_cluster_test_c(self):
        """ Tests add_to_cluster """
        print("\n**************\nTesting add_to_cluster function.")

        print("\nTesting recusion:")
        d4_copy = dict(self.d4)
        earthquake_clusters.add_to_cluster(self.p4, self.cluster_num, d4_copy, 
                            self.max_distance, self.min_pts)
        self.assertEqual(d4_copy, self.d4_after)
            
        print("Test c) of add_to_cluster passed")

    def dbscan_test(self):
        """ Tests dbscan """
        print("\n**************\nTesting dbscan function.")

        eq_locations_database_copy = dict(self.eq_locations_database)
        num_clusters = earthquake_clusters.dbscan(eq_locations_database_copy, 
                    self.max_distance_2, self.min_pts)
        self.assertEqual(eq_locations_database_copy, self.eq_locations_database_after)
        self.assertEqual(num_clusters, self.num_clusters)
            
        print("Test of dbscan passed")

    def get_clusters_test(self):
        """ Tests get_clusters """
        print("\n**************\nTesting get_clusters function.")
        clusters = earthquake_clusters.get_clusters(self.eq_locations_database_after, 
                    self.num_clusters)
        self.assertEqual(clusters, self.clusters)
            
        print("Test of get_clusters passed")

    def plot_clusters_test(self):
        """ Tests plot_clusters """
        print("\n**************\nTesting plot_clusters function.")

        mock = Mock(return_value=None)
        with patch('matplotlib.pyplot.scatter') as mock:
            earthquake_clusters.plot_clusters(self.clusters_for_plot)

        mock.assert_has_calls(self.expected_calls_for_plot, any_order=True)

        print("Test of plot_clusters correct")


    @patch('earthquake_clusters.get_eq_locations')
    @patch('earthquake_clusters.initialize_database')
    @patch('earthquake_clusters.dbscan')
    @patch('earthquake_clusters.get_clusters')
    @patch('earthquake_clusters.plot_clusters')
    @patch('matplotlib.pyplot.show')
    @patch('imageio.imread')
    @patch('matplotlib.pyplot.imshow')
    @patch('matplotlib.pyplot.axis')
    def plot_earthquakes_test(self, axis_mock, imshow_mock, imread_mock,
                    show_mock, plot_clusters_mock, get_clusters_mock, \
                    dbscan_mock, initialize_database_mock,get_eq_locations_mock):
        """ Tests plot_earthquakes """
        print("\n**************\nTesting plot_earthquakes function.")

        get_eq_locations_mock.return_value='locations'
        initialize_database_mock.return_value='data'
        dbscan_mock.return_value='num_clusters'
        get_clusters_mock.return_value='clusters'
        plot_clusters_mock.return_value='None'
        show_mock.return_value='None'
        axis_mock.return_value='None' 
        imshow_mock.return_value='None'
        imread_mock.return_value='None'

        earthquake_clusters.plot_earthquakes("filename")

        #print(get_eq_locations_mock.call_args_list)
        #print(initialize_database_mock.call_args_list)
        #print(dbscan_mock.call_args_list)
        #print(get_clusters_mock.call_args_list)
        #print(plot_clusters_mock.call_args_list)
        #print(show_mock.call_args_list)

        get_eq_locations_mock.assert_has_calls([call("filename")])
        initialize_database_mock.assert_has_calls([call("locations")])
        dbscan_mock.assert_has_calls([call("data", 2, 4)])
        get_clusters_mock.assert_has_calls([call("data", "num_clusters")])
        plot_clusters_mock.assert_has_calls([call("clusters")])

        print("Test of plot_earthquakes correct")
