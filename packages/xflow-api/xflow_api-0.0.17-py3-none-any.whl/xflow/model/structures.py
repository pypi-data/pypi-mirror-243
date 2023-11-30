from dataclasses import dataclass

from pydantic import BaseModel, validator


@dataclass
class DataTypes:
    BOOL: str = "BOOL"
    UINT8: str = "UINT8"
    UINT16: str = "UINT16"
    UINT32: str = "UINT32"
    UINT64: str = "UINT64"
    INT8: str = "INT8"
    INT16: str = "INT16"
    INT32: str = "INT32"
    INT64: str = "INT64"
    FP16: str = "FP16"
    FP32: str = "FP32"
    FP64: str = "FP64"
    BYTES: str = "BYTES"
    BF16: str = "BF16"


@dataclass
class ModelTypes:
    TensorRT: str = "TensorRT"
    TensorFlow: str = "TensorFlow"
    PyTorch: str = "PyTorch"
    ONNX: str = "ONNX"


class ModelSignature(BaseModel):
    name: str
    data_type: str
    dimension: list

    @validator("data_type")
    def data_type_check(cls, v):
        if v not in list(DataTypes().__dict__.values()):
            raise ValueError(f"unsupported datatype {v}. use DataTypes class in xflow.model")
        return v

    class Config:
        extra = 'forbid'


