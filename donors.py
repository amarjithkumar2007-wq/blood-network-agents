"""Synthetic demo data only. No real people, phones or facilities."""
from dataclasses import dataclass

@dataclass
class Donor:
    id: str
    group: str
    km: float
    days_since_last: int
    facility: str
    will_accept: bool  # scripted reply for the demo

DONORS = [
    Donor("donor-1", "O+", 2.1, 200, "Facility A", False),   # declines
    Donor("donor-2", "O-", 3.5, 120, "Facility A", True),    # accepts
    Donor("donor-3", "O+", 1.0, 30, "Facility A", True),     # too recent (blood cooldown 90d)
    Donor("donor-4", "A+", 0.8, 400, "Facility A", True),    # wrong group
    Donor("donor-5", "O+", 6.0, 300, "Facility B", True),    # other facility, not used by Facility A
]
COOLDOWN_DAYS = {"blood": 90, "plasma": 28, "platelets": 14}
# Whole-blood red cells: who can give to whom (recipient -> donor groups)
RED_CELL_OK = {
    "O-": {"O-"}, "O+": {"O-", "O+"},
    "A-": {"O-", "A-"}, "A+": {"O-", "O+", "A-", "A+"},
    "B-": {"O-", "B-"}, "B+": {"O-", "O+", "B-", "B+"},
    "AB-": {"O-", "A-", "B-", "AB-"}, "AB+": {"O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"},
}
