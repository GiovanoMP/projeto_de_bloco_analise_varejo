from fastapi import Request
from fastapi.responses import JSONResponse
from enum import Enum
from typing import Optional, Dict, Any
import logging

class ErrorCode(Enum):
    """Códigos de erro customizados para a aplicação"""
    DATABASE_ERROR = "DATABASE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    INTERNAL_ERROR = "INTERNAL_ERROR"

class APIError(Exception):
    """Classe base para erros customizados da API"""
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)

class DatabaseError(APIError):
    """Erro específico para problemas de banco de dados"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=ErrorCode.DATABASE_ERROR,
            message=message,
            status_code=503,
            details=details
        )

class ValidationError(APIError):
    """Erro específico para validação de dados"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=ErrorCode.VALIDATION_ERROR,
            message=message,
            status_code=400,
            details=details
        )

class NotFoundError(APIError):
    """Erro específico para recursos não encontrados"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=ErrorCode.NOT_FOUND,
            message=message,
            status_code=404,
            details=details
        )

async def error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler global para tratamento de erros"""
    if isinstance(exc, APIError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.code.value,
                "message": exc.message,
                "details": exc.details,
                "path": request.url.path
            }
        )
    
    # Log do erro não tratado
    logging.error(f"Erro não tratado: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "code": ErrorCode.INTERNAL_ERROR.value,
            "message": "Erro interno do servidor",
            "path": request.url.path
        }
    )

# Exportar todas as classes e funções necessárias
__all__ = ['error_handler', 'APIError', 'DatabaseError', 'ValidationError', 'NotFoundError']