from django.contrib.auth import authenticate
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import (
    LoginRequestSerializer,
    UserModelSerializer,
    UserQuerySerializer,
)


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):

    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    def get_queryset(self):
        serializer = UserQuerySerializer(data=self.request.query_params)

        queryset = self.queryset
        if not serializer.is_valid(raise_exception=True):
            return queryset.all()

        if user_type := serializer.validated_data.get("user_type"):
            queryset = queryset.filter(user_type=user_type)

        return queryset.all()

    @action(methods=["POST"], detail=False)
    def login(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        if user := authenticate(username=username, password=password):
            return Response(UserModelSerializer(user).data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
