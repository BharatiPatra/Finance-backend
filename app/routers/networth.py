# routers/networth.py
from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter()
DATA_PATH = Path("app/data/net_worth.json")  # adjust this path as needed


def load_networth_data():
    print(f"Attempting to load data from: {DATA_PATH}") # Added print
    try:
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
            print(f"Net worth data loaded successfully: ") # Added print
            return data
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_PATH}") # Added print
        # You might want to raise an HTTPException here in a real API
        raise
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {DATA_PATH}. Check file format.") # Added print
        raise


@router.get("/total_net_worth")
def get_total_net_worth():
    data = load_networth_data()
    total_net_worth = data["netWorthResponse"]["totalNetWorthValue"]
    return {
        "total_net_worth": total_net_worth
    }
    # o/p:{"total_net_worth":{"currencyCode":"INR","units":"868721"}}

@router.get("/assets")
def get_asset_breakdown():
    data = load_networth_data()
    asset_values = data["netWorthResponse"].get("assetValues", [])
    return {
        "assets": asset_values
    }
    # o/p:{"assets":[{"netWorthAttribute":"ASSET_TYPE_MUTUAL_FUND","value":{"currencyCode":"INR","units":"84613"}},
    #        {"netWorthAttribute":"ASSET_TYPE_EPF","value":{"currencyCode":"INR","units":"211111"}},
    #        {"netWorthAttribute":"ASSET_TYPE_INDIAN_SECURITIES","value":{"currencyCode":"INR","units":"200642"}},
    #        {"netWorthAttribute":"ASSET_TYPE_SAVINGS_ACCOUNTS","value":{"currencyCode":"INR","units":"436355"}}]}
# 

@router.get("/liabilities")
def get_liability_breakdown():
    print("GET /liabilities endpoint called.") # Added print
    data = load_networth_data()
    liabilities = data["netWorthResponse"].get("liabilityValues", [])
    return {
        "liabilities": liabilities
    }
    # o/p:{"liabilities":[{"netWorthAttribute":"LIABILITY_TYPE_OTHER_LOAN","value":{"currencyCode":"INR","units":"42000"}},
    #                     {"netWorthAttribute":"LIABILITY_TYPE_HOME_LOAN","value":{"currencyCode":"INR","units":"17000"}},
    #                     {"netWorthAttribute":"LIABILITY_TYPE_VEHICLE_LOAN","value":{"currencyCode":"INR","units":"5000"}}]}

@router.get("/raw")
def get_raw_networth():
    data = load_networth_data()
    return data

