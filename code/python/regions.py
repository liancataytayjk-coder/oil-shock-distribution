"""Map PSA geography labels to harmonised region codes."""

import re

# Ordered: first matching pattern wins.
REGION_PATTERNS = [
    (r"^PHILIPPINES$", "PH"),
    (r"AREAS OUTSIDE|^AONCR$", "AONCR"),
    (r"NATIONAL CAPITAL|^NCR$", "NCR"),
    (r"CORDILLERA|^CAR$", "CAR"),
    (r"MIMAROPA|IV-B|^REGION 4B$", "R04B"),
    (r"IV-A|CALABARZON|^REGION 4A$", "R04A"),
    (r"NEGROS ISLAND|^NIR$", "NIR"),
    (r"MUSLIM MINDANAO|BARMM|ARMM", "BARMM"),
    (r"CARAGA|XIII|^REGION 13$", "R13"),
    (r"XII\b|SOCCSKSARGEN|^REGION 12$", "R12"),
    (r"XI\b|DAVAO|^REGION 11$", "R11"),
    (r"\bX\b|NORTHERN MINDANAO|^REGION 10$", "R10"),
    (r"IX\b|ZAMBOANGA|^REGION 9$", "R09"),
    (r"VIII\b|EASTERN VISAYAS|^REGION 8$", "R08"),
    (r"VII\b|CENTRAL VISAYAS|^REGION 7$", "R07"),
    (r"VI\b|WESTERN VISAYAS|^REGION 6$", "R06"),
    (r"\bV\b|BICOL|^REGION 5$", "R05"),
    (r"III\b|CENTRAL LUZON|^REGION 3$", "R03"),
    (r"II\b|CAGAYAN VALLEY|^REGION 2$", "R02"),
    (r"\bI\b|ILOCOS|^REGION 1$", "R01"),
]


def region_code(label: str) -> str:
    s = label.strip(". ").upper()
    s = re.sub(r"^REG(ION)?\s*(\d+[AB]?)$", r"REGION \2", s)  # e.g. "Reg12"
    for pat, code in REGION_PATTERNS:
        if re.search(pat, s):
            return code
    raise ValueError(f"unmapped region label: {label!r}")


REGIONS_17 = ["NCR", "CAR", "R01", "R02", "R03", "R04A", "R04B", "R05", "R06", "R07", "R08",
              "R09", "R10", "R11", "R12", "R13", "BARMM"]
