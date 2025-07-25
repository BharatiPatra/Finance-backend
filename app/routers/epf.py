# routers/epf.py
from fastapi import APIRouter,HTTPException
from pathlib import Path
import json

router = APIRouter()
DATA_PATH = Path("app/data/epf_details.json")

def load_epf_data():
    with open(DATA_PATH, "r") as f:
        return json.load(f)

@router.get("/total_epf_balance")
def get_total_epf_balance():
    data = load_epf_data()
    balance_info = data["uanAccounts"][0]["rawDetails"]["overall_pf_balance"]
    return {
        "total_current_balance": balance_info.get("current_pf_balance"),
        "pension_balance": balance_info.get("pension_balance")
    }
    # o/p:{"total_current_balance":"211111","pension_balance":"1000000"}

@router.get("/epf_accounts")
def get_epf_accounts():
    data = load_epf_data()
    return {
        "epf_accounts": data["uanAccounts"][0]["rawDetails"]["est_details"]
    }
#    o/p:{
#   "epf_accounts": [
#     {
#       "est_name": "KARZA TECHNOLOGIES PRIVATE LIMITED",
#       "member_id": "MHBANXXXXXXXXXXXXXXXXX",
#       "office": "(RO)BANDRA(MUMBAI-I)",
#       "doj_epf": "24-03-2021",
#       "doe_epf": "02-01-2022",
#       "doe_eps": "02-01-2022",
#       "pf_balance": {
#         "net_balance": "200000",
#         "employee_share": {
#           "credit": "100000",
#           "balance": "100000"
#         },
#         "employer_share": {
#           "credit": "100000",
#           "balance": "100000"
#         }
#       }
#     },
#     {
#       "est_name": "TSS CONSULTANCY PRIVATE LIMITED",
#       "member_id": "MHBAN*****************",
#       "office": "(RO)BANDRA(MUMBAI-I)",
#       "doj_epf": "07-08-2018",
#       "doe_epf": "02-01-2022",
#       "doe_eps": "02-01-2022",
#       "pf_balance": {
#         "net_balance": "11111",
#         "employee_share": {
#           "credit": "5000"
#         },
#         "employer_share": {
#           "credit": "5000"
#         }
#       }
#     }
#   ]
# }
@router.get("/epf_account/{member_id}")
def get_epf_account(member_id: str):
    """
    Retrieve a single EPF account by its member_id.
    """
    data = load_epf_data()
    accounts = data["uanAccounts"][0]["rawDetails"]["est_details"]
    for acct in accounts:
        if acct.get("member_id") == member_id:
            return acct
    raise HTTPException(status_code=404, detail=f"EPF account '{member_id}' not found")
# o/p:{
#   "est_name": "KARZA TECHNOLOGIES PRIVATE LIMITED",
#   "member_id": "MHBANXXXXXXXXXXXXXXXXX",
#   "office": "(RO)BANDRA(MUMBAI-I)",
#   "doj_epf": "24-03-2021",
#   "doe_epf": "02-01-2022",
#   "doe_eps": "02-01-2022",
#   "pf_balance": {
#     "net_balance": "200000",
#     "employee_share": {
#       "credit": "100000",
#       "balance": "100000"
#     },
#     "employer_share": {
#       "credit": "100000",
#       "balance": "100000"
#     }
#   }
# }
@router.get("/raw")
def get_raw_epf_data():
    data = load_epf_data()
    return data
