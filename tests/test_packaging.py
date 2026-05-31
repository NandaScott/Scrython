import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import pytest


@pytest.mark.slow
def test_py_typed_in_wheel():
    repo_root = Path(__file__).parent.parent

    with tempfile.TemporaryDirectory() as tmp_dir:
        subprocess.run(
            [sys.executable, "-m", "build", "--wheel", "--outdir", tmp_dir],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )

        wheels = list(Path(tmp_dir).glob("*.whl"))
        assert len(wheels) == 1, f"Expected 1 wheel, found {len(wheels)}"

        with zipfile.ZipFile(wheels[0]) as whl:
            assert "scrython/py.typed" in whl.namelist()
