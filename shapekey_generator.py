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

def subdivide(obj, name, levels):
    modifier = obj.modifiers.new(type='SUBSURF', name=name)
    modifier.levels = levels
    return modifier
    
def create_voronoi_texture(noise_intensity, noise_scale):
    texture = bpy.data.textures.new('voronoi', type='VORONOI')
    texture.distance_metric = 'DISTANCE_SQUARED'
    texture.noise_intensity = noise_intensity
    texture.noise_scale = noise_scale
    return texture
    
def voronoi(obj, name, noise_intensity, noise_scale):
    modifier = obj.modifiers.new(type='DISPLACE', name=name)
    texture = create_voronoi_texture(random.uniform(1, 1.5), random.uniform(0.4, 0.7))
    modifier.texture = texture
    modifier.strength = random.uniform(0.1, 0.3)
    return modifier
        
def voronois(obj, iterations):
    for i in range(iterations):
        name = 'Voronoi' + str(i)
        modifier = voronoi(obj, name, random.uniform(1, 1.5), random.uniform(0.4, 0.7))
        bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=False, modifier=name)
            
def create_wood_texture(turbulence):
    texture = bpy.data.textures.new('wood', type='WOOD')
    texture.turbulence = turbulence # 0 30
    texture.noise_scale = 2.0
    texture.wood_type = 'RINGNOISE'
    texture.noise_basis_2 = 'SIN'
    texture.noise_type = 'SOFT_NOISE'
    texture.noise_basis = 'VORONOI_F4'
    return texture     

def wood(obj, name, turbulence):
    modifier = obj.modifiers.new(type='DISPLACE', name=name)
    texture = create_wood_texture(turbulence)
    modifier.texture = texture
    modifier.strength = 0.18
    return modifier
        
def woods(obj, turbulences):
    for i, turbulence in enumerate(turbulences):
        name = 'Wood' + str(i)
        modifier = wood(obj, name, turbulence)
        bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=False, modifier=name)       
            
def taper(obj, name, factor):
    modifier = obj.modifiers.new(type='SIMPLE_DEFORM', name=name)
    modifier.deform_method = 'TAPER'
    modifier.factor = factor
            
def tapers(obj, factors):
    for i, factor in enumerate(factors):
        name = 'Taper' + str(i) 
        modifier = taper(obj, name, factor)
        bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=False, modifier=name)
        
        
def run():
    obj = create_cube()
    modifier = subdivide(obj, 'Subdivide', 4)
    #offset_vertices(obj, 1)
    apply_modifiers(obj)
    
    voronois(obj, 5)  
    tapers(obj, [-1.5, 1.5])
    woods(obj, range(0, 30, 2))
        
clean_scene()
run()