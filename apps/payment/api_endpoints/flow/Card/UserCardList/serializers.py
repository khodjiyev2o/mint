from rest_framework import serializers

from apps.payment.models import UserCard


class UserCardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCard
        fields = ("type", "last_four_digits")
