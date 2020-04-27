from django.urls import path,include
from .views import bookshome,createrelated,topicdetail,searchview


urlpatterns = [
    path('', bookshome),
    path('topic/<slug>', topicdetail,name="topicdetail"),
    path('related/', createrelated),
    path('search/', searchview),

]

