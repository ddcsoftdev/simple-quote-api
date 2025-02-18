from .models import Quote
from rest_framework import serializers

class QuoteSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Quote
        fields = ["id", "context", "author", "created_at"]
        
    #TODO: add some checks to return more info to client
