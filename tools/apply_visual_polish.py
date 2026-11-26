from pathlib import Path
import re
p=Path("source/Railvito")

def edit(path, pairs):
    f=p/path
    s=f.read_text()
    for old,new in pairs:
        assert old in s, f"Missing expected source in {path}: {old[:100]}"
        s=s.replace(old,new,1)
    f.write_text(s)

def function(s,name,new):
    start=s.index("func "+name+"(")
    end=s.find("\nfunc ",start+1)
    if end<0:end=len(s)
    return s[:start]+new.strip()+"\n"+s[end:]

# Keep a real landscape viewport, expanding the canvas instead of cropping the 16:9 content.
edit("project.godot",[
('config/version="1.3.0"','config/version="1.4.0"'),
('window/stretch/aspect="keep"','window/stretch/aspect="expand"')])
f=p/"export_presets.cfg";q=f.read_text().replace("1.3.0","1.4.0").replace("version/code=4","version/code=5");assert 'version/code=5' in q;f.write_text(q)

# Original, layered, scalable launcher art. No faces, text, or borrowed trademarks.
icon_defs='''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#0753ad"/><stop offset=".58" stop-color="#37b8f0"/><stop offset="1" stop-color="#b6f6fc"/></linearGradient>
<linearGradient id="green" x2="0" y2="1"><stop stop-color="#9eeb70"/><stop offset="1" stop-color="#1b9352"/></linearGradient>
<linearGradient id="blue" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#9aeaff"/><stop offset=".25" stop-color="#278dea"/><stop offset=".75" stop-color="#104ea7"/><stop offset="1" stop-color="#123269"/></linearGradient>
<linearGradient id="red" x2="0" y2="1"><stop stop-color="#ff9e68"/><stop offset=".4" stop-color="#ed4431"/><stop offset="1" stop-color="#a01929"/></linearGradient>
<linearGradient id="gold" x2="0" y2="1"><stop stop-color="#fff6a3"/><stop offset=".45" stop-color="#f9c340"/><stop offset="1" stop-color="#b56b17"/></linearGradient>
<linearGradient id="steel" x2="1" y2="1"><stop stop-color="#abc8e4"/><stop offset=".35" stop-color="#395a78"/><stop offset="1" stop-color="#182d4c"/></linearGradient>
<radialGradient id="lamp"><stop stop-color="#fff"/><stop offset=".6" stop-color="#fff0a1"/><stop offset="1" stop-color="#ffac28"/></radialGradient>
</defs>'''
background='''<rect width="512" height="512" fill="url(#sky)"/>
<circle cx="403" cy="87" r="49" fill="#fff4b0" opacity=".88"/>
<g fill="#f4fcff" opacity=".88"><ellipse cx="97" cy="81" rx="63" ry="20"/><circle cx="86" cy="66" r="29"/><circle cx="117" cy="64" r="31"/><ellipse cx="418" cy="157" rx="62" ry="18"/></g>
<path d="M0 263L106 146 170 222 258 106 386 239 455 162 512 225V512H0Z" fill="#4e8caf"/>
<path d="M65 194L106 146 148 197 106 180ZM213 160L258 106 310 168 258 140Z" fill="#e5f8ff"/>
<path d="M0 274Q109 210 221 282T512 258V512H0Z" fill="url(#green)"/>
<path d="M0 380Q104 306 226 358T512 320V512H0Z" fill="#267e50"/>
<path d="M162 512L232 336H281L361 512Z" fill="#84684e"/>
<path d="M182 512L243 336M340 512L270 336" stroke="#c9dfe6" stroke-width="13"/>
<g stroke="#513c32" stroke-width="10"><path d="M178 490H346M192 454H332M206 418H313M221 385H299"/></g>
<g fill="#176d49"><path d="M40 182L5 280H25L0 340H80L55 280H75Z"/><path d="M463 204L428 289H442L416 352H511L484 289H499Z"/></g>'''
train='''<g transform="translate(24 18)">
<ellipse cx="231" cy="408" rx="170" ry="32" fill="#173d4b" opacity=".40"/>
<path d="M80 167Q83 139 114 131H236Q257 138 267 165V303H80Z" fill="url(#red)" stroke="#7e2130" stroke-width="7" stroke-linejoin="round"/>
<path d="M62 161L84 123Q88 112 110 110H237Q257 112 269 129L281 161Q280 174 264 174H79Q64 174 62 161Z" fill="url(#blue)" stroke="#143a78" stroke-width="7"/>
<rect x="103" y="181" width="93" height="80" rx="15" fill="#bdefff" stroke="url(#gold)" stroke-width="10"/>
<path d="M111 189H134L190 244H166Z" fill="#fff" opacity=".67"/>
<path d="M71 303H371L401 354H64Z" fill="url(#red)" stroke="#802131" stroke-width="8"/>
<g fill="url(#steel)" stroke="#142f50" stroke-width="8"><circle cx="106" cy="358" r="45"/><circle cx="215" cy="365" r="50"/><circle cx="322" cy="359" r="42"/></g>
<g fill="url(#gold)" stroke="#a85d1a" stroke-width="5"><circle cx="106" cy="358" r="28"/><circle cx="215" cy="365" r="32"/><circle cx="322" cy="359" r="26"/></g>
<g stroke="#fff0a0" stroke-width="5"><path d="M106 335V382M82 358H130M215 339V391M189 365H241M322 337V380M300 359H344"/></g>
<path d="M106 358L215 365 322 359" stroke="#d5e4ef" stroke-width="12" stroke-linecap="round"/>
<path d="M176 177Q199 155 240 155H324Q366 158 378 211V275Q367 312 325 317H220Q178 313 166 278V217Q166 189 176 177Z" fill="url(#blue)" stroke="#163977" stroke-width="8"/>
<path d="M194 182Q216 173 245 173H313" fill="none" stroke="#a7edff" stroke-width="12" stroke-linecap="round" opacity=".85"/>
<path d="M220 164V310M277 158V315" stroke="url(#gold)" stroke-width="11"/>
<path d="M286 157L298 94H340L353 157Z" fill="url(#steel)" stroke="#223a54" stroke-width="5"/>
<ellipse cx="319" cy="94" rx="36" ry="14" fill="url(#gold)" stroke="#674622" stroke-width="5"/>
<ellipse cx="319" cy="92" rx="24" ry="8" fill="#263a51"/>
<g fill="#eff9ff" opacity=".84"><circle cx="309" cy="64" r="15"/><circle cx="288" cy="48" r="21"/><circle cx="266" cy="28" r="25"/></g>
<ellipse cx="343" cy="235" rx="70" ry="82" fill="url(#gold)" stroke="#a85f21" stroke-width="7"/>
<ellipse cx="346" cy="235" rx="59" ry="69" fill="url(#steel)" stroke="#f6d26a" stroke-width="5"/>
<ellipse cx="346" cy="235" rx="40" ry="48" fill="#203c5a" stroke="#799ab8" stroke-width="5"/>
<path d="M313 225Q317 201 338 194" stroke="#9bbcd8" stroke-width="5" fill="none" stroke-linecap="round"/>
<circle cx="344" cy="142" r="27" fill="url(#gold)" stroke="#b77122" stroke-width="6"/>
<circle cx="344" cy="142" r="19" fill="url(#lamp)"/>
<path d="M319 316H382L432 377Q436 389 421 393H290Q279 390 285 378Z" fill="url(#red)" stroke="#92202d" stroke-width="7"/>
<g stroke="#ffae77" stroke-width="7" stroke-linecap="round"><path d="M325 327L308 376M345 327L339 376M363 327L371 376M382 330L404 376"/></g>
<path d="M297 382H418" stroke="#f9c44c" stroke-width="8" stroke-linecap="round"/>
</g>'''
def icon(path,body):
    (p/path).write_text('<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">'+icon_defs+body+'</svg>')
icon("assets/icon.svg",background+train)
icon("assets/icon_background.svg",background)
icon("assets/icon_foreground.svg",'<g transform="translate(65 65) scale(.75)">'+train+'</g>')
edit("export_presets.cfg",[
('launcher_icons/adaptive_foreground_432x432="res://assets/icon.svg"','launcher_icons/adaptive_foreground_432x432="res://assets/icon_foreground.svg"'),
('launcher_icons/adaptive_background_432x432="res://assets/icon.svg"','launcher_icons/adaptive_background_432x432="res://assets/icon_background.svg"')])

# Procedural train detail preserves the authored route and original rolling wheel hierarchy.
(p/"scripts"/"train_polish.gd").write_text('''extends RefCounted
static func _mat(hex: String) -> StandardMaterial3D:
	var m:=StandardMaterial3D.new()
	m.albedo_color=Color(hex)
	m.roughness=0.42
	m.metallic_specular=0.4
	return m

static func _box(parent: Node3D, pos: Vector3, extent: Vector3, mat: Material) -> MeshInstance3D:
	var mesh:=BoxMesh.new();mesh.size=extent
	var obj:=MeshInstance3D.new();obj.mesh=mesh;obj.material_override=mat
	parent.add_child(obj);obj.position=pos
	return obj

static func _cylinder(parent: Node3D,pos: Vector3, radius: float, height: float, mat: Material, along_z:=false) -> MeshInstance3D:
	var mesh:=CylinderMesh.new();mesh.top_radius=radius;mesh.bottom_radius=radius;mesh.height=height;mesh.radial_segments=24;mesh.rings=2
	var obj:=MeshInstance3D.new();obj.mesh=mesh;obj.material_override=mat
	parent.add_child(obj);obj.position=pos
	if along_z:obj.rotation.x=PI/2
	return obj

static func _hide_body(node: Node) -> void:
	if node is MeshInstance3D and str(node.name).begins_with("train-"):
		node.visible=false
	for c in node.get_children():
		if not str(c.name).to_lower().begins_with("wheel"):_hide_body(c)

static func apply(car: Node3D, index: int, choice: int) -> void:
	_hide_body(car)
	var body:=Node3D.new();body.name="DeluxeBody";car.add_child(body)
	var primary:=_mat(["237ad2","e8a327","1d987f"][choice])
	var accent:=_mat(["d84230","195baf","e5bb39"][choice])
	var metal:=_mat("263c51")
	var gold:=_mat("efb83e")
	var glass:=_mat("9ce8ff")
	var cream:=_mat("fff2ca")
	_box(body,Vector3(0,0.32,0),Vector3(1.22,0.22,2.65),accent)
	_box(body,Vector3(0,0.44,0),Vector3(1.16,0.10,2.48),gold)
	if index==0:
		if choice==0:
			_cylinder(body,Vector3(0,0.94,0.37),0.48,1.62,primary,true)
			for z in [-0.18,0.36,0.91]:
				_cylinder(body,Vector3(0,0.94,z),0.50,0.07,gold,true)
			_cylinder(body,Vector3(0,0.94,1.18),0.45,0.12,metal,true)
			_cylinder(body,Vector3(0,1.53,0.74),0.16,0.40,metal)
			_cylinder(body,Vector3(0,1.76,0.74),0.23,0.10,gold)
			_box(body,Vector3(0,1.04,-0.85),Vector3(1.08,1.15,0.75),accent)
			_box(body,Vector3(0,1.69,-0.85),Vector3(1.30,0.15,0.98),metal)
			for side in [-1.0,1.0]:
				_box(body,Vector3(side*0.548,1.27,-0.85),Vector3(0.035,0.49,0.52),gold)
				_box(body,Vector3(side*0.572,1.27,-0.85),Vector3(0.035,0.37,0.40),glass)
		else:
			_box(body,Vector3(0,0.98,0),Vector3(1.13,1.0,2.31),primary)
			_box(body,Vector3(0,1.51,0),Vector3(1.20,0.14,2.40),accent)
			_box(body,Vector3(0,1.19,1.166),Vector3(0.89,0.52,0.035),metal)
			_box(body,Vector3(0,1.19,1.195),Vector3(0.77,0.40,0.03),glass)
			for side in [-1.0,1.0]:
				for z in [-0.72,0.0,0.72]:
					_box(body,Vector3(side*0.575,1.18,z),Vector3(0.028,0.45,0.48),glass)
		_box(body,Vector3(0,0.49,1.33),Vector3(1.28,0.19,0.20),accent)
		var lamp:=_mat("fff0a6");lamp.emission_enabled=true;lamp.emission=Color("ffd36a");lamp.emission_energy_multiplier=0.55
		for x in [-0.41,0.41]:
			_cylinder(body,Vector3(x,0.71,1.26),0.13,0.12,gold,true)
			_cylinder(body,Vector3(x,0.71,1.34),0.10,0.035,lamp,true)
	elif index==1:
		_box(body,Vector3(0,0.94,0),Vector3(1.08,0.96,2.28),primary)
		_box(body,Vector3(0,1.48,0),Vector3(1.24,0.15,2.42),accent)
		for side in [-1.0,1.0]:
			for z in [-0.72,0.0,0.72]:
				_box(body,Vector3(side*0.55,1.06,z),Vector3(0.045,0.46,0.52),gold)
				_box(body,Vector3(side*0.58,1.06,z),Vector3(0.03,0.36,0.42),glass)
			_box(body,Vector3(side*0.56,0.66,0),Vector3(0.035,0.11,2.15),cream)
	else:
		for side in [-1.0,1.0]:
			_box(body,Vector3(side*0.55,0.59,0),Vector3(0.10,0.35,2.33),primary)
			for z in [-1.01,-0.33,0.33,1.01]:
				_box(body,Vector3(side*0.55,0.74,z),Vector3(0.13,0.10,0.10),gold)
		for z in [-1.14,1.14]:
			_box(body,Vector3(0,0.58,z),Vector3(1.09,0.34,0.12),primary)
''')

f=p/"scripts"/"main.gd";q=f.read_text()
q=q.replace('var world: Node3D','const TrainPolish = preload("res://scripts/train_polish.gd")\n\nvar world: Node3D',1)
q=q.replace('cars.append(obj)\n\t\t_collect_wheels(obj)','cars.append(obj)\n\t\t_collect_wheels(obj)\n\t\tTrainPolish.apply(obj,i,train_choice)',1)
q=q.replace('cars[i].basis=Basis.looking_at(tangent,Vector3.UP,true)','cars[i].basis=Basis.looking_at(tangent,Vector3.UP,true).scaled_local(Vector3(1.16,1.23,1.0))',1)
# Responsive positions, while preserving minimum tap targets and RTL.
q=function(q,"_flow_position",'''func _flow_position(pos: Vector2, extent: Vector2, parent: Control=null) -> Vector2:
	var host: Control=parent if parent else ui
	var point:=pos
	if parent==null:
		point.x+=(host.size.x-1280.0)*clampf(pos.x/maxf(1.0,1280.0-extent.x),0.0,1.0)
		point.y+=(host.size.y-720.0)*clampf(pos.y/maxf(1.0,720.0-extent.y),0.0,1.0)
	return Vector2(host.size.x-point.x-extent.x,point.y) if language=="ar" else point
''')
q=q.replace('child.position.x=1280-child.position.x-child.size.x','child.position.x=ui.size.x-child.position.x-child.size.x')
q=q.replace('bg.stretch_mode=TextureRect.STRETCH_SCALE','bg.stretch_mode=TextureRect.STRETCH_KEEP_ASPECT_COVERED')
# Add distance and target guidance in the actual 3D world.
q=q.replace('var goal_ring: MeshInstance3D','var goal_ring: MeshInstance3D\nvar goal_sign: Label3D\nvar proximity_label: Label',1)
q=q.replace('goal_ring=null\n\tcamera=','goal_ring=null;goal_sign=null\n\tcamera=',1)
q=q.replace('ring.inner_radius=1.1;ring.outer_radius=1.30','ring.inner_radius=1.22;ring.outer_radius=1.55')
q=q.replace('goal_ring=art.mesh_node(ring,art.material(s.color.to_html()),point+Vector3(0,0.075,0))','''var goal_mat:=StandardMaterial3D.new();goal_mat.albedo_color=Color("ffd84f");goal_mat.emission_enabled=true;goal_mat.emission=Color("ffbf37");goal_mat.shading_mode=BaseMaterial3D.SHADING_MODE_UNSHADED
	goal_ring=art.mesh_node(ring,goal_mat,point+Vector3(0,0.10,0))
	if is_instance_valid(goal_sign):goal_sign.queue_free()
	goal_sign=Label3D.new();goal_sign.name="DestinationSign";goal_sign.text="★ "+str(station+1);goal_sign.billboard=BaseMaterial3D.BILLBOARD_ENABLED
	goal_sign.font_size=72;goal_sign.pixel_size=0.013;goal_sign.modulate=Color("fff2b1");goal_sign.outline_modulate=Color("493322");goal_sign.outline_size=15
	world.add_child(goal_sign);goal_sign.position=point+Vector3(0,2.5,0)''')
q=q.replace('var pulse:=1.12+sin(timer*2)*0.08;goal_ring.scale=Vector3(pulse,0.3,pulse)','var pulse:=1.12+sin(timer*2)*0.08;goal_ring.scale=Vector3(pulse,0.3,pulse)')
# A close cab-follow view in driving missions; retain a wider puzzle view for gap placement.
q=q.replace('zoom=35.5 if world_id>=2 else (26.5 if world_id==0 else 28.5)','''zoom=30.0 if world_id>=2 else 22.5
	if data.mode!="build":
		camera_follow=true;zoom=16.5;pitch=0.57''')
q=q.replace('target=Vector3.ZERO\n\t_update_train(0);_update_camera(1);_game_ui()','target=Vector3.ZERO\n\t_update_train(0);_update_camera(10.0);_game_ui()')
q=function(q,"_update_camera",'''func _update_camera(delta: float) -> void:
	var focus:=Vector3.ZERO
	if screen=="game" and camera_follow and not cars.is_empty():
		focus=cars[0].position + cars[0].basis.z.normalized()*1.9
	elif world_id>=2:
		focus=Vector3(0,1.2,-1.7)
	elif screen=="menu":
		focus=Vector3(3.5 if language=="ar" else -3.5,0,0)
	target=target.lerp(focus,1.0-exp(-delta*3.5))
	var offset:=Vector3(sin(yaw)*cos(pitch),sin(pitch),cos(yaw)*cos(pitch))*42
	camera.position=target+offset
	camera.look_at(target,Vector3.UP)
	camera.size=lerpf(camera.size,zoom,1.0-exp(-delta*7))

func _toggle_camera() -> void:
	camera_follow=not camera_follow
	zoom=16.5 if camera_follow else (30.0 if world_id>=2 else 22.5)
	pitch=0.57 if camera_follow else (0.78 if world_id>=2 else 0.72)
''')
q=q.replace('func():camera_follow=not camera_follow,"blue","",camera_panel,28','_toggle_camera,"blue","",camera_panel,28')
q=q.replace('zoom=clampf(zoom-2,14,40)','zoom=clampf(zoom-2,11,44)').replace('zoom=clampf(zoom+2,14,40)','zoom=clampf(zoom+2,11,44)').replace('0.035,14,40)','0.035,11,44)').replace('zoom-1.4,14,40)','zoom-1.4,11,44)').replace('zoom+1.4,14,40)','zoom+1.4,11,44)')
# Make 2D control text solid and sharply legible, not hollow from a heavy outline.
q=q.replace('b.add_theme_constant_override("outline_size",0 if palette=="neutral" else 4)','b.add_theme_constant_override("outline_size",0 if palette=="neutral" else 2)')
q=q.replace('var theme := Theme.new()','var theme := Theme.new()',1)
# Fix achievement number ordering even in mixed-direction locale; separate text components.
q=function(q,"_achievements",'''func _achievements() -> void:
	var p:=_open_modal(Vector2(660,410))
	_label(t("menu_achievements"),Vector2(24,12),Vector2(612,64),35,TEAL,p).horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	var total:=0
	for value in stars:total+=clampi(int(value),0,3)
	var star_icon:=TextureRect.new();p.add_child(star_icon);star_icon.texture=load("res://assets/deluxe/icon_star.svg");star_icon.expand_mode=TextureRect.EXPAND_IGNORE_SIZE;star_icon.position=Vector2(291,75);star_icon.size=Vector2(78,78)
	var earned:=_label(str(total),Vector2(30,158),Vector2(600,66),56,INK,p);earned.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER;earned.text_direction=Control.TEXT_DIRECTION_LTR;earned.name="EarnedStars"
	var max_stars:=_label(t("out_of_stars") % (stars.size()*3),Vector2(24,225),Vector2(612,44),24,TEAL,p);max_stars.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER;max_stars.name="MaximumStars"
	var completed:=_label(t("all_progress") % [stars.size()-stars.count(0),stars.size()],Vector2(24,274),Vector2(612,48),25,INK,p);completed.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	_deluxe_button(t("close"),Vector2(70,335),Vector2(520,64),_close_modal,"green","",p)
''')
# More legible compact HUD: do not reserve a huge duplicated instruction bar on drive stages.
q=q.replace('Vector2(20,15),Vector2(875,82),Color("eaf6ff")','Vector2(20,15),Vector2(815,74),Color(0.93,0.98,1,0.94)')
q=q.replace('Vector2(7,7),Vector2(68,68)','Vector2(7,6),Vector2(62,62)')
q=q.replace('Vector2(92,5),Vector2(770,43),29','Vector2(82,4),Vector2(720,40),29')
q=q.replace('Vector2(94,46),Vector2(760,29),20','Vector2(84,42),Vector2(715,30),21')
q=q.replace('Vector2(20,106),Vector2(425,92)','Vector2(20,98),Vector2(370,78)')
q=q.replace('Vector2(12,4),Vector2(401,84),20','Vector2(12,4),Vector2(346,70),21')
q=q.replace('var controls:=_panel(Vector2(20,590),Vector2(744,112),Color("eaf6ff"))','var controls:=_panel(Vector2(20,590),Vector2(744,112),Color(0.93,0.98,1,0.95))')
q=q.replace('elif data.mode=="drive":\n\t\t\t_label(t("station_hint"),Vector2(14,8),Vector2(710,90),24,INK,controls)','''elif data.mode=="drive":
			controls.hide()
			var indicator:=_panel(Vector2(20,620),Vector2(338,82),Color(0.93,0.98,1,0.94))
			proximity_label=_label(t("station_hint"),Vector2(14,6),Vector2(310,70),24,INK,indicator)
			proximity_label.name="StationProximity"''')
q=q.replace('task_label=_label(instruction','proximity_label=null\n\ttask_label=_label(instruction')
q=q.replace('func _process(delta: float) -> void:\n\ttimer+=delta','''func _process(delta: float) -> void:
	timer+=delta
	if screen=="game" and is_instance_valid(proximity_label):
		var near_goal: bool=_circular_distance(distance,goal_distance)<2.4
		proximity_label.text=t("brake_now") if near_goal else t("station_hint")
		proximity_label.add_theme_color_override("font_color",Color("c23c25") if near_goal else INK)''')
# No orbit-on-tap after a successful assisted placement; avoid accidental double touches.
q=q.replace('_drop_at(event.position);orbiting=true','var count_before:=missing.size()\n\t\t\t_drop_at(event.position);orbiting=missing.size()==count_before')
# Keep 3D visuals clear, gap labels always visible.
q=q.replace('ring.inner_radius=0.80;ring.outer_radius=1.04','ring.inner_radius=0.82;ring.outer_radius=1.12')
q=q.replace('art.material("f1bb53"),piece.center','art.material("ffc52e"),piece.center')
# Stronger rail shape / ballast in closed-loop routes without altering the original GLB files.
q=q.replace('if ghost:\n\t\t_override(obj,ghost)\n\treturn obj','''if ghost:
		_override(obj,ghost)
	else:
		_add_ballast(obj,piece,line)
	return obj

func _add_ballast(obj: Node3D,piece: Dictionary,line: Dictionary) -> void:
	var curve: Curve3D=line.curve
	var mesh:=SurfaceTool.new();mesh.begin(Mesh.PRIMITIVE_TRIANGLES)
	var steps:=maxi(4,ceili(float(piece.length)/0.20))
	for i in range(steps):
		var a: Vector3=curve.sample_baked(float(piece.from)+float(piece.length)*i/steps,true)
		var b: Vector3=curve.sample_baked(float(piece.from)+float(piece.length)*(i+1)/steps,true)
		var across:=Vector3(b.z-a.z,0,-(b.x-a.x)).normalized()*0.71
		var c:=Vector3(0,-0.045,0)
		for v in [a-across+c,b-across+c,b+across+c,a-across+c,b+across+c,a+across+c]:
			mesh.set_normal(Vector3.UP);mesh.add_vertex(obj.to_local(v))
	var node:=MeshInstance3D.new();node.mesh=mesh.commit();node.material_override=art.material("aa957c");obj.add_child(node)
	node.name="Ballast"
''',1)
# Update first-world camera and help copy; actual rail logic stays intact.
f.write_text(q)
edit("scripts/strings.gd",[('const ADVENTURE_WORDS := {','''const ADVENTURE_WORDS := {
	"out_of_stars": ["of %s possible stars","من أصل %s نجمة","de %s estrelas possíveis"],
	"brake_now": ["Brake now!","اضغط الفرامل الآن!","Freie agora!"],''')])

# Continuous landscape removes the tabletop border from the first two worlds.
f=p/"scripts"/"world_builder.gd";q=f.read_text()
q=re.sub(r'\tvar ground := PlaneMesh.new\(\)\n\tground.size = Vector2\(200,200\)\n\tmesh_node\(ground,material\("[^"]+"\),Vector3\(0,-1.12,0\)\)\n\tvar w :=.*?\n\t_make_river\(id\)', '''	var ground := PlaneMesh.new()
	ground.size=Vector2(180,180)
	var landscape:=ShaderMaterial.new()
	landscape.shader=load("res://scripts/meadow.gdshader")
	landscape.set_shader_parameter("base",Color("65ad43" if id==0 else "65b78a"))
	mesh_node(ground,landscape,Vector3(0,0.035,0))
	_make_river(id)''',q,count=1,flags=re.S)
assert 'landscape.shader=' in q
# Keep water readable and river flowing beyond the previous artificial board.
q=q.replace('var bound:=10.7 if id==0 else 12.7','var bound:=33.0')
q=q.replace('_make_waterfall(Vector3(sin(bound*0.42)*0.5,-0.93,bound-0.02),1.04)','')
q=q.replace('var width := 1.3 if id == 0 else 1.6','var width := 1.3 if id == 0 else 1.6')
q=q.replace('e.ambient_light_energy = 0.45','e.ambient_light_energy = 0.66').replace('e.tonemap_exposure = 0.65','e.tonemap_exposure = 0.82').replace('sun.shadow_bias = 0.04','sun.shadow_bias = 0.035')
# Reuse verified existing CC0 objects in carefully spaced outer landscape clusters.
q=q.replace('\tfor i in range(5):\n\t\tvar cloud := Node3D.new()', '''	for i in range(34):
		var angle:=float(i)*TAU/34.0
		var radius:=16.0+rng.randf_range(0.6,7.0)
		var pos:=Vector3(cos(angle)*radius,0.06,sin(angle)*radius)
		if absf(pos.x)<3.4:continue
		var kind: String=["tree_oak","tree_pineRoundA","tree_small"][i%3]
		model("nature-kit",kind,pos,Vector3.ONE*rng.randf_range(2.0,3.5),angle)
	for i in range(12):
		var angle:=float(i)*TAU/12.0
		var pos:=Vector3(cos(angle)*19.5,0.07,sin(angle)*19.5)
		if absf(pos.x)<3.5:continue
		model("nature-kit","rock_largeB",pos,Vector3(1.35,0.85,1.2),angle)
	for i in range(5):
		var cloud := Node3D.new()''',1)
# Station shelters get distinctive signs and a new platform edge, with no changes to stop coordinates.
q=q.replace('stations.append({"node":n,"pos":pos,"color":color,"label":label})','''var rim:=CylinderMesh.new();rim.top_radius=1.82;rim.bottom_radius=1.82;rim.height=0.10;rim.radial_segments=32
	mesh_node(rim,material("d9aa48"),Vector3(0,-0.07,0),n)
	var signpost:=BoxMesh.new();signpost.size=Vector3(0.10,1.5,0.10)
	mesh_node(signpost,material("72523a"),Vector3(1.39,0.75,0),n)
	var sign:=BoxMesh.new();sign.size=Vector3(0.7,0.43,0.13)
	mesh_node(sign,material(color.to_html()),Vector3(1.39,1.54,0),n)
	stations.append({"node":n,"pos":pos,"color":color,"label":label})''')
f.write_text(q)
(p/"scripts"/"meadow.gdshader").write_text('''shader_type spatial;
render_mode cull_disabled;
uniform vec4 base : source_color = vec4(0.35,0.62,0.25,1.0);
varying vec3 world_pos;
void vertex(){world_pos=(MODEL_MATRIX*vec4(VERTEX,1.0)).xyz;}
void fragment(){
	vec2 p=world_pos.xz;
	float broad=sin(p.x*0.38)*cos(p.y*0.29);
	float fine=sin(p.x*32.0+sin(p.y*14.0))*cos(p.y*27.0);
	ALBEDO=base.rgb*(0.92+0.10*broad+0.035*fine);
	ROUGHNESS=0.95;
}''')
# Better terrain and water in outdoor worlds; keep safe clearance from train track.
f=p/"scripts"/"adventure_art.gd";q=f.read_text().replace('["e9f1f5","bfd6df","8e9da9"]','["e6f0ff","bacfe3","879dae"]').replace('for i in range(120):','for i in range(155):').replace('art.material("e2edf2",0.30)','art.material("c1d4e1",0.30)');f.write_text(q)
f=p/"scripts"/"river_water.gdshader";q=f.read_text().replace('vec3(0.09, 0.47, 0.57)','vec3(0.035, 0.39, 0.63)').replace('float ripple = smoothstep(0.72, 1.0, wave) * 0.12;','float ripple = smoothstep(0.72, 1.0, wave) * 0.10;');f.write_text(q)

# Test real project nodes, responsive viewport positioning and achievements ordering.
(p/"tests"/"verify_polish.gd").write_text('''extends SceneTree
func _initialize() -> void:
	call_deferred("verify")
func verify() -> void:
	var game = load("res://scenes/main.tscn").instantiate()
	root.add_child(game)
	await process_frame
	game.set_process(false)
	assert(ProjectSettings.get_setting("display/window/stretch/aspect")=="expand")
	assert(ProjectSettings.get_setting("application/config/version")=="1.4.0")
	for lang in ["en_GB","ar","pt_BR"]:
		game.language=lang
		game._show_menu()
		game.stars.fill(0);game.stars[0]=3;game.stars[1]=2
		game._achievements()
		assert(game.modal.find_child("EarnedStars",true,false).text=="5")
		assert(game.modal.find_child("MaximumStars",true,false).text.contains("72"))
		game._close_modal()
		game._start_level(2)
		assert(game.camera_follow and game.zoom==16.5)
		assert(game.cars[0].get_node_or_null("DeluxeBody")!=null)
		assert(game.cars[0].scale.y>1.1)
		assert(game.goal_sign!=null and game.goal_sign.text.contains("1"))
		game._toggle_camera()
		assert(not game.camera_follow and game.zoom>20)
		game._start_level(0)
		assert(not game.camera_follow)
		assert(game.track_nodes[0].get_node_or_null("Ballast")!=null)
		await process_frame
	print("POLISH_PASS: responsive viewport, clearer train, goals, achievement count and six world compatibility")
	game.queue_free()
	await process_frame
	quit()
''')
print("RAILVITO_1_4_PATCH_OK")
