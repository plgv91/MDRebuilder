import arcpy

newfcName = 'newfc.shp'

outpath = 'C:\\Users\\PLGV\\Downloads'

# Declaration
arcpy.env.overwriteOutput = True

arcpy.env.workspace = outpath

# Create new Shapefile and add FIELDS
newfc = arcpy.CreateFeatureclass_management(outpath, newfcName, "Point")
# get the coordinate system by describing a feature class
dsc = arcpy.Describe("newfc.shp")

coord_sys = dsc.spatialReference

try:
   # run the tool
   arcpy.DefineProjection_management(newfcName, coord_sys)

   # print messages when the tool runs successfully
   print(arcpy.GetMessages(0))

except arcpy.ExecuteError:
   print(arcpy.GetMessages(2))

except Exception as ex:
   print(ex.args[0])

arcpy.AddField_management(newfc, "I", "FLOAT", field_length=50)
arcpy.AddField_management(newfc, "Z", "STRING", field_length=50)
arcpy.AddField_management(newfc, "X", "STRING", field_length=50)
arcpy.AddField_management(newfc, "Y", "STRING", field_length=50)

# Reference Cursors
cursor = arcpy.da.InsertCursor(newfc, ["I", "Z", "X", "Y"])

# Read File
a = open("C:\\Users\\PLGV\\Downloads\\COORDENADAS.txt", "r")

inputF = a.readlines()

for line in inputF:

    xCoordinate, yCoordinate, zValue, iValue = line.split(" ")

    newRow = (float(iValue), str(zValue), str(xCoordinate), str(yCoordinate))

    cursor.insertRow(newRow)

a.close()



'''
cursor=arcpy.da.InsertCursor(newfc, [ "SHAPE@XY", "X", "Y", "Z", "I"])

# Read File 
a = open("C:/FLOOD/IKEJA AND KOSOFE/DEM/532722.txt","r")

inputF = a.readlines()

for line in inputF:
    xCoordinate, yCoordinate, zValue, iValue = line.split(" ")

    xy = (float(xCoordinate), float(yCoordinate))

    newRow = (xy, str(xCoordinate), str(yCoordinate), str(zValue), float(iValue))

    cursor.insertRow(newRow)
'''