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