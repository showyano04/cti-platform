from datetime import date

from pydantic import BaseModel, Field


class KevEntry(BaseModel):
    cve_id: str = Field(alias="cveID")
    vendor_project: str = Field(alias="vendorProject")
    product: str
    vulnerability_name: str = Field(alias="vulnerabilityName")
    date_added: date = Field(alias="dateAdded")
    short_description: str = Field(alias="shortDescription")
    required_action: str = Field(alias="requiredAction")
    due_date: date = Field(alias="dueDate")
    known_ransomware_use: str = Field(alias="knownRansomwareCampaignUse")

class CvssInfo(BaseModel):
    version: str
    base_score: float
    base_severity: str