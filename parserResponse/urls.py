from django.urls import path
from .views import MainView


urlpatterns = [
	path('', MainView.as_view()),
	path('accept-ajax/', MainView.as_view())
]