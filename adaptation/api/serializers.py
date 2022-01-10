from rest_framework import serializers
from adaptation.models import AdapatationClass, Adaptation, Faculty,Science, StudentClass
from django.forms.models import model_to_dict

class FacultyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faculty
        fields = "__all__"

class ScienceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Science
        fields = "__all__"
   
class AdaptationClassListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdapatationClass
        fields = "__all__"        

class AdaptationCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Adaptation
        exclude = ['created_at', 'updated_at']
    
    @property
    def errors(self):
        # get errors
        errors = super().errors
        verbose_errors = {}

        # fields = { field.name: field.verbose_name } for each field in model
        fields = {field.name: field.verbose_name for field in
                   self.Meta.model._meta.get_fields() if hasattr(field, 'verbose_name')}

        # iterate over errors and replace error key with verbose name if exists
        for field_name, error in errors.items():
            if field_name in fields:
                
                verbose_errors[str(fields[field_name])] = error
            else:
                verbose_errors[field_name] = error
        print(verbose_errors)
        return verbose_errors
    
    def validate(self, data):
        data = super().validate(data)
        
        adaptation_year = data.get('adaptation_year')        
        adaptation_semester = data.get('adaptation_semester')    
        if (adaptation_semester != adaptation_year * 2) and (adaptation_semester != ((adaptation_year * 2) - 1) ):
            raise serializers.ValidationError({"adaptation_semester": ("İntibak yarıyılı hatalı seçilmiş, lütfen intibak yılı ve yarıyılı tekrar gözden geçirin.")})
        return data

class StudentClassCreateSerializer(serializers.ModelSerializer):

    adaptation_class = serializers.PrimaryKeyRelatedField(queryset=AdapatationClass.objects.all())
    adaptation_class_data = serializers.SerializerMethodField()

    class Meta:
        model = StudentClass
        exclude = ['created_at','updated_at']
        depth = 1

    def get_adaptation_class_data(self, obj):
        return model_to_dict(obj.adaptation_class)

    def validate(self, data):   
        print(data)           
        validated_data = super().validate(data)
        return validated_data
        
    def create(self, validated_data):
        data = super().create(validated_data)    
        return data
        
 
class StudentClassListserializer(serializers.ModelSerializer):
    
    adaptation_class = AdaptationClassListSerializer(read_only=True)
    
    class Meta:
        model=StudentClass
        exclude = ['created_at', 'updated_at']









