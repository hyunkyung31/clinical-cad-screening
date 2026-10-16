"""Review public artifacts without executing notebook code or contacting services."""
from pathlib import Path
import ast,hashlib,json,re,sys
import nbformat
from IPython.core.inputtransformer2 import TransformerManager
ROOT=Path(__file__).resolve().parents[1]
errors=[];counts={'notebooks':0,'code_cells':0,'figures':0}
secret=re.compile(r'\b(?:hf_[A-Za-z0-9]{20,}|sk-(?:proj-)?[A-Za-z0-9_-]{25,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AIza[A-Za-z0-9_-]{30,})\b')
private=re.compile(r'/(?:home|Users)/[^/\s]+/|/workspace/(?:attachments|portfolio-analysis|onboarding)(?:/|$)')
manifest=json.loads((ROOT/'docs/source_manifest.json').read_text())
for entry in manifest['notebooks']:
 p=ROOT/entry['published_path'];n=nbformat.read(p,as_version=4);nbformat.validate(n);counts['notebooks']+=1
 if hashlib.sha256(p.read_bytes()).hexdigest()!=entry['published_file_sha256']:errors.append(f'{p.name}: notebook hash changed; refresh source manifest')
 if len(n.cells)!=entry['source_cell_count']:errors.append(f'{p.name}: original cell numbering changed')
 for i,c in enumerate(n.cells,1):
  if c.metadata!={'original_cell_1based':i}:errors.append(f'{p.name} cell {i}: unexpected cell metadata')
  if c.get('attachments'):errors.append(f'{p.name} cell {i}: attachment')
  source=c.source
  if secret.search(source) or private.search(source):errors.append(f'{p.name} cell {i}: sensitive-looking literal (value withheld)')
  if re.search(r'["\']patient_id["\']\s*:\s*\d+',source):errors.append(f'{p.name} cell {i}: literal patient annotation')
  if c.cell_type=='code':
   counts['code_cells']+=1
   if c.get('outputs') or c.get('execution_count') is not None:errors.append(f'{p.name} cell {i}: retained execution output')
   try:ast.parse(TransformerManager().transform_cell(source))
   except SyntaxError as e:errors.append(f'{p.name} cell {i}: syntax error line {e.lineno}')
  if hashlib.sha256(source.encode()).hexdigest()!=entry['cell_hashes'][i-1]['published_sha256']:errors.append(f'{p.name} cell {i}: source hash mismatch')
for p in ROOT.rglob('*'):
 if not p.is_file() or any(part in ('.git','.venv','__pycache__') for part in p.parts):continue
 if p.is_symlink():errors.append(f'{p.relative_to(ROOT)}: symlink')
 if p.suffix.lower() in {'.zip','.rar','.xlsx','.xls','.pt','.pth','.joblib','.pkl','.pickle','.npz','.npy','.dcm'} or p.name.endswith(('.nii','.nii.gz')):errors.append(f'{p.relative_to(ROOT)}: non-public artifact type')
 if p.suffix in {'.md','.csv','.json','.txt','.py','.ipynb'}:
  text=p.read_text()
  private_text=text
  if secret.search(text) or private.search(private_text):errors.append(f'{p.relative_to(ROOT)}: sensitive-looking literal (value withheld)')
  if re.search(r'[A-Za-z0-9+/]{300,}={0,2}',text):errors.append(f'{p.relative_to(ROOT)}: possible embedded binary')
 if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
 if p.suffix=='.md':
  for target in re.findall(r'\]\(([^\n]+?)\)',p.read_text()):
   target=target.strip('<>').split('#')[0]
   if target and not re.match(r'(https?:|mailto:)',target) and not (p.parent/target).exists():errors.append(f'{p.relative_to(ROOT)}: missing link target {target}')
figures=json.loads((ROOT/'figures/manifest.json').read_text())
if figures['metrics_sha256']!=hashlib.sha256((ROOT/'results/metrics.csv').read_bytes()).hexdigest():errors.append('Figure metrics input hash mismatch')
if figures['generator_sha256']!=hashlib.sha256((ROOT/'scripts/plot_results.py').read_bytes()).hexdigest():errors.append('Figure generator hash mismatch')
for f in figures['figures']:
 p=ROOT/f['path'];counts['figures']+=1
 if f['contains_patient_images'] or hashlib.sha256(p.read_bytes()).hexdigest()!=f['sha256']:errors.append(f'{f["path"]}: figure provenance mismatch')
for p in ROOT.rglob('*.png'):
 if str(p.relative_to(ROOT)) not in {f['path'] for f in figures['figures']}:errors.append(f'{p.relative_to(ROOT)}: unregistered PNG')
print(json.dumps({'scope':'static inspection; no notebook execution or model validation','counts':counts,'errors':errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
