import bpy
import os
import bmesh
import mathutils
import json

M = 1000
wallPrefix = "wall"
baseboardPrefix = "baseboard"
floorPrefix = "floor"
ceilingPrefix = "ceiling"

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
        bpy.data.objects.remove(object,do_unlink=True,do_id_user=True,do_ui_user=True)
        
        
        
def removeAllCollections():
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)
        
        


def createCeiling(spaceDocument):
    name = ceilingPrefix
    emptyMesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, emptyMesh)
    
    vertices = []
    for wall in spaceDocument['room']['walls']:
        for point in wall['points']:
            vertex = mathutils.Vector((point['x']/M, point['y']/M, point['z']/M))

            if(point['z'] != 0 and vertex not in vertices):
                vertices.append(mathutils.Vector(vertex))
                print(vertex)


    objMesh = obj.data
    bm = bmesh.new()

    for v in vertices:
        bm.verts.new(v)
    bm.verts.ensure_lookup_table()

    for idx, v in enumerate(bm.verts):
        if(idx == len(bm.verts)-1):
            bm.edges.new([bm.verts[len(bm.verts)-1], bm.verts[0]])
        else:
            bm.edges.new([bm.verts[idx], bm.verts[idx+1]])

    bm.faces.new(bm.verts)

    bm.to_mesh(objMesh)
    bm.free()


    newWallCollection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(newWallCollection)
    newWallCollection.objects.link(obj)
    
    return obj
        
        
    
def createFloor(spaceDocument):
    name = floorPrefix
    emptyMesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, emptyMesh)
    
    vertices = []
    for wall in spaceDocument['room']['walls']:
        for point in wall['points']:
            vertex = mathutils.Vector((point['x']/M, point['y']/M, point['z']/M))

            if(point['z'] == 0 and vertex not in vertices):
                vertices.append(mathutils.Vector(vertex))


    objMesh = obj.data
    bm = bmesh.new()

    for v in vertices:
        bm.verts.new(v)
    bm.verts.ensure_lookup_table()

    for idx, v in enumerate(bm.verts):
        if(idx == len(bm.verts)-1):
            bm.edges.new([bm.verts[len(bm.verts)-1], bm.verts[0]])
        else:
            bm.edges.new([bm.verts[idx], bm.verts[idx+1]])

    bm.faces.new(bm.verts)

    bm.to_mesh(objMesh)
    bm.free()


    newWallCollection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(newWallCollection)
    newWallCollection.objects.link(obj)
    
    return obj
        
        
    
def createWalls(spaceDocument):

    for wall in spaceDocument['room']['walls']:
        name = f"{wallPrefix}{wall['id']}"
        emptyMesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, emptyMesh)

        vertices = []
        for point in wall['points']:
            vertices.append(mathutils.Vector((point['x']/M, point['y']/M, point['z']/M)))

            
        objMesh = obj.data
        bm = bmesh.new()

        for v in vertices:
            bm.verts.new(v)
        bm.verts.ensure_lookup_table()

        for idx, v in enumerate(bm.verts):
            if(idx == len(bm.verts)-1):
                bm.edges.new([bm.verts[len(bm.verts)-1], bm.verts[0]])
            else:
                bm.edges.new([bm.verts[idx], bm.verts[idx+1]])

        bm.faces.new(bm.verts)

        bm.to_mesh(objMesh)
        bm.free()


        newWallCollection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(newWallCollection)
        newWallCollection.objects.link(obj)
    
 






aFile = getJson()
aSpaceDocument = getSpaceDocument(aFile)

removeAllObjects()
removeAllCollections()

# createWalls(aSpaceDocument)
# createFloor(aSpaceDocument)
createCeiling(aSpaceDocument)
