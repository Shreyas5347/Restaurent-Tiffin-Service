# nlp package
import sys
from pathlib import Path

# Add project root (parent directory of 'nlp') to sys.path so 'import nlp...' works from anywhere
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
