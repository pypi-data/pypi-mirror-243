from typing import Any, Dict, List
from deprecated.sphinx import deprecated

__all__ = ["BenchmarkLabels", "BenchmarkTags"]


class BenchmarkLabels(dict):
    @deprecated(version="0.8.7", reason="Use DflowLabels instead of BenchmarkLabels")
    def get_value(self) -> Dict:
        if hasattr(self, "value"):
            return self.value
        return {}

    @classmethod
    @deprecated(version="0.8.7", reason="Use DflowLabels instead of BenchmarkLabels")
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(format="benchmark_labels", scope="executor")

    @classmethod
    @deprecated(version="0.8.7", reason="Use DflowLabels instead of BenchmarkLabels")
    def __get_validators__(cls) -> Any:  # type: ignore
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> "BenchmarkLabels":
        if isinstance(value, dict):
            f = BenchmarkLabels(value)
            f.value = value
            return f
        else:
            raise Exception(f"BenchmarkLabels Wrong type: {type(value)}")


class BenchmarkTags(list):
    def get_value(self) -> List:
        if hasattr(self, "value"):
            return self.value
        return []

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(format="benchmark_tags", scope="executor")

    @classmethod
    def __get_validators__(cls) -> Any:  # type: ignore
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> "BenchmarkTags":
        if isinstance(value, list):
            f = BenchmarkTags(value)
            f.value = value
            return f
        else:
            raise Exception(f"BenchmarkTags Wrong type: {type(value)}")
