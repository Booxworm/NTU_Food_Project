import googlemaps
from math import sin, cos, sqrt, atan2, radians

"""
#lat and lon of the mouse click
import arcpy
import pythonaddins

class XYTool(object):
  """Implementation for xy_addin.XYTool (Tool)"""
     def __init__(self):
            self.enabled = True
            self.cursor=3
     def onMouseDownMap(self, x, y, button, shift):

            mxd=arcpy.mapping.MapDocument("current")
            df = arcpy.mapping.ListDataFrames(mxd)[0]
            pt=arcpy.PointGeometry(arcpy.Point(x,y))
            #ptfeat=arcpy.management.CopyFeatures(pt,r"in_memory\pt")
            print x,y
            pythonaddins.MessageBox(str(x) + ", " + str(y), 'Coordinates', 0)  """

#calc the dist between the user loc and the canteens



def dist(a,b):
    # Approximate radius of earth in km
    R = 6373.0


   lat1 = radians(a[0])
   lon1 = radians(a[1])
   lat2 = radians(b[0])
   lon2 = radians(b[1])

   #dist between the user loc and each canteen
   dlon = lon2 - lon1
   dlat = lat2 - lat1

   a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
   c = 2 * atan2(sqrt(a), sqrt(1 - a))

   distance = R * c

   return distance
