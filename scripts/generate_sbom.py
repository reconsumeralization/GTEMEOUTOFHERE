#!/usr/bin/env python3
"""
Generate a minimal SBOM (sbom.json) listing installed Python packages.

For production, integrate CycloneDX/SPDX as available; this script is a lightweight fallback.
"""

import json
from pathlib import Path


def generate_sbom():
    try:
        import pkg_resources
    except ImportError:
        print("pkg_resources not available.")
        return

    deps = []
    for dist in pkg_resources.working_set:
        deps.append({"name": dist.project_name, "version": dist.version})

    sbom = {
        "type": "sbom-lite",
        "packages": sorted(deps, key=lambda x: x["name"].lower()),
    }

    Path("sbom.json").write_text(json.dumps(sbom, indent=2), encoding="utf-8")
    print("sbom.json written with", len(deps), "packages.")


if __name__ == "__main__":
    generate_sbom()
