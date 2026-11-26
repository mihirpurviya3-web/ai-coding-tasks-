import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
IMPL = os.environ.get("IMPL_DIR", "starter")
IMPL_PATH = IMPL if os.path.isabs(IMPL) else os.path.join(TASK, IMPL)
sys.path.insert(0, IMPL_PATH)
