from rest_framework import serializers

from apps.preventa.models import UserContentPaymentPlan


class FourReproductionPlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContentPaymentPlan
        fields = ("available_reproductions", "payment_plan")
        extra_kwargs = {"available_reproductions": {"read_only": True}, "payment_plan": {"read_only": True}}

    def update(self, instance, validated_data):
        instance.available_reproductions -= 1
        instance.save()
        return instance
