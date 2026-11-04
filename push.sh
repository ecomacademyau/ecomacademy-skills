#!/usr/bin/env bash
# Ship whatever is in this folder to the live marketplace.
#
#   bash push.sh                 ship it
#   bash push.sh --dry-run       show what would ship, change nothing
#
# This folder IS the repo. Claude edits the skills here; this script checks them,
# bumps the version of every plugin that changed, commits, and pushes to main.
# Nothing is copied in from anywhere else. (The old push-new-skills.sh copied a stale
# mirror over the clone, which is how eca-reel-editor once got deleted.)
set -euo pipefail
cd "$(dirname "$0")"

DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1
BRANCH=main

say() { printf '%s\n' "$*"; }
die() { printf '\nSTOP: %s\nNothing was pushed.\n' "$*"; exit 1; }

[ -d .git ] || die "this folder is not a git repo."
[ "$(git branch --show-current)" = "$BRANCH" ] || die "not on $BRANCH. Members install from $BRANCH."

# 1. Get anything a teammate pushed. Local edits are set aside and put back automatically.
say "== Pulling $BRANCH"
git pull --rebase --autostash --quiet origin "$BRANCH" || die "pull failed. Paste this output to Claude."

# 2. Bytecode never ships: it embeds the build machine's paths (once leaked a brand name).
find plugins -name "__pycache__" -type d -prune -exec rm -rf {} + 2>/dev/null || true
find plugins \( -name "*.pyc" -o -name ".DS_Store" \) -delete 2>/dev/null || true

# 3. Anything to ship?
if [ -z "$(git status --porcelain)" ]; then say "Nothing to ship. Folder matches $BRANCH."; exit 0; fi

# 4. Check every skill, bump changed plugins.
say "== Checking skills and versions"
python3 -I - "$DRY" <<'PY' || die "a check failed (see above). Paste this output to Claude."
import json, os, re, subprocess, sys
DRY = sys.argv[1] == "1"
LIMIT = 1024
LEAKS = re.compile(r"getdosed|\bdosed\b|catherine|liquid instant", re.I)   # brand-specific strings that must never ship

def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout

market = json.load(open(".claude-plugin/marketplace.json"))
listed = {e["name"]: e for e in market["plugins"]}

# what changed, per plugin, including new and deleted files
changed = {}
for line in git("status", "--porcelain", "-uall").splitlines():
    path = line[3:].split(" -> ")[-1].strip('"')
    m = re.match(r"plugins/([^/]+)/(skills/([^/]+)/)?", path)
    if not m:
        continue
    plug, skill = m.group(1), m.group(3)
    c = changed.setdefault(plug, {"new": set(), "updated": set(), "removed": set(), "other": False})
    if not skill:
        c["other"] = True
        continue
    exists_upstream = bool(git("ls-tree", "-d", "HEAD", f"plugins/{plug}/skills/{skill}").strip())
    exists_here = os.path.isdir(f"plugins/{plug}/skills/{skill}")
    if exists_here and not exists_upstream:
        c["new"].add(skill)
    elif exists_upstream and not exists_here:
        c["removed"].add(skill)
    else:
        c["updated"].add(skill)

bad = 0
for plug in sorted(listed):
    sk = f"plugins/{plug}/skills"
    if not os.path.isdir(sk):
        continue
    for d in sorted(os.listdir(sk)):
        f = os.path.join(sk, d, "SKILL.md")
        if not os.path.isfile(f):
            continue
        s = open(f, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n", s, re.S)
        try:
            import yaml
            fm = yaml.safe_load(m.group(1)) if m else None
        except ImportError:
            fm = {"name": re.search(r"^name:\s*\"?([^\"\n]+)", m.group(1), re.M).group(1),
                  "description": re.search(r"^description:\s*(.+)$", m.group(1), re.M).group(1)} if m else None
        except Exception as e:
            fm = None
            print(f"  FAIL {plug}/{d}: frontmatter isn't valid YAML ({str(e).splitlines()[0]})")
            print("       usually a description with an unquoted colon. Wrap it in double quotes.")
            bad += 1
            continue
        if not fm or not fm.get("name") or not fm.get("description"):
            print(f"  FAIL {plug}/{d}: SKILL.md needs a name and a description"); bad += 1; continue
        if fm["name"] != d:
            print(f"  FAIL {plug}/{d}: name is '{fm['name']}' but the folder is '{d}'. They must match."); bad += 1
        if len(fm["description"]) > LIMIT:
            print(f"  FAIL {plug}/{d}: description is {len(fm['description'])} chars; over {LIMIT} and members don't see the skill"); bad += 1
        for root, _, fs in os.walk(os.path.join(sk, d)):
            for fn in fs:
                if fn.endswith((".md", ".py", ".json", ".liquid", ".html", ".txt")):
                    t = open(os.path.join(root, fn), encoding="utf-8", errors="ignore").read()
                    hit = LEAKS.search(t)
                    if hit:
                        print(f"  FAIL leak: '{hit.group(0)}' in {os.path.join(root, fn)}"); bad += 1
if bad:
    sys.exit(1)
print("  all skills pass")

def bump(v, minor):
    a, b, c = (int(x) for x in v.split("."))
    return f"{a}.{b + 1}.0" if minor else f"{a}.{b}.{c + 1}"

notes = []
for plug, c in sorted(changed.items()):
    if plug not in listed:
        print(f"  note: {plug} changed but isn't in the marketplace, so members don't get it")
        continue
    pj = f"plugins/{plug}/.claude-plugin/plugin.json"
    d = json.load(open(pj))
    new_v = bump(d["version"], bool(c["new"] or c["removed"]))
    parts = []
    if c["new"]:     parts.append("added " + ", ".join(sorted(c["new"])))
    if c["updated"]: parts.append("updated " + ", ".join(sorted(c["updated"])))
    if c["removed"]: parts.append("removed " + ", ".join(sorted(c["removed"])))
    summary = "; ".join(parts) or "plugin files"
    print(f"  {plug}: {d['version']} -> {new_v}  ({summary})")
    notes.append(f"{plug} v{new_v}: {summary}")
    if DRY:
        continue
    d["version"] = new_v
    json.dump(d, open(pj, "w"), indent=2, ensure_ascii=False); open(pj, "a").write("\n")
    if "version" in listed[plug]:
        listed[plug]["version"] = new_v

if not DRY:
    json.dump(market, open(".claude-plugin/marketplace.json", "w"), indent=2, ensure_ascii=False)
    open(".claude-plugin/marketplace.json", "a").write("\n")
    open(".git/ECA_RELEASE_MSG", "w").write("Release " + " | ".join(notes) if notes else "Update repo files")
PY

if [ "$DRY" = 1 ]; then
  say ""; say "== Dry run. Would ship:"; git status --short; exit 0
fi

# 5. Commit everything and push.
say "== Shipping"
git add -A
MSG="$(cat .git/ECA_RELEASE_MSG)"; rm -f .git/ECA_RELEASE_MSG
git commit --quiet -m "$MSG"
git push --quiet origin "$BRANCH" || die "push was rejected. Paste this output to Claude."
say "$MSG"
say ""
say "Live. In Claude: Settings > Plugins > ECA ... > Update, to see it."
