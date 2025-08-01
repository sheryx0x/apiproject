from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewSet, SubmissionViewSet, RegisterView, ProfileView , StudentSubmissionViewSet , AssignmentListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('assignments', AssignmentViewSet, basename='assignment')
router.register('submissions', SubmissionViewSet, basename='submission')
router.register('student/submissions', StudentSubmissionViewSet, basename='student-submissions')
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('student/assignments/', AssignmentListView.as_view(), name='student-assignments'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
] + router.urls
