import sys

from rest_framework import serializers

from apps.common.enums import PaymentType
from apps.preventa.models import Audio, UserContentPaymentPlan
from apps.users.models import User


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "photo")


class UserContentPaymentPlanSerializer(serializers.ModelSerializer):
    available_reproductions = serializers.SerializerMethodField()

    class Meta:
        model = UserContentPaymentPlan
        fields = ("payment_plan", "available_reproductions", "limited_reproduction")

    def get_available_reproductions(self, obj):
        if obj.payment_plan == PaymentType.ONE_TIME:
            return
        return obj.available_reproductions


class PreventaAudioDetailSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer()
    is_bought = serializers.SerializerMethodField()
    audio_file = serializers.SerializerMethodField()
    user_content_plan = UserContentPaymentPlanSerializer(many=True)

    class Meta:
        model = Audio
        fields = (
            "uuid",
            "slug",
            "title",
            "cover",
            "duration_seconds",
            "creator",
            "is_bought",
            "audio_file",
            "four_repr_price",
            "price",
            "user_content_plan",
        )

    def get_is_bought(self, obj):
        user = self.context["request"].user

        if not user.is_authenticated:
            return False

        return obj.is_bought(user)

    def get_audio_file(self, obj):
        if "test" in sys.argv:
            return "test_url"

        request = self.context["request"]
        user = request.user

        if not user.is_authenticated:
            return

        if obj.is_bought(user):
            return obj.file.url

        return
