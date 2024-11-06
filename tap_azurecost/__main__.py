"""azureCostManagement entry point."""

from __future__ import annotations

from tap_azurecost.tap import TapazureCostManagement

TapazureCostManagement.cli()
