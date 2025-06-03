"""
Search serializer
"""

from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=False, allow_blank=True)
