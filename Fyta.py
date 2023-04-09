from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler


class Fyta(AliceSkill):
	"""
	Author: Psychokiller1888
	Description: Connect with your plants!
	"""


	@IntentHandler('MyIntentName')
	def testIntent(self, session: DialogSession, **_kwargs):
		pass


	@IntentHandler('MySecondIntentName')
	def secondTestIntent(self, session: DialogSession, **_kwargs):
		pass