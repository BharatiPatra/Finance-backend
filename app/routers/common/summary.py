from fastapi import APIRouter
from app.routers.credit import get_total_credit_spending
from app.routers.epf import get_total_epf_balance

from app.routers.mutualfunds import total_mutual_fund,get_transactions_summary
from app.routers.networth import get_total_net_worth,get_liability_breakdown

router = APIRouter()

@router.get("/summary")
def get_dashboard_summary():
    epf       = get_total_epf_balance()
    spending  = get_total_credit_spending()
    mf        = total_mutual_fund()
    networth  = get_total_net_worth()
    liabilities = get_liability_breakdown()
    transactions_summary = get_transactions_summary()

    # flatten or namespace as you like
    return {
        "total_current_balance":     epf["total_current_balance"],
        "pension_balance":           epf["pension_balance"],
        "total_credit_spending":     spending["total_credit_card_spending"],
        "total_mutual_fund_value":   mf["totalMutualFundValue"],
        "mutual_fund_currency":      mf["currency"],
        "total_net_worth":           networth["total_net_worth"],
        "liabilities":               liabilities["liabilities"],
        "mutual_fund":  transactions_summary ,
    }
