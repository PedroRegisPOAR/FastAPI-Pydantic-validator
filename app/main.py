from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator

app = FastAPI()


class SpecialNumber(BaseModel):
    special_number: Optional[int]

    @validator("special_number")
    def validate_special_number(cls, value):
        if value not in [3, 5]:
            raise ValueError("The field special_number only accepts 3 or 5.")
        return value


@app.patch("/define-special-number")
async def update_special_number(special_number_in: SpecialNumber):
    if special_number_in.special_number == 3:
        number = 10 * special_number_in.special_number
    elif special_number_in.special_number == 5:
        number = 15 * special_number_in.special_number
    else:
        raise HTTPException(status_code=400, detail="Invalid special_number!")
    return {"number": number}
