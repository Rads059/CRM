from django.urls import path, include
from .views import  AgentView, LeadView



urlpatterns = [
    path('form/unclaimed', LeadView.as_view(), name='unclaimed_leads'),
    path('form/<int:id>/claim', AgentView.as_view(), name='claim_lead')
]