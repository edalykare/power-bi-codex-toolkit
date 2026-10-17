import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "examples" / "retail"


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def write_json(path: Path, data) -> Path:
    return write(path, json.dumps(data))


def minimal_model(root: Path) -> Path:
    write(root / "Product.tmdl", "table Product\n\tcolumn Key\n\t\tdataType: int64\n")
    write(
        root / "Sales.tmdl",
        "table Sales\n\tcolumn ProductKey\n\t\tdataType: int64\n"
        "\t/// Number of sales rows.\n\tmeasure Rows = COUNTROWS('Sales')\n"
        "\t\tformatString: 0\n\t\tdisplayFolder: Counts\n",
    )
    write(
        root / "relationships.tmdl",
        "relationship Sales_Product\n\tfromColumn: Sales.ProductKey\n\ttoColumn: Product.Key\n",
    )
    return root
