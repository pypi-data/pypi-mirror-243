from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response, HTTPException, status as http_status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials


class HTTPBasicAuthMiddleware:
    @classmethod
    def setup(
        cls,
        app: FastAPI,
        check_handler: Callable[[HTTPBasicCredentials], bool],
        ignore_paths: list[str] | None = None,
        scheme_name: str | None = None,
        realm: str | None = None,
    ):
        middleware = cls(app, check_handler, ignore_paths, scheme_name, realm)
        app.middleware("http")(middleware.middleware)

    def __init__(
        self,
        app: FastAPI,
        check_handler: Callable[[HTTPBasicCredentials], bool],
        ignore_paths: list[str] | None = None,
        scheme_name: str | None = None,
        realm: str | None = None,
    ) -> None:
        self.app = app
        self.check_handler = check_handler
        self.ignore_paths = ignore_paths
        self.scheme_name = scheme_name
        self.realm = realm
        self.security = HTTPBasic(scheme_name=self.scheme_name, realm=self.realm)

    async def middleware(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if self.ignore_paths and request.url.path in self.ignore_paths:
            return await call_next(request)
        try:
            credential = await self.security(request)
            if not credential or not self.check_handler(credential):
                raise HTTPException(
                    status_code=http_status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect credentials",
                    headers={"WWW-Authenticate": "Basic"},
                )
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail}, headers=e.headers)  # type: ignore
        return await call_next(request)
