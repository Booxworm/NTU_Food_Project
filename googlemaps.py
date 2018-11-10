import googlemaps

                                     
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
                                     
                                     
                                     
                                     
                                     
