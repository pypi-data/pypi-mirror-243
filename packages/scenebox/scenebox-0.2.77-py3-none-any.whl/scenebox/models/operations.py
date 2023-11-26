from abc import ABC, abstractmethod
from typing import Optional, List, Union, NamedTuple, Any, Dict

from ..clients import SceneEngineClient
from ..constants import AssetsConstants, JobConstants, AnnotationGroups, AnnotationTypes
from ..custom_exceptions import OperationError
from ..tools.logger import get_logger

logger = get_logger(__name__)


class ParameterDataType:
    INT = "int"
    FLOAT = "float"
    STR = "str"
    BOOL = "bool"
    DICT = "dict"
    LIST_FLOAT = "list_float"
    LIST_INT = "list_int"
    LIST_STR = "list_str"
    LIST_DICT = "list_dict"


class BaseParameter:
    def __init__(self, field_name: str,
                 field_data_type: str,
                 accept_none_as_valid: bool = False,
                 description: Optional[str] = None):

        self.field_name = field_name
        self.field_data_type = field_data_type
        self.description = description
        self.accept_none_as_valid = accept_none_as_valid

    def _validate_datatype(self, value):
        try:
            if self.field_data_type == ParameterDataType.INT:
                if value is None:
                    if not self.accept_none_as_valid:
                        raise AssertionError
                else:
                    assert isinstance(value, int)
            elif self.field_data_type == ParameterDataType.FLOAT:
                if value is None:
                    if not self.accept_none_as_valid:
                        raise AssertionError
                else:
                    assert isinstance(value, float)
            elif self.field_data_type == ParameterDataType.STR:
                if value is None:
                    if not self.accept_none_as_valid:
                        raise AssertionError
                else:
                    assert isinstance(value, str)
            elif self.field_data_type == ParameterDataType.BOOL:
                if value is None:
                    if not self.accept_none_as_valid:
                        raise AssertionError
                else:
                    assert isinstance(value, bool)
            elif self.field_data_type == ParameterDataType.DICT:
                if value is None:
                    if not self.accept_none_as_valid:
                        raise AssertionError
                else:
                    assert isinstance(value, dict)
            elif self.field_data_type == ParameterDataType.LIST_FLOAT:
                assert isinstance(value, list)
                for item in value:
                    if value is None:
                        if not self.accept_none_as_valid:
                            raise AssertionError
                    else:
                        assert isinstance(item, float)
            elif self.field_data_type == ParameterDataType.LIST_INT:
                assert isinstance(value, list)
                for item in value:
                    if value is None:
                        if not self.accept_none_as_valid:
                            raise AssertionError
                    else:
                        assert isinstance(item, int)
            elif self.field_data_type == ParameterDataType.LIST_STR:
                assert isinstance(value, list)
                for item in value:
                    if value is None:
                        if not self.accept_none_as_valid:
                            raise AssertionError
                    else:
                        assert isinstance(item, str)
            elif self.field_data_type == ParameterDataType.LIST_DICT:
                assert isinstance(value, list)
                for item in value:
                    if value is None:
                        if not self.accept_none_as_valid:
                            raise AssertionError
                    else:
                        assert isinstance(item, dict)
            else:
                raise ValueError("Invalid data type definition for parameter {}".format(self.field_name))

        except (AssertionError, ValueError):
            logger.error("Invalid value {} for param {}. Expecting {}".format(value,
                                                                              self.field_name,
                                                                              self.field_data_type))

            raise ValueError("Invalid value {} for param {}. Expecting {}".format(value,
                                                                                  self.field_name,
                                                                                  self.field_data_type))

    def as_dict(self):
        return self.__dict__


class RangeParameter(BaseParameter):
    def __init__(self,
                 field_name: str,
                 field_data_type: str,
                 min_value: Union[float, int],
                 max_value: Union[float, int],
                 default_value: Optional[Union[float, int]] = None,
                 accept_none_as_valid: bool = False,
                 description: Optional[str] = None):

        # UI is created as a slider
        super().__init__(field_name=field_name,
                         field_data_type=field_data_type,
                         description=description)
        self.min_value = min_value
        self.max_value = max_value
        self.default_value = default_value
        self.parameter_type = "range_parameter"
        self.accept_none_as_valid = accept_none_as_valid

    def validate(self, value):

        assert value is not None
        try:
            self._validate_datatype(value)
        except Exception as e:
            logger.error("Error validating datatype for {} with value {}".format(self.field_name,
                                                                                 value))
            raise e
        assert self.min_value <= value <= self.max_value, \
            "Incorrect value for {}. Must be in range [{}, {}]".format(
                self.field_name, self.min_value, self.max_value)


class FieldValueParameter(BaseParameter):
    # If values are provided, UI is a one-of-many choice
    # If not, this is a value input from the user
    def __init__(self,
                 field_name: str,
                 field_data_type: str,
                 values: Optional[List[Union[int, str]]] = None,
                 default_value: Optional[Union[float, int, str, List[float], List[int], List[str]]] = None,
                 accept_none_as_valid: bool = False,
                 description: Optional[str] = None):

        super().__init__(field_name=field_name,
                         field_data_type=field_data_type,
                         description=description)
        self.values = values
        self.default_value = default_value
        self.parameter_type = "field_value_parameter"
        self.accept_none_as_valid = accept_none_as_valid

    def validate(self, value):
        try:
            self._validate_datatype(value)
        except Exception as e:
            logger.error("Error validating datatype for {} with value {}. Error {}".format(self.field_name,
                                                                                           value, e))
            raise e
        if self.values:
            if isinstance(value, list):
                for item in value:
                    assert item in self.values, \
                        "Invalid value for {}. Choose one of {}".format(self.field_name, self.values)
            else:
                assert value in self.values, \
                    "Invalid value for {}. Choose one of {}".format(self.field_name, self.values)


class RawParameter(BaseParameter):
    # For parameters that are read as json or dictionaries
    def __init__(self,
                 field_name: str,
                 default_value: Optional[dict] = None,
                 accept_none_as_valid: bool = False,
                 description: Optional[str] = None):

        super().__init__(field_name=field_name,
                         field_data_type=ParameterDataType.DICT,
                         description=description)
        self.default_value = default_value
        self.parameter_type = "raw_parameter"
        self.accept_none_as_valid = accept_none_as_valid

    def validate(self, value):
        try:
            self._validate_datatype(value)
        except Exception as e:
            logger.error("Error validating datatype for {} with value {}".format(self.field_name,
                                                                                 value))
            raise e


class BooleanParameter(BaseParameter):
    # UI is a single checkbox
    def __init__(self,
                 field_name: str,
                 default_value: Optional[bool] = None,
                 accept_none_as_valid: bool = False,
                 description: Optional[str] = None):

        super().__init__(field_name=field_name,
                         field_data_type=ParameterDataType.BOOL,
                         description=description)
        self.default_value = default_value
        self.parameter_type = "boolean_parameter"
        self.accept_none_as_valid = accept_none_as_valid

    def validate(self, value):
        try:
            self._validate_datatype(value)
        except Exception as e:
            logger.error("Error validating datatype for {} with value {}".format(self.field_name,
                                                                                 value))
            raise e


class OperationPayloadEntity:
    def __init__(self, field_name: str, field_data_type: str):
        self.field_name = field_name
        self.field_data_type = field_data_type

    def as_dict(self):
        return self.__dict__


class SetsList(OperationPayloadEntity):
    def __init__(self,
                 content_asset_types: List[str]):

        super().__init__(field_name="sets", field_data_type=ParameterDataType.LIST_STR)
        for asset_type in content_asset_types:
            assert asset_type in AssetsConstants.VALID_ASSETS
        self.content_asset_types = content_asset_types
        self.payload_type = "sets_list"

    def validate(self,
                 values,
                 sec: SceneEngineClient):

        assert isinstance(values, list) or isinstance(values, tuple)
        sets_amc = sec.get_asset_manager(asset_type=AssetsConstants.SETS_ASSET_ID)
        for set_id in values:
            if sets_amc.exists(id=set_id):
                set_metadata = sets_amc.get_metadata(id=set_id)
                assert set_metadata["assets_type"] in self.content_asset_types, "Incorrect asset type " \
                    "for input set. Need {}. Found {}".format(self.content_asset_types,
                                                              set_metadata["assets_type"])
            else:
                raise OperationError("set with id {} does not exist".format(set_id))


class PhaseEntity:
    def __init__(self,
                 name: str,
                 param_schema: List[BaseParameter],
                 description: Optional[str] = None):

        self.name = name
        self.param_schema = param_schema
        self.description = description

    def validate(self, phase_name: str, params: dict):
        assert self.name == phase_name

        param_name_schema_map = {param.field_name: param for param in self.param_schema}
        for param_name, value in params.items():
            param_schema_object = param_name_schema_map.get(param_name)
            assert param_schema_object, "Parameter schema for {} is not defined".format(param_name)
            param_schema_object.validate(value)

    def as_dict(self):
        self_as_dict = {
            "name": self.name,
        }

        params_list = []
        for param in self.param_schema:
            params_list.append(param.as_dict())

        self_as_dict["param_schema"] = params_list

        return self_as_dict


class BaseOperation(ABC):
    """
    Abstract class for defining an Operation
    """

    def __init__(self, scene_engine_client: SceneEngineClient):
        """
        Definition the config, input, output, phase and parameter schemas for this operation here.
        config_schema: List[BaseParameter]
        Example:
            self.config_schema = [
                FieldValueParameter(field_name="my_input",
                                    default_value="value_1",
                                    field_data_type=ParameterDataType.STR),
                BooleanParameter(field_name="Do_More",
                                 default_value=False)
            ]

        input_schema: List[OperationPayloadEntity]
        Example:
            self.input_schema = [
                SetsList(content_asset_types=[AssetsConstants.IMAGES_ASSET_ID])
            ]

        output_schema: List[OperationPayloadEntity]
        Example:
            self.output_schema = [
                SetsList(content_asset_types=[AssetsConstants.IMAGES_ASSET_ID])
            ]

        phase_params_schema: List[PhaseEntity]
        Example:
            self.phase_params_schema = [
                PhaseEntity(name="phase_1",
                            param_schema=[
                                FIeldValueParameter(field_name="phase_input",
                                                    default_value="phase_value_1",
                                                    field_data_type=ParameterDataType.STR),
                                BooleanParameter(field_name="Do_More_Phase",
                                                 default_value=True)
                            ])
            ]
        """

        self.config_schema = None
        self.input_schema = None
        self.output_schema = None
        self.phase_params_schema = None
        self.sec = scene_engine_client

    def _serialized_config_schema(self) -> list:
        """
        Returns the config schema in json format
        """
        schema_list = []
        if self.config_schema:
            for param in self.config_schema:
                param_dict = param.as_dict()
                schema_list.append(param_dict)

        return schema_list

    def _serialized_input_schema(self) -> list:
        """
        Returns the input schema in json format
        """
        schema_list = []
        if self.input_schema:
            for entity in self.input_schema:
                entity_dict = entity.as_dict()
                schema_list.append(entity_dict)
            return schema_list
        else:
            raise OperationError("Operation missing input schema definition")

    def _serialized_output_schema(self) -> list:
        """
        Returns the output schema in json format
        """
        schema_list = []
        if self.output_schema:
            for entity in self.output_schema:
                entity_dict = entity.as_dict()
                schema_list.append(entity_dict)

        return schema_list

    def _serialized_phase_params_schema(self) -> list:
        """
        Returns the phase params schema in json format
        """
        schema_list = []
        if self.phase_params_schema:
            for entity in self.phase_params_schema:
                entity_dict = entity.as_dict()
                schema_list.append(entity_dict)
        return schema_list

    def _validate_input_payload(self, input_payload: dict):
        """
        Validates data before running the process.
        """
        # Validate config against schema
        payload_entity_name__schema_map = {payload_entity.field_name: payload_entity
                                           for payload_entity in self.input_schema}

        for payload_entity_name, values in input_payload.items():
            payload_schema_object = payload_entity_name__schema_map.get(payload_entity_name)
            assert payload_schema_object, "input payload schema for {} is not defined".format(
                payload_entity_name)
            payload_schema_object.validate(values=values,
                                           sec=self.sec)

    def _validate_output_payload(self, output_payload: dict):
        """
        Validates data after running the process.
        """
        # Validate config against schema
        if self.output_schema:
            payload_entity_name__schema_map = {payload_entity.field_name: payload_entity
                                               for payload_entity in self.output_schema}

            for payload_entity_name, values in output_payload.items():
                payload_schema_object = payload_entity_name__schema_map.get(payload_entity_name)
                assert payload_schema_object, "output payload schema for {} is not defined".format(
                    payload_entity_name)
                payload_schema_object.validate(values=values,
                                               sec=self.sec)
        else:
            assert not output_payload, "Operation is not expected to generate an output payload"

    def _validate_config(self, config: dict):
        """
        Validates every new config
        """
        # Validate config against schema
        param_name__schema_map = {param.field_name: param for param in self.config_schema}

        for param_name, value in config.items():
            param_schema_object = param_name__schema_map.get(param_name)
            assert param_schema_object, "Parameter schema for {} is not defined".format(param_name)
            param_schema_object.validate(value)

    def _validate_phase_params(self, phase_name: str, phase_params: dict):
        """
        Validates parameters for each phase of the operation
        """
        # Validate config against schema
        phase_name__param_schema_map = {phase.name: phase for phase in self.phase_params_schema}
        assert phase_name in phase_name__param_schema_map.keys(), "Invalid phase {}".format(phase_name)

        param_schema_object = phase_name__param_schema_map.get(phase_name)
        assert param_schema_object, "Parameter schema for phase {} is not defined".format(phase_name)
        param_schema_object.validate(phase_name, phase_params)

    def save_state(self,
                   instance_id: str,
                   state_dict: dict,
                   overwrite: bool = False):
        """
        Save state for an operation instance
        """
        current_state = {}
        if not overwrite:
            instance_meta = self.sec._get_operation_instance(operation_instance_id=instance_id)
            current_state = instance_meta["state_dict"] or {}

        # Merge two dictionaries
        if current_state.get("user_data"):
            current_state["user_data"].update(state_dict)
        else:
            current_state["user_data"] = state_dict

        self.sec._update_operation_instance(operation_instance_id=instance_id,
                                            state_dict=current_state)

    def get_state(self,
                  instance_id: str) -> dict:
        """
        Get current state of the operation instance
        """
        instance_meta = self.sec._get_operation_instance(operation_instance_id=instance_id)
        current_state = instance_meta.get("state_dict", {}).get("user_data", {})

        return current_state

    def _save_state_internal(self,
                             instance_id: str,
                             state_dict: dict,
                             overwrite: bool = False):
        """
        Save state for an operation instance
        """
        current_state = {}
        if not overwrite:
            instance_meta = self.sec._get_operation_instance(operation_instance_id=instance_id)
            current_state = instance_meta["state_dict"] or {}

        # Merge two dictionaries
        if current_state.get("internal_data"):
            current_state["internal_data"].update(state_dict)
        else:
            current_state["internal_data"] = state_dict

        self.sec._update_operation_instance(operation_instance_id=instance_id,
                                            state_dict=current_state)

    def _get_state_internal(self,
                            instance_id: str) -> dict:
        """
        Get current state of the operation instance
        """
        instance_meta = self.sec._get_operation_instance(operation_instance_id=instance_id)
        current_state = instance_meta.get("state_dict", {}).get("internal_data", {})

        return current_state

    @abstractmethod
    def process(self,
                instance_id: str,
                job_id: str,
                input_payload: dict,
                config: Optional[dict] = None,
                phase: Optional[str] = None,
                phase_payload: Optional[dict] = None) -> dict:

        if config:
            self._validate_config(config=config)

        if input_payload:
            self._validate_input_payload(input_payload=input_payload)

        if phase:
            self._validate_phase_params(phase_name=phase, phase_params=phase_payload)

        # Write operation login here
        output_payload = {}

        return output_payload


class OperationPriorities:
    HIGH_PRIORITY_OPERATION = "high_priority_operation"
    LOW_PRIORITY_OPERATION = "low_priority_operation"
