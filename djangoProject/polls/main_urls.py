from django.conf.urls import url
import views

# from django.conf.urls import url
# from . import views

urlpatterns = [url(r'^polls/', include('polls.urls', namespace="polls")),]