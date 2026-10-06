# Contributing

Thanks for your interest in improving `hm_dis_ep_wm55`! This is a small,
solo-maintained project, but issues, pull requests and translation fixes are
welcome.

## Development Setup

```bash
git clone https://github.com/RhonanMS/hm-dis-ep-wm55-integration.git
cd hm-dis-ep-wm55-integration
python3 -m venv .venv
.venv/bin/pip install --upgrade pip pytest
```

## Running Tests

```bash
.venv/bin/pytest tests/
```

`custom_components/hm_dis_ep_wm55/protocol.py` and `const.py` have **no
Home Assistant dependency** on purpose, so the encoder logic can be fully
unit-tested without installing Home Assistant (see `tests/conftest.py` for
how the module is loaded standalone).

## Protocol Changes

The SUBMIT byte protocol in `protocol.py` was reverse-engineered and
hardware-verified (see "Verified Tests" in [HM-Dis-EP-WM55.md](HM-Dis-EP-WM55.md)).
If you change anything in `protocol.py`:

1. Make sure `tests/test_protocol.py` still passes — it pins the two
   hardware-verified reference strings (Test A/B) byte-for-byte.
2. If possible, verify the change against a real HM-Dis-EP-WM55 device
   before opening a PR, and mention the result in the PR description.

## Translations

New/updated `translations/<lang>.json` files should mirror the structure of
`translations/en.json` (same keys for `config`, `services`, `selector`).
Partial translations are fine — missing keys fall back to English.

## Reporting Issues

Please open a [GitHub Issue](https://github.com/RhonanMS/hm-dis-ep-wm55-integration/issues)
with your Home Assistant version, the integration version, and (if
relevant) the exact `send_message` service call and what the display showed.

## AI-Assisted Contributions

This project is developed with agentic AI assistance. See
[AI_POLICY.md](AI_POLICY.md) for what that means for your contributions.
