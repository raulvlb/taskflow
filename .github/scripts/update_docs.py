"""
Reads the PR diff, the current DOCUMENTATION.md, and all source code files,
then calls the GitHub Models API to produce an updated documentation that
reflects additions, modifications, AND deletions in the codebase.

Required env vars:
  GITHUB_TOKEN  — automatically provided by GitHub Actions
  DIFF_FILE     — path to the file containing the git diff (default: /tmp/pr_diff.txt)
"""

import json
import os
import sys
import urllib.error
import urllib.request

GITHUB_MODELS_API = "https://models.inference.ai.azure.com/chat/completions"
DOCS_FILE = "DOCUMENTATION.md"
SOURCE_FILES = ["index.html", "js/app.js", "css/style.css"]


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        print("::error::GITHUB_TOKEN is not available.", file=sys.stderr)
        sys.exit(1)

    diff_file = os.environ.get("DIFF_FILE", "/tmp/pr_diff.txt")
    with open(diff_file, encoding="utf-8", errors="replace") as f:
        diff = f.read().strip()

    if not diff:
        print("Diff is empty — nothing to update.")
        return

    with open(DOCS_FILE, encoding="utf-8") as f:
        current_docs = f.read()

    source_snapshot = _read_source_files()
    prompt = _build_prompt(current_docs, diff, source_snapshot)
    updated_docs = _call_github_models(token, prompt)

    with open(DOCS_FILE, "w", encoding="utf-8") as f:
        f.write(updated_docs + "\n")

    print("DOCUMENTATION.md updated successfully.")


def _read_source_files() -> str:
    parts = []
    for path in SOURCE_FILES:
        if os.path.exists(path):
            with open(path, encoding="utf-8", errors="replace") as f:
                content = f.read()
            parts.append(f"### {path}\n```\n{content}\n```")
    return "\n\n".join(parts)


def _build_prompt(current_docs: str, diff: str, source_snapshot: str) -> str:
    return (
        "You are a senior technical writer specializing in software documentation.\n\n"
        "You have three inputs:\n"
        "1. The CURRENT DOCUMENTATION.md with existing functional requirements (RFs)\n"
        "2. The GIT DIFF of the latest pull request (shows what changed)\n"
        "3. The COMPLETE CURRENT SOURCE CODE (ground truth of what actually exists)\n\n"
        "Your task: produce a fully updated DOCUMENTATION.md.\n\n"
        "Rules — follow ALL of them strictly:\n"
        "- CROSS-REFERENCE every existing RF against the current source code.\n"
        "  If the feature described by an RF no longer exists in the code, REMOVE that RF.\n"
        "- ADD new RFs for features introduced in the diff that are not yet documented.\n"
        "  Continue the existing RF numbering (e.g. if the last is RF009, next is RF010).\n"
        "- UPDATE existing RFs whose described behavior was modified by the diff.\n"
        "- Keep all non-RF sections (Overview, Technologies, File Structure, Business Rules,\n"
        "  How to Run, License) intact unless directly impacted.\n"
        "- Preserve the exact Markdown formatting, table styles, and heading hierarchy.\n"
        "- Return ONLY the complete updated DOCUMENTATION.md — no explanations, no code fences.\n\n"
        f"## 1. Current DOCUMENTATION.md:\n{current_docs}\n\n"
        f"## 2. Git diff of the pull request:\n```diff\n{diff}\n```\n\n"
        f"## 3. Complete current source code:\n{source_snapshot}\n\n"
        "Return the complete updated DOCUMENTATION.md:"
    )


def _call_github_models(token: str, prompt: str) -> str:
    payload = json.dumps(
        {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 4096,
        }
    ).encode()

    req = urllib.request.Request(
        GITHUB_MODELS_API,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"::error::GitHub Models API returned {e.code}: {body}", file=sys.stderr)
        sys.exit(1)

    content = data["choices"][0]["message"]["content"].strip()

    # Strip markdown fences if the model wrapped the response
    if content.startswith("```"):
        lines = content.splitlines()
        end = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
        content = "\n".join(lines[1:end]).strip()

    return content


if __name__ == "__main__":
    main()
