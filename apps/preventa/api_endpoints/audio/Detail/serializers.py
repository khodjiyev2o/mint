from rest_framework import serializers

from apps.common.models import PaymentPlan
from apps.preventa.models import Audio, UserContentPaymentPlan
from apps.users.models import User


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "full_name", "photo")


class PaymentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlan
        fields = ("type", "price")


class UserContentPaymentPlanSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="payment_plan.type")

    class Meta:
        model = UserContentPaymentPlan
        fields = ("id", "available_reproductions", "type")


class PreventaAudioDetailSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer()
    is_bought = serializers.SerializerMethodField()
    payment_plans = serializers.SerializerMethodField()
    audio_file = serializers.SerializerMethodField()

    class Meta:
        model = Audio
        fields = ("slug", "title", "cover", "duration_seconds", "creator", "is_bought", "payment_plans", "audio_file")

    def get_is_bought(self, obj):
        user = self.context["request"].user

        if not user.is_authenticated:
            return False

        return obj.is_bought(user)

    def get_audio_file(self, obj):
        request = self.context["request"]
        user = request.user

        if not user.is_authenticated:
            return

        if obj.is_bought(user):
            return obj.file.url

        return

    def get_payment_plans(self, obj):
        user = self.context["request"].user
        payment_plans = obj.payment_plans.all()

        if not user.is_authenticated:
            return PaymentPlanSerializer(payment_plans, many=True).data

        if obj.is_bought(user):
            return UserContentPaymentPlanSerializer(obj.user_payment_plans, many=True).data

        return PaymentPlanSerializer(payment_plans, many=True).data
