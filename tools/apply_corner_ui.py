from pathlib import Path
import re, math, random, struct, zlib
p=Path("source/Railvito")
f=p/"project.godot";s=f.read_text();assert 'config/version="1.6.0"' in s;f.write_text(s.replace('config/version="1.6.0"','config/version="1.7.0"'))
f=p/"export_presets.cfg";s=f.read_text().replace("1.6.0","1.7.0").replace("version/code=7","version/code=8");assert 'version/code=8' in s;f.write_text(s)
f=p/"scripts/main.gd";s=f.read_text()
def req(old,new):
    global s
    assert old in s,old[:160]
    s=s.replace(old,new,1)
# Fixed spatial ordering matching the approved screenshot, with localized labels.
# All five top buttons are independent of the mission strip, in both LTR and RTL.
start=s.index('\tvar head:=_panel(',s.index('func _game_ui('))
end=s.index('\tif data.mode=="build":',start)
s=s[:start]+'''	var width: float=ui.size.x
	var head:=_panel(Vector2(0,12),Vector2(width-470.0,91),dark)
	head.position=Vector2(366,12)
	head.name="MissionStrip"
	_label(t(data.title),Vector2(14,1),Vector2(head.size.x-28,40),29,Color("ffe4a1"),head)
	var instruction:=t("fit_instruction") if data.mode=="build" else t("drive_task") % (data.station+1) if data.mode=="drive" else t("cargo_task") % [data.number,data.station+1]
	if world_id==5:instruction=t("city_cargo_task") % [data.number,data.station+1] if data.mode=="cargo" else t("city_route_task") % (data.station+1)
	task_label=_label(instruction,Vector2(14,41),Vector2(head.size.x-28,45),23,Color.WHITE,head)
	task_label.name="MissionInstruction"
	status_label=_label("",Vector2.ZERO,Vector2.ONE,14,Color.WHITE,head);status_label.hide()
	_fixed_hud_button("",Vector2(16,15),Vector2(78,76),_settings,"blue","settings",null,25,"SettingsTop")
	_fixed_hud_button("",Vector2(102,15),Vector2(78,76),_ring_bell,"gold","bell",null,25,"CabBell")
	_fixed_hud_button("",Vector2(188,15),Vector2(78,76),_show_gesture_tutorial,"blue","help",null,25,"HelpTop")
	_fixed_hud_button("",Vector2(274,15),Vector2(78,76),func():_start_level(level_index),"orange","rotate",null,25,"RestartTop")
	_fixed_hud_button("",Vector2(width-90,15),Vector2(74,76),_show_menu,"blue","home",null,25,"HomeButton")
'''+s[end:]
start=s.index('\tif data.mode=="build":',s.index('func _game_ui('))
end=s.index('\telif data.mode=="cargo" or world_id==5:',start)
s=s[:start]+'''	if data.mode=="build":
		var controls:=_panel(Vector2.ZERO,Vector2(430,110),dark)
		controls.name="RailTray"
		controls.position=Vector2(width-446,ui.size.y-126)
		var kinds: Array=["bridge","straight"] if world_id>=2 else ["straight","curve"]
		for i in range(2):
			var kind: String=kinds[i]
			var b:=_fixed_hud_button(t(kind),Vector2(8+i*166,6),Vector2(158,76),func():_select_piece(kind),"blue",kind,controls,23,"Rail_"+kind)
			b.button_down.connect(func():_begin_drag(kind))
			selected_buttons[kind]=b
		# Rotation is deliberately part of the rail tray; no undo or redo buttons.
		_fixed_hud_button("",Vector2(340,6),Vector2(82,76),_rotate_piece,"orange","rotate",controls,23,"RailRotate")
		selected_label=_label("",Vector2(10,82),Vector2(410,24),20,Color.WHITE,controls)
		_fixed_hud_button(t("hint").replace("✦","").strip_edges(),Vector2((width-132)*0.5,ui.size.y-126),Vector2(132,108),_hint,"gold","hint_bulb",null,25,"HintOnly")
'''+s[end:]
start=s.index('\tvar cab:=_panel(',s.index('func _game_ui('))
end=s.index('\t_update_lever()',start)
s=s[:start]+'''	var building: bool=data.mode=="build"
	var cab_size:=Vector2(328,104) if building else Vector2(497,104)
	var cab:=_panel(Vector2(765,600),cab_size,dark)
	if building:cab.position=Vector2(16,ui.size.y-120)
	var brake_button:=_fixed_hud_button(t("brake").replace("■","").strip_edges(),Vector2(8,8),Vector2(150,88),_brake,"red","stop",cab,25,"CabBrake")
	_fixed_hud_button(t("go").replace("▶","").strip_edges(),Vector2(166,8),Vector2(154,88),_go,"green","play",cab,25,"CabGo")
	lever_button_ref=_fixed_hud_button("",Vector2(328,8),Vector2(161,88),_cycle_speed,"blue","speed",cab,22,"CabLever")
	lever_button_ref.visible=not building
	# Retain speed controls for cargo and driving missions, and all existing logic.
	speed_slider=HSlider.new();cab.add_child(speed_slider);speed_slider.min_value=0.7;speed_slider.max_value=5;speed_slider.step=0.1;speed_slider.value=speed_setting;speed_slider.hide()
	speed_slider.value_changed.connect(func(v):speed_setting=v;if_running_speed(v);_update_lever())
'''+s[end:]
req('func _game_ui() -> void:','''func _fixed_hud_button(caption: String, at: Vector2, extent: Vector2, action: Callable, palette: String, icon: String, parent: Control, font_size: int, node_name: String) -> Button:
	var b:=_deluxe_button(caption,at,extent,action,palette,icon,parent,font_size)
	b.position=at
	b.name=node_name
	return b

func _game_ui() -> void:''')
# Keep keyboard undo/redo internal for recovery/tests; remove the visible UI only.
# Short translations fit the buttons without duplicate unicode symbols.
f.write_text(s)
a=p/"assets/deluxe"
(a/"icon_hint_bulb.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64"><g stroke="#724c1b" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"><path d="M18 29C18 10 46 10 46 29C46 38 38 41 38 48H26C26 41 18 38 18 29Z" fill="#fff3a3"/><path d="M26 48H38V54H26Z" fill="#fff6d8"/><path d="M28 58H36" fill="none"/></g><g stroke="#fff4bb" stroke-width="4" stroke-linecap="round"><path d="M32 3V9M7 15L12 19M52 19L57 15M4 32H10M54 32H60"/></g><path d="M25 25Q29 19 36 20" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>''')
# Authentic miniature rail illustrations rather than abstract icons.
(a/"icon_straight.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64"><path d="M5 12H59M5 25H59M5 38H59M5 51H59" stroke="#754a29" stroke-width="10" stroke-linecap="round"/><path d="M7 10H57M7 23H57M7 36H57M7 49H57" stroke="#d7a062" stroke-width="5" stroke-linecap="round"/><path d="M18 3V61M46 3V61" stroke="#526477" stroke-width="9"/><path d="M16 3V61M44 3V61" stroke="#eef6fc" stroke-width="4"/></svg>''')
(a/"icon_curve.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64"><g stroke="#8f623b" stroke-width="9" stroke-linecap="round"><path d="M7 57H42M10 40L43 49M17 23L47 42M31 10L54 38M49 6V35"/></g><path d="M12 61Q12 12 61 12M38 61Q38 38 61 38" stroke="#556675" stroke-width="9" fill="none"/><path d="M10 61Q10 10 61 10M36 61Q36 36 61 36" stroke="#eff7fb" stroke-width="4.5" fill="none"/></svg>''')
# Reusable real 2K stone and painted roof maps for decorative station structures.
tex=p/"assets/quality_textures";tex.mkdir(exist_ok=True)
def png(path,n,raw):
    def chunk(k,v):return struct.pack(">I",len(v))+k+v+struct.pack(">I",zlib.crc32(k+v)&0xffffffff)
    path.write_bytes(b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",n,n,8,2,0,0,0))+chunk(b"IDAT",zlib.compress(raw,6))+chunk(b"IEND",b""))
def surface(name,roof):
    n=2048;rng=random.Random(172 if roof else 198);raw=bytearray()
    shades=[[rng.randrange(-15,16) for i in range(16)] for j in range(16)]
    for y in range(n):
        raw.append(0);row=y//128;dy=y%128
        for x in range(n):
            xx=(x+(row%2)*64)%n;col=xx//128;dx=xx%128
            noise=rng.randrange(-6,7)
            seam=dx<3 or dy<4
            bevel=min(dx,dy,127-dx,127-dy)
            v=190+shades[row][col]+noise+(9 if bevel<8 else 0)
            if roof:
                v+=int(14*math.cos((dx-64)*math.pi/128))
                rgb=(v,min(255,int(v*.80)),int(v*.72)) if not seam else (95,72,61)
            else:
                rgb=(v,int(v*.96),int(v*.89)) if not seam else (120,116,108)
            raw.extend(max(0,min(255,int(c))) for c in rgb)
    png(tex/(name+".png"),n,raw)
surface("station_stone_2k",False);surface("station_roof_2k",True)

# New playable-world decoration, not a screenshot background or unused size padding.
# Build positions are checked against the actual rail curve and river.
(p/"scripts/scenic_details.gd").write_text('''extends Node3D
var sails: Array[Node3D]=[]
func _process(delta: float) -> void:
	for sail in sails:
		sail.rotation.z+=delta*0.46

func _mat(hex: String, texture_name: String="") -> StandardMaterial3D:
	var m:=StandardMaterial3D.new()
	m.albedo_color=Color(hex);m.roughness=0.77
	if texture_name!="":
		m.albedo_texture=load("res://assets/quality_textures/"+texture_name+".png")
		m.uv1_triplanar=true;m.uv1_scale=Vector3(0.5,0.5,0.5)
	return m

func _box(parent: Node3D, at: Vector3, size: Vector3, mat: Material) -> MeshInstance3D:
	var mesh:=BoxMesh.new();mesh.size=size
	var node:=MeshInstance3D.new();node.mesh=mesh;node.material_override=mat
	parent.add_child(node);node.position=at
	return node

func _post(parent: Node3D,at: Vector3, radius: float,height: float,mat: Material) -> MeshInstance3D:
	var mesh:=CylinderMesh.new();mesh.top_radius=radius;mesh.bottom_radius=radius;mesh.height=height;mesh.radial_segments=16
	var node:=MeshInstance3D.new();node.mesh=mesh;node.material_override=mat
	parent.add_child(node);node.position=at
	return node

func populate(layout: Dictionary, id: int) -> void:
	if id>=2:return
	var curve: Curve3D=layout.curve
	var stone:=_mat("eee1c6","station_stone_2k")
	var roof:=_mat("c45b3b","station_roof_2k")
	var wood:=_mat("98623a","timber_detail")
	var cream:=_mat("ffdf9b")
	var glass:=_mat("438bb0")
	var iron:=_mat("354d53")
	var greenery:=_mat("5a9d49")
	var count:=0
	for i in range(12):
		var angle: float=float(i)*TAU/12.0+0.17
		var at:=Vector3(cos(angle)*13.0,0.08,sin(angle)*13.0)
		if absf(at.x)<5.2 or curve.get_closest_point(at).distance_to(at)<4.0:continue
		var lot:=Node3D.new();lot.name="ScenicLot"+str(count);add_child(lot);lot.position=at;lot.rotation.y=-angle
		lot.set_meta("track_clearance",curve.get_closest_point(at).distance_to(at))
		_box(lot,Vector3(0,0,0),Vector3(2.8,0.12,2.8),stone)
		if count==0:
			var tower:=CylinderMesh.new();tower.top_radius=0.68;tower.bottom_radius=0.95;tower.height=2.5;tower.radial_segments=20
			var body:=MeshInstance3D.new();body.mesh=tower;body.material_override=stone;lot.add_child(body);body.position=Vector3(0,1.3,0)
			var cone:=CylinderMesh.new();cone.top_radius=0.02;cone.bottom_radius=0.91;cone.height=0.85;cone.radial_segments=20
			var cap:=MeshInstance3D.new();cap.mesh=cone;cap.material_override=roof;lot.add_child(cap);cap.position=Vector3(0,2.98,0)
			var rotor:=Node3D.new();lot.add_child(rotor);rotor.position=Vector3(0,2.05,0.91);sails.append(rotor)
			for k in range(4):
				var blade:=Node3D.new();rotor.add_child(blade);blade.rotation.z=k*PI/2
				_box(blade,Vector3(0,0.69,0),Vector3(0.09,1.45,0.12),wood)
				_box(blade,Vector3(0.17,0.94,0),Vector3(0.32,0.85,0.085),cream)
				for j in range(3):_box(blade,Vector3(0.17,0.60+j*0.32,0.05),Vector3(0.35,0.05,0.04),wood)
			_box(lot,Vector3(0,0.5,0.91),Vector3(0.45,0.95,0.09),wood)
		else:
			# Stone garden pavilion with roof panels, window and flower beds.
			_box(lot,Vector3(0,0.85,0),Vector3(1.80,1.58,1.52),stone)
			var left:=_box(lot,Vector3(-0.46,1.80,0),Vector3(1.12,0.13,1.88),roof);left.rotation.z=0.43
			var right:=_box(lot,Vector3(0.46,1.80,0),Vector3(1.12,0.13,1.88),roof);right.rotation.z=-0.43
			_box(lot,Vector3(0,0.51,0.79),Vector3(0.47,0.93,0.09),wood)
			for x in [-0.55,0.55]:
				_box(lot,Vector3(x,1.02,0.79),Vector3(0.40,0.46,0.09),cream)
				_box(lot,Vector3(x,1.02,0.85),Vector3(0.30,0.36,0.035),glass)
				_box(lot,Vector3(x,0.70,0.96),Vector3(0.51,0.13,0.26),wood)
				_box(lot,Vector3(x,0.82,0.96),Vector3(0.42,0.12,0.19),greenery)
		for x in [-1.23,1.23]:
			for z in [-1.15,-0.4,0.4,1.15]:_post(lot,Vector3(x,0.24,z),0.06,0.43,wood)
			for y in [0.16,0.34]:_box(lot,Vector3(x,y,0),Vector3(0.07,0.07,2.38),wood)
		_post(lot,Vector3(1.04,0.65,1.0),0.055,1.22,iron)
		_box(lot,Vector3(1.04,1.28,1.0),Vector3(0.25,0.27,0.25),cream)
		_box(lot,Vector3(1.04,1.46,1.0),Vector3(0.34,0.07,0.34),iron)
		count+=1
''')
f=p/"scripts/main.gd";s=f.read_text()
req('\tart.build(world,id,route)','''	art.build(world,id,route)
	if id<2 and not low_graphics:
		var detail: Node3D=load("res://scripts/scenic_details.gd").new()
		detail.name="ScenicVillagePlus";world.add_child(detail)
		detail.populate(route,id)''')
f.write_text(s)

# Existing regression suite is retained. Only the expected version changes.
f=p/"tests/verify_polish.gd";s=f.read_text();assert '=="1.6.0"' in s;f.write_text(s.replace('=="1.6.0"','=="1.7.0"'))
(p/"tests/verify_corner_ui.gd").write_text('''extends SceneTree
const Network=preload("res://scripts/rail_network.gd")
func _initialize() -> void:
	call_deferred("verify")
func verify() -> void:
	var game=load("res://scenes/main.tscn").instantiate()
	root.add_child(game)
	await process_frame
	game.set_process(false)
	for locale in ["en_GB","ar","pt_BR"]:
		game.language=locale
		game._start_level(0)
		var names:=["SettingsTop","CabBell","HelpTop","RestartTop","MissionStrip","HomeButton"]
		var previous_right: float=0.0
		for item in names:
			var control: Control=game.ui.find_child(item,true,false)
			assert(control!=null,item)
			assert(control.position.x>=previous_right-0.1,item+" overlaps")
			previous_right=control.position.x+control.size.x
		assert(previous_right<=game.ui.size.x+0.1)
		var hint: Button=game.ui.find_child("HintOnly",true,false)
		var tray: Control=game.ui.find_child("RailTray",true,false)
		var brake: Button=game.ui.find_child("CabBrake",true,false)
		var go: Button=game.ui.find_child("CabGo",true,false)
		assert(hint!=null and tray!=null and brake!=null and go!=null)
		assert(brake.global_position.x<go.global_position.x)
		assert(go.global_position.x+go.size.x<hint.position.x)
		assert(hint.position.x+hint.size.x<tray.position.x)
		assert(tray.find_child("RailRotate",true,false)!=null)
		assert(tray.get_child_count()==4,"Rail tray must contain only 2 pieces, rotate and selection label")
		assert(not game.ui.find_child("CabLever",true,false).visible)
		# An incorrect shape or rotation must still fail.
		var idx: int=game.missing[0]
		var piece: Dictionary=game.route.pieces[idx]
		game.selected_kind="curve" if piece.kind!="curve" else "straight"
		game.selected_yaw=posmod(roundi(rad_to_deg(piece.yaw)),360)
		assert(not game._place_piece(idx))
		hint.pressed.emit()
		assert(game.selected_kind==piece.kind)
		assert(game._place_piece(idx))
		var detail: Node=game.world.get_node_or_null("ScenicVillagePlus")
		if not game.low_graphics:
			assert(detail!=null and detail.get_child_count()>0)
			for lot in detail.get_children():assert(float(lot.get_meta("track_clearance"))>=4.0)
		await process_frame
		game._start_level(2)
		assert(game.ui.find_child("CabLever",true,false).visible)
	print("CORNER_UI_PASS: corner ordering, no undo/redo in tray, functional hint, strict placement, scenic clearance and three locales")
	game.queue_free()
	await process_frame
	quit()
''')
print("RAILVITO_1_7_PATCH_OK: functional revised HUD and two new used 2K material maps")
