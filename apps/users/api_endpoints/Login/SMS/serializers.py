from rest_framework import serializers


class SendSMSSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
