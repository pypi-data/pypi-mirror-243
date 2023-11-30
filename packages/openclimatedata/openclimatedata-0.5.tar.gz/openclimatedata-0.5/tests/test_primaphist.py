import os

import pytest
from pytest import approx

from openclimatedata import PRIMAPHIST

GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"

versions = PRIMAPHIST.keys()

def test_primaphist():
    for version in versions:
        assert PRIMAPHIST[version].name
        assert PRIMAPHIST[version].doi

@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_primaphist_2_5():
    df = PRIMAPHIST["2.5"].to_dataframe()
    assert df.iloc[0]["1750"] == approx(0.00564)
    assert df.iloc[-1]["2022"] == approx(0.0)

    assert df.iloc[0]["provenance"] == "measured"

    ocdf = PRIMAPHIST["2.5"].to_ocd()
    # First and last value should be the same after re-shaping.
    assert ocdf.iloc[0]["value"] == df.iloc[0]["1750"]
    assert ocdf.iloc[-1]["value"] == df.iloc[-1]["2022"]

    assert ocdf.iloc[0]["provenance"] == "measured"

@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_primaphist_2_4_2():
    df = PRIMAPHIST["2.4.2"].to_dataframe()
    assert df.iloc[0]["1750"] == approx(0.00564)
    assert df.iloc[-1]["2021"] == approx(13.9)

    ocdf = PRIMAPHIST["2.4.2"].to_ocd()
    # First and last value should be the same after re-shaping.
    assert ocdf.iloc[0]["value"] == df.iloc[0]["1750"]
    assert ocdf.iloc[-1]["value"] == df.iloc[-1]["2021"]

    assert ocdf.iloc[0]["provenance"] == None
