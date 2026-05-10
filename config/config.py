from pydantic import BaseModel, BeforeValidator, conint, model_validator, ValidationError
from typing import Any, Tuple, Annotated, Optional


def parse_tuple(value: Any) -> Any:
    """Pydantic receives tuple as a string. It has to be converted to tuple of int"""
    if isinstance(value, str):
        coordinates: list = value.split(',', 1)
        return tuple(map(int, coordinates))
    return value

""" Pydantic basemodel for Config.txt data validation"""
class Config(BaseModel):
    width: int
    height: int
    entry: Annotated[Tuple[int, int], BeforeValidator(parse_tuple)]
    exit: Annotated[Tuple[int, int], BeforeValidator(parse_tuple)]
    output_file: str
    perfect: bool
    seed: Optional[int] = None

    @model_validator(mode='after')
    def validate_datas(self):
        x, y = self.entry
        if x >= self.width and y >= self.height:
            raise ValueError("Entry out of bound!")

        x, y = self.exit
        if x >= self.width and y >= self.height:
            raise ValueError("Exit out of bound!")
        
        if self.entry == self.exit:
            raise ValueError("Entry and Exit must be different")
        
        if self.width < 0 or self.height < 0:
            raise ValueError("Width and height must be positive")
        if self.width < 7 or self.height < 7:
            raise ValueError("Too small for maze! Minimum 7x7")

        return self