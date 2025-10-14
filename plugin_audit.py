# plugins_audit.py
import os, re, json

base = os.path.abspath(os.path.dirname(__file__))
plugins_dir = os.path.join(base, "plugins")
diag = {}
third_party = set()

stdlib_candidates = set([
    'os','sys','re','json','time','datetime','pathlib','math','subprocess','typing',
    'itertools','collections','random','csv','io','logging','http','threading','asyncio',
    'urllib','urllib3','glob'
])

if not os.path.isdir(plugins_dir):
    print("Aucun dossier plugins/ trouvé dans", base)
    raise SystemExit(1)

for name in sorted(os.listdir(plugins_dir)):
    pdir = os.path.join(plugins_dir, name)
    pfile = os.path.join(pdir, "plugin.py")
    info = {"path": pfile, "has_file": os.path.exists(pfile)}
    if os.path.exists(pfile):
        txt = open(pfile, 'r', encoding='utf-8').read()
        info['has_run'] = bool(re.search(r'def\s+run\s*\(', txt))
        info['has_meta'] = bool(re.search(r'\bmeta\s*=\s*{', txt))
        lowered = txt.lower()
        markers = []
        for m in ['demo', 'sample', 'placeholder', 'todo', 'notimplementederror']:
            if m in lowered:
                markers.append(m)
        info['markers'] = markers
        imps = re.findall(r'^\s*(?:from|import)\s+([^\s,]+)', txt, flags=re.MULTILINE)
        info['imports'] = sorted(set(imps))
        for im in info['imports']:
            pkg = im.split('.')[0]
            if pkg and pkg not in stdlib_candidates:
                third_party.add(pkg)
    diag[name] = info

# Write diag
with open(os.path.join(base, "PLUGINS_AUDIT.json"), 'w', encoding='utf-8') as f:
    json.dump(diag, f, indent=2, ensure_ascii=False)

# Write inferred requirements
rpath = os.path.join(base, "requirements_plugins.txt")
with open(rpath, 'w', encoding='utf-8') as f:
    if third_party:
        f.write("# Dependencies inferred from plugin imports (verify versions)\n")
        for pkg in sorted(third_party):
            f.write(pkg + "\n")
    else:
        f.write("# No obvious third-party imports detected automatically. Verify plugin files.\n")

print("Audit créé:", os.path.join(base, "PLUGINS_AUDIT.json"))
print("requirements_plugins.txt créé:", rpath)