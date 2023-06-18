from rest_framework import serializers


class GoogleAuthSerializer(serializers.Serializer):
    """Data serialization from Google"""

    token = serializers.CharField()
    client = serializers.CharField()
