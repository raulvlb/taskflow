"""
Reads the PR diff and the current DOCUMENTATION.md,
calls the GitHub Models API (powered by GitHub Copilot infrastructure),
and writes the updated documentation back.

Required env vars:
  GITHUB_TOKEN  — automatically provided by GitHub Actions (no extra secret needed)
  DIFF_FILE     — path to the file containing the git diff (default: /tmp/pr_diff.txt)
"""

import json
import os
import sys
import urllib.error
import urllib.request

GITHUB_MODELS_API = "https://models.inference.ai.azure.com/chat/completions"
DOCS_FILE = "DOCUMENTATION.md"


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

    prompt = _build_prompt(current_docs, diff)
    updated_docs = _call_github_models(token, prompt)

    with open(DOCS_FILE, "w", encoding="utf-8") as f:
        f.write(updated_docs + "\n")

    print("DOCUMENTATION.md updated successfully.")


def _build_prompt(current_docs: str, diff: str) -> str:
    return (
        "You are a senior technical writer specializing in software documentation.\n\n"
        "Update the DOCUMENTATION.md below based on the pull request code changes.\n\n"
        "Rules:\n"
        "- ADD new functional requirements (RF00X) for new features — continue the existing numbering\n"
        "- UPDATE existing requirements whose described behavior was modified by the diff\n"
        "- REMOVE requirements that correspond to functionality deleted in the diff\n"
        "- Keep all non-RF sections (Overview, Technologies, File Structure, Business Rules,"
        " How to Run, License) intact unless directly impacted by the changes\n"
        "- Preserve the exact Markdown formatting, table styles, and heading hierarchy\n"
        "- Return ONLY the complete updated DOCUMENTATION.md — no explanations, no code fences\n\n"
        f"## Current DOCUMENTATION.md:\n{current_docs}\n\n"
        f"## Pull request diff (code changes only):\n```diff\n{diff}\n```\n\n"
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
