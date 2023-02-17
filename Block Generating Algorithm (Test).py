import bpy
import random
import bmesh
from mathutils import Vector


print("NEW RUN")
def calculate_volume(obj_name):
    # Get the 'Cube' object
    current_object = bpy.data.objects[obj_name]

    # Set the 'Cube' object as the active object in the current view layer
    bpy.context.view_layer.objects.active = current_object

    # Select the 'Cube' object
    current_object.select_set(True)

    context = bpy.context
    depsgraph = bpy.context.evaluated_depsgraph_get()
    obj = context.object
    object_eval = obj.evaluated_get(depsgraph)
    mesh_from_eval = bpy.data.meshes.new_from_object(object_eval)
    # Convert the mesh to a BMesh
    bm = bmesh.new()
    bm.from_mesh(mesh_from_eval)

    # Triangulate the faces
    bm.transform(obj.matrix_world)
    bmesh.ops.triangulate(bm, faces=bm.faces)

    # Calculate the volume of the mesh
    volume = 0
    for f in bm.faces:
        v1 = f.verts[0].co
        v2 = f.verts[1].co
        v3 = f.verts[2].co
        volume += v1.dot(v2.cross(v3)) / 6

    return volume


bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

for obj in bpy.data.objects:
    bpy.data.objects.remove(obj)
    print(obj)
    print("APPLES")

# Randomly generate first cube position and size
x = random.uniform(-10, 10)
y = random.uniform(-10, 10)
z = 0
width = random.uniform(1, 20)
depth = random.uniform(1, 20)
height = random.uniform(1, 20)

# Create first cube
bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
cube1 = bpy.context.active_object
cube1.scale = (width, depth, height)
# Generate 19 more prisms
objectnumber=50
for i in range(objectnumber): 
    # Randomly generate position and size of next prism
    face = random.choice(["front", "back", "top", "bottom", "left", "right"])
    if face == "front":
        shape = random.choice(["block", "cone", "sphere"])
        if shape == "block":
            width = random.uniform(1, 20)
            depth = random.uniform(1, 20)
            height = random.uniform(1, 20)
            x = x + width/2
            y = random.uniform(y - depth/2, y + depth/2)
            z = random.uniform(z - height/2, z + height/2)
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
            cube1 = bpy.context.active_object
            cube1.scale = (width, depth, height)
        if shape == "cone":
            conedepth = random.uniform(1, 20)
            radius1 = random.uniform(1, 20)
            radius2 = random.uniform(1, 20)
            x = x + conedepth/2
            y = random.uniform(y - radius1/2, y + radius1/2)
            z = random.uniform(z - radius1/2, z + radius1/2)
            bpy.ops.mesh.primitive_cone_add(radius1 = radius1, radius2 = radius2, depth = conedepth, location=(x, y, z))
            cone1 = bpy.context.active_object
            cone1.rotation_euler = (1.5708, 0 , 1.5708)
        if shape == "sphere":
            radius = random.uniform(1,20)
            x = x + radius/2
            y = random.uniform(y - radius/2, y + radius/2)
            z = random.uniform(z - radius/2, z + radius/2)
            bpy.ops.mesh.primitive_uv_sphere_add(radius = radius, location=(x, y, z))
    elif face == "back":
        width = random.uniform(1, 20)
        depth = random.uniform(1, 20)
        height = random.uniform(1, 20)
        x = x - width/2
        y = random.uniform(y - depth/2, y + depth/2)
        z = random.uniform(z - height/2, z + height/2)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
        cube1 = bpy.context.active_object
        cube1.scale = (width, depth, height)
    elif face == "top":
        depth = random.uniform(1, 20)
        width = random.uniform(1, 20)
        height = random.uniform(1, 20)
        x = random.uniform(x - width/2, x + width/2)
        y = y + depth/2
        z = random.uniform(z - height/2, z + height/2)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
        cube1 = bpy.context.active_object
        cube1.scale = (width, depth, height)
    elif face == "bottom":
        depth = random.uniform(1, 20)
        width = random.uniform(1, 20)
        height = random.uniform(1, 20)
        x = random.uniform(x - width/2, x + width/2)
        y = y - depth/2
        z = random.uniform(z - height/2, z + height/2)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
        cube1 = bpy.context.active_object
        cube1.scale = (width, depth, height)
    elif face == "left":
        height = random.uniform(1, 20)
        width = random.uniform(1, 20)
        depth = random.uniform(1, 20)
        x = random.uniform(x - width/2, x + width/2)
        y = random.uniform(y - depth/2, y + depth/2)
        z = z + height/2
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
        cube1 = bpy.context.active_object
        cube1.scale = (width, depth, height)
    else: # right
        height = random.uniform(1, 20)
        width = random.uniform(1, 20)
        depth = random.uniform(1, 20)
        x = random.uniform(x - width/2, x + width/2)
        y = random.uniform(y - depth/2, y + depth/2)
        z = z - height/2
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
        cube1 = bpy.context.active_object
        cube1.scale = (width, depth, height)
        

# Get all objects in the scene

volume = calculate_volume('Cube')
print("Volume of Cube before booleans:", volume)

# Get the 'Cube' object
cube = bpy.data.objects['Cube']

# Loop through all objects in the scene
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH' and obj.name != 'Cube':
        # Create a new boolean union modifier for the 'Cube' object
        bool_mod = cube.modifiers.new('bool_mod', 'BOOLEAN')
        bool_mod.operation = 'UNION'
        bool_mod.object = obj
        
        # Apply the modifier to the 'Cube' object
        bpy.ops.object.modifier_apply(modifier=bool_mod.name)



inside_volume = calculate_volume('Cube')
print("Volume of Cube after union:", inside_volume)


# Create a UV test sphere 
bpy.ops.mesh.primitive_uv_sphere_add(radius=35, location=(0, 0, 0))

# Get the active object and set its name to 'testsphere'
testsphere = bpy.context.active_object
testsphere.name = 'testsphere'

bool_mod = cube.modifiers.new('bool_mod', 'BOOLEAN')
bool_mod.operation = 'DIFFERENCE'
bool_mod.object = bpy.data.objects['testsphere']

outside_volume = calculate_volume('Cube')
print("Volume of Cube after difference:", outside_volume)

print("Fitness Score:", inside_volume-outside_volume*2)


# Get the 'Cube' object
cube = bpy.data.objects['Cube']
testsphere = bpy.data.objects['testsphere']

# Deselect all objects in the scene
for obj in bpy.context.scene.objects:
    obj.select_set(False)

# Select all objects in the scene except the 'Cube' object
for obj in bpy.context.scene.objects:
    if obj != cube and obj != testsphere:
        obj.select_set(True)
bpy.ops.object.delete()
