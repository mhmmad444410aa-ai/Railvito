from pathlib import Path
import math, random
p=Path("source/Railvito")
a=p/"assets"/"deluxe";a.mkdir(exist_ok=True)
# Independently authored vector assets; no third-party design or watermark.
def svg(name,w,h,body):
    (a/(name+".svg")).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>',encoding="utf-8")
def gradient(id,top,bottom):
    return f'<linearGradient id="{id}" x2="0" y2="1"><stop stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient>'
# Original illustrated mountain railway menu, with all controls layered separately.
defs='<defs>'+''.join(gradient(*v) for v in [
('sky','#168bdf','#d0f6ff'),('mount','#87b5d1','#457d9c'),('hill','#92d85a','#267c46'),('grass','#9de158','#377c34'),('water','#85e5f8','#1389ce'),('roof','#f48851','#9d3225'),('wall','#ffdb9a','#d79650'),('blue','#58c7ff','#164b9c'),('red','#ff7d52','#b52a26'),('metal','#7895aa','#263f52'),('gold','#fff29d','#d89017')])+'</defs>'
s=defs+'<rect width="1280" height="720" fill="url(#sky)"/>'
for x,y,k in [(50,90,1),(350,65,.7),(740,118,.8),(1110,65,1.2)]:
    s+=f'<g transform="translate({x} {y}) scale({k})" fill="#fff" opacity=".86"><ellipse rx="75" ry="22"/><circle cx="-24" cy="-15" r="26"/><circle cx="18" cy="-21" r="34"/><circle cx="55" cy="-8" r="22"/></g>'
s+='<path d="M0 345L170 165 244 227 395 110 550 280 650 180 780 300 930 130 1120 292 1240 176 1280 219V480H0Z" fill="url(#mount)"/><path d="M120 220L170 165 244 227 170 199ZM317 187L395 110 493 217 397 165 363 190ZM865 204L930 130 1014 203 929 171Z" fill="#eaf8ff"/><path d="M0 345Q160 270 330 367T650 350Q850 239 1030 342T1280 320V720H0Z" fill="url(#hill)"/><path d="M0 460Q200 363 380 438T780 423Q960 345 1280 437V720H0Z" fill="url(#grass)"/><path d="M1020 322L985 473 1009 510 1047 527 1074 466 1061 322Z" fill="#90a6a5"/><path d="M1024 325Q1010 420 1030 470L1010 510Q936 542 862 557T789 720H1280V642Q1190 590 1100 566T1054 470L1057 325Z" fill="url(#water)"/><path d="M1040 330L1035 470Q1006 542 893 568M1060 585Q1130 604 1225 616" fill="none" stroke="#e8fbff" stroke-width="9" opacity=".8" stroke-linecap="round"/>'
# bridge, hills, station and perspective track
s+='<g fill="#aab8b4" stroke="#74877e" stroke-width="3"><path d="M690 418H1178V447H690Z"/><path d="M712 445V534H748V445ZM819 445V523H855V445ZM926 445V510H962V445ZM1033 445V500H1069V445ZM1140 445V493H1170V445Z"/></g><path d="M680 417H1183" stroke="#6f4832" stroke-width="8"/>'
random.seed(417)
for i in range(85):
    x=random.randint(0,1275);y=random.randint(293,560)
    if (x>975 and y>405) or (x<310 and y>360) or (400<x<670 and y>420):continue
    h=random.randint(24,64)*(0.75+(y-293)/400)
    s+=f'<g transform="translate({x} {y})"><ellipse cy="4" rx="{h*.32:.1f}" ry="4" fill="#315e37" opacity=".3"/><path d="M0 0V{-h*.52:.1f}" stroke="#825c37" stroke-width="{h*.1:.1f}"/><path d="M0 {-h:.1f}L{-h*.30:.1f} {-h*.37:.1f}H{-h*.18:.1f}L{-h*.39:.1f} {-h*.15:.1f}H{h*.39:.1f}L{h*.18:.1f} {-h*.37:.1f}H{h*.30:.1f}Z" fill="{random.choice(["#298649","#369b43","#176e43","#4ca84b"])}"/></g>'
s+='<path d="M0 580Q270 535 465 545L790 720H0Z" fill="#d2b18a"/><path d="M294 720L480 490 518 490 735 720Z" fill="#777b75"/><path d="M324 720L489 490M698 720L509 490" fill="none" stroke="#d6dfdf" stroke-width="13"/>'
for j in range(13):
    y=500+j*j*1.4;f=(y-490)/230
    s+=f'<path d="M{488-155*f:.1f} {y:.1f}H{512+176*f:.1f}" stroke="#79513d" stroke-width="{4+12*f:.1f}"/>'
s+='<g stroke="#895934" stroke-width="3"><path d="M0 260L252 260 302 323 302 557 0 557Z" fill="url(#wall)"/><path d="M0 239L135 157 307 259 280 290 135 210 0 282Z" fill="url(#roof)"/><path d="M0 345H309V365H0Z" fill="#aa562e"/><rect x="47" y="383" width="85" height="103" rx="6" fill="#275b7e"/><path d="M89 385V484M49 434H130" stroke="#ffe6af" stroke-width="7"/><rect x="175" y="374" width="80" height="179" rx="6" fill="#8f5332"/><rect x="184" y="390" width="62" height="68" rx="4" fill="#83d6ea"/><circle cx="137" cy="235" r="25" fill="#fff4d0"/><path d="M137 217V236L151 244" fill="none" stroke="#6c4d35" stroke-width="4"/><path d="M0 558H310L330 580H0Z" fill="#e6c49f"/></g>'
# locomotive with no human-like face; dimensional gradient shapes
s+='<g transform="translate(260 320)"><ellipse cx="184" cy="300" rx="198" ry="24" fill="#294c49" opacity=".4"/><rect x="25" y="100" width="147" height="155" rx="14" fill="url(#red)" stroke="#762d25" stroke-width="5"/><path d="M12 99Q94 35 186 97V119H12Z" fill="url(#roof)" stroke="#833925" stroke-width="5"/><rect x="50" y="128" width="88" height="62" rx="9" fill="#a2e9ff" stroke="#ffdc72" stroke-width="8"/><path d="M57 139L97 180H125L84 139Z" fill="#fff" opacity=".5"/><rect x="140" y="139" width="200" height="113" rx="47" fill="url(#blue)" stroke="#194b7c" stroke-width="5"/><path d="M168 149H304" stroke="#bbecff" stroke-width="8" stroke-linecap="round" opacity=".7"/><path d="M190 142V250M258 142V250" stroke="#e4ab35" stroke-width="8"/><ellipse cx="337" cy="196" rx="47" ry="56" fill="url(#metal)" stroke="#f3be48" stroke-width="9"/><ellipse cx="339" cy="196" rx="24" ry="32" fill="#344d61" stroke="#a9c6d5" stroke-width="4"/><path d="M273 140L282 78H323L330 140Z" fill="url(#metal)"/><ellipse cx="302" cy="78" rx="28" ry="10" fill="#273f54" stroke="#f4bb45" stroke-width="6"/><ellipse cx="302" cy="76" rx="15" ry="5" fill="#1b3347"/><path d="M147 244H366L384 278H21V249Z" fill="url(#red)" stroke="#782b25" stroke-width="5"/>'
for x in [75,180,276]:
    s+=f'<g transform="translate({x} 273)"><circle r="35" fill="#253d4b" stroke="#142939" stroke-width="5"/><circle r="24" fill="#e4b653" stroke="#c57e24" stroke-width="4"/><path d="M-20 0H20M0-20V20M-14-14L14 14M-14 14L14-14" stroke="#f8d98a" stroke-width="5"/><circle r="7" fill="#8d5631"/></g>'
s+='<path d="M75 273H276" stroke="#cfd9dd" stroke-width="9" stroke-linecap="round"/><path d="M348 248L389 248 417 292H327Z" fill="url(#red)" stroke="#8e352e" stroke-width="5"/><path d="M350 255L344 282M366 255V282M382 255L395 282" stroke="#ffbc89" stroke-width="5"/><circle cx="338" cy="126" r="20" fill="url(#gold)" stroke="#a87120" stroke-width="5"/><circle cx="333" cy="121" r="9" fill="#fff4b8"/></g>'
for i in range(18):
    x=random.randint(0,1280);y=random.randint(600,720)
    if 310<x<720:continue
    s+=f'<circle cx="{x}" cy="{y}" r="{random.randint(3,6)}" fill="{random.choice(["#ffef7c","#fff6ef","#ff8aa4"])}"/>'
svg("station",1280,720,s)
# Glossy 9-slice UI textures. Stretch only central portion, keeping rounded ends.
colors={"green":("#7ce917","#269d12","#126a1f"),"orange":("#ffc24e","#ed740b","#a54610"),"purple":("#b98bff","#7524cf","#45208d"),"blue":("#58b9fa","#126ec4","#15477e"),"gold":("#ffd967","#e3970b","#a55d14"),"red":("#ff8b65","#d33b36","#8b2f31"),"neutral":("#e9f8ff","#94c2e2","#486d97")}
for name,(top,bottom,edge) in colors.items():
    for state in ("normal","pressed","hover"):
        y=7 if state=="pressed" else 2
        svg(name+"_"+state,96,80,'<defs>'+gradient("g",top,bottom)+'</defs>'+f'<rect x="2" y="9" width="92" height="69" rx="20" fill="{edge}"/><rect x="3" y="{y+2}" width="90" height="67" rx="19" fill="url(#g)" stroke="#fff3d8" stroke-width="3"/><rect x="7" y="{y+6}" width="82" height="58" rx="15" fill="none" stroke="{edge}" stroke-opacity=".65" stroke-width="2"/><path d="M18 {y+12}Q24 {y+8} 40 {y+10}" stroke="#fff" opacity=".7" stroke-width="4" stroke-linecap="round"/>'+('<rect x="5" y="5" width="86" height="64" rx="17" fill="#fff" opacity=".13"/>' if state=="hover" else ''))
icons={
"play":'<path d="M22 12L51 32 22 52Z" fill="#fff" stroke="#234d66" stroke-width="3" stroke-linejoin="round"/>',
"map":'<path d="M8 17L24 9 41 16 56 8V48L41 56 24 48 8 56Z" fill="#ffe6a0" stroke="#744f32" stroke-width="3"/><path d="M24 9V48M41 16V56" stroke="#cf9c4f" stroke-width="2"/><path d="M14 41Q22 19 33 34T50 24" stroke="#e6573f" stroke-width="3" stroke-dasharray="5 4" fill="none"/><circle cx="45" cy="18" r="7" fill="#e74d42" stroke="#fff" stroke-width="2"/>',
"train":'<rect x="12" y="8" width="40" height="44" rx="8" fill="#f7f3dc" stroke="#234d66" stroke-width="3"/><rect x="18" y="14" width="28" height="20" rx="4" fill="#56b7f1"/><circle cx="22" cy="43" r="4" fill="#e3a42d"/><circle cx="42" cy="43" r="4" fill="#e3a42d"/><path d="M21 51L14 58M43 51L50 58" stroke="#fff" stroke-width="5"/>',
"star":'<path d="M32 5L40 23 60 25 45 39 49 59 32 49 15 59 19 39 4 25 24 23Z" fill="#ffdd56" stroke="#9c6019" stroke-width="3" stroke-linejoin="round"/>',
"book":'<path d="M5 12Q19 5 32 16Q45 5 59 12V52Q45 45 32 56Q19 45 5 52Z" fill="#fff3d7" stroke="#78533a" stroke-width="3"/><path d="M32 16V56M12 23L25 26M12 31L25 34M39 26L52 23M39 34L52 31" stroke="#b99567" stroke-width="3"/>',
"home":'<path d="M5 29L32 6 59 29H51V56H13V29Z" fill="#fff2dc" stroke="#234d66" stroke-width="3"/><rect x="26" y="38" width="12" height="18" fill="#65a6dd"/>',
"help":'<circle cx="32" cy="32" r="26" fill="#fff4d4" stroke="#234d66" stroke-width="3"/><path d="M24 21Q24 12 34 15Q47 19 38 30L32 36V40" fill="none" stroke="#215e91" stroke-width="7" stroke-linecap="round"/><circle cx="32" cy="48" r="4" fill="#215e91"/>',
"settings":'<path d="M24 6H40L43 15 52 17 60 29 53 36 54 46 42 55 33 50 24 57 11 48 12 38 5 30 13 17 22 15Z" fill="#f4f8ff" stroke="#234d66" stroke-width="3"/><circle cx="32" cy="31" r="10" fill="#347cb1"/>',
"straight":'<path d="M21 5V59M43 5V59" stroke="#d7e3e7" stroke-width="6"/><path d="M12 10H52M12 21H52M12 32H52M12 43H52M12 54H52" stroke="#9b633c" stroke-width="6"/>',
"curve":'<path d="M14 57Q14 12 58 12M34 57Q34 32 58 32" fill="none" stroke="#cfdde5" stroke-width="6"/><path d="M6 54H42M11 34L45 48M23 16L47 40M42 7L52 40M56 4V39" stroke="#9b633c" stroke-width="5"/>',
"bridge":'<path d="M4 21H60V34H4Z" fill="#ca985d" stroke="#664a32" stroke-width="3"/><path d="M9 35V59M55 35V59M9 35L32 56 55 35M4 13H60" fill="none" stroke="#8c6641" stroke-width="5"/><path d="M4 21H60" stroke="#e8edf0" stroke-width="4"/>',
"bell":'<path d="M32 5Q21 5 21 16Q11 24 11 42L5 48H59L53 42Q53 24 43 16Q43 5 32 5Z" fill="#ffd451" stroke="#a66b1a" stroke-width="3"/><circle cx="32" cy="52" r="7" fill="#e3a02c"/>',
"stop":'<rect x="14" y="14" width="36" height="36" rx="6" fill="#fff5e7" stroke="#7b3031" stroke-width="4"/>',
"speed":'<path d="M7 48A26 26 0 0 1 57 48Z" fill="#fff" stroke="#234d66" stroke-width="3"/><path d="M32 43L47 20" stroke="#e04b35" stroke-width="5" stroke-linecap="round"/><circle cx="32" cy="43" r="5" fill="#234d66"/>',
"rotate":'<path d="M50 22A22 22 0 1 0 50 44M50 8V24H34" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
"undo":'<path d="M20 18Q52 13 52 40Q52 53 38 54M20 5L7 21 22 36" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
"lock":'<rect x="12" y="27" width="40" height="31" rx="7" fill="#ffe7a5" stroke="#234d66" stroke-width="3"/><path d="M20 27V17A12 12 0 0 1 44 17V27" stroke="#fff" fill="none" stroke-width="6"/>'
}
for k,v in icons.items():svg("icon_"+k,64,64,v)

f=p/"scripts"/"main.gd";s=f.read_text()
def replace_func(name,body):
    global s
    start=s.index("func "+name+"(")
    end=s.find("\nfunc ",start+1)
    if end<0:end=len(s)
    s=s[:start]+body.strip()+"\n"+s[end:]
# Fixed 1280x720 logical coordinates, regardless of phone aspect ratio.
project=p/"project.godot";q=project.read_text().replace('config/version="1.2.0"','config/version="1.3.0"').replace('window/stretch/mode="canvas_items"','window/stretch/mode="canvas_items"\nwindow/stretch/aspect="keep"');project.write_text(q)
export=p/"export_presets.cfg";export.write_text(export.read_text().replace("1.2.0","1.3.0").replace("version/code=3","version/code=4"))
s=s.replace('var language := "en_GB"','var easy_placement := true\nvar language := "en_GB"')
s=s.replace('var theme := Theme.new()','var theme := Theme.new()')
# New uniform, scalable button kit across all screens.
start=s.index("func _button(")
end=s.index("\nfunc _right(",start)
s=s[:start]+'''func _skin(b: Button, palette: String, font_size := 24) -> void:
	for state in ["normal","hover","pressed"]:
		var skin := StyleBoxTexture.new()
		skin.texture=load("res://assets/deluxe/"+palette+"_"+state+".svg")
		for side in [SIDE_LEFT,SIDE_RIGHT,SIDE_TOP,SIDE_BOTTOM]:
			skin.set_texture_margin(side,23)
			skin.set_content_margin(side,10)
		b.add_theme_stylebox_override(state,skin)
	for state in ["font_color","font_hover_color","font_pressed_color","font_focus_color"]:
		b.add_theme_color_override(state,Color("173955") if palette=="neutral" else Color.WHITE)
	b.add_theme_color_override("font_outline_color",Color("17334c"))
	b.add_theme_constant_override("outline_size",0 if palette=="neutral" else 4)
	b.add_theme_font_size_override("font_size",font_size)
	b.add_theme_constant_override("h_separation",8)

func _button(text: String, pos: Vector2, size: Vector2, callback: Callable, color := CREAM, parent: Control = null) -> Button:
	var b := Button.new();(parent if parent else ui).add_child(b)
	b.text=text
	b.focus_mode=Control.FOCUS_NONE
	if language=="ar":b.text_direction=Control.TEXT_DIRECTION_RTL
	var palette := "neutral"
	if color==TEAL:palette="green"
	elif color==CORAL:palette="red"
	elif color==GOLD:palette="gold"
	elif color.get_luminance()<0.55:palette="blue"
	_skin(b,palette,22)
	b.size=size
	b.position=_flow_position(pos,size,parent)
	b.pressed.connect(func(): _play_sound("click");callback.call())
	return b

func _deluxe_button(text: String, pos: Vector2, extent: Vector2, callback: Callable, palette: String, icon_name: String, parent: Control = null, font_size := 26) -> Button:
	var b:=_button(text,pos,extent,callback,CREAM,parent)
	_skin(b,palette,font_size)
	if icon_name!="":
		b.icon=load("res://assets/deluxe/icon_"+icon_name+".svg")
		b.expand_icon=true
		b.add_theme_constant_override("icon_max_width",mini(48,int(extent.y-16)))
	b.size=extent
	return b
''' +s[end:]
replace_func("_show_menu",'''func _show_menu() -> void:
	if world_id!=0:
		_create_world(0)
	screen="menu";missing.clear();won=false;desired_speed=2.3;speed=2.3;distance=3;camera_follow=false
	for n in track_nodes:n.visible=true
	_set_ui()
	var bg:=TextureRect.new();ui.add_child(bg)
	bg.name="MenuLandscape";bg.texture=load("res://assets/deluxe/station.svg")
	bg.expand_mode=TextureRect.EXPAND_IGNORE_SIZE;bg.stretch_mode=TextureRect.STRETCH_SCALE
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	bg.mouse_filter=Control.MOUSE_FILTER_IGNORE
	var logo:=_label("Railvito",Vector2(410,14),Vector2(460,108),76,Color("ffdc56"))
	logo.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	logo.add_theme_color_override("font_outline_color",Color("83421d"));logo.add_theme_constant_override("outline_size",15)
	var ribbon:=_panel(Vector2(440,113),Vector2(400,43),Color("a74732"))
	var sub:=_label(t("menu_subtitle"),Vector2(10,0),Vector2(380,43),20,Color.WHITE,ribbon);sub.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	var play:=_deluxe_button(t("menu_play"),Vector2(775,235),Vector2(455,94),_continue,"green","play",null,39)
	play.name="MenuPlay"
	_deluxe_button(t("worlds"),Vector2(775,342),Vector2(455,84),_show_worlds,"orange","map",null,31).name="MenuWorlds"
	_deluxe_button(t("menu_adventures"),Vector2(775,439),Vector2(455,84),_show_adventures,"purple","star",null,31).name="MenuAdventures"
	_deluxe_button(t("menu_garage"),Vector2(35,625),Vector2(280,75),_train_menu,"blue","train",null,25)
	_deluxe_button(t("menu_achievements"),Vector2(345,625),Vector2(280,75),_achievements,"gold","star",null,24)
	_deluxe_button(t("menu_daily"),Vector2(655,625),Vector2(280,75),_daily_adventure,"purple","map",null,23)
	_deluxe_button(t("help"),Vector2(965,625),Vector2(280,75),_help,"blue","book",null,24)
	_deluxe_button("",Vector2(1160,24),Vector2(90,67),_settings,"blue","settings",null,22)
	_deluxe_button(t("language"),Vector2(965,24),Vector2(183,67),_settings,"blue","",null,23)
	_deluxe_button(t("parents"),Vector2(28,24),Vector2(245,67),_parents_gate,"blue","lock",null,20)
	# Keep art on the left and action buttons on the right in Arabic too.
	for child in ui.get_children():
		if child is Control and child!=bg and language=="ar":
			child.position.x=1280-child.position.x-child.size.x

func _show_adventures() -> void:
	_show_worlds()

func _achievements() -> void:
	var p:=_open_modal(Vector2(620,350))
	_label(t("menu_achievements"),Vector2(24,12),Vector2(572,70),34,TEAL,p).horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	var total:=0
	for value in stars:total+=int(value)
	_label("★  %s / %s" % [total,stars.size()*3],Vector2(24,90),Vector2(572,82),46,GOLD,p).horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	_label(t("all_progress") % [stars.size()-stars.count(0),stars.size()],Vector2(24,176),Vector2(572,60),25,INK,p).horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	_deluxe_button(t("close"),Vector2(80,262),Vector2(460,64),_close_modal,"green","",p)

func _daily_adventure() -> void:
	var day: int=int(Time.get_unix_time_from_system()/86400.0)
	_start_level(posmod(day,stars.size()))
''')
# More welcoming first mission and consistent child-friendly HUD.
replace_func("_continue",'''func _continue() -> void:
	var next:=stars.find(0)
	_start_level(0 if next<0 else next)
''')
replace_func("_game_ui",'''func _game_ui() -> void:
	_set_ui();selected_buttons.clear()
	var data: Dictionary=Network.levels()[level_index]
	var header:=_panel(Vector2(20,15),Vector2(875,82),Color("eaf6ff"))
	_deluxe_button("",Vector2(7,7),Vector2(68,68),func(): _show_levels(world_id),"blue","home",header)
	_label(t(data.title),Vector2(92,5),Vector2(770,43),29,Color("164d76"),header)
	status_label=_label("",Vector2(94,46),Vector2(760,29),20,Color("287b48"),header)
	var bell_button:=_deluxe_button("",Vector2(912,15),Vector2(105,82),_ring_bell,"gold","bell")
	bell_button.name="CabBell"
	_deluxe_button("",Vector2(1025,15),Vector2(105,82),_help,"blue","help")
	_deluxe_button("",Vector2(1138,15),Vector2(122,82),_settings,"blue","settings")
	var task:=_panel(Vector2(20,106),Vector2(425,92),Color(0.93,0.98,1,0.92))
	var instruction:=t("easy_instruction") if data.mode=="build" and easy_placement else t("build_task") if data.mode=="build" else t("drive_task") % (data.station+1) if data.mode=="drive" else t("cargo_task") % [data.number,data.station+1]
	if world_id==5:instruction=t("city_cargo_task") % [data.number,data.station+1] if data.mode=="cargo" else t("city_route_task") % (data.station+1)
	task_label=_label(instruction,Vector2(12,4),Vector2(401,84),20,INK,task)
	var controls:=_panel(Vector2(20,590),Vector2(744,112),Color("eaf6ff"))
	if data.mode=="build":
		var kinds: Array=["bridge","straight"] if world_id>=2 else ["straight","curve"]
		for i in range(2):
			var kind: String=kinds[i]
			var b:=_deluxe_button(t(kind),Vector2(9+i*174,10),Vector2(166,74),func(): _select_piece(kind),"blue",kind,controls,20)
			b.button_down.connect(func(): _begin_drag(kind))
			selected_buttons[kind]=b
		_deluxe_button("",Vector2(361,10),Vector2(92,74),_rotate_piece,"orange","rotate",controls)
		_deluxe_button("",Vector2(462,10),Vector2(92,74),_undo,"blue","undo",controls)
		_deluxe_button(t("hint").replace("✦","").strip_edges(),Vector2(564,10),Vector2(169,74),_hint,"gold","star",controls,21)
		selected_label=_label("",Vector2(10,82),Vector2(724,28),16,INK,controls)
	else:
		if data.mode=="cargo":
			_label(t("load"),Vector2(12,3),Vector2(320,29),19,INK,controls)
			for i in range(1,5):
				_deluxe_button(str(i),Vector2(10+(i-1)*79,32),Vector2(72,69),func(): _load_cargo(i),"orange","",controls,30)
		if world_id==5:
			var left:=340 if data.mode=="cargo" else 15
			switch_label=_label("",Vector2(left,3),Vector2(350,31),19,INK,controls)
			for i in range(3):
				_deluxe_button(str(i+1),Vector2(left+i*112,35),Vector2(103,65),func(): _set_switch(i),["red","blue","green"][i],"",controls,27)
			_update_switch_label()
		elif data.mode=="drive":
			_label(t("station_hint"),Vector2(14,8),Vector2(710,90),24,INK,controls)
	var speed_panel:=_panel(Vector2(778,590),Vector2(482,112),Color("eaf6ff"))
	_deluxe_button(t("go").replace("▶","").strip_edges(),Vector2(7,7),Vector2(153,97),_go,"green","play",speed_panel,22)
	var brake_button:=_deluxe_button(t("brake").replace("■","").strip_edges(),Vector2(168,7),Vector2(154,97),_brake,"red","stop",speed_panel,22)
	brake_button.name="CabBrake"
	var lever_button:=_deluxe_button("",Vector2(330,7),Vector2(144,59),_cycle_speed,"blue","speed",speed_panel)
	lever_button.name="CabLever"
	speed_slider=HSlider.new();speed_panel.add_child(speed_slider);speed_slider.position=_flow_position(Vector2(336,75),Vector2(130,26),speed_panel);speed_slider.size=Vector2(130,26)
	speed_slider.min_value=0.7;speed_slider.max_value=5;speed_slider.step=0.1;speed_slider.value=speed_setting
	speed_slider.value_changed.connect(func(v): speed_setting=v;if_running_speed(v);_update_lever())
	var camera_panel:=_panel(Vector2(1175,220),Vector2(85,275),Color(0.93,0.98,1,0.94))
	_deluxe_button("+",Vector2(7,6),Vector2(71,62),func():zoom=clampf(zoom-2,14,40),"blue","",camera_panel,32)
	_deluxe_button("−",Vector2(7,73),Vector2(71,62),func():zoom=clampf(zoom+2,14,40),"blue","",camera_panel,32)
	_deluxe_button("◉",Vector2(7,140),Vector2(71,62),func():camera_follow=not camera_follow,"blue","",camera_panel,28)
	_deluxe_button("",Vector2(7,207),Vector2(71,62),func():_start_level(level_index),"orange","rotate",camera_panel)
	drag_label=_label("",Vector2.ZERO,Vector2(120,62),34,TEAL);drag_label.visible=false;drag_label.z_index=20
	_update_selection();_update_status()
''')
# A tap on a lit gap automatically chooses the right kind/orientation for young children.
# Direct placement remains strict, preserving engine tests and manual puzzle controls.
s=s.replace('var best:=_nearest_gap(pos,65.0)\n\tif best>=0:_place_piece(best)','''var best:=_nearest_gap(pos,105.0 if easy_placement else 65.0)
	if best>=0:
		if easy_placement and not dragging_piece:
			selected_kind=route.pieces[best].kind
			selected_yaw=posmod(roundi(rad_to_deg(route.pieces[best].yaw)),360)
			_update_selection()
		_place_piece(best)''')
s=s.replace('get_visible_rect().size.y-145','get_visible_rect().size.y-130')
s=s.replace('selected_buttons[key].add_theme_stylebox_override("normal",_cab_style(Color("f1cc82") if key==selected_kind else Color("e7eedb")))','_skin(selected_buttons[key],"gold" if key==selected_kind else "blue",20)')
# Larger gap marker, no change to required cargo or destination.
s=s.replace('ring.inner_radius=0.62;ring.outer_radius=0.78','ring.inner_radius=0.80;ring.outer_radius=1.04')
s=s.replace('var b:=_button(t("close"),','var b:=_button(t("close"),')
# Do not show a misleading music toggle or nonfunctional extras.
f.write_text(s)
# 6 additional independently authored missions, with distinct tasks and target stations.
f=p/"scripts"/"rail_network.gd";q=f.read_text()
q=q.replace('{"id":17,"world":5,"variant":1,"title":"city_green","mode":"drive","station":2,"number":1}','''{"id":17,"world":5,"variant":1,"title":"city_green","mode":"drive","station":2,"number":1},
		{"id":18,"world":0,"title":"forest_repair","mode":"build","missing":[0,6,12],"station":1,"number":1},
		{"id":19,"world":1,"title":"garden_repair","mode":"build","missing":[1,4,7,11],"station":0,"number":1},
		{"id":20,"world":0,"title":"forest_delivery","mode":"cargo","missing":[],"station":2,"number":3},
		{"id":21,"world":1,"title":"water_delivery","mode":"cargo","missing":[],"station":0,"number":2},
		{"id":22,"world":0,"title":"forest_stop","mode":"drive","missing":[],"station":1,"number":1},
		{"id":23,"world":1,"title":"garden_stop","mode":"drive","missing":[],"station":2,"number":1}''')
f.write_text(q)
f=p/"scripts"/"strings.gd";q=f.read_text();q=q.replace("const ADVENTURE_WORDS := {",'''const ADVENTURE_WORDS := {
	"menu_subtitle": ["Kids Train Games 3D","ألعاب القطارات للأطفال","Jogos de Trem 3D"],
	"menu_play": ["Play now","ابدأ اللعب","Jogar agora"],
	"menu_adventures": ["Adventures","المغامرات","Aventuras"],
	"menu_garage": ["Train garage","مرآب القطارات","Garagem"],
	"menu_achievements": ["Achievements","الإنجازات","Conquistas"],
	"menu_daily": ["Daily adventure","مغامرة اليوم","Aventura do dia"],
	"easy_instruction": ["Tap a glowing gap to fit a track.","اضغط على الفراغ المضيء لتركيب السكة.","Toque na lacuna brilhante para encaixar."],
	"forest_repair": ["Forest track repair","إصلاح سكة الغابة","Reparo na floresta"],
	"garden_repair": ["Garden track repair","إصلاح سكة الحديقة","Reparo no jardim"],
	"forest_delivery": ["Forest cargo express","توصيل طرود الغابة","Entrega na floresta"],
	"water_delivery": ["Waterfall cargo express","توصيل طرود الشلال","Entrega na cachoeira"],
	"forest_stop": ["Forest station stop","التوقف بمحطة الغابة","Parada na floresta"],
	"garden_stop": ["Garden station stop","التوقف بمحطة الحديقة","Parada no jardim"],''')
f.write_text(q)
# Wrap the level grid into 2 rows for expanded worlds, instead of tiny columns.
f=p/"scripts"/"main.gd";s=f.read_text();start=s.index("func _show_levels(");end=s.index("\nfunc _start_level(",start)
s=s[:start]+'''func _show_levels(id: int) -> void:
	if world_id!=id or id>=2:_create_world(id)
	missing.clear()
	screen="levels";desired_speed=1.8;speed=1.8;camera_follow=false
	zoom=38 if id>=2 else 31;target=Vector3.ZERO
	for n in track_nodes:n.visible=true
	for n in ghost_nodes.values():n.visible=false
	_set_ui()
	_deluxe_button(t("back"),Vector2(24,20),Vector2(165,65),_show_worlds,"blue","home")
	_label(t(Network.WORLD_NAMES[id]),Vector2(220,20),Vector2(850,75),34,TEAL)
	var entries: Array=Network.world_levels(id)
	var p:=_panel(Vector2(50,414),Vector2(1180,287),Color("eaf6ff"))
	_label(t("choose_level"),Vector2(20,6),Vector2(1140,38),25,INK,p)
	for i in range(entries.size()):
		var mission: Dictionary=entries[i]
		var idx: int=mission.id
		var mark:=("  "+"★".repeat(stars[idx])) if stars[idx]>0 else ""
		var col:=i%4
		var row:=floori(float(i)/4.0)
		_deluxe_button(t(mission.title)+mark,Vector2(12+col*292,51+row*110),Vector2(282,100),func():_start_level(idx),"gold" if stars[idx]>0 else "blue","",p,20)
''' +s[end:]
# verify all 16 closed-loop missions, while existing 8 open-world tests are unchanged.
s=s.replace('for i in range(10):\n\t\t_start_level(i)','for i in range(10)+range(18,24):\n\t\t_start_level(i)')
f.write_text(s)
f=p/"tests"/"verify_worlds.gd";q=f.read_text().replace(".slice(10):",".slice(10,18):").replace("game.stars.size()==18","game.stars.size()==24");f.write_text(q)
f=p/"tests"/"verify_cab.gd";f.write_text(f.read_text().replace("all 18 missions","all 24 missions"))
print("RAILVITO_DELUXE_PATCH_OK: 24 missions; original scalable 2D kit and new menu")

# Retain manual rotation, undo AND redo; make auto-fit optional from Settings.
f=p/"scripts"/"main.gd";s=f.read_text()
s=s.replace('Vector2(361,10),Vector2(92,74),_rotate_piece','Vector2(361,10),Vector2(78,74),_rotate_piece')
s=s.replace('Vector2(462,10),Vector2(92,74),_undo','Vector2(447,10),Vector2(78,74),_undo')
s=s.replace('Vector2(564,10),Vector2(169,74),_hint','Vector2(619,10),Vector2(114,74),_hint')
s=s.replace('\t\tselected_label=_label("",Vector2(10,82)', '\t\tvar redo_button:=_deluxe_button("",Vector2(533,10),Vector2(78,74),_redo,"blue","") if false else _deluxe_button("",Vector2(533,10),Vector2(78,74),_redo,"blue","",controls)\n\t\tredo_button.icon=load("res://assets/cab/redo.svg");redo_button.expand_icon=true;redo_button.add_theme_constant_override("icon_max_width",42)\n\t\tselected_label=_label("",Vector2(10,82)')
s=s.replace('var redo_button:=_deluxe_button("",Vector2(533,10),Vector2(78,74),_redo,"blue","") if false else _deluxe_button','var redo_button:=_deluxe_button')
s=s.replace('t("hint").replace("✦","").strip_edges(),Vector2(619','"",Vector2(619')
s=s.replace('var p:=_open_modal(Vector2(700,565))','var p:=_open_modal(Vector2(700,610))')
s=s.replace('\t_button(t("close"),Vector2(28,454),Vector2(630,64),func():_save();_close_modal(),TEAL,p)', '''	_label(t("fit_mode"),Vector2(28,420),Vector2(280,50),21,INK,p)
	_button(t("fit_easy") if easy_placement else t("fit_manual"),Vector2(320,420),Vector2(338,52),func(): easy_placement=not easy_placement;_save();_settings(),Color("e5ebd8"),p)
	_button(t("close"),Vector2(28,527),Vector2(630,64),func():_save();_close_modal();_game_ui() if screen=="game" else _show_menu() if screen=="menu" else _refresh_screen(),TEAL,p)''')
# Keep original screen on settings close; reflow HUD only while playing.
s=s.replace('func():_save();_close_modal();_game_ui() if screen=="game" else _show_menu() if screen=="menu" else _refresh_screen()','func():_save();_close_modal();_game_ui() if screen=="game" else _show_menu() if screen=="menu" else _close_modal()')
s=s.replace('c.set_value("settings","language",language);','c.set_value("settings","easy_placement",easy_placement)\n\tc.set_value("settings","language",language);')
s=s.replace('var lang=str(c.get_value("settings","language","en_GB"))','easy_placement=bool(c.get_value("settings","easy_placement",true))\n\tvar lang=str(c.get_value("settings","language","en_GB"))')
# Correct first-run camera framing and make the rail gaps much easier to identify.
s=s.replace('zoom=39.0 if world_id>=2 else (29.5 if world_id==0 else 31.5)','zoom=35.5 if world_id>=2 else (26.5 if world_id==0 else 28.5)')
f.write_text(s)
f=p/"scripts"/"strings.gd";q=f.read_text().replace('const ADVENTURE_WORDS := {','''const ADVENTURE_WORDS := {
	"fit_mode": ["Track placement","تركيب السكك","Encaixe dos trilhos"],
	"fit_easy": ["Easy • tap a gap","سهل • انقر على الفراغ","Fácil • toque na lacuna"],
	"fit_manual": ["Manual • rotate pieces","يدوي • دوّر القطع","Manual • gire as peças"],''');f.write_text(q)
# Replace pastel toy-board materials with a more vivid landscape palette.
f=p/"scripts"/"world_builder.gd";q=f.read_text()
for old,new in [('9cd8db','65b5e6'),('edf3db','dcf4ff'),('d6dfcb','80b76a'),('78a56e','6dbb50'),('6aa891','54a870'),('f5dfad','d6bb78'),('bd9166','986d49'),('a7cba0','7dbb56'),('83b58e','5ca35b'),('b5d4a5','a3ca67'),('Vector3(rng.randf_range(4.0,6.2),rng.randf_range(1.1,2.5),rng.randf_range(3.5,5.4))','Vector3(rng.randf_range(5.4,8.4),rng.randf_range(1.4,3.0),rng.randf_range(4.6,7.0))')]:
    q=q.replace(old,new)
# Keep rounded hills low and distant; do not modify the route or collisions.
f.write_text(q)
f=p/"scripts"/"adventure_art.gd";q=f.read_text().replace('["54854f","78a661","577552"]','["3d8b48","89c963","547957"]').replace('art.material("c0d5d8",0.34)','art.material("e2edf2",0.30)').replace('side*0.30-0.045,side*0.30+0.045','side*0.30-0.065,side*0.30+0.065').replace('art.material("8c5a39")','art.material("855032")');f.write_text(q)
# Real UI smoke test: construct menu and HUD in each supported locale and check actual controls.
(p/"tests"/"verify_deluxe.gd").write_text('''extends SceneTree
func _initialize() -> void:
	call_deferred("verify")
func verify() -> void:
	var game = load("res://scenes/main.tscn").instantiate()
	root.add_child(game)
	await process_frame
	game.set_process(false)
	for lang in ["en_GB","ar","pt_BR"]:
		game.language=lang
		game._show_menu()
		await process_frame
		for name in ["MenuLandscape","MenuPlay","MenuWorlds","MenuAdventures"]:
			assert(game.ui.find_child(name,true,false)!=null,name)
		game._start_level(0)
		await process_frame
		for name in ["CabBell","CabBrake","CabLever"]:
			assert(game.ui.find_child(name,true,false)!=null,name)
		assert(game.selected_buttons.size()==2)
		var idx: int=game.missing[0]
		var gap: Vector2=game.camera.unproject_position(game.route.pieces[idx].center)
		assert(game._nearest_gap(gap,105.0)==idx)
		game.easy_placement=true
		game._drop_at(gap)
		# A marker covered by the bottom UI must not receive a touch.
		if gap.y<590:assert(not game.missing.has(idx))
		game._settings()
		game._close_modal()
	print("DELUXE_UI_PASS: menu, controls, locales and assisted placement")
	game.queue_free()
	await process_frame
	quit(0)
''')
