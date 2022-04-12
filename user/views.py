from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.UserSerializer import RegistrationSerializer
from django.contrib.auth import authenticate, login, logout


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = RegistrationSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return JsonResponse({
            "msg": "create user successfully.",
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is not None:
        login(request, user)
        Token.objects.filter(user=user).delete()
        token = Token.objects.get_or_create(user=user)[0]
        user.token = token.key
        user.save()
        return JsonResponse({"user": {
            "username": user.username,
            "email": user.email
        }, "token": token.key}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({
            "msg": "The username and/or password is incorrect."
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    # Logout will remove all session data
    logout(request)
    return JsonResponse({
        "msg": "logout successfully."
    }, status=status.HTTP_200_OK)
