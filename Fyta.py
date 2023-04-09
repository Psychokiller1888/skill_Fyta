from typing import Dict

import requests

from core.ProjectAliceExceptions import SkillStartingFailed
from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler


class Fyta(AliceSkill):
	"""
	Author: Psychokiller1888
	Description: Connect with your plants!
	"""

	API_URL = 'https://web.fyta.de/api'
	HEADERS: Dict[str, str] = dict()


	def __init__(self):
		super().__init__()
		self._connected = False
		self._plants = dict()
		self._gardens = dict()


	def onStart(self):
		super().onStart()
		connected = self.reconnect()
		if not connected:
			raise SkillStartingFailed(skillName=self.name, error='Please provide valid credentials in the skill settings')

		self.getData()
		self.logInfo(f'Retrieved {len(self._gardens)} garden and {len(self._plants)} plant', plural=['garden', 'plant'])


	def onQuarterHour(self):
		self.getData()


	def getData(self):
		response = requests.get(
			url=f'{self.API_URL}/user-plant',
			headers=self.HEADERS
		)
		if response.status_code != 200:
			self.logWarning(f'Failed to retrieve account data, error code {response.status_code}')
			return

		data = response.json()
		self._gardens = data['gardens']
		self._plants = data['plants']

	def reconnect(self):
		email = self.getConfig('email')
		password = self.getConfig('password')
		token = self.getConfig('token')
		refreshToken = self.getConfig('refreshToken')

		if token:
			response = requests.post(
				url=f'{self.API_URL}/user',
				headers={
					'Accept':        'application/json',
					'Authorization': f'Bearer {token}'
				}
			)
			if response.status_code != 200:
				# Try the refresh token
				if refreshToken:
					token = refreshToken
					response = requests.post(
						url=f'{self.API_URL}/user',
						headers={
							'Accept':        'application/json',
							'Authorization': f'Bearer {token}'
						}
					)
					if response.status_code != 200:
						# Try to connect with credentials
						self.updateConfig('token', '')
						self.updateConfig('refreshToken', '')
						return self.reconnect()

			self.HEADERS = {
				'Accept':        'application/json',
				'Authorization': f'Bearer {token}'
			}
		elif email and password:
			response = requests.post(
				url=f'{self.API_URL}/user',
				headers={'Accept': 'application/json'},
				data={'email': email, 'password': password}
			)
			if response.status_code != 200:
				self._connected = False
				self.logInfo('Invalid credentials or API failure')
				return False
			else:
				self._connected = True
				data = response.json()
				self.updateConfig('token', data['token'])
				self.updateConfig('refreshToken', data['refreshToken'])
				self.HEADERS = {
					'Accept':        'application/json',
					'Authorization': f'Bearer {token}'
				}
		else:
			self._connected = False
			return False

		self.logInfo('Fyta API connected!')
		self._connected = True
		return True
