from dataclasses import dataclass
import pooch
import pandas as pd


@dataclass
class _GCB:
    sheet_name: str
    skiprows: int
    note: str
    citation: str
    name: str = "Global Carbon Budget 2021 - v0.6"
    doi: str = "10.18160/gcp-2021"
    filename: str = "Global_Carbon_Budget_2021v0.6.xlsx"
    license: str = "CC BY 4.0"

    def __repr__(self):
        return f"""{self.name}
'{self.filename}' - '{self.sheet_name}'

License: {self.license}
https://doi.org/{self.doi}

{self.note}

{self.citation}"""

    def to_dataframe(self):
        file_path = pooch.retrieve(
            path=pooch.os_cache("openclimatedata"),
            fname=self.filename,
            url="https://data.icos-cp.eu/licence_accept?ids=%5B%220ST81nXCND5VfAQdOCSJDveT%22%5D",
            known_hash="d124fcd675c2343e557c041d3824890ef793840d1d0c78875dd1fb6d2e14e6a8",
        )
        return pd.read_excel(
            file_path, sheet_name=self.sheet_name, skiprows=self.skiprows, index_col=0
        )

    def to_long_dataframe(self):
        df = self.to_dataframe()
        value_vars = df.columns
        return df.reset_index().melt(
            id_vars=["Year"],
            value_vars=value_vars,
            var_name="Category",
            value_name="Value",
        )


GCB = {
    "2021_historical_budget": _GCB(
        sheet_name="Historical Budget",
        skiprows=15,
        note="""Historical CO2 budget
All values in billion tonnes of carbon per year (GtC/yr), for the globe. For values in billion tonnes of carbon dioxide (CO2) per year, multiply the numbers below by 3.664.
1 billion tonnes C = 1 petagram of carbon (10^15 gC) = 1 gigatonne C = 3.664 billion tonnes of CO2
Please note: The methods used to estimate the historical fluxes presented below differ from the carbon budget presented from 1959 onwards. For example, the atmospheric growth and ocean sink do not account for year-to-year variability before 1959.
Uncertainties: see the original papers for uncertainties""",
        citation="""Cite as:  Friedlingstein et al (2021; https://doi.org/10.5194/essd-2021-386)
Fossil fuel combustion and cement production emissions:  Friedlingstein et al. (2021)
Land-use change emissions:  As in Global Carbon Budget from 1959: average of three bookkeeping models: H&N (Houghton &Nassikas, 2017), BLUE (Hansis, et al., 2015) and OSCAR (Gasser et al., 2020). Cite as:  Friedlingstein et al (2021; https://doi.org/10.5194/essd-2021-386)
Atmospheric CO2 growth rate: Joos, F. and Spahni, R.: Rates of change in natural and anthropogenic radiative forcing over the past 20,000 years, Proceedings of the National Academy of Science, 105, 1425-1430, 2008.
The ocean CO2 sink prior to 1959 is the average of the two diagnostic ocean models: DeVries, T. et al., Global Biogeochemical Cycles, 28, 631-647, 2014; and Khatiwala, S et al., Biogeosciences, 10, 2169-2191, 2013.
The land sink is as in Global Carbon Budget from 1959: average of 17 dynamic global vegetation models that reproduce the observed mean total land sink of the 1990s.
Cement carbonation is the average of two estimates: Friedlingstein et al. (2021)
The budget imbalance is the sum of emissions (fossil fuel and industry + land-use change) minus (atmospheric growth + ocean sink + land sink + cement carbonation sink); it is a measure of our imperfect data and understanding of the contemporary carbon cycle.
""",
    ),
    "2021_fossil_emissions_by_category": _GCB(
        sheet_name="Fossil Emissions by Category",
        skiprows=8,
        note="""Fossil fuel and cement production emissions by fuel type
All values in million tonnes of carbon per year (MtC/yr), except the per capita emissions which are in tonnes of carbon per person per year (tC/person/yr). For values in million tonnes of CO2 per year, multiply the values below by 3.664
1MtC = 1 million tonne of carbon = 3.664 million tonnes of CO2
Methods: Full details of the method are described in Friedlingstein et al (2021) and Andrew and Peters (2021)
The uncertainty for the global estimates is about ±5 % for a ± 1 sigma confidence level.""",
        citation="""Cite as: Friedlingstein et al (2021; https://doi.org/10.5194/essd-2021-386)""",
    ),
}
