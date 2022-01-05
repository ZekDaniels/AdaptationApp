from rest_framework import serializers
from adaptation.models import AdapatationClass, Adaptation, Faculty,Science, StudentClass

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

class AdaptationClassListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdapatationClass
        fields = "__all__" 

class StudentClassCreateSerializer(serializers.ModelSerializer):

    adaptation_class = AdaptationClassListSerializer(read_only=True)
    class Meta:
        model = StudentClass
        exclude = ['created_at','updated_at']
        
 







