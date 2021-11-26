from django.db.models.base import Model
from rest_framework import serializers
from adaptation.models import Adaptation, Faculty,Science

class FacultyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faculty
        fields = "__all__"

class ScienceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Science
        fields = "__all__"
        
class AdaptationCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Adaptation
        exclude = ['created_at', 'updated_at']
 







