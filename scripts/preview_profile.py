#!/usr/bin/env python3
"""Render actual README assets and measure SVG layout in local Chrome.

Optional local QA dependencies: Markdown, PyYAML, Playwright (not used by Actions).
Install into the ignored .profile-validation-deps directory, or use your own venv.
Use --compare to render the two user-specified reference commits without checkout.
"""
from pathlib import Path
import argparse
import base64
import json
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.profile-validation-deps'))
import markdown
import yaml
from playwright.sync_api import sync_playwright

CSS='''
* { box-sizing: border-box; } body { margin: 0; background: #0d1117; color: #e6edf3; font: 16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
article { max-width: 960px; padding: 32px; margin: 24px auto; border: 1px solid #30363d; border-radius: 8px; }
img { max-width: 100%; height: auto; vertical-align: middle; } a { color: #58a6ff; text-decoration: none; } a:hover { text-decoration: underline; }
h2 { font-size: 24px; font-weight: 600; padding-bottom: .3em; border-bottom: 1px solid #30363d; margin: 28px 0 16px; line-height: 1.25; }
p { margin: 0 0 16px; } ul { padding-left: 2em; margin: 16px 0; } li { margin: 4px 0; } sub { font-size: 12px; } strong { font-weight: 600; }
@media (max-width: 600px) { article { border: 0; padding: 16px; margin: 0; } h2 { margin-top: 24px; } }
@media (prefers-color-scheme: light) { body { background: #ffffff; color: #1f2328; } article, h2 { border-color: #d1d9e0; } a { color: #0969da; } }
'''


def preview_html(content):
    return '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mubasheer KC — Profile preview</title><style>'+CSS+'</style></head><body><article>'+markdown.markdown(content,extensions=['tables'])+'</article></body></html>'


def historical_readme(ref):
    def blob(path):
        return subprocess.check_output(['git','show',f'{ref}:{path}'],cwd=ROOT)
    source=blob('README.md').decode('utf-8')
    def embed(match):
        path=match.group(1)
        mime='image/svg+xml' if path.endswith('.svg') else 'image/png'
        return '="data:'+mime+';base64,'+base64.b64encode(blob(path.removeprefix('./'))).decode('ascii')+'"'
    return re.sub(r'="(\./assets/[^\"]+)"',embed,source)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compare',action='store_true')
    args=parser.parse_args()
    workflow=ROOT/'.github/workflows/update-profile-activity.yml'
    original=subprocess.check_output(['git','show','HEAD:.github/workflows/update-profile-activity.yml'],cwd=ROOT)
    assert workflow.read_bytes().replace(b'\r\n',b'\n')==original.replace(b'\r\n',b'\n')
    config=yaml.load(workflow.read_text(),Loader=yaml.BaseLoader)
    assert config['on']['schedule'][0]=={'cron':'0 0 * * *','timezone':'Asia/Kolkata'}
    assert config['permissions']=={'contents':'write'}
    print('PASS: workflow YAML and existing schedule/permissions unchanged')
    content=(ROOT/'README.md').read_text(encoding='utf-8')
    target=ROOT/'preview_v3.html'
    target.write_text(preview_html(content),encoding='utf-8')
    results=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
        page=browser.new_page(viewport={'width':1280,'height':1000},device_scale_factor=1)
        for width,theme in [(1280,'dark'),(1280,'light'),(390,'dark'),(390,'light'),(320,'dark')]:
            page.set_viewport_size({'width':width,'height':1000})
            page.emulate_media(color_scheme=theme,reduced_motion='reduce')
            page.goto(target.as_uri())
            page.wait_for_function('Array.from(document.images).every(i=>i.complete)')
            state=page.evaluate('''() => ({width:innerWidth,scroll:document.documentElement.scrollWidth,
                broken:[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src),
                selected:[...document.images].map(i=>i.currentSrc.split('/').pop())})''')
            assert state['scroll']<=width and not state['broken'],state
            page.screenshot(path=str(ROOT/f'preview_v3_{width}_{theme}.png'),full_page=True)
            if width in (1280,390) and theme=='dark':
                for name,source in [('header','assets/header.svg'),('fintrack','assets/projects/fintrack.svg'),('kodehax','assets/projects/kodehax.svg'),('toolkit','assets/ui/toolkit.svg')]:
                    page.locator(f'img[src="./{source}"]').screenshot(path=str(ROOT/f'preview_v3_detail_{width}_{name}.png'))
            results.append({'viewport':width,'theme':theme,'state':state})
            print('PASS: README render',width,theme)
        paths=[*ROOT.glob('assets/*.svg'),*ROOT.glob('assets/ui/*.svg'),*ROOT.glob('assets/cta/*.svg'),*ROOT.glob('assets/projects/*.svg'),ROOT/'assets/activity/activity.svg']
        issues=[]
        for width in (1280,390):
            page.set_viewport_size({'width':width,'height':1000})
            for path in paths:
                page.set_content(path.read_text(encoding='utf-8'))
                found=page.evaluate('''() => {
                    const s=document.querySelector('svg'),v=s.viewBox.baseVal;
                    const visible=t=>{for(let n=t;n&&n!==s;n=n.parentElement) if(getComputedStyle(n).display==='none') return false; return true;};
                    const boxes=[...s.querySelectorAll('text')].filter(visible).map(t=>{const b=t.getBBox(); return {text:t.textContent,x:b.x,y:b.y,w:b.width,h:b.height};});
                    const errors=boxes.filter(b=>b.x<-.5||b.y<-.5||b.x+b.w>v.width+.5||b.y+b.h>v.height+.5);
                    for(let i=0;i<boxes.length;i++) for(let j=i+1;j<boxes.length;j++) {
                      const a=boxes[i],b=boxes[j];
                      if(Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>1&&Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>1) errors.push({overlap:[a.text,b.text]});
                    } return errors;
                }''')
                if found:
                    issues.append({'viewport':width,'file':str(path.relative_to(ROOT)),'issues':found})
        # Exercise the finite header animation under both motion preferences.
        for motion in ('reduce','no-preference'):
            page.emulate_media(reduced_motion=motion)
            page.set_content((ROOT/'assets/header.svg').read_text(encoding='utf-8'))
            animations=page.locator('.trace').evaluate_all('(nodes)=>nodes.map(n=>({name:getComputedStyle(n).animationName,duration:getComputedStyle(n).animationDuration,iterations:getComputedStyle(n).animationIterationCount}))')
            assert all(a['name']=='none' for a in animations) if motion=='reduce' else all(a['duration']=='4s' and a['iterations']=='1' for a in animations)
        if args.compare:
            for ref in ('9deb0155de','d3c553c2e7'):
                historical=ROOT/f'preview_reference_{ref}.html'
                historical.write_text(preview_html(historical_readme(ref)),encoding='utf-8')
                page.set_viewport_size({'width':1280,'height':1000})
                page.emulate_media(color_scheme='dark',reduced_motion='reduce')
                page.goto(historical.as_uri())
                page.wait_for_function('Array.from(document.images).every(i=>i.complete)')
                page.screenshot(path=str(ROOT/f'preview_reference_{ref}.png'),full_page=True)
        browser.close()
    report={'renders':results,'svg_layout_issues':issues,'motion':'PASS: finite 4s; reduced motion disabled','workflow':'unchanged'}
    (ROOT/'scratch_v3_render_results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('SVG layout issues:',json.dumps(issues))
    assert not issues,'Resolve SVG clipping/overlap before delivery'
    print('PASS: SVG font metrics and reduced-motion behavior')


if __name__=='__main__':
    main()
