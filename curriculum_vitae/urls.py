from django.urls import path
from django.views.generic import TemplateView
from curriculum_vitae import views


app_name = 'curriculum_vitae'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('curriculum_vitae_info/', views.CurriculumVitaeInformation.as_view(), name='curriculum_vitae_info'),
    path('curriculum_vitae_submit/', views.CVSubmission.as_view(), name='curriculum_vitae_submit'),
    path('success/', TemplateView.as_view(template_name='curriculum_vitae/success.html'), name='success'),
    path('fail/', TemplateView.as_view(template_name='curriculum_vitae/fail.html'), name='fail'),

]