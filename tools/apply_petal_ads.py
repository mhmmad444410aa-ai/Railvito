from pathlib import Path
import sys,re,zipfile
p=Path("source/Railvito")
def change(f,a,b):
    s=f.read_text();assert a in s,(str(f),a[:90]);f.write_text(s.replace(a,b,1))
if len(sys.argv)==1:
    change(p/"project.godot",'config/version="1.7.0"','config/version="1.8.0"')
    f=p/"export_presets.cfg";s=f.read_text().replace("1.7.0","1.8.0").replace("version/code=8","version/code=9").replace("gradle_build/use_gradle_build=false","gradle_build/use_gradle_build=true").replace('gradle_build/min_sdk=""','gradle_build/min_sdk="24"').replace('gradle_build/target_sdk=""','gradle_build/target_sdk="36"').replace("permissions/internet=false","permissions/internet=true").replace("permissions/access_network_state=false","permissions/access_network_state=true")
    f.write_text(s)
    change(p/"tests/verify_polish.gd",'=="1.7.0"','=="1.8.0"')
    f=p/"scripts/main.gd"
    change(f,"var web_clock := 0.0","""var web_clock := 0.0
var ads_bridge: Object
var ads_screen_state := false
var ads_state_known := false
var ad_transition := false
var ad_screen_clock := 0.0""")
    change(f,'\t_show_menu()\n\tif OS.has_feature("web"):', '''	_show_menu()
	if OS.has_feature("android") and Engine.has_singleton("RailvitoAds"):
		ads_bridge=Engine.get_singleton("RailvitoAds")
		get_viewport().size_changed.connect(_ads_resize)
		_ads_sync()
	if OS.has_feature("web"):''')
    change(f,'func _process(delta: float) -> void:\n\ttimer+=delta','''func _process(delta: float) -> void:
	ad_screen_clock+=delta
	if ad_screen_clock>=0.2:
		ad_screen_clock=0.0
		_ads_sync()
	timer+=delta''')
    change(f,'func(): _start_level(level_index+1) if level_index<stars.size()-1 else _show_worlds(),TEAL,p)','_ads_next_adventure,TEAL,p)')
    change(f,'func _open_modal(size: Vector2) -> Panel:','''func _ads_sync() -> void:
	if not is_instance_valid(ads_bridge):return
	var visible_banner: bool=(screen=="menu" or screen=="game") and not is_instance_valid(modal) and not ad_transition
	if not ads_state_known or visible_banner!=ads_screen_state:
		ads_state_known=true;ads_screen_state=visible_banner
		ads_bridge.setScreenVisible(visible_banner)

func _ads_resize() -> void:
	if not is_instance_valid(ui) or is_instance_valid(modal):return
	if screen=="menu":_show_menu()
	elif screen=="game":_game_ui()
	elif screen=="worlds":_show_worlds()
	elif screen=="levels":_show_levels(world_id)

func _ads_next_adventure() -> void:
	if ad_transition:return
	ad_transition=true
	_ads_sync()
	if is_instance_valid(ads_bridge):
		ads_bridge.betweenMissions()
		while is_instance_valid(ads_bridge) and ads_bridge.transitionPending():
			await get_tree().process_frame
	ad_transition=false
	if level_index<stars.size()-1:_start_level(level_index+1)
	else:_show_worlds()
	_ads_sync()

func _ads_privacy() -> void:
	var p:=_open_modal(Vector2(780,560))
	_label(t("ads_privacy_title"),Vector2(28,10),Vector2(720,56),30,TEAL,p)
	var body:=_label(t("ads_privacy_body"),Vector2(28,80),Vector2(720,235),23,INK,p)
	body.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	var approved: bool=is_instance_valid(ads_bridge) and ads_bridge.hasConsent()
	_button(t("ads_withdraw") if approved else t("ads_agree"),Vector2(28,344),Vector2(720,62),func():
		if is_instance_valid(ads_bridge):ads_bridge.setConsent(not approved)
		_close_modal()
		_show_menu()
		_ads_sync(),TEAL,p)
	_button(t("close"),Vector2(28,436),Vector2(720,62),_parents_area,CREAM,p)

func _open_modal(size: Vector2) -> Panel:''')
    change(f,'\tmodal=Control.new();ui.add_child(modal);modal.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)','\tmodal=Control.new();ui.add_child(modal);modal.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)\n\t_ads_sync()')
    change(f,'\t_button(t("close"),Vector2(28,362),Vector2(662,62),_close_modal,TEAL,p)','''	if is_instance_valid(ads_bridge):
		_button(t("ads_privacy_title"),Vector2(28,362),Vector2(662,48),_ads_privacy,Color("e4ebd8"),p)
	_button(t("close"),Vector2(28,419),Vector2(662,48),_close_modal,TEAL,p)''')
    f=p/"scripts/strings.gd";s=f.read_text()
    s=s.replace('const ADVENTURE_WORDS := {','''const ADVENTURE_WORDS := {
	"privacy_body": ["Play works offline. Optional child-directed contextual Petal Ads require adult privacy consent and internet. The SDK may process limited technical and ad-event information. Progress stays on this device. No accounts, chat or location permission. Adults may withdraw consent in the parents area.","اللعب يعمل دون إنترنت. تتطلب إعلانات Petal Ads السياقية الموجهة للأطفال موافقة الوالد واتصال الإنترنت. قد تعالج الحزمة معلومات تقنية وأحداث الإعلان المحدودة. يبقى التقدم على الجهاز. لا حسابات أو دردشة أو إذن الموقع. يمكن للوالد سحب الموافقة من قسم الوالدين.","O jogo funciona offline. Anúncios contextuais infantis da Petal Ads exigem consentimento do responsável e internet. O SDK pode processar dados técnicos e eventos publicitários limitados. O progresso fica no aparelho. Sem contas, chat ou permissão de localização. O responsável pode retirar o consentimento."],
	"parent_note": ["Rewards come from play. No purchases or paid random rewards. Adults can review the privacy notice for contextual ads.","المكافآت من اللعب فقط. لا مشتريات أو مكافآت عشوائية مدفوعة. يمكن للوالد مراجعة إشعار خصوصية الإعلانات السياقية.","Recompensas vêm do jogo. Sem compras ou prêmios aleatórios pagos. Responsáveis podem revisar a privacidade dos anúncios contextuais."],
	"ads_privacy_title": ["Advertising privacy","خصوصية الإعلانات","Privacidade dos anúncios"],
	"ads_privacy_body": ["For adults only. Petal Ads can show contextual ads, using child and under-age protection and rating W. Limited technical information and ad interactions may be processed by Huawei. No personalised ads. Read the privacy policy first. Consent is optional, can be withdrawn here, and is not needed to play.","للوالدين فقط. قد تعرض Petal Ads إعلانات سياقية مع حماية الأطفال والقاصرين وتصنيف W. قد تعالج هواوي معلومات تقنية وتفاعلات إعلانية محدودة. لا إعلانات مخصصة. اقرأ سياسة الخصوصية أولًا. الموافقة اختيارية ويمكن سحبها هنا، ولا يشترط تقديمها للعب.","Somente responsáveis. Petal Ads pode mostrar anúncios contextuais com proteção infantil e classificação W. A Huawei pode tratar dados técnicos limitados e interações publicitárias. Sem anúncios personalizados. Leia a política primeiro. O consentimento é opcional, revogável aqui e não é necessário para jogar."],
	"ads_agree": ["I consent as the parent / guardian","أوافق بصفتي ولي الأمر","Consinto como responsável"],
	"ads_withdraw": ["Withdraw consent","سحب الموافقة","Retirar consentimento"],''',1)
    f.write_text(s)
    print("ADS_GDSCRIPT_PATCH_OK")
else:
    # Install the official, version-matched Gradle export source.
    template=Path(sys.argv[1]);root=p/"android/build";root.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(template) as z:z.extractall(root)
    (root/".gdignore").touch()
    (root.parent/".build_version").write_text(sys.argv[2]+"\n")
    f=root/"build.gradle";s=f.read_text()
    assert "dependencies {" in s and "repositories {" in s
    s=s.replace("repositories {","repositories {\n        maven { url 'https://developer.huawei.com/repo/' }",1)
    s=s.replace("dependencies {","dependencies {\n    implementation 'com.huawei.hms:ads-prime:3.4.91.300'",1)
    f.write_text(s)
    f=root/"src/main/AndroidManifest.xml";s=f.read_text()
    assert "</application>" in s and "</manifest>" in s
    s=s.replace("</application>",'<meta-data android:name="org.godotengine.plugin.v2.RailvitoAds" android:value="com.railvito.ads.RailvitoAds" />\n    </application>',1)
    # No location, advertising ID permission, or optional sensitive permissions.
    if 'xmlns:tools=' not in s:s=s.replace("<manifest ","<manifest xmlns:tools=\"http://schemas.android.com/tools\" ",1)
    denied=["android.permission.ACCESS_FINE_LOCATION","android.permission.ACCESS_COARSE_LOCATION","android.permission.READ_PHONE_STATE","android.permission.QUERY_ALL_PACKAGES","com.google.android.gms.permission.AD_ID"]
    s=s.replace("</manifest>","\n".join('<uses-permission android:name="'+x+'" tools:node="remove" />' for x in denied)+"\n</manifest>")
    f.write_text(s)
    f=root/"proguard-rules.pro"
    with f.open("a") as w:w.write("\n-keep class com.huawei.openalliance.ad.** { *; }\n-keep class com.huawei.hms.ads.** { *; }\n-keep class com.railvito.ads.** { *; }\n")
    f=root/"src/main/java/com/railvito/ads/RailvitoAds.java";f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(r'''package com.railvito.ads;

import android.app.Activity;
import android.content.Context;
import android.content.SharedPreferences;
import android.content.pm.ApplicationInfo;
import android.graphics.Color;
import android.os.Handler;
import android.os.Looper;
import android.os.SystemClock;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import com.huawei.hms.ads.AdListener;
import com.huawei.hms.ads.AdParam;
import com.huawei.hms.ads.HwAds;
import com.huawei.hms.ads.InterstitialAd;
import com.huawei.hms.ads.RequestOptions;
import com.huawei.hms.ads.banner.BannerView;
import com.huawei.hms.ads.BannerAdSize;
import org.godotengine.godot.Godot;
import org.godotengine.godot.plugin.GodotPlugin;
import org.godotengine.godot.plugin.UsedByGodot;

public final class RailvitoAds extends GodotPlugin {
    private static final String TAG="RailvitoAds";
    private static final String BANNER="v6hj6tigae", INTERSTITIAL="d58nfmswrt";
    private static final String TEST_BANNER="testw6vs28auh3", TEST_INTERSTITIAL="teste9ih9j0rc3";
    private final Handler main=new Handler(Looper.getMainLooper());
    private FrameLayout slot;
    private BannerView banner;
    private InterstitialAd inter;
    private SharedPreferences prefs;
    private volatile boolean consent, pending;
    private boolean initialized, foreground, eligible, showing, opened, bannerVisible, destroyed;
    private long lastShown, lastLoad;
    private int transitions;
    public RailvitoAds(Godot godot){super(godot);}
    @Override public String getPluginName(){return "RailvitoAds";}
    @Override public View onMainCreate(Activity a){
        prefs=a.getSharedPreferences("railvito_ad_privacy_v1",Context.MODE_PRIVATE);
        consent=prefs.getBoolean("adult_consent",false);
        slot=new FrameLayout(a);
        slot.setBackgroundColor(Color.rgb(20,37,48));
        slot.setVisibility(View.GONE);
        slot.setClickable(false);
        slot.setLayoutParams(new FrameLayout.LayoutParams(-1,dp(64),Gravity.BOTTOM));
        reserve();
        return slot;
    }
    private int dp(int n){return Math.round(n*getActivity().getResources().getDisplayMetrics().density);}
    private boolean fits(){return getActivity()!=null && getActivity().getResources().getDisplayMetrics().widthPixels>=dp(320) && getActivity().getResources().getDisplayMetrics().heightPixels>=dp(300);}
    private void reserve(){
        if(slot==null||getGodot().getRenderView()==null)return;
        View render=getGodot().getRenderView().getView();
        if(render==null)return;
        FrameLayout.LayoutParams lp=new FrameLayout.LayoutParams(-1,-1,Gravity.TOP);
        lp.bottomMargin=consent&&fits()?dp(64):0;
        if(render.getLayoutParams() instanceof FrameLayout.LayoutParams){
            FrameLayout.LayoutParams old=(FrameLayout.LayoutParams)render.getLayoutParams();
            if(old.bottomMargin==lp.bottomMargin)return;
        }
        render.setLayoutParams(lp);
    }
    private boolean debug(){return (getActivity().getApplicationInfo().flags&ApplicationInfo.FLAG_DEBUGGABLE)!=0;}
    private AdParam request(){
        return new AdParam.Builder().setRequestLocation(false).build();
    }
    private boolean configure(){
        if(!consent||destroyed||getActivity()==null)return false;
        if(!initialized){
            try{
                RequestOptions child=new RequestOptions.Builder()
                    .setTagForChildProtection(1).setTagForUnderAgeOfPromise(1)
                    .setNonPersonalizedAd(1).setAdContentClassification("W").build();
                HwAds.setRequestOptions(child);
                HwAds.init(getActivity().getApplicationContext());
                HwAds.setRequestOptions(child);
                initialized=true;
            }catch(Exception|LinkageError e){Log.w(TAG,"Ad initialization unavailable",e);return false;}
        }
        return true;
    }
    @UsedByGodot public boolean hasConsent(){return consent;}
    @UsedByGodot public void setConsent(boolean value){
        consent=value;
        main.post(()->{
            if(destroyed||prefs==null)return;
            prefs.edit().putBoolean("adult_consent",value).putLong("consent_time_ms",System.currentTimeMillis()).apply();
            if(!value){hideBanner();if(banner!=null){banner.destroy();banner=null;}inter=null;}
            reserve();update();
        });
    }
    @UsedByGodot public void setScreenVisible(boolean value){
        main.post(()->{eligible=value;update();});
    }
    private void hideBanner(){
        if(slot!=null)slot.setVisibility(View.GONE);
        if(banner!=null&&bannerVisible)banner.pause();
        bannerVisible=false;
    }
    private void update(){
        if(destroyed||!consent||!foreground||!eligible||showing||pending||!fits()){hideBanner();return;}
        if(!configure()){hideBanner();return;}
        try{
            if(banner==null){
                banner=new BannerView(getActivity());
                banner.setAdId(debug()?TEST_BANNER:BANNER);
                banner.setBannerAdSize(BannerAdSize.BANNER_SIZE_320_50);
                banner.setBannerRefresh(60);
                FrameLayout.LayoutParams b=new FrameLayout.LayoutParams(dp(320),dp(50),Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);
                slot.addView(banner,b);
                slot.setVisibility(View.VISIBLE);bannerVisible=true;
                banner.loadAd(request());
            }else if(!bannerVisible){slot.setVisibility(View.VISIBLE);banner.resume();bannerVisible=true;}
            preload();
        }catch(Exception|LinkageError e){Log.w(TAG,"Banner unavailable",e);hideBanner();}
    }
    private void preload(){
        if(!consent||!foreground||showing||!configure())return;
        long now=SystemClock.elapsedRealtime();
        if(inter!=null&&(inter.isLoaded()||inter.isLoading()))return;
        if(lastLoad!=0&&now-lastLoad<60000)return;
        lastLoad=now;
        try{
            inter=new InterstitialAd(getActivity());
            inter.setAdId(debug()?TEST_INTERSTITIAL:INTERSTITIAL);
            inter.setAdListener(new AdListener(){
                @Override public void onAdOpened(){opened=true;lastShown=SystemClock.elapsedRealtime();transitions=0;}
                @Override public void onAdClosed(){finishTransition();}
                @Override public void onAdFailed(int error){if(showing)finishTransition();Log.d(TAG,"Interstitial unavailable: "+error);}
            });
            inter.loadAd(request());
        }catch(Exception|LinkageError e){inter=null;Log.w(TAG,"Interstitial load unavailable",e);}
    }
    @UsedByGodot public boolean transitionPending(){return pending;}
    @UsedByGodot public void betweenMissions(){
        if(!consent||pending||destroyed)return;
        pending=true;
        main.post(()->{
            if(destroyed){pending=false;return;}
            transitions++;
            // Only after a finished mission, at most once per 2 transitions and 120 seconds.
            long now=SystemClock.elapsedRealtime();
            if(!consent||!foreground||!configure()||transitions<2||(lastShown!=0&&now-lastShown<120000)||inter==null||!inter.isLoaded()){
                pending=false;preload();return;
            }
            hideBanner();showing=true;opened=false;
            try{
                inter.show(getActivity());
                main.postDelayed(()->{if(showing&&!opened)finishTransition();},5000);
            }catch(Exception|LinkageError e){finishTransition();}
        });
    }
    private void finishTransition(){showing=false;opened=false;pending=false;inter=null;lastLoad=0;}
    @Override public void onMainResume(){foreground=true;update();}
    @Override public void onMainPause(){foreground=false;hideBanner();}
    @Override public void onMainDestroy(){destroyed=true;pending=false;main.removeCallbacksAndMessages(null);hideBanner();if(banner!=null)banner.destroy();banner=null;inter=null;}
}
''')
    print("ADS_ANDROID_TEMPLATE_PATCH_OK")
