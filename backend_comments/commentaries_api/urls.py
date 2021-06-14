from django.urls import path
from .views import AnswerListApiView, CommentModelViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'comments/list', CommentModelViewSet)

urlpatterns = [
    path('answers/list/', AnswerListApiView.as_view())
]


urlpatterns += router.urls
