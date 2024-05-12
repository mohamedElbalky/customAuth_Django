from uuid import uuid4

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse


from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    parser_classes
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from .tasks import send_verification_email

from . import verify_user_email

from . import serializers
from . import models


@extend_schema(request=serializers.RegisterSerializer, responses=None, tags=["manage account"])
@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    """register new user view"""
    serializer = serializers.RegisterSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get("email")
        validation_token = verify_user_email.generate_verification_token(email=email)
        verify_url = reverse("account:verify_token", kwargs={"token": validation_token})
        verification_url = request.build_absolute_uri(verify_url)
        # verification_url = request.build_absolute_uri('/api/account/verify/') + str(validation_token)
        # print("--------------------------")
        # print(verification_url)
        # print("--------------------------")
        sent = send_verification_email.delay(
            user_email=email, verification_url=verification_url
        )
        if sent:
            serializer.save()
            return Response(
                {"message": "Verification email sent"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": "Failed to send verification email"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=None, responses=None, tags=["manage account"])
@api_view(["POST"])
@permission_classes([AllowAny])
def verify_email_view(request, token):
    email = verify_user_email.get_email_from_token(token=token)
    if not email:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    verified_email = verify_user_email.verify_user_email(email=email)
    if not verified_email:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Email verified"}, status=status.HTTP_200_OK)


@extend_schema(request=serializers.LoginSerializer, responses=None, tags=["manage account"])
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """user login view"""
    serializer = serializers.LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        print(dir(refresh))
        return Response(
            {"access": str(refresh.access_token), "refresh": str(refresh)},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=serializers.UserSerializer, responses=None)
@api_view(["GET"])
@permission_classes([IsAdminUser])
def user_list_view(request):
    """list users view: staff users can only use this endpoint"""
    users = get_user_model().objects.all().order_by("-date_joined")
    serializer = serializers.UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(request=serializers.UserSerializer, responses=None)
@api_view(["GET"])
def user_detail_view(request):
    """user detail view"""
    user = request.user
    # if not user:
    #     return Response(
    #         {"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
    #     )
    serializer = serializers.UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(request=serializers.UserAvatarSerializer, responses=None)
@parser_classes([MultiPartParser, FormParser])
@api_view(["POST"])
def change_avatar_view(request):
    """change user's avatar view, NOTE: user 'Content-Type: multipart/form-data'"""
    user = request.user
    serializer = serializers.UserAvatarSerializer(instance=user, data=request.data, context={"request": request})
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"message": "Success added Avatar"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=serializers.UserEditSerializer, responses=None)
@api_view(["PATCH"])
def edit_user_info(request):
    user = request.user
    serializer = serializers.UserEditSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Success edited user info [firstname and lastname]"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)