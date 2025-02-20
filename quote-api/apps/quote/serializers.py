from .models import Quote
from rest_framework import serializers


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ["id", "content", "author", "created_at"]

    def to_internal_value(self, attrs):
        if self.context["request"].method in ["PUT", "PATCH", "POST"]:
            if "id" in attrs:
                raise serializers.ValidationError({"id": "id field not expected"})
            elif "created_at" in attrs:
                raise serializers.ValidationError(
                    {"created_at": "created_at field not expected"}
                )
        return super().to_internal_value(attrs)
