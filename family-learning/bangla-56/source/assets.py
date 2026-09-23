from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
import shutil

ROOT=Path(__file__).resolve().parent
DEST=ROOT/'release'/'assets'
ICONS={'star':'2b50','moon':'1f319','mango':'1f96d','woman':'1f469','man':'1f468','child':'1f9d2','wave':'1f44b','snake':'1f40d','mouse':'1f401','eagle':'1f985','camel':'1f42a','minus':'2796','sun':'2600','one':'31-20e3','point':'1f449','plus':'2795','medicine':'1f48a','banana':'1f34c','notebook':'1f4d3','cow':'1f404','house':'1f3e0','palette':'1f3a8','wheel':'1f6de','umbrella':'2602','water':'1f4a7','basket':'1f9fa','hand':'1f590','tomato':'1f345','lips':'1f444','egg':'1f95a','drum':'1f941','deer':'1f98c','melon':'1f349','plate':'1f37d','milk':'1f95b','rice':'1f33e','boat':'26f5','bird':'1f426','flower':'1f33a','ball':'26bd','bowl':'1f35a','fish':'1f41f','car':'1f697','night':'1f303','lemon':'1f34b','lotus':'1fab7','ox':'1f402','soap':'1f9fc','elephant':'1f418','rain':'1f327','foot':'1f9b6','party':'1f389','book':'1f4d6','sad':'1f622','shirt':'1f455','shoe':'1f45f','hat':'1f452','toothbrush':'1faa5','spoon':'1f944','bed':'1f6cf','bag':'1f392','pencil':'270f','apple':'1f34e','eye':'1f441','happy':'1f642','angry':'1f620','palm':'1f334','tree':'1f333','sky':'2601'}

def fetch(pair):
    name,code=pair
    target=DEST/(name+'.svg')
    if target.exists(): return
    with urlopen('https://raw.githubusercontent.com/jdecked/twemoji/main/assets/svg/'+code+'.svg',timeout=40) as r:
        data=r.read()
    if b'<svg' not in data: raise ValueError(name)
    target.write_bytes(data)

if __name__=='__main__':
    DEST.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(fetch,ICONS.items()))
    shutil.copy2(ROOT.parent/'NotoSansBengali.ttf',DEST/'NotoSansBengali.ttf')
    # A pillow and river drawn for this book, rather than unrelated emoji substitutes.
    (DEST/'pillow.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 100"><rect x="8" y="20" width="104" height="60" rx="16" fill="#c8d7f5" stroke="#3c5c91" stroke-width="4"/><path d="M20 30 Q60 40 100 30 M20 70 Q60 60 100 70" fill="none" stroke="#fff" stroke-width="4"/></svg>')
    (DEST/'river.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120"><path fill="#d4edce" d="M0 0h120v120H0z"/><path fill="#57bade" d="M60 0h20C20 40 110 65 65 120H25C90 70 0 40 60 0"/><path d="M65 15C40 45 84 72 54 107" fill="none" stroke="#c5f4ff" stroke-width="3"/></svg>')
    for name,url in [('FONT-LICENSE.txt','https://raw.githubusercontent.com/google/fonts/main/ofl/notosansbengali/OFL.txt'),('ART-LICENSE.txt','https://raw.githubusercontent.com/jdecked/twemoji/main/LICENSE-GRAPHICS')]:
        with urlopen(url,timeout=40) as r:(DEST/name).write_bytes(r.read())
    print('Assets ready:',len(list(DEST.glob('*.svg'))))
