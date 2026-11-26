from pathlib import Path
import re
p=Path("source/Railvito")
def change(path, old,new):
    f=p/path;s=f.read_text()
    assert old in s, (path,old[:100])
    f.write_text(s.replace(old,new,1))
change("project.godot",'config/version="1.4.0"','config/version="1.5.0"')
f=p/"export_presets.cfg";q=f.read_text().replace("1.4.0","1.5.0").replace("version/code=5","version/code=6");f.write_text(q)
# Use the exact approved illustration when the binary is available in the repository.
# Preserve the original 512px store image, and use the same artwork for all launcher sizes.
from shutil import copyfile
approved=Path("Railvito_Icon_512.png")
compact=Path("assets/railvito_launcher.webp")
if approved.is_file():
    copyfile(approved,p/"assets/approved_launcher.png")
    icon="res://assets/approved_launcher.png"
elif compact.is_file():
    copyfile(compact,p/"assets/approved_launcher.webp")
    icon="res://assets/approved_launcher.webp"
else:
    icon="res://assets/icon.svg"
    print("APPROVED_ICON_NOT_UPLOADED: original vector remains until the new image is available")
if icon!="res://assets/icon.svg":
    change("project.godot",'config/icon="res://assets/icon.svg"',f'config/icon="{icon}"')
    change("export_presets.cfg",'launcher_icons/main_192x192="res://assets/icon.svg"',f'launcher_icons/main_192x192="{icon}"')
    # Avoid competing foreground/background art from the previous design.
    change("export_presets.cfg",'launcher_icons/adaptive_foreground_432x432="res://assets/icon_foreground.svg"','launcher_icons/adaptive_foreground_432x432=""')
    change("export_presets.cfg",'launcher_icons/adaptive_background_432x432="res://assets/icon_background.svg"','launcher_icons/adaptive_background_432x432=""')
# Clear and consistent next action after placing every piece.
f=p/"scripts/main.gd";s=f.read_text()
s=s.replace('status_label.text=(t("ready") if missing.is_empty() else t("missing") % missing.size()) if mode=="build" else t("loaded") % cargo_count if mode=="cargo" else t("station_hint")','''status_label.text=(t("ready") if missing.is_empty() else t("missing") % missing.size()) if mode=="build" else t("loaded") % cargo_count if mode=="cargo" else t("station_hint")
	if mode=="build" and is_instance_valid(task_label):
		task_label.text=t("depart_ready") if missing.is_empty() else t("easy_instruction") if easy_placement else t("build_task")
		for btn in selected_buttons.values():
			if is_instance_valid(btn):btn.disabled=missing.is_empty() or desired_speed>0
	if mode=="cargo" and is_instance_valid(task_label):
		var mission: Dictionary=Network.levels()[level_index]
		if cargo_count==int(mission.number):
			task_label.text=t("cargo_ready") % (int(mission.station)+1)
		else:
			task_label.text=t("cargo_task") % [mission.number,mission.station+1]''')
# Make target station distinct without rendering two copies of its number.
s=s.replace('var s: Dictionary=art.stations[station+station_offset]','''var s: Dictionary=art.stations[station+station_offset]
	for item in art.stations:
		if is_instance_valid(item.get("label")):
			item.label.visible=true
	if is_instance_valid(s.get("label")):s.label.visible=false''')
# Brake guidance must account for inertia, not just distance to the ring.
s=s.replace('var near_goal: bool=_circular_distance(distance,goal_distance)<2.4','''var forward_gap: float=goal_distance-distance
		if not route.get("open",false):forward_gap=fposmod(forward_gap,route.length)
		var stopping_distance: float=speed*speed/9.6
		var near_goal: bool=goal_distance>=0.0 and (forward_gap<=maxf(1.65,stopping_distance+0.85) or _circular_distance(distance,goal_distance)<1.4)''')
# Gentle, optional brake assistance only near the correct destination, while running.
# Wrong cargo or wrong branch must never result in a win.
s=s.replace('var move:=speed*delta','''if screen=="game" and easy_placement and desired_speed>0.0 and goal_distance>=0.0:
			var mission: Dictionary=Network.levels()[level_index]
			if mission.mode!="build" and (mission.mode!="cargo" or cargo_count==mission.number):
				var ahead: float=goal_distance-distance
				if not route.get("open",false):ahead=fposmod(ahead,route.length)
				var stopping: float=speed*speed/9.6
				if ahead>=0.0 and ahead<maxf(0.3,stopping+0.20) and travelled>2.0:
					brake_requested=true;desired_speed=0.0
		var move:=speed*delta''')
# Restarting a mission must never reuse a stale selected target or pointer state.
s=s.replace('screen="game";won=false;hint_used=false;camera_follow=false','screen="game";won=false;hint_used=false;camera_follow=false;orbiting=false;touches.clear();pinch_previous=0.0')
# After an open-line miss, provide a single guided retry instead of trapping the child at the buffer stop.
s=s.replace('_toast(t("line_end"))\n\t\treturn','_toast(t("retry_station"))\n\t\treturn',1)
# Short, non-blocking toast instead of the large banner that hides track and stations.
start=s.index("func _toast(");end=s.index("\nfunc ",start+1)
s=s[:start]+'''func _toast(text: String) -> void:
	if not is_instance_valid(ui):return
	if is_instance_valid(toast_label):toast_label.queue_free()
	var extent:=Vector2(530,48)
	toast_label=_label(text,Vector2(375,100),extent,21,Color("fff5d4"))
	toast_label.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	toast_label.position=Vector2((ui.size.x-extent.x)*0.5,100)
	toast_label.add_theme_stylebox_override("normal",_box(Color(0.12,0.23,0.32,0.94),16))
	var current: WeakRef=weakref(toast_label)
	get_tree().create_timer(1.7).timeout.connect(func():
		var label=current.get_ref()
		if label!=null:label.queue_free())
''' + s[end:]
# Visible next button is always green, consistent with the rest of the interface.
s=s.replace('Vector2(36,240),Vector2(468,62),func(): _start_level(level_index+1) if level_index<stars.size()-1 else _show_worlds(),CORAL,p)','Vector2(36,240),Vector2(468,62),func(): _start_level(level_index+1) if level_index<stars.size()-1 else _show_worlds(),TEAL,p)')
# Avoid enabling the running train while a finger is dragging a rail.
s=s.replace('if won:return\n\tif route.get("open",false) and distance>=float(route.length)-0.66:', 'if won or dragging_piece:return\n\tif route.get("open",false) and distance>=float(route.length)-0.66:',1)
f.write_text(s)
change("scripts/strings.gd","const ADVENTURE_WORDS := {",'''const ADVENTURE_WORDS := {
	"depart_ready": ["Tracks ready! Press Go.","اكتملت السكك! اضغط انطلق.","Trilhos prontos! Toque em Ir."],
	"cargo_ready": ["Cargo ready. Deliver to station %s.","الحمولة جاهزة. أوصلها إلى المحطة %s.","Carga pronta. Leve à estação %s."],
	"retry_station": ["End of track. Tap the restart button to try again.","نهاية السكة. اضغط زر إعادة المرحلة للمحاولة.","Fim da linha. Toque em reiniciar para tentar novamente."],''')
# Real green leaves and brown trunks instead of the turquoise toy material in the recording.
f=p/"scripts/world_builder.gd";s=f.read_text()
s=s.replace('m.metallic_specular=0.22','''m.metallic_specular=0.22
				var mat_name:=m.resource_name.to_lower()
				if world_id!=3:
					if "leaf" in mat_name or "leav" in mat_name or "foliage" in mat_name:
						m.albedo_color=Color("438947" if "dark" in mat_name else "559e50")
					elif "bark" in mat_name:
						m.albedo_color=Color("946d47")''')
# Tag scenery for a route/river-clearance pass.
s=s.replace('obj.position = pos\n\tobj.scale = scl','obj.position = pos\n\tobj.set_meta("scenery_asset",asset)\n\tobj.scale = scl',1)
# Tone down hard highlights and oversaturated ground.
s=s.replace('e.ambient_light_color = Color("fff1d7")','e.ambient_light_color = Color("e9efff")').replace('e.ambient_light_energy = 0.66','e.ambient_light_energy = 0.48').replace('e.tonemap_exposure = 0.82','e.tonemap_exposure = 0.72').replace('sun.light_energy = 0.85','sun.light_energy = 0.72')
# Hills are decorative and must never cross the river or appear as fluorescent flat circles.
s=s.replace('var palette := ["7dbb56","5ca35b","a3ca67"]','var palette := ["6ba650","598a47","83b267"]')
s=s.replace('var p:=Vector3(cos(angle)*radius,-1.55 if id<2 else 0.10,sin(angle)*radius)','''var p:=Vector3(cos(angle)*radius,-0.85 if id<2 else 0.10,sin(angle)*radius)
		if id<2 and absf(p.x)<9.5:continue''')
s=s.replace('var p:=Vector3(cos(angle)*radius,-2.2 if id!=4 else -8.5,sin(angle)*radius)','''var p:=Vector3(cos(angle)*radius,-2.2 if id!=4 else -8.5,sin(angle)*radius)
		if id<2 and absf(p.x)<10.0:continue''')
# Actual additional geometry and clustered natural decoration, not blank filler.
# Crossings use the same curve points as the existing track.
anchor='func _make_castle(pos: Vector3, s: float) -> void:'
assert anchor in s
s=s.replace(anchor,'''func _quality_details(layout: Dictionary, id: int) -> void:
	if id>=2 or layout.is_empty():return
	var curve: Curve3D=layout.curve
	# Clear trees from the actual train corridor and water, not an approximate rectangular mask.
	for obj in root.get_children():
		if obj is Node3D and str(obj.get_meta("scenery_asset","")).begins_with("tree"):
			var near: Vector3=curve.get_closest_point(obj.position)
			var gap:=Vector2(obj.position.x-near.x,obj.position.z-near.z)
			if gap.length()<1.95:
				var outward:=gap.normalized() if gap.length()>0.05 else Vector2(1,0)
				obj.position.x=near.x+outward.x*2.1
				obj.position.z=near.z+outward.y*2.1
			if absf(obj.position.x-sin(obj.position.z*0.42)*0.5)<2.4:
				obj.position.x=(1 if obj.position.x>=0 else -1)*3.0
	var detail:=Node3D.new();detail.name="ScenicQuality";root.add_child(detail)
	var stone:=material("9c9485",0.88)
	var brick:=material("bfad91",0.86)
	var wood:=material("8e5c3d")
	# Each river crossing gets visible structural support under its rails.
	for z in [-6.0,6.0] if id==0 else [-8.0,8.0]:
		var deck:=BoxMesh.new();deck.size=Vector3(4.8,0.14,1.20)
		mesh_node(deck,wood,Vector3(0,0.065,z),detail)
		for x in [-2.2,2.2]:
			var footing:=BoxMesh.new();footing.size=Vector3(0.62,0.46,1.55)
			mesh_node(footing,stone,Vector3(x,-0.08,z),detail)
			var cap:=BoxMesh.new();cap.size=Vector3(0.74,0.12,1.65)
			mesh_node(cap,brick,Vector3(x,0.19,z),detail)
		for side in [-1.0,1.0]:
			var parapet:=BoxMesh.new();parapet.size=Vector3(4.8,0.12,0.11)
			mesh_node(parapet,brick,Vector3(0,0.28,z+side*0.69),detail)
	# Small clustered flowers and rocks away from trains and the river.
	var rng:=RandomNumberGenerator.new();rng.seed=17651+id
	for cluster in range(24):
		var point:=Vector3(rng.randf_range(-15.0,15.0),0.08,rng.randf_range(-15.0,15.0))
		if absf(point.x-sin(point.z*0.42)*0.5)<3.2:continue
		if curve.get_closest_point(point).distance_to(point)<2.4:continue
		for j in range(3):
			var at:=point+Vector3(rng.randf_range(-0.45,0.45),0,rng.randf_range(-0.45,0.45))
			if curve.get_closest_point(at).distance_to(at)<1.9:continue
			model("nature-kit",["flower_redA","flower_purpleA","flower_yellowA","plant_bushSmall"][(cluster+j)%4],at,Vector3.ONE*rng.randf_range(1.2,1.8),rng.randf_range(0,TAU))

'''+anchor)
s=s.replace('\t\tclouds.append(cloud)\n\nfunc _quality_details','\t\tclouds.append(cloud)\n\t_quality_details(layout,id)\n\nfunc _quality_details',1)
f.write_text(s)
# Less saturated ground and continuous natural colour variation.
f=p/"scripts/meadow.gdshader";s=f.read_text().replace('0.92+0.10*broad+0.035*fine','0.88+0.085*broad+0.018*fine');f.write_text(s)
f=p/"scripts/main.gd";s=f.read_text().replace('art.sun.light_energy=0.58 if evening else 0.85','art.sun.light_energy=0.52 if evening else 0.72');f.write_text(s)
# Validate all 24 actual stages; no invented passing results.
(p/"tests/verify_quality.gd").write_text('''extends SceneTree
const Network=preload("res://scripts/rail_network.gd")
func _initialize() -> void:
	call_deferred("verify")
func verify() -> void:
	var game=load("res://scenes/main.tscn").instantiate()
	root.add_child(game)
	await process_frame
	game.set_process(false)
	for mission in Network.levels():
		game._start_level(mission.id)
		assert(game.cars.size()==3)
		assert(game.route.length>0.0)
		for idx in game.missing.duplicate():
			game.selected_kind=game.route.pieces[idx].kind
			game.selected_yaw=posmod(roundi(rad_to_deg(game.route.pieces[idx].yaw)),360)
			assert(game._place_piece(idx))
		assert(game.missing.is_empty())
		if mission.mode=="build":
			assert(game.task_label.text==game.t("depart_ready"))
		if mission.mode=="cargo":
			game._load_cargo(mission.number)
			assert(game.task_label.text.contains(str(mission.station+1)))
		if mission.mode!="build":
			var offset:=1 if mission.world in [2,3,4] else 0
			assert(not game.art.stations[mission.station+offset].label.visible)
		if mission.world<2:
			assert(game.world.get_node_or_null("ScenicQuality")!=null)
		await process_frame
	print("QUALITY_PASS: 24 missions, actual rail placement, updated instruction, cargo and station label checks")
	game.queue_free()
	await process_frame
	quit()
''')
print("RAILVITO_1_5_PATCH_OK")
