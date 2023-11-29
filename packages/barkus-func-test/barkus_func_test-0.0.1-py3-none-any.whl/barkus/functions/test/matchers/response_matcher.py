class _AssertResponseMatcher:
	def __init__(self, response, _matcher_state: bool):
		self.__response = response
		self._matcher_state = _matcher_state

	def notFound(self, data = ""):
		self.any(data = data, statusCode = 404)

	def ok(self, data = "", statusCode: int = 200):
		self.any(data = data, statusCode = statusCode)

	def error(self, data = "", statusCode: int = 500):
		self.any(error = data, statusCode = statusCode)

	def serverError(self, data = ""):
		self.error(data = data, statusCode = 500)

	def unauthenticated(self, data = ""):
		self.error(data = data, statusCode = 403)

	def unauthorized(self, data = ""):
		self.error(data = data, statusCode = 401)

	def badRequest(self, data = ""):
		self.error(data = data, statusCode = 400)

	def unprocessableEntity(self):
		self.error(statusCode = 422)

	def any(self, data = "", error: str = "", statusCode: int = 0):
		checks = 0
		if statusCode > 0:
			checks = checks + 1
			self.__assertStatusCode(statusCode)
		if not isinstance(data, str) or len(data) > 0:
			checks = checks + 1
			self.__assertData(data)
		if len(error) > 0:
			checks = checks + 1
			self.__assertErrorMessage(error)
		assert checks > 0, f"ResponseAssertion: at least one assertion must be made"

	def __assertErrorMessage(self, expected: str):
		self.__assertData({'error': expected})

	def __assertData(self, expected: str|dict):
		received = self.__response[0]
		self.__assertEqual(received, expected, source_name="Response Data")

	def __assertStatusCode(self, expected: int):
		received = self.__response[1]
		self.__assertEqual(received, expected, source_name="Status Code")

	def __assertEqual(self, received, expected, *, source_name: str):
		if self._matcher_state:
			assert received == expected, f"{source_name}: received [{received}], but should be [{expected}]"
		else:
			assert received != expected, f"{source_name}: received [{received}], but should be other than [{expected}]"

class _AssertResponse:
	_matcher: _AssertResponseMatcher
	_inv_matcher: _AssertResponseMatcher


	def __init__(self, response):
		self._matcher = _AssertResponseMatcher(response, True)
		self._inv_matcher = _AssertResponseMatcher(response, False)
		self._response = response

	@property
	def toBe(self) -> _AssertResponseMatcher:
		return self._matcher
	
	@property
	def notToBe(self) -> _AssertResponseMatcher:
		return self._inv_matcher

def assert_response(response):
	return _AssertResponse(response)