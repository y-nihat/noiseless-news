"""Run `night_loop.sh`'s own shell functions against a scratch repository.

The supervisor that publishes this site is shell, and its security-relevant
parts — the path allowlist and the content gate — had only ever been tested by
grepping the script for the string `guard_paths`. A string test cannot tell the
difference between a guard that blocks a write and a guard that logs it and
commits it anyway, which is precisely the difference that mattered.

`NIGHT_SOURCE_ONLY=1 source night_loop.sh` defines the functions and returns
before any real work starts, so the functions under test are the ones that run
at 22:00 UTC, not a Python transcription of them.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / ".github" / "scripts" / "night_loop.sh"

# The supervisor, the gate, the cycle prompt and the pipeline all live outside
# content/ and data/, and all of them are read back and executed by the next
# cycle. One tracked file standing in for that whole class is enough to tell a
# working allowlist from a decorative one.
OUT_OF_SCOPE = ".github/scripts/supervisor.sh"
ORIGINAL = "#!/bin/sh\necho original\n"


def _git(*args: str, cwd: Path) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout


def make_scratch(tmp_path: Path) -> dict[str, Path]:
    """A repo with a real (bare, local) origin, plus stubs for pytest/python.

    A local bare remote means `git push` is exercised for real, without a
    network and without a token.
    """
    remote = tmp_path / "remote.git"
    work = tmp_path / "work"
    subprocess.run(["git", "init", "--bare", "-b", "main", str(remote)],
                   check=True, capture_output=True)
    subprocess.run(["git", "clone", str(remote), str(work)],
                   check=True, capture_output=True)
    _git("config", "user.email", "test@example.invalid", cwd=work)
    _git("config", "user.name", "test", cwd=work)

    for owned in ("content", "data"):
        (work / owned).mkdir()
        (work / owned / "seed.txt").write_text("seed\n", encoding="utf-8")
    # The supervisor reads its siblings by relative path — check_result.py and
    # flag_issue.sh — so a whole-script run needs them where it expects them.
    shutil.copytree(REPO_ROOT / ".github" / "scripts", work / ".github" / "scripts")
    shutil.copy(REPO_ROOT / ".github" / "cycle-prompt.md", work / ".github")
    unowned = work / OUT_OF_SCOPE
    unowned.write_text(ORIGINAL, encoding="utf-8")

    _git("add", "content", "data", ".github", cwd=work)
    _git("commit", "-m", "seed", cwd=work)
    _git("push", "-u", "origin", "main", cwd=work)
    seed = _git("rev-parse", "HEAD", cwd=work).strip()

    stubs = tmp_path / "stubs"
    stubs.mkdir()
    for tool in ("pytest", "python"):
        # The gate's own exit code is what is under test, so the tools it calls
        # are reduced to a settable exit code.
        stub = stubs / tool
        stub.write_text(
            f'#!/bin/sh\necho "stub {tool} $*"\nexit "${{STUB_{tool.upper()}_EXIT:-0}}"\n',
            encoding="utf-8",
        )
        stub.chmod(0o755)

    return {"work": work, "remote": remote, "stubs": stubs, "home": tmp_path,
            "seed": seed}


def drive(scratch: dict[str, Path], snippet: str) -> subprocess.CompletedProcess:
    """Source the real supervisor in the scratch repo and run `snippet` against it."""
    program = (
        "set -uo pipefail\n"
        f'cd "{scratch["work"]}"\n'
        f'NIGHT_SOURCE_ONLY=1 source "{SCRIPT}"\n'
        f"{snippet}\n"
    )
    return subprocess.run(
        ["bash", "-c", program],
        capture_output=True,
        text=True,
        timeout=120,
        env={
            "PATH": f"{scratch['stubs']}:/usr/bin:/bin",
            "HOME": str(scratch["home"]),
            "GIT_TERMINAL_PROMPT": "0",
        },
    )


# Snippets end with this so the harness can read the supervisor's counters back.
REPORT = (
    'echo "STATE gate_ok=$content_gate_ok trips=$gate_trips'
    ' guard_trips=$guard_trips push_failed=$push_failed push_blocked=$push_blocked"'
)


def state(result: subprocess.CompletedProcess) -> dict[str, str]:
    """Parse the `STATE key=value …` line a snippet prints."""
    lines = [line for line in result.stdout.splitlines() if line.startswith("STATE ")]
    assert lines, f"snippet printed no STATE line.\nstdout:\n{result.stdout}\n" \
                  f"stderr:\n{result.stderr}"
    return dict(part.split("=", 1) for part in lines[-1][len("STATE "):].split())


def pushed_files(scratch: dict[str, Path]) -> str:
    """Paths touched by whatever reached the bare remote after the seed commit.

    Measured from the seed rather than from the root: the seed itself creates
    the out-of-scope file, so "is it present in origin's history" would be true
    before the test even ran.
    """
    _git("fetch", "-q", "origin", cwd=scratch["work"])
    return _git("diff", "--name-only", f"{scratch['seed']}..origin/main",
                cwd=scratch["work"])


def committed_content(scratch: dict[str, Path], path: str) -> str:
    """The committed (HEAD) version of a file, which is what the next cycle runs."""
    return _git("show", f"HEAD:{path}", cwd=scratch["work"])


ISSUE_SENTINEL = Path("/tmp/night-issue-filed")


def run_night(scratch: dict[str, Path], **env: str) -> subprocess.CompletedProcess:
    """Run the whole supervisor, not just its functions, against the scratch repo.

    Used for the paths that only exist after the cycle loop — the end-of-night
    verdict, which is where two contradictory issues used to be filed ten
    seconds apart. `gh` is stubbed and logs its argv, so what the night actually
    reported is observable.
    """
    ISSUE_SENTINEL.unlink(missing_ok=True)
    log = scratch["home"] / "gh.log"
    log.unlink(missing_ok=True)
    (scratch["stubs"] / "gh").write_text(
        f'#!/bin/sh\necho "$@" >> "{log}"\n'
        '[ "$1" = "issue" ] && [ "$2" = "list" ] && echo "[]"\nexit 0\n',
        encoding="utf-8",
    )
    (scratch["stubs"] / "gh").chmod(0o755)
    return subprocess.run(
        ["bash", str(SCRIPT)],
        cwd=scratch["work"],
        capture_output=True,
        text=True,
        timeout=300,
        env={
            "PATH": f"{scratch['stubs']}:/usr/local/bin:/usr/bin:/bin",
            "HOME": str(scratch["home"]),
            "GIT_TERMINAL_PROMPT": "0",
            **env,
        },
    )


def gh_calls(scratch: dict[str, Path]) -> list[str]:
    log = scratch["home"] / "gh.log"
    return log.read_text(encoding="utf-8").splitlines() if log.exists() else []


def origin_content(scratch: dict[str, Path], path: str) -> str:
    """The version that actually reached the remote — what tomorrow's runner clones."""
    _git("fetch", "-q", "origin", cwd=scratch["work"])
    return _git("show", f"origin/main:{path}", cwd=scratch["work"])
