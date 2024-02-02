from ninja import Schema


class OrderIn(Schema):
    name: str
    description: str
    category: str


class OrderOut(Schema):
    id: int
    name: str
    description: str
    category: str


class UserRegistrationSchema(Schema):
    username: str
    password: str
    email: str
    category: str


class UserAuthSchema(Schema):
    username: str
    password: str


class AuthSchema(Schema):
    username: str
    password: str

class AuthOutSchema(Schema):
    access: str
    refresh: str
