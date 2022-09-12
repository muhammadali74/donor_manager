from django.urls import path, register_converter
from . import views

from main.utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    #     path('', views.index, name='index'),
    #     path('login', views.login, name='login'),
    #     path('logout', views.logout, name='logout'),
    #     path('delete/<int:id_>', views.delete_instance, name='delete'),
    #     path('duplicate/<str:date>/<int:fyear>/<str:type>/<str:amount>/<int:cheque>/<str:namenew>/<str:name>/<str:onaccof>/<str:country>/<str:remarks>/<str:email>/<int:phone>',
    #          views.duplicate, name='duplicate'),
    #     path('export', views.export_csv, name='export'),
    #     path('upload', views.pdf_extractor, name='upload'),
    #     path('receipt/<hashid:pk>/<str:date>/<str:amount>',  # changed <int:id> to hashid:pk here and in url from index.html likewise
    #          views.receipt, name='receipt'),
    #     # changed <int:id> to hashid:pk here and in url from index.html likewise
    #     path('records/<hashid:pk>/', views.records, name='record'),
]
