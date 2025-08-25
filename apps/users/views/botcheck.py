from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from apps.users.serializers.user import UserSerializer
from apps.users.models.user import User
from django.db.models import Count

import uuid
import os


BOT_USERNAME = os.getenv("BOT_USERNAME")



class CheckUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        tg_id = request.data.get("tg_id")
        phone = request.data.get("phone")

        if tg_id:
            user = User.objects.filter(tg_id=tg_id).first()
            if user:
                if not user.referral_code:
                    user.referral_code = str(uuid.uuid4())[:8]
                    user.save(update_fields=["referral_code"])

                referral_link = f"https://t.me/{BOT_USERNAME}?startapp={user.referral_code}"
                return Response(
                    {
                        "exists": True,
                        "message": "Foydalanuvchi topildi (tg_id orqali).",
                        "referral_link": referral_link,
                    },
                    status=status.HTTP_200_OK,
                )

        if phone:
            try:
                user = User.objects.get(phone=phone)

                if tg_id and not user.tg_id:
                    user.tg_id = tg_id

                if not user.referral_code:
                    user.referral_code = str(uuid.uuid4())[:8]

                user.save(update_fields=["tg_id", "referral_code"])

                referral_link = f"https://t.me/{BOT_USERNAME}?startapp={user.referral_code}"
                return Response(
                    {
                        "exists": True,
                        "message": "Foydalanuvchi telefon raqami orqali topildi.",
                        "referral_link": referral_link,
                    },
                    status=status.HTTP_200_OK,
                )
            except User.DoesNotExist:
                return Response(
                    {
                        "exists": False,
                        "message": "Bunday telefon raqam topilmadi.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(
            {
                "exists": False,
                "message": "tg_id yoki telefon raqam yuborilmadi.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
        
        



class UserByIdView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        tg_id = request.query_params.get("tg_id")
        if not tg_id:
            return Response({"detail": "Tg id topilmadi"})
        
        try:
            user = User.objects.get(tg_id=tg_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Foydalanuvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
                
                
                
class TopReferrersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = (
            User.objects.annotate(referral_count=Count("referrals"))
            .order_by("-referral_count")[:10]
        )
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)