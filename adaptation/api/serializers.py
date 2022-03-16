from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from adaptation.models import AdapatationClass, Adaptation, Faculty,Science, StudentClass, AdaptationClassConfirmation, University
from django.forms.models import model_to_dict
from django.db import transaction
from user.api.serializers import UserListSerializer
from user.models import Profile


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

class UniversityListSerializer(serializers.ModelSerializer):

    class Meta:
        model = University
        fields = "__all__"

class FacultyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faculty
        fields = "__all__"

class ScienceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Science
        fields = "__all__"

class AdaptationListSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField(source="get_username")
    name_surname = serializers.SerializerMethodField(source="get_name_surname")
    is_confirmated = serializers.SerializerMethodField(source="get_is_confirmated")
    university = serializers.SerializerMethodField(source="get_university")
    
    def get_username(self, obj):
        return obj.get_username()

    def get_name_surname(self, obj):
        return obj.get_name_surname()

    def get_is_confirmated(self, obj):
        return obj.is_confirmated
        
    def get_university(self, obj):
        return obj.university.name

    class Meta:
        model = Adaptation
        exclude = ["user"]
        
class AdaptationCreateSerializer(serializers.ModelSerializer, ErrorNameMixin):
    
    class Meta:
        model = Adaptation
        exclude = ['decision_date', 'adaptation_year', 'adaptation_semester','created_at','updated_at']
    
    def validate(self, data):
        validated_data = super().validate(data)

        if self.instance:
             
            request_owner = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                request_owner = request.user
            is_closed = validated_data.get('is_closed')

            if not request_owner.profile.is_allowed_user():
                if self.instance.user != request_owner:
                    raise serializers.ValidationError(("Bu kullanıcının intibak başvurusunu değiştiremezsiniz."))

                if self.instance.is_closed:
                    raise serializers.ValidationError(("Bu intibak başvurusu kapatılmış, değiştirmek istediğinize eminseniz tekrar hocanıza başvurun."))       
              
            if is_closed:
                if not self.instance.student_classes.exists():
                    raise serializers.ValidationError(("Başvuruyu onaya göndermek için en az bir ders ekleyin."))

        return validated_data

class AdaptationAdminUpdateSerializer(AdaptationCreateSerializer):

    class Meta:
        model = Adaptation
        exclude = ['created_at','updated_at']

    def validate(self, data):
        validated_data = super().validate(data)

        adaptation_year = validated_data.get('adaptation_year', 0)        
        adaptation_semester = validated_data.get('adaptation_semester', 0)    

        if (adaptation_semester != adaptation_year * 2) and (adaptation_semester != ((adaptation_year * 2) - 1) ):
            raise serializers.ValidationError({"adaptation_semester": ("İntibak yarıyılı hatalı seçilmiş, lütfen intibak yılı ve yarıyılı tekrar gözden geçirin.")})

        return validated_data


class AdaptationClosedUpdateSerializer(serializers.ModelSerializer, ErrorNameMixin):

    adaptation_year = serializers.IntegerField(read_only=True, required=False)
    adaptation_semester = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Adaptation
        fields = ['adaptation_year','adaptation_semester','is_confirmated']


    def validate(self, data):
        validated_data = super().validate(data)
        is_confirmated = validated_data.get('is_confirmated')  

        if is_confirmated:
            if not self.instance.is_closed:
                raise serializers.ValidationError(("Kapalı olmayan başvuruyu onaylayamazsınız."))

            if not self.instance.student_classes.exists():
                raise serializers.ValidationError(("Başvuruyu onaylamak için en az bir ders ekleyin."))

        return validated_data

    def update(self, instance, validated_data):
        array = [1, 2, 3]
        with transaction.atomic():
            updated_instance = super().update(instance, validated_data) 
            if updated_instance.is_confirmated:
                old_year = updated_instance.adaptation_year
                updated_instance.adaptation_year = 1
                updated_instance.adaptation_semester = 1
                sum_of_akts = updated_instance.get_adaptation_class_list_akts_sum()

                for item in array:
                    if sum_of_akts > ((30*item) + 1):
                        updated_instance.adaptation_year = (item + 1)
                        updated_instance.adaptation_semester = (item + updated_instance.adaptation_year)

                if old_year == updated_instance.adaptation_year:       
                    return Adaptation.objects.get(pk=instance.pk)
                else: 
                    updated_instance.save()
            
            return updated_instance


class AdaptationClassConfirmationCreateSerializer(serializers.ModelSerializer, ErrorNameMixin):

    class Meta:
        model = AdaptationClassConfirmation
        fields = "__all__"

class AdaptationClassListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdapatationClass
        fields = "__all__"        

class StudentClassListSerializer(serializers.ModelSerializer):
    
    adaptation_class = AdaptationClassListSerializer(read_only=True)
    max_grade = SerializerMethodField(source='get_max_grade', read_only=True)
    confirmation = SerializerMethodField(source='get_confirmation', read_only=True)

    def get_confirmation(self, obj):
        return obj.adaptation.is_confirmated
    
    def get_max_grade(self, obj):
        return obj.get_max_grade()

    class Meta:
        model = StudentClass
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

        request_owner = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            request_owner = request.user

        if not request_owner.profile.is_allowed_user():

            adaptation = validated_data.get('adaptation', None)
            if adaptation.is_closed:
                raise serializers.ValidationError(("Bu intibak başvurusu kapatılmış, değiştirmek istediğinize eminseniz tekrar hocanıza başvurun."))
       
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
        
        adaptation_class = validated_data.get('adaptation_class')

        if validated_data['credit'] is None and validated_data['akts'] is None:
            raise serializers.ValidationError(("Kredi tamsayı veya virgüllü sayı olmalı, AKTS tam sayı olmalı. Her iki değerden birisi mutlaka girilmeli.")) 

        if validated_data['credit'] is not None and validated_data['credit']  < 1:
            raise serializers.ValidationError({"credit": ("Bu alan 1 veya 1'den büyük olmalı.")}) 
        
        if validated_data['akts'] is not None and validated_data['akts'] < 1:
            raise serializers.ValidationError({"akts": ("Bu alan 1 veya 1'den büyük olmalı.")}) 

        if validated_data['credit'] is None:
            try:
                validated_data['akts'] = int(akts)
            except:
                raise serializers.ValidationError({"akts": ("Lütfen bir tamsayı giriniz.")}) 

        if validated_data['credit'] is None and validated_data['akts'] is not None:
            if validated_data['akts'] < adaptation_class.akts:
                raise serializers.ValidationError(("Seçtiğiniz dersin kredi veya akts alanlarından biri alınan dersin kredi veya akts alanlarından birinden eşit veya büyük olmalı ve AKTS tam sayı olmalı.")) 

        if validated_data['akts'] is None and validated_data['credit'] is not None:
            if validated_data['credit'] < adaptation_class.credit:
                raise serializers.ValidationError(("Seçtiğiniz dersin kredi veya akts alanlarından biri alınan dersin kredi veya akts alanlarından birinden eşit veya büyük olmalı ve AKTS tam sayı olmalı.")) 

        if validated_data['akts'] is not None and validated_data['credit'] is not None:
            if validated_data['credit'] < adaptation_class.credit and validated_data['akts'] < adaptation_class.akts:
                raise serializers.ValidationError(("Seçtiğiniz dersin kredi veya akts alanlarından biri alınan dersin kredi veya akts alanlarından birinden eşit veya büyük olmalı ve AKTS tam sayı olmalı.")) 
           
        return validated_data
        
    def create(self, validated_data):
        data = super().create(validated_data) 
        return data
        

