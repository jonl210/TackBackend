from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from users.models import Profile
from users.serializers import RegisterFormSerializer

#Sign up new user
@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    if request.method == "POST":
        serializer = RegisterFormSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data["username"]
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            new_user = User.objects.create_user(username, email, password)
            Token.objects.create(user=new_user)
            Profile.objects.create(user=new_user)
            return Response(status=status.HTTP_201_CREATED)
