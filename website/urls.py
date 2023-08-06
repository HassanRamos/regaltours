from django.urls import path,re_path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name="Home"),
    path('<path>', Index.as_view(), name="index"),
    path('v1/<product>/search', SearchDestinationAPIView.as_view(), name="destination search"),
    path('v1/tasks', Background_tasks.as_view(), name="Background_tasks")

]

