import os
import pytest
from pytest import approx

from openclimatedata import GCB_Fossil_Emissions

GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


versions = GCB_Fossil_Emissions.keys()

@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_primaphist():
    for version in versions:
        assert GCB_Fossil_Emissions[version].name
        assert GCB_Fossil_Emissions[version].doi

@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_gcb_fossil_2023v28():
    df = GCB_Fossil_Emissions["2023v28"].to_dataframe()
    assert df.iloc[0]["Total"] == 0
    assert df.iloc[-1]["Per Capita"] == approx(4.663492)

    ocdf = GCB_Fossil_Emissions["2023v28"].to_ocd()
    # First and last value should be the same after re-shaping.
    assert ocdf.iloc[0]["value"] == df.iloc[0]["Total"]
    assert ocdf.iloc[-1]["value"] == df.iloc[-1]["Per Capita"]

@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_gcb_fossil_2023v36():
    df = GCB_Fossil_Emissions["2023v36"].to_dataframe()
    assert df.iloc[0]["Total"] == 0
    assert df.iloc[-1]["Per Capita"] == approx(4.658219)

    ocdf = GCB_Fossil_Emissions["2023v36"].to_ocd()
    # First and last value should be the same after re-shaping.
    assert ocdf.iloc[0]["value"] == df.iloc[0]["Total"]
    assert ocdf.iloc[-1]["value"] == df.iloc[-1]["Per Capita"]

