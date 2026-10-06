# AI Contribution Policy

This project — the `hm_dis_ep_wm55` Home Assistant integration — was
developed with agentic AI assistance, primarily
[Claude Code](https://www.anthropic.com/claude-code). This includes:

- Reverse-engineering and documenting the HM-Dis-EP-WM55 SUBMIT protocol
  (`HM-Dis-EP-WM55.md`), based on a public reference script and iterative,
  human-supervised testing against real hardware.
- The integration code (`custom_components/hm_dis_ep_wm55/`), its tests, and
  the project documentation (this file included).
- The example automation (`examples/automations.yaml`).

## Human Review and Hardware Verification

AI assistance accelerated the work; it did not replace verification. Every
protocol detail that ended up in `protocol.py` was checked against actual
SUBMIT strings sent to a physical HM-Dis-EP-WM55 device by the maintainer —
see the "Verified Tests" section in [HM-Dis-EP-WM55.md](HM-Dis-EP-WM55.md)
for the exact byte strings and observed display behavior. Several
AI-generated assumptions about the protocol turned out to be wrong on first
attempt and were corrected only after hardware testing; this history is kept
in the project (commit messages, `docs/troubleshooting.md`) rather than
smoothed over.

## Expectations for Contributions

AI-assisted pull requests are welcome, but:

- You (the human submitting the PR) are responsible for the change —
  review the generated code/docs yourself before opening the PR.
- Changes to `protocol.py` or anything affecting the wire format must be
  verified against real hardware where feasible; say so (or say why not)
  in the PR description.
- `pytest tests/` must pass.
- Don't let an AI assistant invent protocol details that aren't backed by
  either the hardware tests in this repo or a cited external source — this
  project's one hard-won lesson is that plausible-looking protocol
  descriptions can be confidently wrong.
