from typing import Callable
from fastapi.routing import APIRoute
from fastapi import Request, Response

from loader import crud
from .errors import invalid_token


class CheckAuthMiddleware(APIRoute):
	def get_route_handler(self) -> Callable:
		handler = super().get_route_handler()

		async def check_auth(request: Request) -> Response:
			token = request.cookies.get("token")
				  
			if not token:
				raise invalid_token
			
			checked = await crud.check_token(token)

			if not checked:
				raise invalid_token

			response = await handler(request)
			return response

		return check_auth
	