import googlemaps
from math import sin, cos, sqrt, atan2, radians

                                     
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
            pythonaddins.MessageBox(str(x) + ", " + str(y), 'Coordinates', 0)  
 
#calc the dist between the user loc and the canteens

# approximate radius of earth in km
R = 6373.0
"""lat and lon of each canteen
can1=(1.346763,103.686018)
can2=(1.348434,103.685535)
can9=(1.352515,103.685760)
can11=(1.355156,103.686944)
can13=(1.351925,103.681628)
can14=(1.352961,103.682432)
can16=(1.350618,103.681652)
koufu=(1.342642,103.682791)
NS=(1.347243,103.680236)
quad=(1.345193,103.680549)"""

lat=[]
lat[0]=1.346763
lat[1]=1.348434
lat[2]=1.352515
lat[3]=1.355156
lat[4]=1.351925
lat[5]=1.352961
lat[6]=1.350618
lat[7]=1.342642
lat[8]=1.347243
lat[9]=1.345193

lon=[]
lon[0]=103.686018
lon[1]=103.685535
lon[2]=103.685760
lon[3]=103.686944
lon[4]=103.681628
lon[5]=103.682432
lon[6]=103.681652
lon[7]=103.682791
lon[8]=103.680236
lon[9]=103.680549

for i in range(10):

   lat1 = radians(lat[i])
   lon1 = radians(lon[i])
   lat2 = radians(x)
   lon2 = radians(y)

   #dist between the user loc and each canteen
   dlon = lon2 - lon1
   dlat = lat2 - lat1

   a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
   c = 2 * atan2(sqrt(a), sqrt(1 - a))

   distance = R * c

   print("Result:", distance)
                                     
                                     
                                     
                                     
                                     
