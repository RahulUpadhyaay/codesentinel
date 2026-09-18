from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database import get_session
from app.models.user import User
from app.models.scan import CodeScan
from app.schemas.scan import ScanRequest, ScanResponse
from app.core.dependencies import get_current_user
from app.services.scanner import run_multi_agent_scan

router = APIRouter(prefix="/api/audit", tags=["Code Audit"])

@router.post("/scan", response_model=ScanResponse)
def scan_code(
    request: ScanRequest,
    current_user: User = Depends(get_current_user),  # 🔒 PROTECTED ROUTE!
    session: Session = Depends(get_session)
):
    """
    Protected Endpoint: Analyzes code snippet using AI Multi-Agent engine and saves scan report.
    """
    # 1. Run AI Multi-Agent Scan
    audit_result = run_multi_agent_scan(request.filename, request.code_content)
    
    # 2. Save scan report to Database
    scan_record = CodeScan(
        user_id=current_user.id,
        filename=request.filename,
        code_content=request.code_content,
        security_score=audit_result.get("security_score", 100),
        security_findings=str(audit_result.get("findings", []))
    )
    session.add(scan_record)
    session.commit()
    session.refresh(scan_record)
    
    return ScanResponse(
        scan_id=scan_record.id,
        filename=scan_record.filename,
        security_score=scan_record.security_score,
        summary=audit_result.get("summary", "Scan completed"),
        findings=audit_result.get("findings", [])
    )