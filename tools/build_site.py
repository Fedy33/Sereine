import re,shutil,os,json
import sys
# Usage : python3 tools/build_site.py <page.html publiée par l'artifact, sans l'enveloppe> <dossier du dépôt>
SRC,REPO=sys.argv[1],sys.argv[2]
src=open(SRC).read()
if src.lstrip().lower().startswith('<!doctype'):
    lines=src.split('\n'); src='\n'.join(lines[1:-1] if lines[-1].strip()=='</body></html>' else lines[1:])
head='''<!doctype html>
<html lang="fr"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#FBF8F3" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#1A1714" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Sereine">
<meta name="description" content="Démarches, aides, garde et soutien pour les futures et jeunes mamans.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script>window.SEREINE_SITE=true;</script>
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
</head><body>
'''
body=src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
body=body.replace('<title>Sereine</title>\n','',1)
out=head.replace('<meta charset="utf-8">','<meta charset="utf-8">\n<title>Sereine</title>')+body+'\n<script>if("serviceWorker" in navigator)navigator.serviceWorker.register("sw.js").catch(()=>{});</script>\n</body></html>\n'
open(REPO+'/index.html','w').write(out)
json.dump({"name":"Sereine","short_name":"Sereine","description":"Démarches, aides, garde et soutien pour les futures et jeunes mamans.","lang":"fr","start_url":"./","scope":"./","display":"standalone","background_color":"#FBF8F3","theme_color":"#FBF8F3",
 "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]},open(REPO+'/manifest.webmanifest','w'),ensure_ascii=False,indent=1)
open(REPO+'/sw.js','w').write('''const V="sereine-v1-"+"BUILD";
self.addEventListener("install",e=>{self.skipWaiting();e.waitUntil(caches.open(V).then(c=>c.addAll(["./","index.html","manifest.webmanifest","icon-192.png"])))});
self.addEventListener("activate",e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim())));
self.addEventListener("fetch",e=>{const u=new URL(e.request.url);if(e.request.method!=="GET"||u.origin!==location.origin)return;
 e.respondWith(fetch(e.request).then(r=>{const c=r.clone();caches.open(V).then(x=>x.put(e.request,c));return r}).catch(()=>caches.match(e.request)))});
'''.replace('BUILD',str(int(__import__('time').time()))))
open(REPO+'/.nojekyll','w').write('')
print('site ok')
