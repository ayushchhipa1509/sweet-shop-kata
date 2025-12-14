from pydantic import BaseModel


# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True


# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# --- Sweet Schemas ---
class SweetBase(BaseModel):
    name: str
    category: str
    price: float
    quantity: int


class SweetCreate(SweetBase):
    pass


class SweetPublic(SweetBase):
    id: int

    class Config:
        from_attributes = True
