import bpy
bpy.context.preferences.addons['cycles'].preferences.get_devices()
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA' 
bpy.context.preferences.addons['cycles'].preferences.devices[0].use = True
bpy.data.scenes["Scene"].render.filepath = "/tmp/blender/output.png"
bpy.ops.render.render(write_still=True)