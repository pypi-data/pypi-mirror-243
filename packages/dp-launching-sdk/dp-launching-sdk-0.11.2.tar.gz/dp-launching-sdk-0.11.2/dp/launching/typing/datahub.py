from typing import Any, Dict

__all__ = ["DatasetsSelect", "ModelsSelect"]


class DatasetsSelect(object):
    datahub_type = "datasets"

    def get_value(self):
        if hasattr(self, "value"):
            return self.value
        return None

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(format="datasets_select", scope="io")

    @classmethod
    def __get_validators__(cls) -> Any:
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> "DatasetsSelect":
        if isinstance(value, DatasetsSelect):
            return value
        elif isinstance(value, str):
            ds = DatasetsSelect()
            ds.value = value
            return ds
        elif isinstance(value, list):
            ds = DatasetsSelect()
            ds.value = value
            return ds
        else:
            raise Exception(f"DatasetsSelect Wrong type: {type(value)}")


class ModelsSelect(object):
    type = "models"

    def get_value(self):
        if hasattr(self, "value"):
            return self.value
        return None

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(format="models_select", scope="io")

    @classmethod
    def __get_validators__(cls) -> Any:
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> "ModelsSelect":
        if isinstance(value, ModelsSelect):
            return value
        elif isinstance(value, str):
            ds = ModelsSelect()
            ds.value = value
            return ds
        elif isinstance(value, list):
            ds = ModelsSelect()
            ds.value = value
            return ds
        else:
            raise Exception(f"ModelsSelect Wrong type: {type(value)}")
