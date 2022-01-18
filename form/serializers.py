from rest_framework import serializers
from .models import Lead

# Create your serializers here:

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        # fields = ['fname', 'lname', 'email', 'phone', 'course']
        fields = '__all__'

class LeadSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'