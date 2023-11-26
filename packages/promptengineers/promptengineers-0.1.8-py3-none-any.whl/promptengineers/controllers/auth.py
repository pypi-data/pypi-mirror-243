import os

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from promptengineers.config.test import TEST_USER_ID

app = FastAPI()
security = HTTPBasic()


class AuthController:
	def __init__(self) -> None:
		self.users_db = self.load_users_from_env()

	def load_users_from_env(self):
		users = {}
		for key, value in os.environ.items():
			if key.startswith("USER_"):
				username = key[5:]  # Remove 'USER_' prefix
				users[username] = value
		return users

	def get_current_user(
		self,
		request: Request,
		credentials: HTTPBasicCredentials = Depends(security)
	):
		user = self.users_db.get(credentials.username)
		if user is None or user != credentials.password:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Invalid credentials",
				headers={"WWW-Authenticate": "Basic"},
			)
		else:
			request.state.user_id = TEST_USER_ID
			return request