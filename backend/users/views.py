from django.contrib.auth import authenticate
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import LoginRequestSerializer, UserModelSerializer


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):

    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    @action(methods=["POST"], detail=False)
    def login(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        if user := authenticate(username=username, password=password):
            return Response(UserModelSerializer(user).data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
