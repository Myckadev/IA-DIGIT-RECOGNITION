from django.urls import path
from .views import RecognizeNumber, VerifyPrediction

urlpatterns = [
    path('recognize/', RecognizeNumber.as_view(), name='recognize'),
    path('verify/', VerifyPrediction.as_view(), name='verify'),
]
