from django.urls import path, re_path

from apps.rwandaApp import views

urlpatterns = [
    path('lab-orders', views.LabView.as_view(), name='lab-orders'),
    path('lab-orders-uuid-generator', views.LabUUIDView.as_view(), name='lab-orders-uuid'),
    path('lab-orders-source-id', views.LabOrderSourceIdView.as_view(), name='lab-orders-source-id'),
    path('lab-results', views.LabResult.as_view(), name='lab-results'),
    path('get-lab-results', views.GetLabResults.as_view(), name='get-lab-results'),

]
