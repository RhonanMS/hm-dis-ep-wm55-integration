"""Lädt die reinen Encoder-Module (const.py, protocol.py) ohne Home-Assistant-Abhängigkeit.

custom_components/hm_dis_ep_wm55/__init__.py importiert Home-Assistant-Module,
die in dieser einfachen Testumgebung nicht installiert sind. Da protocol.py und
const.py selbst keine HA-Abhängigkeit haben, laden wir das Paket über einen
Stub-Parent (ohne die echte __init__.py auszuführen), damit die relativen
Importe (`from .const import ...`) trotzdem funktionieren.
"""
from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parents[1] / "custom_components" / "hm_dis_ep_wm55"
PACKAGE_NAME = "hm_dis_ep_wm55"

if PACKAGE_NAME not in sys.modules:
    stub = types.ModuleType(PACKAGE_NAME)
    stub.__path__ = [str(PACKAGE_DIR)]
    sys.modules[PACKAGE_NAME] = stub

protocol = importlib.import_module(f"{PACKAGE_NAME}.protocol")
const = importlib.import_module(f"{PACKAGE_NAME}.const")
