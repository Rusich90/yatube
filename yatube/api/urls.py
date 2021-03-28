from rest_framework.routers import DefaultRouter
from .views import PostViewSet, api_comments, api_comments_edit
from django.urls import path, include
from rest_framework.authtoken import views

router = DefaultRouter()
router.register('v1/posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('v1/posts/<int:pk>/comments/', api_comments),
    path('v1/posts/<int:pk>/comments/<int:cpk>/', api_comments_edit),
]

urlpatterns += [
    path('token-auth/', views.obtain_auth_token)
]