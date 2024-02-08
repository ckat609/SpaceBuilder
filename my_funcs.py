import bpy
import os
import bmesh
import mathutils
import json
from operator import itemgetter

M = 1000


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
        bpy.data.objects.remove(object, do_unlink=True,
                                do_id_user=True, do_ui_user=True)


def removeAllCollections():
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)


def addMeshToObject(vertices, obj):
    objMesh = obj.data
    bm = bmesh.new()

    for v in vertices:
        bm.verts.new(v)
    bm.verts.ensure_lookup_table()

    for idx, v in enumerate(bm.verts):
        if (idx == len(bm.verts)-1):
            bm.edges.new([bm.verts[len(bm.verts)-1], bm.verts[0]])
        else:
            bm.edges.new([bm.verts[idx], bm.verts[idx+1]])

    bm.faces.new(bm.verts)

    bm.to_mesh(objMesh)
    bm.free()

    return obj


def linkObjectToCollection(obj, collectionName):

    if collectionName not in bpy.data.collections:
        collection = bpy.data.collections.new(collectionName)
        bpy.context.scene.collection.children.link(collection)

    bpy.data.collections[collectionName].objects.link(obj)
    print(bpy.data.collections[collectionName])


def drawCeiling(walls):
    name = "ceiling"
    emptyMesh = bpy.data.meshes.new(name)
    tempObj = bpy.data.objects.new(name, emptyMesh)

    vertices = []
    for wall in walls:
        points = wall['points']
        points.reverse()

        for point in wall['points']:
            vertex = mathutils.Vector(
                (point['x']/M, point['y']/M, point['z']/M))

            if (point['z'] != 0 and vertex not in vertices):
                vertices.append(mathutils.Vector(vertex))

    newObj = addMeshToObject(vertices, tempObj)
    linkObjectToCollection(newObj, name)

    return newObj


def drawFloor(walls):
    name = "floor"
    emptyMesh = bpy.data.meshes.new(name)
    tempObj = bpy.data.objects.new(name, emptyMesh)

    vertices = []
    for wall in walls:
        for point in wall['points']:
            vertex = mathutils.Vector(
                (point['x']/M, point['y']/M, point['z']/M))

            if (point['z'] == 0 and vertex not in vertices):
                vertices.append(mathutils.Vector(vertex))

    newObj = addMeshToObject(vertices, tempObj)
    linkObjectToCollection(newObj, name)

    return newObj


def drawWalls(walls):
    for wall in walls:
        name = f"wall{wall['id']}"
        emptyMesh = bpy.data.meshes.new(name)
        tempObj = bpy.data.objects.new(name, emptyMesh)

        vertices = []
        for point in wall['points']:
            vertices.append(mathutils.Vector(
                (point['x']/M, point['y']/M, point['z']/M)))

        newObj = addMeshToObject(vertices, tempObj)
        linkObjectToCollection(newObj, name)


def drawObstructions(obstructions):
    for obstruction in obstructions:
        elementType = obstruction['type']
        wallId = obstruction['wallId']
        x = obstruction['x']/M
        y = obstruction['y']/M
        width = obstruction['width']/M
        height = obstruction['height']/M
        depth = obstruction['depth']/M

        emptyMesh = bpy.data.meshes.new(elementType)
        tempObj = bpy.data.objects.new(elementType, emptyMesh)

        verticesBack = [mathutils.Vector((x, 0, y)),  mathutils.Vector(
            (x+width, 0, y)), mathutils.Vector((x+width,  0, y-height)), mathutils.Vector((x,  0, y-height))]
        verticesFront = [mathutils.Vector((x, -depth, y)),  mathutils.Vector(
            (x+width, -depth, y)), mathutils.Vector((x+width,  -depth, y-height)), mathutils.Vector((x,  -depth, y-height))]
        verticesTop = [mathutils.Vector((x, 0, y)),  mathutils.Vector(
            (x+width, 0, y)), mathutils.Vector((x, -depth, y)),  mathutils.Vector(
            (x+width, -depth, y))]
        verticesBottom = [mathutils.Vector((x+width,  0, y-height)), mathutils.Vector(
            (x,  0, y-height)), mathutils.Vector((x+width,  -depth, y-height)), mathutils.Vector((x,  -depth, y-height))]
        verticesLeft = [mathutils.Vector((x, 0, y)), mathutils.Vector(
            (x,  0, y-height)), mathutils.Vector((x,  -depth, y-height)), mathutils.Vector((x, -depth, y))]
        verticesRight = [mathutils.Vector((x+width, 0, y)), mathutils.Vector(
            (x+width,  0, y-height)), mathutils.Vector((x+width,  -depth, y-height)), mathutils.Vector((x+width, -depth, y))]
        vertices = verticesLeft + verticesRight

        newObj = addMeshToObject(vertices, tempObj)
        linkObjectToCollection(newObj, f"wall{wallId}")


aFile = getJson()
aSpaceDocument = getSpaceDocument(aFile)
walls = aSpaceDocument['room']['walls']
obstructions = aSpaceDocument['room']['obstructions']

removeAllObjects()
removeAllCollections()

drawWalls(walls)
drawFloor(walls)
drawCeiling(walls)
drawObstructions(obstructions)


# print(f"{obstructions}")
