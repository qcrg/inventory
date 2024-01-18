from flask import Response
from sys import float_info as _finfo

_INT_MAX = 2_147_483_647

def _check_min_max(min_val, max_val):
  if not (min_val < max_val):
    raise ValueError("max_value must be greater than min_value")

class Validator:
  def __init__(self, name: str):
    self._NAME = name
    self._resp = (None, 200)
    self.value = None
    pass

  def check(self, value) -> bool:
    raise NotImplementedError("Please Implement this method")

  def response(self) -> (Response, int):
    return self.resp

  def is_ok(self) -> bool:
    return self.resp[1] == 200
  
  def __nonzero__(self) -> bool:
    return self.is_ok()
  
  def _set_ok_resp(self):
    self.resp = (None, 200)
  
  def _set_error_resp(self, error_message):
    from flask import jsonify
    self.resp = (jsonify(message=error_message), 400)

class NotNoneValidator(Validator):
  def __init__(self, name: str):
    super().__init__(name)

  def check(self, value) -> bool:
    if value is None:
      self._set_error_resp(f"{self._NAME} is undefined")
      return False
    self._set_ok_resp()
    self.value = value
    return True

class EmptyValidator(NotNoneValidator):
  def __init__(self, name: str):
    super().__init__(name)

  def check(self, value: str) -> bool:
    if not super().check(value):
      return False
    self.value = None

class _NumberValidator(NotNoneValidator):
  def __init__(self, name, min_val, max_val, number_type):
    super().__init__(name)
    _check_min_max(min_val, max_val)
    self._MIN_VALUE = min_val
    self._MAX_VALUE = max_val
    self._number_type = number_type

  def check(self, value_str: str) -> bool:
    nt = self._number_type

    if not super().check(value_str):
      return False
    self.value = None

    try:
      value = nt(value_str)
    except:
      self._set_error_resp(f"{self._NAME} must be {nt.__name__}")
      return False
    
    if value < self._MIN_VALUE:
      self._set_error_resp(
        f"{self._NAME} value must be equal to or less than {nt(self._MIN_VALUE)}"
      )
      return False
    
    if value > self._MAX_VALUE:
      self._set_error_resp(
        f"{self._NAME} value must be equal to or greater than {nt(self._MAX_VALUE)}"
      )
      return False

    self._set_ok_resp()
    self.value = value
    return True

class IntValidator(_NumberValidator):
  def __init__(self, name, min_val: int = 0, max_val: int = _INT_MAX):
    super().__init__(name, min_val, max_val, int)

class FloatValidator(_NumberValidator):
  def __init__(self, name, min_val: float = 0.0, max_val: float = _finfo.max):
    super().__init__(name, min_val, max_val, float)

class StringValidator(NotNoneValidator):
  def __init__(self, name, min_val: int = 0, max_val: int = _INT_MAX):
    super().__init__(name)
    if min_val < 0:
      raise ValueError("min_val must be equal to or greater than 0")
    _check_min_max(min_val, max_val)
    self._MIN_VALUE = min_val
    self._MAX_VALUE = max_val
  
  def check(self, value: str) -> bool:
    if not super().check(value):
      return False
    self.value = None

    if self._MIN_VALUE == 0 and len(value) == 0:
      self._set_error_resp(
        f"{self._NAME} can't be empty"
      )
      return False

    if self._MIN_VALUE > len(value):
      self._set_error_resp(
        f"{self._NAME} length must be equal to or greater than {self._MIN_VALUE}"
      )
      return False
    
    if self._MAX_VALUE < len(value):
      self._set_error_resp(
        f"{self._NAME} length must be equal to or less than {self._MAX_VALUE}"
      )
      return False

    self._set_ok_resp()
    self.value = value
    return True