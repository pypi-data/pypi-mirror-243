from __future__ import annotations

import pydantic.alias_generators


class PascalModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        alias_generator=pydantic.alias_generators.to_pascal,
        populate_by_name=True,
    )
