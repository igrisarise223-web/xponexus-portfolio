from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "pdfs"
PREVIEW_DIR = ROOT / "previews"
OUT = ROOT / "portfolio-projects.json"

CATEGORY_DEFAULTS = {
    "rear extension": ("extension", "Rear extension and associated structural alterations.", "Structural drawings, steelwork and construction details."),
    "loft conversion": ("loft", "Loft conversion and associated structural alterations.", "Structural drawings, roof alterations, steelwork and construction details."),
    "flat conversion": ("conversion", "Residential conversion and coordinated structural alterations.", "Structural drawings, alterations and construction details."),
    "chimney removal": ("alteration", "Chimney removal and retained support strategy.", "Retained support arrangement, steelwork and construction details."),
    "new build": ("new-build", "New-build residential structural design and technical documentation.", "Structural drawings, member layouts and construction details."),
    "structural alteration": ("alteration", "Structural alteration and coordinated technical documentation.", "Structural drawings, steelwork and construction details."),
}

def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("_", " ")).strip()

def category_data(category: str):
    key = category.lower().strip()
    if key in CATEGORY_DEFAULTS:
        return CATEGORY_DEFAULTS[key]
    for label, data in CATEGORY_DEFAULTS.items():
        if label in key or key in label:
            return data
    slug = re.sub(r"[^a-z0-9]+", "-", key).strip("-") or "external"
    return slug, "Project drawing package and coordinated technical documentation.", "Project drawings and technical information."

def find_preview(stem: str):
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        path = PREVIEW_DIR / f"{stem}{ext}"
        if path.exists():
            return path.relative_to(ROOT).as_posix()
    return ""

projects = []
PDF_DIR.mkdir(exist_ok=True)
PREVIEW_DIR.mkdir(exist_ok=True)
for pdf in sorted(PDF_DIR.glob("*.pdf"), key=lambda p: p.name.lower()):
    stem = pdf.stem
    parts = [clean(p) for p in stem.split("__")]
    if len(parts) >= 3:
        client, title, category = parts[0], parts[1], parts[2]
    elif len(parts) == 2:
        client, title = parts
        category = "Project"
    else:
        client = clean(stem)
        title = clean(stem)
        category = "Project"

    category_key, context, scope = category_data(category)
    sidecar = pdf.with_suffix(".json")
    metadata = {}
    if sidecar.exists():
        try:
            metadata = json.loads(sidecar.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"Warning: could not read {sidecar.name}: {exc}")

    projects.append({
        "title": metadata.get("title", title),
        "client": metadata.get("client", client),
        "category": metadata.get("category", category),
        "categoryKey": metadata.get("categoryKey", category_key),
        "context": metadata.get("context", context),
        "scope": metadata.get("scope", scope),
        "pdf": pdf.relative_to(ROOT).as_posix(),
        "preview": metadata.get("preview", find_preview(stem)),
        "previewLabel": metadata.get("previewLabel", "Click to open PDF"),
        "sheetCount": metadata.get("sheetCount", 1),
    })

OUT.write_text(json.dumps({"projects": projects}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Generated {OUT.name} with {len(projects)} project(s).")
