"""Base controller class following fa-pidum pattern"""

import datetime
import decimal
import uuid
from typing import Any
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from sqlalchemy.engine.row import RowMapping


class BBaseController:
    """Base controller with standardized JSON responses and serialization"""

    force_show_data = True

    def __init__(self, repository=None):
        self.repository = repository

    def _serialize_data(self, data):
        """
        Recursively serialize data to JSON-compatible types

        Handles:
        - Pydantic models → dict
        - datetime objects → ISO format
        - UUID → string
        - Decimal → float
        - Sets → list
        - Dicts → recursively serialize values
        - SQLAlchemy RowMapping → dict
        - Lists/tuples → recursively serialize items
        """
        if data is None:
            return None

        # Handle Pydantic models
        if isinstance(data, BaseModel):
            return data.model_dump()

        # Handle datetime objects
        if isinstance(data, (datetime.datetime, datetime.date)):
            return data.isoformat()

        # Handle UUID
        if isinstance(data, uuid.UUID):
            return str(data)

        # Handle Decimal
        if isinstance(data, decimal.Decimal):
            return float(data)

        # Handle sets
        if isinstance(data, set):
            return list(data)

        # Handle dictionaries
        if isinstance(data, dict):
            return {k: self._serialize_data(v) for k, v in data.items()}

        # Handle RowMapping (SQLAlchemy result)
        if isinstance(data, RowMapping):
            return {k: self._serialize_data(v) for k, v in data.items()}

        # Handle lists/tuples
        if isinstance(data, (list, tuple)):
            return [self._serialize_data(item) for item in data]

        # Return as-is for primitive types
        return data

    def base_json(self, http_code: int, code=None, success="success", msg="-", data=None):
        """
        Base JSON response builder

        Args:
            http_code: HTTP status code
            code: Optional error/success code
            success: Success status string
            msg: Message string
            data: Response data

        Returns:
            JSONResponse with standardized format
        """
        return JSONResponse(
            status_code=http_code,
            content={
                "success": success,
                "message": msg,
                "data": self._serialize_data(data) if data or self.force_show_data else None,
                "code": code,
            }
        )

    def success(self, msg="success", data=None, http_code=200):
        """Success response helper"""
        return self.base_json(http_code=http_code, success="success", msg=msg, data=data)

    def fail(self, msg="Maaf ada kesalahan", data=None):
        """Failure response helper"""
        return self.base_json(http_code=400, success="error", msg=msg, data=data)

    def validation_fail(self, http_code, msg, data):
        """Validation error response"""
        return self.base_json(http_code=http_code, success="validation_error", msg=msg, data=data)

    def server_fail(self, msg, data=None):
        """Server error response"""
        return self.base_json(http_code=500, success="server_error", msg=msg, data=data or {})
