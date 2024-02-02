from django.contrib.auth import authenticate

from .models import Order, User
from .schemas import OrderIn, OrderOut, UserRegistrationSchema, AuthOutSchema, AuthSchema
from django.contrib.auth.hashers import make_password
from ninja import NinjaAPI
from ninja.security import HttpBearer
from rest_framework_simplejwt.tokens import AccessToken

from .utils import get_tokens_for_user

api = NinjaAPI(title='Order API', description='API for creating and listing orders', version='1.0.0', )


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = AccessToken(token).payload
            user_id = payload.get('user_id')
            user = User.objects.get(id=user_id)
            return user
        except Exception as e:
            return None


auth = AuthBearer()


@api.post("/orders/", response=OrderOut, auth=auth)
def create_order(request, payload: OrderIn):
    order = Order.objects.create(**payload.dict())
    return order


@api.get("/orders/", response=list[OrderOut], auth=auth)
def list_orders(request):
    user = request.auth
    orders = Order.objects.filter(category=user.category)
    return orders


@api.post("/register/")
def register(request, user_in: UserRegistrationSchema):
    user = User.objects.create(
        username=user_in.username,
        email=user_in.email,
        category=user_in.category,
        password=make_password(user_in.password)
    )
    tokens = get_tokens_for_user(user)
    return {
        "id": user.id,
        "username": user.username,
        "tokens": tokens,
    }


@api.post("/token/", response=AuthOutSchema)
def get_token(request, auth_data: AuthSchema):
    user = authenticate(username=auth_data.username, password=auth_data.password)
    if user is not None:
        tokens = get_tokens_for_user(user)
        return tokens
    else:
        return api.create_response(request, {"detail": "Invalid credentials"}, status=401)
