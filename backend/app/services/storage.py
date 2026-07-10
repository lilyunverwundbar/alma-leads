from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.core.config import Settings


ALLOWED_RESUME_TYPES = {
    "application/pdf": ".pdf",
    "application/msword": ".doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
}


def store_resume(file: UploadFile, settings: Settings) -> tuple[str, str]:
    extension = ALLOWED_RESUME_TYPES.get(file.content_type or "")
    if extension is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume must be a PDF, DOC, or DOCX file",
        )

    settings.resume_dir.mkdir(parents=True, exist_ok=True)
    original_name = Path(file.filename or f"resume{extension}").name
    stored_name = f"{uuid4()}{extension}"
    destination = settings.resume_dir / stored_name

    total = 0
    with destination.open("wb") as output:
        while chunk := file.file.read(1024 * 1024):
            total += len(chunk)
            if total > settings.max_resume_bytes:
                output.close()
                destination.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="Resume must be 10MB or smaller",
                )
            output.write(chunk)

    return original_name, str(destination)
