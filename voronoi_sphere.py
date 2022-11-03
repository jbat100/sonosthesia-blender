import bpy
import math

def clean_scene():
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)
        
def create_cube():
    bpy.ops.mesh.primitive_cube_add(size=1)
    return bpy.context.object    
        
def create_sphere():
    cube = create_cube()    
    print(cube)    
    #bpy.ops.object.modifier_add(type='SUBSURF')
    #1bpy.context.object.modifiers["Subdivision"].levels = 3
    
    subdiv_modifier = cube.modifiers.new(type='SUBSURF', name="subdiv_cube")
    subdiv_modifier.levels = 5
    cast_cube = cube.modifiers.new(type='CAST', name="cast_cube")
    decimate_cube = cube.modifiers.new(type='DECIMATE', name="decimate_cube")
    decimate_cube.decimate_type = 'DISSOLVE'
    decimate_cube.angle_limit = math.radians(20)
    decimate_cube.use_dissolve_boundaries = True



        
clean_scene()
create_sphere()