from rest_framework.routers import DefaultRouter
from .views import QuoteViewSet

router = DefaultRouter()
router.register(r"quote", QuoteViewSet, basename="quote")

urlpatterns = router.urls