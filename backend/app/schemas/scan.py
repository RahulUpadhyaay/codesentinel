from pydantic import BaseModel
from typing import List, Optional

class ScanRequest(BaseModel):
    filename: str = "main.py"
    code_content: str

class SecurityFinding(BaseModel):
    issue_title: str
    severity: str  # HIGH, MEDIUM, LOW
    description: str
    line_number: Optional[int] = None
    suggested_fix: str

class ScanResponse(BaseModel):
    scan_id: int
    filename: str
    security_score: int
    summary: str
    findings: List[SecurityFinding]