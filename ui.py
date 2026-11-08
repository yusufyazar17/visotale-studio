STUDIO_HTML = r"""<!doctype html>
<html lang="tr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Visotale Studio</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Fraunces:opsz,wght@9..144,500;9..144,600&display=swap" rel="stylesheet">
<style>
:root{--bg:#FFFFFF;--bg2:#FAFAF7;--bg3:#F4F2EC;--text:#1A1A1A;--mut:#6B6B6B;--sub:#A0A0A0;--gd:#1B3E28;--gm:#225033;--acc:#5EC37E;--soft:#E8F7EC;--bd:#E8E8E5;--bds:#D0D0CB;--err:#D14545}
*{box-sizing:border-box}
body{margin:0;background:var(--bg2);color:var(--text);font-family:'DM Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:'Fraunces',Georgia,serif;font-weight:500;margin:0;letter-spacing:-.01em}
header{background:#fff;border-bottom:1px solid var(--bd);padding:16px 24px;text-align:center}
.logo{font-family:'Fraunces',Georgia,serif;font-weight:500;font-size:28px;letter-spacing:-.02em;background:radial-gradient(140% 100% at 50% 0%,var(--gm) 0%,var(--gd) 65%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none}
.logo em{font-style:italic;font-weight:400}
.hero{text-align:center;padding:30px 16px 6px}
.hero h1{font-size:34px;color:var(--gd)}
.hero p{margin:8px auto 0;max-width:520px;color:var(--mut);font-size:15px;line-height:1.5}
.wrap{max-width:1120px;margin:0 auto;padding:22px 16px 80px;display:grid;grid-template-columns:400px 1fr;gap:24px;align-items:start}
@media(max-width:860px){.wrap{grid-template-columns:1fr}.hero h1{font-size:28px}}
.card{background:#fff;border:1px solid var(--bd);border-radius:20px;padding:22px}
.sec{margin-bottom:22px}
.step{display:flex;align-items:center;gap:10px;margin:0 0 12px}
.step b{width:28px;height:28px;border-radius:50%;background:var(--soft);color:var(--gd);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:600}
.step h2{font-size:19px;color:var(--gd)}
label.l{display:block;font-size:12.5px;color:var(--mut);margin:12px 0 4px}
input[type=password],input[type=number],textarea,select{width:100%;padding:11px 12px;border:1px solid var(--bds);border-radius:12px;font:inherit;font-size:14px;background:#fff}
input:focus,textarea:focus{outline:none;border-color:var(--gm);box-shadow:0 0 0 3px rgba(94,195,126,.25)}
textarea{min-height:100px;resize:vertical;line-height:1.4}
#drop{border:1.5px dashed var(--bds);border-radius:16px;padding:22px 16px;text-align:center;cursor:pointer;background:var(--bg2);color:var(--mut);font-size:14px;transition:all .2s}
#drop:hover,#drop.on{border-color:var(--acc);background:var(--soft)}
#drop img{max-width:100%;max-height:200px;border-radius:12px;display:block;margin:0 auto 10px}
#styles{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.sty{border:1.5px solid var(--bd);background:#fff;border-radius:14px;padding:14px 12px;font:inherit;font-size:14px;font-weight:600;cursor:pointer;text-align:left}
.sty.on{border-color:var(--gm);background:var(--soft);color:var(--gd);box-shadow:0 0 0 3px rgba(94,195,126,.25)}
.seg{display:flex;gap:8px}.seg button{flex:1;border:1.5px solid var(--bd);background:#fff;border-radius:100px;padding:10px;font:inherit;font-size:14px;font-weight:500;cursor:pointer;transition:all .2s}
.seg button.on{background:var(--gd);color:#fff;border-color:var(--gd)}
.tip{font-size:12.5px;color:var(--mut);margin-top:6px}
.go{width:100%;background:var(--text);color:#fff;border:0;border-radius:100px;padding:17px 28px;font:inherit;font-weight:500;font-size:15px;cursor:pointer;transition:all .3s cubic-bezier(.4,0,.2,1)}
.go:hover:not(:disabled){background:var(--acc);transform:translateY(-2px)}
.go:disabled{opacity:.45;cursor:not-allowed}
details summary{cursor:pointer;font-size:13.5px;color:var(--gm);font-weight:500}
.stage{min-height:420px;display:flex;flex-direction:column;gap:16px}
#view{position:relative;background:var(--bg3);border-radius:16px;aspect-ratio:1/1;max-height:72vh;margin:0 auto;width:100%;max-width:660px;overflow:hidden;display:flex;align-items:center;justify-content:center;color:var(--mut);font-size:14px;text-align:center;padding:24px}
#view img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;transition:filter .08s}
#msg.err{color:var(--err)}
.squint{display:none;align-items:center;gap:12px;max-width:660px;margin:0 auto;width:100%;font-size:13px;color:var(--mut)}
.squint input{flex:1;accent-color:var(--gd)}
.act{display:none;gap:16px;justify-content:center;font-size:13.5px}
.act a{color:var(--gm);font-weight:500}
#hist{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}
#hist img{width:84px;height:84px;object-fit:cover;border-radius:12px;border:2px solid var(--bd);cursor:pointer}
.spin{width:34px;height:34px;border:3px solid var(--bd);border-top-color:var(--gm);border-radius:50%;animation:sp 1s linear infinite;margin:0 auto 12px}
@keyframes sp{to{transform:rotate(360deg)}}
</style></head><body>
<header><a class="logo" href="https://visotale.com">visot<em>a</em>le</a></header>
<div class="hero"><h1>Tablonu oluştur</h1><p>Fotoğrafını yükle, bir stil seç; yüzün tabloya gizlensin. Gözünü kısınca ortaya çıkar.</p></div>
<div class="wrap">
<div class="card">
  <div class="sec"><label class="l" style="margin-top:0">Şifre</label><input id="pw" type="password" placeholder="TEST_PASSWORD" autocomplete="off"></div>
  <div class="sec"><div class="step"><b>1</b><h2>Fotoğraf</h2></div>
    <div id="drop"><span id="dropt">Fotoğraf seç ya da buraya bırak</span></div>
    <input id="file" type="file" accept="image/*" hidden></div>
  <div class="sec"><div class="step"><b>2</b><h2>Stil</h2></div><div id="styles"></div></div>
  <div class="sec"><div class="step"><b>3</b><h2>Yüz belirginliği</h2></div>
    <div class="seg" id="seg"><button data-d="-0.1">Az</button><button data-d="0" class="on">Orta</button><button data-d="0.1">Çok</button></div>
    <div class="tip">Çok: yüz daha belirgin, tablo bozulma riski artar.</div></div>
  <div class="sec"><details><summary>Gelişmiş ayarlar</summary>
    <label class="l">Prompt (bu stile özel, düzenleyebilirsin)</label><textarea id="prompt"></textarea>
    <label class="l">Negatif prompt</label><textarea id="neg"></textarea>
    <label class="l">Adım sayısı</label><input id="steps" type="number" min="10" max="50" value="20">
    <label class="l">Guidance</label><input id="guid" type="number" step="0.5" value="7.5">
    <label class="l">Seed benzeri tekrar sayısı (aynı ayarla kaç görsel)</label><input id="rep" type="number" min="1" max="4" value="1"></details></div>
  <button class="go" id="go">Üret</button>
</div>
<div class="card stage">
  <div id="view"><span id="msg">Fotoğraf ve stil seç, “Üret”e bas.</span></div>
  <div class="squint" id="sq"><span>Net</span><input id="blur" type="range" min="0" max="14" value="0"><span>Gözünü kıs</span></div>
  <div class="act" id="act"><a id="dl" target="_blank" download>İndir</a><a id="rawl" target="_blank">Filigransız / ham görsel</a></div>
  <div id="hist"></div>
</div>
</div>
<script>
var STYLES=__STYLES__, DEF=__DEFAULTS__;
var $=function(i){return document.getElementById(i)};
var cur=STYLES.length?STYLES[0].key:null, delta=0, file=null, hist=[];
try{$('pw').value=sessionStorage.getItem('vpw')||''}catch(e){}
function renderStyles(){var h='';STYLES.forEach(function(s){h+='<button class="sty'+(s.key===cur?' on':'')+'" data-k="'+s.key+'">'+s.label+'</button>'});$('styles').innerHTML=h;
 Array.prototype.forEach.call($('styles').children,function(b){b.onclick=function(){cur=b.dataset.k;renderStyles();loadDef()}})}
function loadDef(){var d=DEF[cur];if(!d)return;$('prompt').value=d.prompt;$('neg').value=d.negative_prompt;$('steps').value=d.num_inference_steps;$('guid').value=d.guidance_scale}
renderStyles();loadDef();
Array.prototype.forEach.call($('seg').children,function(b){b.onclick=function(){Array.prototype.forEach.call($('seg').children,function(x){x.classList.remove('on')});b.classList.add('on');delta=parseFloat(b.dataset.d)}});
var drop=$('drop');drop.onclick=function(){$('file').click()};
drop.ondragover=function(e){e.preventDefault();drop.classList.add('on')};drop.ondragleave=function(){drop.classList.remove('on')};
drop.ondrop=function(e){e.preventDefault();drop.classList.remove('on');if(e.dataTransfer.files[0])setFile(e.dataTransfer.files[0])};
$('file').onchange=function(){if(this.files[0])setFile(this.files[0])};
function setFile(f){file=f;drop.innerHTML='<img src="'+URL.createObjectURL(f)+'"><span>'+f.name+' — değiştirmek için tıkla</span>'}
function show(url){var v=$('view');v.innerHTML='<img id="im" src="'+url+'">';$('sq').style.display='flex';$('act').style.display='flex';$('blur').value=0;$('dl').href=url;$('rawl').href=url}
$('blur').oninput=function(){var i=$('im');if(i)i.style.filter='blur('+this.value+'px)'};
function msg(t,err,sp){$('view').innerHTML='<div>'+(sp?'<div class="spin"></div>':'')+'<span id="msg" class="'+(err?'err':'')+'">'+t+'</span></div>';$('sq').style.display='none';$('act').style.display='none'}
function addHist(url){hist.unshift(url);var h='';hist.forEach(function(u,i){h+='<img src="'+u+'" data-i="'+i+'">'});$('hist').innerHTML=h;
 Array.prototype.forEach.call($('hist').children,function(im){im.onclick=function(){show(hist[im.dataset.i])}})}
function poll(id,done,fail){var n=0;(function t(){n++;fetch('/api/job/'+id).then(function(r){return r.json()}).then(function(d){
 if(d.status==='done')return done(d);if(d.status==='error')return fail(d.error||'Hata');if(n>120)return fail('Zaman aşımı');setTimeout(t,2000)}).catch(function(){if(n>120)fail('Bağlantı hatası');else setTimeout(t,3000)})})()}
$('go').onclick=function(){
 if(!$('pw').value){alert('Şifreyi gir.');return}if(!file){alert('Önce fotoğraf seç.');return}if(!cur){alert('Stil yok.');return}
 try{sessionStorage.setItem('vpw',$('pw').value)}catch(e){}
 var rep=Math.max(1,Math.min(4,parseInt($('rep').value)||1)),left=rep,btn=$('go');btn.disabled=true;
 msg('Tablon hazırlanıyor… (30-60 sn sürebilir)',false,true);
 function one(){var fd=new FormData();fd.append('password',$('pw').value);fd.append('style',cur);fd.append('file',file);
  fd.append('prompt',$('prompt').value);fd.append('negative_prompt',$('neg').value);
  fd.append('conditioning_scale',(DEF[cur].conditioning_scale+delta).toFixed(2));
  fd.append('guidance_scale',$('guid').value);fd.append('num_inference_steps',$('steps').value);
  
  fetch('/api/generate',{method:'POST',body:fd}).then(function(r){return r.json().then(function(j){return{s:r.status,b:j}})}).then(function(x){
   if(!x.b.ok){msg(x.b.error||'Hata',true);fin();return}
   poll(x.b.job_id,function(d){var u=d.image_url;addHist(u);show(u);fin()},function(e){msg(e,true);fin()})
  }).catch(function(){msg('Sunucuya ulaşılamadı',true);fin()})}
 function fin(){left--;if(left<=0)btn.disabled=false}
 for(var i=0;i<rep;i++)one()
};
</script></body></html>
"""
