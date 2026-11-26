from pathlib import Path
p=Path("source/Railvito")
def replace_func(s,name,body):
    start=s.index("func "+name+"(")
    end=s.find("\nfunc ",start+1)
    if end<0:end=len(s)
    return s[:start]+body.strip()+"\n"+s[end:]
def edit(path,old,new):
    f=p/path;s=f.read_text();assert old in s,(path,old);f.write_text(s.replace(old,new,1))
edit("project.godot",'config/version="1.5.0"','config/version="1.6.0"')
f=p/"export_presets.cfg";s=f.read_text().replace("1.5.0","1.6.0").replace("version/code=6","version/code=7");f.write_text(s)
f=p/"scripts/main.gd";s=f.read_text()
# Clearly readable, heavier type in every locale, using bundled licensed fonts.
s=s.replace('theme.default_font=font','''var strong:=FontVariation.new()
	strong.base_font=font
	strong.variation_embolden=0.40 if language=="ar" else 0.65
	theme.default_font=strong''',1)
# New solid tactile 2D button assets; use the same icons as before and retain accessibility.
a=p/"assets/deluxe"
palettes={"blue":("3786c5","1e5388"),"green":("439f58","28693a"),"red":("d65442","943a32"),"orange":("e49933","a86724"),"gold":("dca92f","96701c"),"purple":("8d62c9","593f8d"),"neutral":("d4e9f5","7093b1")}
for name,(color,edge) in palettes.items():
    for state in ("normal","hover","pressed","disabled"):
        top=10 if state=="pressed" else 3
        fill="#65778a" if state=="disabled" else "#"+color
        stroke="#435465" if state=="disabled" else "#"+edge
        sheen="0.14" if state=="hover" else "0.08"
        (a/(name+"_"+state+".svg")).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="96" height="80" viewBox="0 0 96 80"><rect x="2" y="9" width="92" height="69" rx="19" fill="{stroke}"/><rect x="3" y="{top}" width="90" height="66" rx="18" fill="{fill}" stroke="{stroke}" stroke-width="3"/><rect x="7" y="{top+4}" width="82" height="24" rx="12" fill="#fff" opacity="{sheen}"/><path d="M14 {top+11}Q21 {top+7} 32 {top+8}" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".33"/></svg>')
(a/"icon_home.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64"><path d="M5 30L32 7 59 30" fill="none" stroke="#fff4d9" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><path d="M15 29L32 15 49 29V55H15Z" fill="#fff4d9"/><rect x="26" y="36" width="12" height="19" rx="3" fill="#317db0"/></svg>')
s=s.replace('for state in ["normal","hover","pressed"]:','for state in ["normal","hover","pressed","disabled"]:',1)
s=s.replace('b.add_theme_constant_override("outline_size",0 if palette=="neutral" else 2)','b.add_theme_constant_override("outline_size",0)',1)
s=s.replace('b.add_theme_constant_override("h_separation",8)','b.add_theme_color_override("font_disabled_color",Color("c6d5df"))\n\tb.add_theme_constant_override("h_separation",8)',1)
# Gesture state is reset at each level. Never place a rail on mouse-down or during pinch.
s=s.replace('var orbiting := false','''var orbiting := false
var touch_tutorial_seen := false
var world_press := false
var press_position := Vector2.ZERO
var pointer_moved := false
var pinch_used := false
var camera_pan := Vector3.ZERO
var pinch_midpoint := Vector2.ZERO
var lever_button_ref: Button''',1)
s=s.replace('screen="game";won=false;hint_used=false;camera_follow=false','screen="game";won=false;hint_used=false;camera_follow=false;world_press=false;pointer_moved=false;pinch_used=false;camera_pan=Vector3.ZERO',1)
s=s.replace('_update_train(0);_update_camera(10.0);_game_ui()','''_update_train(0);_update_camera(10.0);_game_ui()
	if OS.has_feature("android") and not touch_tutorial_seen:
		_show_gesture_tutorial()''',1)
# Keep the same real 3D world; the camera can be orbit-rotated or panned without buttons.
s=s.replace('target=target.lerp(focus,1.0-exp(-delta*3.5))','target=target.lerp(focus+camera_pan,1.0-exp(-delta*3.5))',1)
s=s.replace('camera_follow=not camera_follow\n\tzoom=','camera_follow=not camera_follow\n\tcamera_pan=Vector3.ZERO\n\tzoom=',1)
s=replace_func(s,"_drop_at",'''func _drop_at(pos: Vector2) -> void:
	if screen!="game" or modal!=null or won or speed>0.01 or desired_speed>0:return
	if pos.y<92 or pos.y>get_viewport().get_visible_rect().size.y-110:return
	var best:=_nearest_gap(pos,75.0)
	if best<0:return
	# The selected piece never changes implicitly. Guided mode only gives feedback.
	_place_piece(best)
''')
# Keep exact authored yaw and matching type checks. Highlight incorrect attempts.
s=replace_func(s,"_place_piece",'''func _place_piece(idx: int) -> bool:
	if not missing.has(idx) or won or speed>0.01 or desired_speed>0:return false
	var piece: Dictionary=route.pieces[idx]
	var expected:=posmod(roundi(rad_to_deg(piece.yaw)),360)
	var modulo:=360 if piece.kind=="curve" else 180
	if selected_kind!=piece.kind:
		_reject_gap(idx,t("need_piece") % t(piece.kind) if easy_placement else t("wrong_piece"))
		return false
	if posmod(selected_yaw,modulo)!=posmod(expected,modulo):
		_reject_gap(idx,t("need_turn") % str(expected) if easy_placement else t("wrong_rotation"))
		return false
	missing.erase(idx);track_nodes[idx].visible=true;ghost_nodes[idx].visible=false
	undo_stack.append(idx);redo_stack.clear();_play_sound("snap");_toast(t("snap"));_update_status()
	return true

func _reject_gap(idx: int, message: String) -> void:
	_toast(message)
	var marker: Node=ghost_nodes[idx].find_child("GapMarker",true,false)
	if not marker is MeshInstance3D:return
	var old: Material=marker.material_override
	var red:=StandardMaterial3D.new();red.albedo_color=Color("ff694f");red.shading_mode=BaseMaterial3D.SHADING_MODE_UNSHADED
	marker.material_override=red
	var marker_ref:=weakref(marker)
	get_tree().create_timer(0.65).timeout.connect(func():
		var node=marker_ref.get_ref()
		if is_instance_valid(node) and node.material_override==red:node.material_override=old)
''')
# Correct drag selection and distinguish a tap, a camera swipe and a pinch.
s=replace_func(s,"_input",'''func _input(event: InputEvent) -> void:
	if event is InputEventMouse:pointer=event.position
	if event is InputEventMouseButton and event.button_index==MOUSE_BUTTON_LEFT and not event.pressed:
		if dragging_piece:
			dragging_piece=false
			if not pinch_used:_drop_at(event.position)
			if is_instance_valid(drag_model):drag_model.queue_free()
			drag_model=null
		elif world_press and not pointer_moved and not pinch_used and modal==null:
			_drop_at(event.position)
		world_press=false;orbiting=false
	if event is InputEventScreenTouch:
		if event.pressed:
			touches[event.index]=event.position
			if touches.size()==1:pinch_used=false
			if touches.size()>=2:
				pinch_used=true;world_press=false;orbiting=false
				if dragging_piece:
					dragging_piece=false
					if is_instance_valid(drag_model):drag_model.queue_free()
					drag_model=null
		else:
			touches.erase(event.index);pinch_previous=0.0
	if event is InputEventScreenDrag:
		touches[event.index]=event.position
		if touches.size()==2 and modal==null and screen=="game":
			var points:=touches.values()
			var gap: float=points[0].distance_to(points[1])
			var mid: Vector2=(points[0]+points[1])*0.5
			if pinch_previous>0.0:
				zoom=clampf(zoom-(gap-pinch_previous)*0.035,11,44)
				var shift:=mid-pinch_midpoint
				var scale_factor:=zoom/maxf(1.0,get_viewport().get_visible_rect().size.y)
				var right:=camera.global_basis.x
				var forward:=Vector3(camera.global_basis.z.x,0,camera.global_basis.z.z).normalized()
				camera_pan-=right*shift.x*scale_factor
				camera_pan-=forward*shift.y*scale_factor
				camera_pan.x=clampf(camera_pan.x,-18,18);camera_pan.z=clampf(camera_pan.z,-18,18)
				camera_follow=false
			pinch_midpoint=mid;pinch_previous=gap;pinch_used=true;orbiting=false;world_press=false
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode==KEY_ESCAPE:
			if modal!=null:_close_modal()
			elif screen=="game":_show_levels(world_id)
			else:_show_menu()
		if screen=="game" and modal==null:
			if event.keycode==KEY_R:_rotate_piece()
			if event.keycode==KEY_SPACE:_go() if desired_speed==0 else _brake()
			if event.keycode==KEY_Z and event.ctrl_pressed:_undo()
			if event.keycode==KEY_Y and event.ctrl_pressed:_redo()
''')
s=replace_func(s,"_unhandled_input",'''func _unhandled_input(event: InputEvent) -> void:
	if modal!=null or screen!="game":return
	if event is InputEventMouseButton:
		if event.button_index==MOUSE_BUTTON_WHEEL_UP:zoom=clampf(zoom-1.4,11,44)
		if event.button_index==MOUSE_BUTTON_WHEEL_DOWN:zoom=clampf(zoom+1.4,11,44)
		if event.button_index==MOUSE_BUTTON_LEFT and event.pressed and touches.size()<2:
			world_press=true;press_position=event.position;pointer_moved=false;pinch_used=false;orbiting=true
	if event is InputEventMouseMotion and orbiting and not dragging_piece and touches.size()<2:
		if event.position.distance_to(press_position)>12:pointer_moved=true
		if pointer_moved and not pinch_used:
			yaw-=event.relative.x*0.006;pitch=clampf(pitch+event.relative.y*0.003,0.35,1.15);camera_follow=false
''')
# One compact mission strip, no large white task or camera boxes.
s=replace_func(s,"_game_ui",'''func _game_ui() -> void:
	_set_ui();selected_buttons.clear()
	selected_label=null;switch_label=null;proximity_label=null
	var data: Dictionary=Network.levels()[level_index]
	var dark:=Color(0.10,0.20,0.28,0.92)
	var head:=_panel(Vector2(104,12),Vector2(690,91),dark)
	head.name="MissionStrip"
	_label(t(data.title),Vector2(14,1),Vector2(662,40),29,Color("ffe4a1"),head)
	var instruction:=t("fit_instruction") if data.mode=="build" else t("drive_task") % (data.station+1) if data.mode=="drive" else t("cargo_task") % [data.number,data.station+1]
	if world_id==5:instruction=t("city_cargo_task") % [data.number,data.station+1] if data.mode=="cargo" else t("city_route_task") % (data.station+1)
	task_label=_label(instruction,Vector2(14,41),Vector2(662,45),23,Color.WHITE,head)
	task_label.name="MissionInstruction"
	status_label=_label("",Vector2.ZERO,Vector2.ONE,14,Color.WHITE,head);status_label.hide()
	_deluxe_button("",Vector2(16,15),Vector2(76,76),_show_worlds,"blue","home").name="HomeButton"
	var bell_button:=_deluxe_button("",Vector2(864,15),Vector2(86,76),_ring_bell,"gold","bell")
	bell_button.name="CabBell"
	_deluxe_button("",Vector2(958,15),Vector2(86,76),_show_gesture_tutorial,"blue","help")
	_deluxe_button("",Vector2(1052,15),Vector2(86,76),_settings,"blue","settings")
	_deluxe_button("",Vector2(1146,15),Vector2(116,76),func():_start_level(level_index),"orange","rotate").name="RestartTop"
	if data.mode=="build":
		var controls:=_panel(Vector2(16,600),Vector2(735,104),dark)
		var kinds: Array=["bridge","straight"] if world_id>=2 else ["straight","curve"]
		for i in range(2):
			var kind: String=kinds[i]
			var b:=_deluxe_button(t(kind),Vector2(8+i*168,9),Vector2(160,78),func():_select_piece(kind),"blue",kind,controls,23)
			b.button_down.connect(func():_begin_drag(kind))
			selected_buttons[kind]=b
		_deluxe_button("",Vector2(344,9),Vector2(86,78),_rotate_piece,"orange","rotate",controls)
		_deluxe_button("",Vector2(438,9),Vector2(86,78),_undo,"blue","undo",controls)
		var redo_button:=_deluxe_button("",Vector2(532,9),Vector2(86,78),_redo,"blue","",controls)
		redo_button.icon=load("res://assets/cab/redo.svg");redo_button.expand_icon=true;redo_button.add_theme_constant_override("icon_max_width",42)
		_deluxe_button("",Vector2(626,9),Vector2(101,78),_hint,"gold","star",controls)
		selected_label=_label("",Vector2(12,83),Vector2(710,21),17,Color.WHITE,controls)
	elif data.mode=="cargo" or world_id==5:
		var controls:=_panel(Vector2(16,590),Vector2(735,114),dark)
		if data.mode=="cargo":
			_label(t("load"),Vector2(10,2),Vector2(300,34),22,Color.WHITE,controls)
			for i in range(1,5):
				_deluxe_button(str(i),Vector2(9+(i-1)*78,37),Vector2(70,68),func():_load_cargo(i),"gold","",controls,32)
		if world_id==5:
			var left:=340 if data.mode=="cargo" else 10
			switch_label=_label("",Vector2(left,3),Vector2(350,34),22,Color.WHITE,controls)
			for i in range(3):
				_deluxe_button(str(i+1),Vector2(left+i*115,37),Vector2(107,68),func():_set_switch(i),["red","blue","green"][i],"",controls,32)
			_update_switch_label()
	var cab:=_panel(Vector2(765,600),Vector2(497,104),dark)
	_deluxe_button(t("go").replace("▶","").strip_edges(),Vector2(8,8),Vector2(150,88),_go,"green","play",cab,25)
	var brake_button:=_deluxe_button(t("brake").replace("■","").strip_edges(),Vector2(166,8),Vector2(150,88),_brake,"red","stop",cab,25)
	brake_button.name="CabBrake"
	lever_button_ref=_deluxe_button("",Vector2(324,8),Vector2(165,88),_cycle_speed,"blue","speed",cab,22)
	lever_button_ref.name="CabLever"
	# Keep the speed model for existing controls and tests, but no visible miniature slider.
	speed_slider=HSlider.new();cab.add_child(speed_slider);speed_slider.min_value=0.7;speed_slider.max_value=5;speed_slider.step=0.1;speed_slider.value=speed_setting;speed_slider.hide()
	speed_slider.value_changed.connect(func(v):speed_setting=v;if_running_speed(v);_update_lever())
	_update_lever()
	drag_label=_label("",Vector2.ZERO,Vector2(120,62),34,TEAL);drag_label.visible=false;drag_label.z_index=20
	_update_selection();_update_status()
''')
s=replace_func(s,"_update_lever",'''func _update_lever() -> void:
	if is_instance_valid(lever_model):
		lever_model.rotation.z=lerpf(0.43,-0.43,inverse_lerp(0.7,5.0,speed_setting))
	if is_instance_valid(lever_button_ref):
		lever_button_ref.text=t("gear_slow") if speed_setting<2.0 else t("gear_fast") if speed_setting>3.6 else t("gear_normal")
''')
# Retain useful status, but only one visible instruction. Update on completion, undo or cargo selection.
s=replace_func(s,"_update_status",'''func _update_status() -> void:
	if not is_instance_valid(status_label) or not is_instance_valid(task_label):return
	var mission: Dictionary=Network.levels()[level_index]
	var mode: String=mission.mode
	if mode=="build":
		status_label.text=t("ready") if missing.is_empty() else t("missing") % missing.size()
		task_label.text=t("depart_ready") if missing.is_empty() else t("fit_instruction") if easy_placement else t("manual_instruction")
		for btn in selected_buttons.values():
			if is_instance_valid(btn):btn.disabled=missing.is_empty() or desired_speed>0
	elif mode=="cargo":
		status_label.text=t("loaded") % cargo_count
		if cargo_count==int(mission.number):task_label.text=t("cargo_ready") % (int(mission.station)+1)
		elif world_id==5:task_label.text=t("city_cargo_task") % [mission.number,mission.station+1]
		else:task_label.text=t("cargo_task") % [mission.number,mission.station+1]
	else:
		status_label.text=t("station_hint")
		task_label.text=t("city_route_task") % (mission.station+1) if world_id==5 else t("drive_task") % (mission.station+1)
''')
# Highlight a correct selection without substituting the selected rail.
s=replace_func(s,"_update_selection",'''func _update_selection() -> void:
	if is_instance_valid(selected_label):
		selected_label.text=t(selected_kind)+"  ·  "+str(selected_yaw)+"°"
	for key in selected_buttons:
		if is_instance_valid(selected_buttons[key]):
			_skin(selected_buttons[key],"gold" if key==selected_kind else "blue",23)
''')
# Friendly first-run gesture instructions, persisted locally; also accessible from help.
s=s.replace('func _settings() -> void:','''func _show_gesture_tutorial() -> void:
	var p:=_open_modal(Vector2(720,530))
	_label(t("gesture_title"),Vector2(28,12),Vector2(664,62),35,TEAL,p).horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	_label("↔",Vector2(32,91),Vector2(125,86),64,TEAL,p).horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	_label(t("gesture_drag"),Vector2(168,91),Vector2(520,86),27,INK,p)
	_label("↔  ↕",Vector2(28,188),Vector2(130,86),35,TEAL,p).horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	_label(t("gesture_pinch"),Vector2(168,188),Vector2(520,86),27,INK,p)
	_label("✓",Vector2(32,285),Vector2(125,80),54,TEAL,p).horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	_label(t("gesture_fit"),Vector2(168,285),Vector2(520,90),25,INK,p)
	_deluxe_button(t("gesture_start"),Vector2(68,400),Vector2(584,78),func():touch_tutorial_seen=true;_save();_close_modal(),"green","play",p,30)

func _settings() -> void:''',1)
s=s.replace('c.set_value("state","version",1);','c.set_value("settings","gesture_tutorial_seen",touch_tutorial_seen)\n\tc.set_value("state","version",1);',1)
s=s.replace('if c.load(SAVE_PATH)!=OK:return','if c.load(SAVE_PATH)!=OK:return\n\ttouch_tutorial_seen=bool(c.get_value("settings","gesture_tutorial_seen",false))',1)
# A smaller notification, legible even with Arabic and no instruction overlap.
s=s.replace('var extent:=Vector2(530,48)','var extent:=Vector2(530,55)',1).replace('Vector2(375,100),extent,21','Vector2(375,110),extent,24',1).replace('extent.x)*0.5,100)','extent.x)*0.5,110)',1)
f.write_text(s)
f=p/"scripts/strings.gd";s=f.read_text()
s=s.replace('const ADVENTURE_WORDS := {','''const ADVENTURE_WORDS := {
	"fit_instruction": ["Choose a rail. Rotate it to match the gap.","اختر السكة ودوّرها لتطابق الفراغ.","Escolha e gire o trilho para encaixar."],
	"manual_instruction": ["Match the shape and direction.","طابق شكل السكة واتجاهها.","Combine o formato e a direção."],
	"need_piece": ["Choose: %s","اختر: %s","Escolha: %s"],
	"need_turn": ["Rotate to %s°","دوّر السكة إلى %s°","Gire até %s°"],
	"gear_slow": ["Slow","بطيء","Lento"],
	"gear_normal": ["Normal","عادي","Normal"],
	"gear_fast": ["Fast","سريع","Rápido"],
	"gesture_title": ["Explore your railway!","استكشف عالم القطارات!","Explore sua ferrovia!"],
	"gesture_drag": ["Swipe the scenery with one finger to turn the view.","اسحب بإصبع واحد لتدوير المشهد.","Deslize com um dedo para girar a vista."],
	"gesture_pinch": ["Pinch to zoom. Move two fingers together to pan.","قرّب أو باعد إصبعين للتكبير والتصغير، وحرّكهما معًا لتحريك المشهد.","Pince para ampliar. Mova dois dedos juntos para deslocar."],
	"gesture_fit": ["Choose the correct rail and turn it to fit the glowing gap.","اختر السكة الصحيحة ودوّرها لتناسب الفراغ المضيء.","Escolha o trilho certo e gire para encaixar na lacuna."],
	"gesture_start": ["Let's play!","هيا نلعب!","Vamos jogar!"],''',1)
s=s.replace('["Easy • tap a gap","سهل • انقر على الفراغ","Fácil • toque na lacuna"]','["Guided • hints","مساعد • تلميحات","Guiado • dicas"]')
f.write_text(s)
# Visual landscape expansion with actual geometry and route-safe placement.
# Each closed-loop world now has a small railway village beyond the track.
f=p/"scripts/world_builder.gd";s=f.read_text()
anchor='func _make_castle(pos: Vector3, s: float) -> void:'
assert anchor in s
s=s.replace(anchor,'''func _railway_village(layout: Dictionary,id: int) -> void:
	if id>=2 or layout.is_empty():return
	var curve: Curve3D=layout.curve
	var village:=Node3D.new();village.name="RailwayVillage";root.add_child(village)
	var rng:=RandomNumberGenerator.new();rng.seed=3321+id
	var roof_colors:=["b74735","36779d","8b5c3c"]
	for i in range(6):
		var angle:=float(i)*TAU/6.0+0.31
		var loc:=Vector3(cos(angle)*16.0,0.08,sin(angle)*16.0)
		if absf(loc.x)<4.0 or curve.get_closest_point(loc).distance_to(loc)<4.5:continue
		var b:=model("city-kit-suburban",["building-type-a","building-type-d","building-type-f"][i%3],loc,Vector3.ONE*1.9,angle+PI)
		b.reparent(village)
		var garden:=BoxMesh.new();garden.size=Vector3(3.7,0.10,3.7)
		mesh_node(garden,material("b8ab8d"),loc+Vector3(0,-0.025,0),village)
		for j in range(2):
			var flower_at:=loc+Vector3(-1.5,0.10,-1.4+j*2.8)
			var bush:=model("nature-kit","plant_bushSmall",flower_at,Vector3.ONE*1.4,rng.randf_range(0,TAU))
			bush.reparent(village)
		var pole:=CylinderMesh.new();pole.top_radius=0.055;pole.bottom_radius=0.09;pole.height=1.55;pole.radial_segments=12
		mesh_node(pole,material("564c3b"),loc+Vector3(1.9,0.78,-1.3),village)
		var light:=SphereMesh.new();light.radius=0.16;light.height=0.32;light.radial_segments=16;light.rings=8
		mesh_node(light,material("ffe2a0",0.38),loc+Vector3(1.9,1.58,-1.3),village)

'''+anchor,1)
s=s.replace('\t_quality_details(layout,id)\n','\t_quality_details(layout,id)\n\t_railway_village(layout,id)\n',1)
f.write_text(s)
# Existing tests must validate deliberate selection, rather than the removed auto-fit behavior.
f=p/"tests/verify_deluxe.gd";s=f.read_text()
start=s.index('\t\tgame.easy_placement=true')
end=s.index('\t\tgame._settings()',start)
s=s[:start]+'''		game.easy_placement=true
		var piece: Dictionary=game.route.pieces[idx]
		game.selected_kind="curve" if piece.kind!="curve" else "straight"
		game.selected_yaw=posmod(roundi(rad_to_deg(piece.yaw)),360)
		game._drop_at(gap)
		assert(game.missing.has(idx),"Wrong shape must not be auto-corrected")
		game.selected_kind=piece.kind
		game.selected_yaw=posmod(roundi(rad_to_deg(piece.yaw))+90,360)
		game._drop_at(gap)
		assert(game.missing.has(idx),"Wrong rotation must not be auto-corrected")
		game.selected_yaw=posmod(roundi(rad_to_deg(piece.yaw)),360)
		game._drop_at(gap)
		if gap.y>=92 and gap.y<610:assert(not game.missing.has(idx))
''' +s[end:]
f.write_text(s)
f=p/"tests/verify_polish.gd";s=f.read_text().replace('=="1.5.0"','=="1.6.0"');f.write_text(s)
# Every missing piece in every mission must reject the wrong type and angle, then accept correct placement.
(p/"tests/verify_rails_ui.gd").write_text('''extends SceneTree
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
		assert(game.ui.find_child("HomeButton",true,false)!=null)
		assert(game.ui.find_child("RestartTop",true,false)!=null)
		assert(game.ui.find_child("MissionStrip",true,false)!=null)
		assert(not game.speed_slider.visible)
		for idx in game.missing.duplicate():
			var piece: Dictionary=game.route.pieces[idx]
			for guided in [true,false]:
				game.easy_placement=guided
				game.selected_kind="curve" if piece.kind!="curve" else "straight"
				game.selected_yaw=posmod(roundi(rad_to_deg(piece.yaw)),360)
				assert(not game._place_piece(idx) and game.missing.has(idx))
				game.selected_kind=piece.kind
				game.selected_yaw=posmod(roundi(rad_to_deg(piece.yaw))+90,360)
				assert(not game._place_piece(idx) and game.missing.has(idx))
			game.selected_yaw=posmod(roundi(rad_to_deg(piece.yaw)),360)
			assert(game._place_piece(idx))
		if mission.mode=="build":assert(game.task_label.text==game.t("depart_ready"))
		await process_frame
	for lang in ["en_GB","ar","pt_BR"]:
		game.language=lang
		game._start_level(0)
		game._show_gesture_tutorial()
		assert(game.modal!=null)
		game._close_modal()
		await process_frame
	print("RAILS_UI_PASS: 24 missions, both modes reject wrong rail and rotation, compact HUD, tutorial and 3 locales")
	game.queue_free()
	await process_frame
	quit()
''')
print("RAILVITO_1_6_PATCH_OK")

# Keep the previous selection feedback meaningful while removing its redundant text bar.
f=p/"scripts/main.gd";s=f.read_text()
s=s.replace('Vector2(8+i*168,9),Vector2(160,78)','Vector2(8+i*168,5),Vector2(160,70)').replace('Vector2(344,9),Vector2(86,78)','Vector2(344,5),Vector2(86,70)').replace('Vector2(438,9),Vector2(86,78)','Vector2(438,5),Vector2(86,70)').replace('Vector2(532,9),Vector2(86,78)','Vector2(532,5),Vector2(86,70)').replace('Vector2(626,9),Vector2(101,78)','Vector2(626,5),Vector2(101,70)').replace('Vector2(12,83),Vector2(710,21)','Vector2(12,75),Vector2(710,25)')
# Prevent a new click from using a stale pinch state after returning from a modal.
s=s.replace('selected_kind=kind;dragging_piece=true;_update_selection()','selected_kind=kind;dragging_piece=true;pinch_used=false;_update_selection()',1)
f.write_text(s)
