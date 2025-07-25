from typing import Dict, List, Any

def parse_money_amount(amount_data: Dict[str, Any]) -> float:
    """
    Parses a money amount object with 'units' (string) and 'nanos' (integer)
    into a float.
    """
    units = float(amount_data.get("units", "0"))
    nanos = amount_data.get("nanos", 0)
    return units + nanos / 1_000_000_000
def get_scheme_type(scheme_name: str) -> str:
    """
    Infers the scheme type based on keywords in the scheme name.
    """
    scheme_name_lower = scheme_name.lower()
    if "equity" in scheme_name_lower or "nifty" in scheme_name_lower or "sensex" in scheme_name_lower or "index fund" in scheme_name_lower:
        return "Equity"
    elif "debt" in scheme_name_lower or "gilt" in scheme_name_lower or "overnight" in scheme_name_lower or "liquid" in scheme_name_lower:
        return "Debt"
    elif "balanced" in scheme_name_lower or "hybrid" in scheme_name_lower or "multi asset" in scheme_name_lower:
        return "Hybrid"
    else:
        return "Other"