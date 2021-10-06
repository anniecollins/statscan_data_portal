# data_utils.py
import pandas as pd
import numpy as np

values = ["Use with caution", "Estimate suppressed", ""]

def process_data(data):
    i = 0
    while i < len(data):
        # Different marker values
        conditions = [data[i]["Marker"] == "*",
                    data[i]["Marker"] == "...",
                    pd.isnull(data[i]["Marker"])]
        # Assign annotation text according to marker values
        data[i]["Annotation"] = np.select(conditions, values)

        # Suppress Estimate and CI Upper where necessary (for visualizations and error bars)
        data[i]["Estimate"] = np.where(data[i]["Marker"]=="...", 0, data[i]["Estimate"])
        data[i]["CI Upper"] = np.where(data[i]["Marker"]=="...", 0, data[i]["CI Upper"])

        # Round rates and dollar amounts to zero decimal places
        data[i]['Estimate'] = data[i]['Estimate'].round(0)
        data[i]["CI Upper"] = data[i]["CI Upper"].round(0)
        i = i + 1


def get_data():
    SubSecAvgDon_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-SubSecAvgDon.csv")
    SubSecDonRates_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-SubSecDonRates.csv")
    DonRates_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-DonRate.csv")
    AvgTotDon_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-AvgTotDon.csv")
    SubSecAvgNumDon_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-SubSecAvgNumDon.csv")
    AvgNumCauses_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-AvgNumCauses.csv")
    AvgTotNumDon_2018 = pd.read_csv("https://raw.githubusercontent.com/ajah/statscan_data_portal/master/Tables/2018-AvgTotNumDon.csv")

    DonRates_2018['Estimate'] = DonRates_2018['Estimate']*100
    DonRates_2018['CI Upper'] = DonRates_2018['CI Upper']*100

    return SubSecAvgDon_2018, SubSecDonRates_2018, DonRates_2018, AvgTotDon_2018,SubSecAvgNumDon_2018, AvgNumCauses_2018, AvgTotNumDon_2018
