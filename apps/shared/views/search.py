from rest_framework import permissions, views, status
from rest_framework.response import Response

from apps.pedagog.models.topic import Topic
from apps.pedagog.models.electron_resource import ElectronResourceCategory, ElectronResourceSubCategory, ElectronResource

from apps.pedagog.serializers.topic import TopicSearchSerializer
from apps.pedagog.serializers import electron_resource as resource_serializer

class SearchApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        text = request.query_params.get('search', '').strip()
        limit = int(request.query_params.get("limit", 10)) 

        if not text:
            return Response(
                {"success": False, "message": "search is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        topics = Topic.objects.filter(name__istartswith=text).select_related('plan_id')[:limit]
        categories = ElectronResourceCategory.objects.filter(name__istartswith=text)[:limit]
        subcategories = ElectronResourceSubCategory.objects.filter(name__istartswith=text).select_related('category')[:limit]
        resources = ElectronResource.objects.filter(name__istartswith=text).select_related('category')[:limit]

        data = {
            "topics": TopicSearchSerializer(topics, many=True).data,
            "electronic_resource_categories": resource_serializer.ElectronResourceCategorySerializer(
                categories, many=True
            ).data,
            "electron_resource_sub_categories": resource_serializer.ElectronResourceSubCategorySearchSerializer(
                subcategories, many=True
            ).data,
            "electron_resources": resource_serializer.ElectronResourceSearchSerializer(
                resources, many=True
            ).data,
        }

        return Response(data, status=status.HTTP_200_OK)