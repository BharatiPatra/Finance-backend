# routers/credit.py
from fastapi import APIRouter,HTTPException
from pathlib import Path
import json

router = APIRouter()
DATA_PATH = Path("app/data/credit_report.json")

def load_credit_data():
    with open(DATA_PATH, "r") as f:
        return json.load(f)

@router.get("/total_spending")
def get_total_credit_spending():
    data = load_credit_data()
    account_summary = data["creditReports"][0]["creditReportData"]["creditAccount"]["creditAccountSummary"]
    total = int(account_summary["totalOutstandingBalance"]["outstandingBalanceAll"])
    return {"total_credit_card_spending": total}

# o/p:{"total_credit_card_spending":75000}

@router.get("/cards")
def get_individual_credit_cards():
    data = load_credit_data()
    accounts = data["creditReports"][0]["creditReportData"]["creditAccount"]["creditAccountDetails"]
    return {"credit_card_accounts": accounts}
# o/p:{
#   "credit_card_accounts": [
#     {
#       "subscriberName": "HDFC Bank",
#       "portfolioType": "I",
#       "accountType": "01",
#       "openDate": "20060110",
#       "highestCreditOrOriginalLoanAmount": "50000",
#       "accountStatus": "83",
#       "paymentRating": "5",
#       "paymentHistoryProfile": "00??????????????????????????????????",
#       "currentBalance": "5000",
#       "amountPastDue": "1000",
#       "dateReported": "20201228",
#       "occupationCode": "S",
#       "rateOfInterest": "11.5",
#       "repaymentTenure": "0",
#       "dateOfAddition": "20201028",
#       "currencyCode": "INR",
#       "accountHolderTypeCode": "1"
#     },
#     {
#       "subscriberName": "ICICI Bank",
#       "portfolioType": "I",
#       "accountType": "03",
#       "openDate": "20060122",
#       "highestCreditOrOriginalLoanAmount": "110000",
#       "accountStatus": "11",
#       "paymentRating": "0",
#       "paymentHistoryProfile": "44??????????????????????????????????",
#       "currentBalance": "17000",
#       "amountPastDue": "13000",
#       "dateReported": "20201228",
#       "occupationCode": "S",
#       "rateOfInterest": "8.24",
#       "repaymentTenure": "0",
#       "dateOfAddition": "20201028",
#       "currencyCode": "INR",
#       "accountHolderTypeCode": "1"
#     },
#     {
#       "subscriberName": "Aditya Brila Finance Limited",
#       "portfolioType": "I",
#       "accountType": "53",
#       "openDate": "20060119",
#       "highestCreditOrOriginalLoanAmount": "95000",
#       "accountStatus": "78",
#       "paymentRating": "2",
#       "paymentHistoryProfile": "33??????????????????????????????????",
#       "currentBalance": "14000",
#       "amountPastDue": "10000",
#       "dateReported": "20201228",
#       "occupationCode": "N",
#       "rateOfInterest": "14",
#       "repaymentTenure": "0",
#       "dateOfAddition": "20201028",
#       "currencyCode": "INR",
#       "accountHolderTypeCode": "1"
#     },
#     {
#       "subscriberName": "Bajaj Finance",
#       "portfolioType": "I",
#       "accountType": "04",
#       "openDate": "20060113",
#       "highestCreditOrOriginalLoanAmount": "65000",
#       "accountStatus": "11",
#       "paymentRating": "0",
#       "paymentHistoryProfile": "11??????????????????????????????????",
#       "currentBalance": "8000",
#       "amountPastDue": "0",
#       "dateReported": "20201228",
#       "occupationCode": "N",
#       "repaymentTenure": "0",
#       "dateOfAddition": "20201028",
#       "currencyCode": "INR",
#       "accountHolderTypeCode": "1"
#     },
#     {
#       "subscriberName": "Epifi Capital",
#       "portfolioType": "R",
#       "accountType": "10",
#       "openDate": "20060116",
#       "creditLimitAmount": "500000",
#       "highestCreditOrOriginalLoanAmount": "80000",
#       "accountStatus": "82",
#       "paymentRating": "4",
#       "paymentHistoryProfile": "22??????????????????????????????????",
#       "currentBalance": "11000",
#       "amountPastDue": "7000",
#       "dateReported": "20201228",
#       "occupationCode": "N",
#       "repaymentTenure": "0",
#       "dateOfAddition": "20201028",
#       "currencyCode": "INR",
#       "accountHolderTypeCode": "1"
#     },
#     {
#       "subscriberName": "Mannapuram Finance",
#       "portfolioType": "I",
#       "accountType": "06",
#       "openDate": "20060125",
#       "highestCreditOrOriginalLoanAmount": "125000",
#       "accountStatus": "71",
#       "paymentRating": "1",
#       "paymentHistoryProfile": "55??????????????????????????????????",
#       "currentBalance": "20000",
#       "amountPastDue": "16000",
#       "dateReported": "20201228",
#       "occupationCode": "N",
#       "repaymentTenure": "0",
#       "dateOfAddition": "20201028",
#       "currencyCode": "INR",
#       "accountHolderTypeCode": "1"
#     }
#   ]
# }
@router.get("/card/{subscriber_name}")
def get_credit_card_by_name(subscriber_name: str):
    data = load_credit_data()
    accounts = data["creditReports"][0]["creditReportData"]["creditAccount"]["creditAccountDetails"]
    for acct in accounts:
        if acct.get("subscriberName", "").lower() == subscriber_name.lower():
            return {"credit_card_account": acct}
    raise HTTPException(status_code=404, detail="Credit card not found")
@router.get("/raw")
def get_raw_credit_report():
    data = load_credit_data()
    return data
