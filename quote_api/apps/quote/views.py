from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Quote
from .serializers import QuoteSerializer

#list, retrieve, create, partial_update, update, destroy, random
class QuoteViewSet(viewsets.ModelViewSet):
    """ViewSet for Quote Model"""
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    filter_backends = [DjangoFilterBackend]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'random']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
        
        
    @action(detail=False, methods=["get"])
    def random(self, request):
        quote = Quote.objects.order_by('?').first()
        serializer = self.get_serializer(quote)
        return Response(serializer.data)
    