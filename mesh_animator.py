import bpy
import math
import random

def clean_scene():
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)
    for obj in bpy.data.textures:
        bpy.data.textures.remove(obj)
        
def create_cube():
    bpy.ops.mesh.primitive_cube_add(size=1)
    return bpy.context.object    

def create_voronoi_texture(noise_intensity, noise_scale):
    texture = bpy.data.textures.new('voronoi', type='VORONOI')
    texture.distance_metric = 'DISTANCE_SQUARED'
    texture.noise_intensity = noise_intensity
    texture.noise_scale = noise_scale
    return texture

def subdivide(obj, name, levels):
    modifier = obj.modifiers.new(type='SUBSURF', name=name)
    modifier.levels = levels
    
def displace(obj, name):
    modifier = obj.modifiers.new(type='DISPLACE', name=name)
    texture = create_voronoi_texture(random.uniform(1, 1.5), random.uniform(0.4, 0.7))
    modifier.texture = texture
    modifier.strength = random.uniform(0.1, 0.3)
    
def offset_vertices(obj, scale):
    for vertex in obj.data.vertices:
        direction = vertex.normal
        direction[0] += random.uniform(-0.5,0.5)
        direction[1] += random.uniform(-0.5,0.5)
        direction[2] += random.uniform(-0.5,0.5)
        vertex.co += direction * scale
        
def apply_modifiers(obj):
    for modifier in obj.modifiers:
        bpy.ops.object.modifier_apply(modifier=modifier.name)
        
def create_rock():
    cube = create_cube()
    subdivide(cube, 'subdivide', 4)
    displace(cube, 'displace')
    offset_vertices(cube, 1)
    apply_modifiers(cube)
    
def other():
    #bpy.ops.object.modifier_add(type='SUBSURF')
    #1bpy.context.object.modifiers["Subdivision"].levels = 3
    
    subdiv_modifier = cube.modifiers.new(type='SUBSURF', name="subdiv_cube")
    subdiv_modifier.levels = 5
    bpy.ops.object.modifier_apply(modifier="subdiv_cube")

    cast_cube = cube.modifiers.new(type='CAST', name="cast_cube")
    bpy.ops.object.modifier_apply(modifier="cast_cube")

    decimate_cube = cube.modifiers.new(type='DECIMATE', name="decimate_cube")
    decimate_cube.decimate_type = 'DISSOLVE'
    decimate_cube.angle_limit = math.radians(20)
    decimate_cube.use_dissolve_boundaries = True
    bpy.ops.object.modifier_apply(modifier="decimate_cube")


        
clean_scene()
create_rock()