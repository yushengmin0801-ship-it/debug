from django.urls import path
from gomoku.views import AIMoveView
urlpatterns = [path('api/ai-move/', AIMoveView.as_view())]
