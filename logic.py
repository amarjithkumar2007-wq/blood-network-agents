import re
from donors import DONORS, COOLDOWN_DAYS, RED_CELL_OK

MONEY_WORDS = ("paytm", "gpay", "upi", "send money", "advance", "payment")

def parse_request(text: str) -> dict:
    """Rule-based parser (the plan is to swap in ASI:One for free-text parsing)."""
    t = text.lower()
    m = re.search(r"\b(ab|a|b|o)\s*(positive|negative|\+|-|pos|neg)", t)
    if not m:
        return {"ok": False, "reason": "no blood group found"}
    sign = "+" if m.group(2) in ("positive", "+", "pos") else "-"
    group = m.group(1).upper() + sign
    if any(w in t for w in MONEY_WORDS):
        return {"ok": False, "reason": "money request, rejected as spam"}
    component = "platelets" if "platelet" in t else "plasma" if "plasma" in t else "blood"
    urgent = any(w in t for w in ("urgent", "emergency", "asap", "now"))
    return {"ok": True, "group": group, "component": component, "urgent": urgent, "facility": "Facility A"}

def rank(req: dict) -> list:
    ok_groups = RED_CELL_OK[req["group"]]
    cd = COOLDOWN_DAYS[req["component"]]
    pool = [d for d in DONORS if d.group in ok_groups and d.days_since_last >= cd]
    # exact group first, then nearest
    pool.sort(key=lambda d: (d.group != req["group"], d.km))
    return pool
