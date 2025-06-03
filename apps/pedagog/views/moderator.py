from django.db.models import Q
from rest_framework import status, exceptions
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payment.services.services import send_money_to_moderator
from apps.pedagog.models.electron_resource import ElectronResource
from apps.pedagog.models.media import Media
from apps.pedagog.models.moderator import Moderator
from apps.pedagog.serializers.electron_resource import ElectronResourceMiniSerializer
from apps.pedagog.serializers.moderator import (
    ModeratorCreateSerializer,
    ModeratorListSerializer,
    ModeratorDetailSerializer,
    SendMoneySerializer,
    ModeratorTemetikPlanSerializer,
)
from apps.shared.pagination.custom import PedagogPagination
from apps.users.models.user import User


class ModeratorCreateViewSet(APIView):
    permission_classes = [AllowAny]
    serializer_class = ModeratorCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        moderators = Moderator.objects.filter(user=request.user)
        if not moderators.exists():
            raise exceptions.PermissionDenied("You are not a moderator.")
        serializer = self.serializer_class(moderators, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ModeratorListView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = ModeratorListSerializer
    pagination_class = PedagogPagination

    def get(self, request):
        try:
            search_query = request.GET.get("search", "")
            classes_filter = request.GET.get("classes", "")
            card_number = request.GET.get("card_number", "")

            moderators = Moderator.objects.filter(
                Q(user__role__icontains=search_query)
                | Q(user__first_name__icontains=search_query)
                | Q(user__last_name__icontains=search_query)
            )

            if classes_filter:
                moderators = moderators.filter(
                    user__classes__name__icontains=classes_filter
                )

            if card_number:
                moderators = moderators.filter(card_number__icontains=card_number)

            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(moderators, request)

            serializer = self.serializer_class(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ModeratorDetailView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = ModeratorDetailSerializer

    def get(self, request, pk):
        try:
            moderator = Moderator.objects.get(pk=pk)
            serializer = self.serializer_class(moderator)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Moderator.DoesNotExist:
            return Response(
                {"error": "Moderator topilmadi"},
                status=status.HTTP_404_NOT_FOUND,
            )


class SendMoneyToModerators(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = SendMoneySerializer(data=request.data)

        if serializer.is_valid():
            moderator_ids = serializer.validated_data["moderator_ids"]
            amount = serializer.validated_data["amount"]

            moderators = Moderator.objects.filter(id__in=moderator_ids)

            if not moderators:
                return Response(
                    {"error": "Tanlangan moderatorlar topilmadi"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            errors = []
            success = []
            for moderator in moderators:
                try:
                    transaction_id = send_money_to_moderator(moderator, amount)
                    success.append("%s -> %s" % (moderator.id, transaction_id))
                except Exception as e:
                    errors.append("%s -> %s" % (moderator.id, str(e)))

            return Response(
                {
                    "message": "Pul yuborish muvaffaqiyatli amalga oshirildi.",
                    "errors": errors,
                    "success": success,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModeratorTemetikPlanApiView(APIView):
    permission_classes = [IsAdminUser]
    pagination_class = PedagogPagination

    def get(self, request, moderator_id, *args, **kwargs):
        try:
            search_query = request.GET.get("search", "").strip()
            name_filter = request.GET.get("name", "").strip()

            medias = Media.objects.filter(user__id=moderator_id, topic__isnull=False)

            if search_query:
                medias = medias.filter(name__icontains=search_query)

            if name_filter:
                medias = medias.filter(name__icontains=name_filter)

            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(medias, request)

            serializer = ModeratorTemetikPlanSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ModeratorElectronResourcesApiView(APIView):
    permission_classes = [IsAdminUser]
    pagination_class = PedagogPagination

    def get(self, request, moderator_id):
        moderator = User.objects.filter(id=moderator_id).first()
        paginator = self.pagination_class()
        resources = paginator.paginate_queryset(
            ElectronResource.objects.filter(user=moderator), request
        )
        serializer = ElectronResourceMiniSerializer(resources, many=True)
        return paginator.get_paginated_response(serializer.data)
