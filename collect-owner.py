"""Small adjacent Python entry for collect-owner.bat; never installs dependencies."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
import owner_pipeline

if __name__ == "__main__":
    check_exit = sys.argv[1:] == ["--check-exit"]
    if not sys.argv[1:]:
        sys.argv.append("collect")
    elif sys.argv[1] in ("--check", "--check-exit"):
        sys.argv[1] = "check"
    elif sys.argv[1] == "--prepare":
        sys.argv[1] = "prepare"
    elif sys.argv[1] == "--review":
        sys.argv[1] = "review-fetch"
    owner_pipeline.main()
    if check_exit:
        raise SystemExit(7)
