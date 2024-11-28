from fastapi import FastAPI, status
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID, uuid4

app = FastAPI()

class UserCreate(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=20)
    age: int = Field(..., gt=18, lt=150)
    class Config:
        json_schema_extra = {
            "example": {
                "email": "example@example.com",
                "password": "password",
                "age": 20
            }
        }
class User(UserCreate):
    id: UUID = Field(default_factory=uuid4)

@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    created_user = User(**user.model_dump())
    return created_user