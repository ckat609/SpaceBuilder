import bpy
import os
import json

def getJson():
    filepath = bpy.data.filepath
    directory = os.path.dirname(filepath)
    jsonFile = os.path.join(directory, 'test.json')
    
    return jsonFile
    


def getSpaceDocument(jsonFile):
    spaceDocument = {}
    
    with open(jsonFile) as file:
        spaceDocument = json.load(file)
    
    return spaceDocument



def removeAllObjects():
    for object in bpy.data.objects:
        print(object)
        bpy.data.objects.remove(object,do_unlink=True,do_id_user=True,do_ui_user=True)
        
        
        
def removeAllCollections():
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)
    


def createWall(wall):
    name = f"wall{wall['id']}"
    emptyMesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, emptyMesh)

    for point in wall['points']:
        print(f"{point}")
        
    newWallCollection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(newWallCollection)
    newWallCollection.objects.link(obj)
    
    return obj
        
        
    
def createWalls(spaceDocument):
    removeAllObjects()
    removeAllCollections()
    
    for wall in spaceDocument['room']['walls']:
        points = wall['points']
        newWall = createWall(wall)
    
 



def drawWalls():
    return




aFile = getJson()
aSpaceDocument = getSpaceDocument(aFile) 
createWalls(aSpaceDocument)

