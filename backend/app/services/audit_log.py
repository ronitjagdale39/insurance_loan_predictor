from sqlalchemy.orm import Session
from app.models.audit import AuditTable


class AuditService:

    @staticmethod
    def log(
        db: Session,
        event: str,
        level: str,
        endpoint: str,
        method: str,
        status_code: int,
        message: str,
        user_id: int = None,
        email: str = None,
        ip_address: str = None,
        payload: dict = None,
    ):
        try:
            audit = AuditTable(
                event=event,
                level=level,
                user_id=user_id,
                email=email,
                endpoint=endpoint,
                method=method,
                status_code=status_code,
                ip_address=ip_address,
                message=message,
                payload=payload,
            )

            db.add(audit)
            db.commit()
            db.refresh(audit)

        except Exception as e:
            db.rollback()
            print(f"Audit Log Error: {e}")