from pydantic import BaseModel, EmailStr


class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class EmotionInput(BaseModel):
    text: str
    case_id: str


class CaseDetails(BaseModel):

    usecase: str

    name: str | None = None
    age: int | None = None
    gender: str | None = None
    doctor: str | None = None

    product: str | None = None
    reviewer: str | None = None
    feedbackType: str | None = None

    notes: str | None = None
