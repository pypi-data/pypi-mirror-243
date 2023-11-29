"""
Allows simple schema parsing and validation for inputs.

Classes:
    Schema
    InputItem
    StringValidator
    NumericValidator
    ArrayValidator
    ValidationError
"""
from typing import (
    List,
    Optional,
    Callable,
    Union,
    Dict,
    TypeVar,
    TYPE_CHECKING,
)
from PyYep.validators.string import StringValidator
from PyYep.validators.numeric import NumericValidator
from PyYep.validators.array import ArrayValidator
from PyYep.exceptions import ValidationError

if TYPE_CHECKING:
    from .validators import Validator


InputT = TypeVar("InputT")
InputValueT = TypeVar("InputValueT")


class Schema:
    """
    A class to represent a schema.

    ...

    Attributes
    ----------
    _inputs: Union[List[InputItem], List[Validator]]
            the schema inputs
    on_fail: Callable[[], None]
            a callable to be used as a error hook
    abort_early: bool
            sets if the schema will raise a exception soon after
            a validation error happens

    Methods
    -------
    validate():
            Execute the inputs validators and return a dict containing all the
            inputs' values
    """

    def __init__(
        self,
        inputs: Union[List["InputItem"], List["Validator"]],
        on_fail: Optional[Callable[[], None]] = None,
        abort_early: Optional[int] = True,
    ) -> None:
        """
        Constructs all the necessary attributes for the schema object.

        Parameters
        ----------
                inputs (Union[List[InputItem], List[Validator]]):
                    the schema inputs
                on_fail (Callable[[], None]):
                    a callable to be used as a error hook
                abort_early (bool):
                    sets if the schema will raise a exception soon after
                    an error happens
        """

        for item in inputs:
            item._set_parent_form(self)

        self._inputs = inputs
        self.on_fail = on_fail
        self.abort_early = abort_early

    def validate(self) -> Dict[str, InputValueT]:
        """
        Execute the inputs validators and return a dict containing
        all the inputs' values

        Raises
        -------
        ValidationError: if any validation error happens in the
        inputs validation methods

        Returns
        -------
        result (dict): a dict containing all the validated values
        """

        result = {}
        errors = []

        for item in self._inputs:
            try:
                result[item.name] = item.verify()
            except ValidationError as error:
                if self.abort_early:
                    raise error

                errors.append(error)

        if not self.abort_early and errors:
            raise ValidationError(
                "", "One or more inputs failed during validation", inner=errors
            )

        return result


class InputItem:
    """
    A class to represent a input item.

    ...

    Attributes
    ----------
    name: str
            the name of the input item
    _form: Schema
            the parent schema
    _input: InputT
            the input itself
    _path: str
            the property or method name that store the value in the input
    _validators: List[Callable[[InputValueT], None]]
            a list of validators
    on_success: Callable[[], None]
            a callable used as a local success hook
    on_fail: Callable[[], None]
            a callable used as a local error hook

    Methods
    -------
    _set_parent_form(form):
            Set the parent schema of the input item

    verify(result):
            Execute the inputs validators and return the result

    validate(validator):
            receives a validator and appends it on the validators list

    condition(condition):
            Set a condition for the execution of the previous validator

    modifier(modifier):
            Set a modifier to allow changes in the value after validation

    string():
            create a StringValidator using the input item as base

    number():
            create a NumericValidator using the input item as base
    """

    def __init__(
        self,
        name: str,
        input_: InputT,
        path: str,
        on_success: Optional[Callable[[], None]] = None,
        on_fail: Optional[Callable[[], None]] = None,
    ):
        """
        Constructs all the necessary attributes for the input item object.

        Parameters
        ----------
                name (str):
                    the name of the input item
                input_ (InputT):
                    the input itself
                path (str):
                    the input's property or method name that store the value
                on_success (Callable[[], None]):
                    a callable to be used as a local success hook
                on_fail (Callable[[], None]):
                    a callable to be used as a local error hook
        """

        self.name = name
        self._form = None
        self._input = input_
        self._path = path

        self._validators = []
        self._conditions = {}
        self._modifier = None
        self.on_fail = on_fail
        self.on_success = on_success

    def _set_parent_form(self, form: Schema) -> None:
        """
        Set the parent schema of the input item

        Parameters
        ----------
        form : Schema
                the input item parent schema

        Returns
        -------
        None
        """

        self.form = form

    def verify(self, result: Optional[InputValueT] = None) -> InputValueT:
        """
        Get the input value and execute all the validators

        Parameters
        ----------
        result : Optional[InputValueT]
                the value stored on the input, if not passed it will use
                the value returned by the method or attribute with the name
                stored on the input item _path attribute

        Raises:
        _______
        ValidationError:
                if any error happens during the validation process

        Returns
        -------
        result (InputValueT): The value received after all the validation
        """

        if result is None:
            result = getattr(self._input, self._path)

        if callable(result):
            result = result()

        for validator in self._validators:
            if validator in self._conditions and not self._conditions[
                validator
            ](result):
                continue

            try:
                validator(result)
            except ValidationError as error:
                if self.on_fail is not None:
                    self.on_fail()
                elif self.form.on_fail is not None:
                    self.form.on_fail()

                raise error

        if self.on_success is not None:
            self.on_success()

        return result if self._modifier is None else self._modifier(result)

    def validate(
        self, validator: Callable[[InputValueT], None]
    ) -> "InputItem":
        """
        Append a validator in the input item validators list

        Returns
        -------
        self (InputItem): The input item itself
        """

        self._validators.append(validator)
        return self

    def condition(
        self, condition: Callable[[InputValueT], bool]
    ) -> "InputItem":
        """
        Set a condition for the execution of the previous validator

        Parameters
        ----------
        condition : Callable
                a callable that return a boolean that defines if the condition
                was satisfied

        Returns
        -------
        InputItem
        """

        self._conditions[self._validators[-1]] = condition
        return self

    def modifier(self, modifier: Callable[[InputValueT], bool]) -> "InputItem":
        """
        Set a modifier to allow changes in the value after validation

        Parameters
        ----------
        modifier : Callable
                a callable that executes changes in the value after validation

        Returns
        -------
        InputItem
        """

        self._modifier = modifier
        return self

    def string(self) -> StringValidator:
        """
        create a StringValidator using the input item as base

        Returns
        -------
        result (StringValidator): A string validator object
        """
        return StringValidator(self)

    def number(self) -> NumericValidator:
        """
        create a NumericValidator using the input item as base

        Returns
        -------
        result (NumericValidator): A numeric validator object
        """
        return NumericValidator(self)

    def array(self) -> ArrayValidator:
        """
        create a ArrayValidator using the input item as base

        Returns
        -------
        result (ArrayValidator): An array validator object
        """
        return ArrayValidator(self)
