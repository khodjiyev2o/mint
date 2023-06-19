from rest_framework import serializers

from apps.preventa.models import UserContentPaymentPlan


class FourReproductionPlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContentPaymentPlan
        fields = ("content", "payment_plan")

    def update(self, instance, validated_data):
        instance.available_reproductions -= 1
        instance.save()
        return instance
