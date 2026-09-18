from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class CodeScan(SQLModel, table=True):
    """
    Code Audit History Database Table
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    filename: str
    code_content: str
    security_score: int  # 0 to 100
    security_findings: str  # JSON summary string
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))