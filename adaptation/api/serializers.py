from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from adaptation.models import AdapatationClass, Adaptation, Faculty,Science, StudentClass
from django.forms.models import model_to_dict
import numbers, decimal


class ErrorNameMixin(serializers.Serializer):
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
    
class FacultyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faculty
        fields = "__all__"

class ScienceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Science
        fields = "__all__"

class AdaptationCreateSerializer(serializers.ModelSerializer, ErrorNameMixin):
    
    class Meta:
        model = Adaptation
        exclude = ['created_at', 'updated_at']
    
    def validate(self, data):
        validated_data = super().validate(data)

        if self.instance:
            if self.instance.is_closed:
                raise serializers.ValidationError(("Bu intibak başvurusu kapatılmış, değiştirmek istediğinize eminseniz tekrar hocanıza başvurun."))       

            request_owner = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                request_owner = request.user

            if self.instance.user != request_owner:
                raise serializers.ValidationError(("Bu kullanıcının intibak başvurusunu değiştiremezsiniz."))

    

        adaptation_year = validated_data.get('adaptation_year', 0)        
        adaptation_semester = validated_data.get('adaptation_semester', 0)    
        if (adaptation_semester != adaptation_year * 2) and (adaptation_semester != ((adaptation_year * 2) - 1) ):
            raise serializers.ValidationError({"adaptation_semester": ("İntibak yarıyılı hatalı seçilmiş, lütfen intibak yılı ve yarıyılı tekrar gözden geçirin.")})
        return validated_data

class AdaptationClassListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdapatationClass
        fields = "__all__"        

class StudentClassListSerializer(serializers.ModelSerializer):
    
    adaptation_class = AdaptationClassListSerializer(read_only=True)
    max_grade = SerializerMethodField(source='get_max_grade', read_only=True)
    sum = SerializerMethodField(source='get_sum', read_only=True)
    adaptation_class_sum = SerializerMethodField(source='get_adaptation_class_sum', read_only=True)

    def get_max_grade(self, obj):
        return obj.get_max_grade()

    def get_sum(self, obj):
        return obj.get_sum()

    def get_adaptation_class_sum(self, obj):
        return obj.get_adaptation_class_sum()

    class Meta:
        model=StudentClass
        exclude = ['created_at', 'updated_at']

class StudentClassCreateSerializer(serializers.ModelSerializer, ErrorNameMixin):
    adaptation = serializers.PrimaryKeyRelatedField(queryset=Adaptation.objects.all())
    adaptation_class = serializers.PrimaryKeyRelatedField(queryset=AdapatationClass.objects.all())
    adaptation_class_data = serializers.SerializerMethodField()

    credit = serializers.CharField(default=None, required=False, allow_blank=True, allow_null=True,)
    akts = serializers.CharField(default=None, required=False, allow_blank=True, allow_null=True,)

    class Meta:
        model = StudentClass
        exclude = ['created_at','updated_at']
        depth = 1

    def get_adaptation_class_data(self, obj):
        return model_to_dict(obj.adaptation_class)

    def validate(self, data): 
         
        credit = data.get('credit')        
        akts = data.get('akts')    
        
        validated_data = super().validate(data)

        adaptation = validated_data.get('adaptation', None)
        if adaptation.is_closed:
            raise serializers.ValidationError(("Bu intibak başvurusu kapatılmış, değiştirmek istediğinize eminseniz tekrar hocanıza başvurun."))

        request_owner = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            request_owner = request.user
            
        if adaptation.user != request_owner:
            raise serializers.ValidationError(("Bu kullanıcının intibak başvurusunu değiştiremezsiniz."))


        try:
            validated_data['credit'] = float(credit)
        except:
            validated_data['credit'] = None
        try:
            validated_data['akts'] = int(akts)
        except:
            validated_data['akts'] = None
        
        # if validated_data['credit'] is not None and not akts.isdigit():
        #     raise serializers.ValidationError({"akts": ("Bu alan tamsayı olmalı")})
        # if validated_data['akts'] is not None and not credit.replace(".", "", 1).isdigit():
        #     raise serializers.ValidationError({"credit": ("Bu alan tamsayı veya virgüllü sayı olmalı.")}) 

        if validated_data['credit'] is None and validated_data['akts'] is None:
            raise serializers.ValidationError(("Kredi tamsayı veya virgüllü sayı olmalı, AKTS tam sayı olmalı. Her iki değerden birisi mutlaka girilmeli.")) 

        if validated_data['credit'] is not None and validated_data['credit']  < 1:
            raise serializers.ValidationError({"credit": ("Bu alan 1 veya 1'den büyük olmalı.")}) 

        if validated_data['akts'] is not None and validated_data['akts'] < 1:
            raise serializers.ValidationError({"akts": ("Bu alan 1 veya 1'den büyük olmalı.")}) 

        return validated_data
        
    def create(self, validated_data):
        data = super().create(validated_data) 
        return data
        


