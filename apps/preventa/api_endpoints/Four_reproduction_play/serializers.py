from rest_framework import serializers

from apps.preventa.models import PaymentType, UserContentPaymentPlan


class FourReproductionPlaySerializer(serializers.ModelSerializer):
    is_bought = serializers.SerializerMethodField()

    class Meta:
        model = UserContentPaymentPlan
        fields = ("available_reproductions", "payment_plan", "is_bought")
        extra_kwargs = {"available_reproductions": {"read_only": True}, "payment_plan": {"read_only": True}}

    def update(self, instance, validated_data):
        if instance.available_reproductions > 0:
            instance.available_reproductions -= 1
        instance.save()
        return instance

    def get_is_bought(self, obj):
        return obj.payment_plan == PaymentType.FOUR_TIME and not obj.available_reproductions <= 0
