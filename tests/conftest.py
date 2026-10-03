import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "samples"))


def pytest_sessionstart(session):
    """Generate the fictional sample PDFs before tests run."""
    import make_samples
    make_samples.build()
