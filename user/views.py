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
    """
    회원가입
    :param request:
        [
            username : 사용자명 - 아이디,
            email : 이메일,
            password : 비밀번호,
            password_check : 비밀번호 확인,
            is_staff : 0 or 1
        ]

    :return: 201 : 회원 가입 성공
             400 : (실패)요청 데이터가 유효하지 않을 경우
    """
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
    """
    로그인
    :param request:
        [
            username : 사용자명 - 아이디,
            password : 비밀번호
        ]
    :return: 200 : 로그인 성공
             401 : 로그인 실패
    """
    if 'username' not in request.data:
        return JsonResponse({
            "msg": "The username is required."
        }, status=status.HTTP_400_BAD_REQUEST)

    if 'password' not in request.data:
        return JsonResponse({
            "msg": "The password is required."
        }, status=status.HTTP_400_BAD_REQUEST)

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
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    로그아웃
    :param request:  token (Headers) : 로그인시 발행한 유효한 토근 값
    :return: 200 : 로그아웃 성공
    """
    request.user.auth_token.delete()
    # Logout will remove all session data
    logout(request)
    return JsonResponse({
        "msg": "logout successfully."
    }, status=status.HTTP_200_OK)
