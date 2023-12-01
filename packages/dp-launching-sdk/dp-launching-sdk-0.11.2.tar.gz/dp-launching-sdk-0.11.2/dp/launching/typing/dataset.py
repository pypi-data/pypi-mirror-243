import base64
from typing import Any, Dict


__all__ = [
    "LaunchingOutputDatasetName",
]


class LaunchingOutputDatasetName(str):
    def get_value(self):
        return str(self)

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(format="launching_output_dataset_name", scope="executor")

    @classmethod
    def __get_validators__(cls) -> Any:
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> "LaunchingOutputDatasetName":
        if isinstance(value, LaunchingOutputDatasetName):
            return value
        elif isinstance(value, str):
            return LaunchingOutputDatasetName(value)
        elif isinstance(value, (bytes, bytearray, memoryview)):
            return LaunchingOutputDatasetName(base64.b64encode(value).decode())
        else:
            raise Exception(f"LaunchingOutputDatasetName Wrong type: {type(value)}")
