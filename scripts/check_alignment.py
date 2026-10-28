from pathlib import Path
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/"editorial/alignment.json").read_text(encoding="utf-8"))
snapshot_hash=hashlib.sha256((ROOT/"zh/book.tex").read_bytes()).hexdigest()
if snapshot_hash!=manifest["source_sha256"]:
    raise SystemExit("The Chinese snapshot has changed; rebuild the alignment manifest.")
active_source=ROOT.parent/"修订版_20261028"/"黏滞：比特、原子与生命的智能演化_修订版.tex"
if active_source.exists() and hashlib.sha256(active_source.read_bytes()).hexdigest()!=snapshot_hash:
    raise SystemExit("The active Chinese revision has changed; refresh the bilingual snapshot.")
stale=[]
written=[]
pending=[]
for unit in manifest["units"]:
    source=ROOT/unit["source"]
    english=ROOT/unit["english"]
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    if english.exists():
        written.append(unit["id"])
        if unit["reviewed_source_sha256"]!=digest:
            stale.append(unit["id"])
        if unit.get("english_sha256") and hashlib.sha256(english.read_bytes()).hexdigest()!=unit["english_sha256"]:
            stale.append(unit["id"]+":english-changed")
    else:
        pending.append(unit["id"])
result={"units":len(manifest["units"]),"english_written":written,"english_pending":pending,"stale_english":stale,"ready_for_publication":not pending and not stale and all(u["status"]=="reviewed" for u in manifest["units"])}
print(json.dumps(result,ensure_ascii=False,indent=2))
if stale:
    sys.exit(1)
