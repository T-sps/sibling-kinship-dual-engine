"""让 tests/ 目录能 import 顶层包 sibling_engine。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
