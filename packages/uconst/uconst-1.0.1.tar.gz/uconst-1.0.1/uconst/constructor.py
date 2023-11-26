from typing import List, Literal, Self, Union

from .const import process_base, splitter


class Constructor:
    def __init__(self, base: str, proto: Literal["https", "http"] = "https"):
        """Initialize constructor"""
        self.base = process_base(base)
        self.proto = proto
        
        self.parts: List[str] = []

    def __truediv__(self, r: Union[str, list]) -> Self:
        if isinstance(r, list):
            self.parts.extend(r)
        elif isinstance(r, str):
            self.parts.append(r)
        else:
            raise TypeError("Wrong url part type!")

        return self

    def __str__(self) -> str:
        return f"{self.proto}://{self.base}{splitter}{splitter.join(self.parts)}"
    
    def as_str(self) -> str:
        return str(self)
