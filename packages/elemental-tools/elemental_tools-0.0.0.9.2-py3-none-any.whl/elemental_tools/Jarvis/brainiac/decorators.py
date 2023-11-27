from typing import Any, Union, Dict
import numpy as np
import spacy
from deep_translator import GoogleTranslator
from icecream import ic

from elemental_tools.Jarvis.tools import Tools, nlp_models, logger
from datetime import datetime
import inspect


tools = Tools()


class ExamplesModel:

	function: Any = None
	examples_lemmas = []

	def __init__(
			self,
			examples: Union[list, np.array],
			depends: dict = None,
			keywords: Union[list, np.array, None] = None,
			examples_exclude: Union[list, np.array, None] = None,
			suggestion_title: str = None,
			bypass_translation: bool = True,
			languages: list = ['pt', 'es']
	):

		"""
        :param examples: A list of matching examples that will be processed and generate models to the brainiac recognition system.
        :param keywords: This contains a list of keywords, that will be used for fast lookup, and will be improved with synonyms to corroborate with the examples list for a better accuracy.
        :param depends: A function that must returns a boolean value indicating the authorization status to this skill execution. If the dependency returns True, it triggers the authorization to this skill execution. Otherwise it triggers the authorization exception as a result. To overwrite the authorization exception...
        """

		self.keywords = keywords
		self.examples = examples
		self.depends = depends
		self.examples_exclude = examples_exclude
		self.examples_lemmas = []
		self.exception = None
		self.args = {}

		self.bypass_translation = bypass_translation
		self.languages = languages

		self.suggestion_title = suggestion_title

		self.generate_models()

	def get_depends(self):
		return self.depends

	def generate_models(self):

		# Convert examples to np array if not yet
		if isinstance(self.examples, list):
			# print(f"examples {self.examples}")
			self.examples = np.array(self.examples)

		if self.keywords is not None:
			for suggestion in self.keywords:
				self.examples = np.concatenate((self.examples, tools.get_syn_list(suggestion), np.array([suggestion])), axis=0)

		# Convert examples_exclude to np array if not yet
		if isinstance(self.examples_exclude, list):
			self.examples_exclude = np.array(self.examples_exclude)
			self.examples_exclude = np.isin(self.examples, self.examples_exclude)

		if self.examples_exclude is not None:
			self.examples = self.examples[~self.examples_exclude]

		self.examples = tools.to_nlp(nlp_models, self.examples)

		for example in self.examples:

			for token in example:
				self.examples_lemmas.append(token.lemma_)

		self.examples_lemmas = np.array(self.examples_lemmas)

		return self


class GrimoireStorage:
	data: Dict[str, ExamplesModel] = {}

	def include(self, name: str, request_model: ExamplesModel):
		self.data[name] = request_model
		return self.data


def Grimoire():
	_storage = GrimoireStorage()

	class GrimoireManagement:

		# here's your decorator definition
		def __call__(self, title: str, example_model: ExamplesModel, suggestion_title: str = None, depends: list = None, description: str = None, hidden: bool = False):

			# here you will retrieve func params and store skill data
			def decorator(func):

				start = datetime.now()
				logger('start', f"Generating {title.capitalize()} Models...", owner='model-generator')

				_skill_model = example_model

				_skill_model.name = title
				_skill_model.function = func
				_skill_model.parameters = inspect.signature(_skill_model.function).parameters
				_skill_model.suggestion_title = suggestion_title
				_skill_model.description = description
				_skill_model.hidden = hidden
				_skill_model.depends = depends

				_storage.include(_skill_model.name, _skill_model)

				end = datetime.now()
				logger('success', f"{title.capitalize()} Models Generated Successfully! It Takes: {end - start} and Renders up to: {len(_skill_model.examples)} examples", owner='model-generator')

			return decorator

		def skills(self):
			# self.fix_overlapping()
			return _storage.data

	_instance = GrimoireManagement()
	return _instance

