from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
print(json.dumps(json.loads((root/"results/snapshot.json").read_text()),ensure_ascii=False,indent=2))
