from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.shared.pagination.custom import CustomPagination
from apps.users.models.user import UserProfile
from apps.users.serializers.profile import UserProfileSerializer


class UserProfileView(APIView):
    """
    View to handle user profile operations.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Return the queryset for the user profile.
        """
        return UserProfile.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        """
        Retrieve user profile information.
        """
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        existing_profile = UserProfile.objects.filter(user=request.user).first()
        if existing_profile:
            return Response(
                {"detail": "Профиль уже существует."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailView(APIView):
    """
    View to handle user profile detail operations.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get(self, request, pk=None, *args, **kwargs):
        """
        Retrieve user profile detail.
        """
        user_profile = get_object_or_404(UserProfile, user=request.user, pk=pk)
        serializer = self.serializer_class(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None, *args, **kwargs):
        """
        Update user profile detail.
        """
        user_profile = get_object_or_404(UserProfile, user=request.user, pk=pk)
        serializer = self.serializer_class(
            user_profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
