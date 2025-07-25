from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from typing import Dict, List
from datetime import datetime

from app.utils.utils import parse_money_amount, get_scheme_type

router = APIRouter()
DATA_PATH = Path("app/data/mf_transaction.json")

def load_mf_data() -> Dict:
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Data file is corrupt")

@router.get("/total_mutual_fund")
def total_mutual_fund() -> Dict[str, object]:
    data = load_mf_data()
    txns = data.get("transactions", [])
    total = sum(
        parse_money_amount(tx.get("transactionAmount", {}))
        for tx in txns
    )
    return {"totalMutualFundValue": round(total, 2), "currency": "INR"}

@router.get("/schemes")
def list_unique_schemes() -> Dict[str, List[str]]:
    data = load_mf_data()
    txns = data.get("transactions", [])
    schemes = {tx.get("schemeName", "").strip() for tx in txns if tx.get("schemeName")}
    return {"schemes": sorted(schemes)}

@router.get("/raw")
def raw_mutual_fund_data() ->Dict:
    return load_mf_data()

@router.get("/transactions_summary")
def get_transactions_summary() -> Dict[str, List[Dict]]:
    """
    Returns a summary of mutual fund transactions including date, scheme name,
    scheme type, transaction type, and transaction amount.
    """
    print(f"Start")
    data = load_mf_data()
    print(f"Loaded data: {data}")  # Debugging line
    transactions = data.get("transactions", [])
    print("1")
    summary = []
    for tx in transactions:
        transaction_date_str = tx.get("transactionDate")
        if transaction_date_str:
            # Parse ISO 8601 string and format to YYYY-MM-DD
            transaction_date = datetime.fromisoformat(transaction_date_str.replace('Z', '+00:00'))
            formatted_date = transaction_date.strftime("%Y-%m-%d")
        else:
            formatted_date = None

        scheme_name = tx.get("schemeName", "N/A").strip()
        scheme_type = get_scheme_type(scheme_name)
        transaction_type = tx.get("externalOrderType", "N/A")
        
        transaction_amount_obj = tx.get("transactionAmount", {})
        price = round(parse_money_amount(transaction_amount_obj), 2)
        print("")
        summary.append({
            "date": formatted_date,
            "schemeName": scheme_name,
            "schemeType": scheme_type,
            "type": transaction_type,
            "price": price
        })
    
    return summary
