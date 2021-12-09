from django.db import models
from django.contrib.auth.models import User

STYLES = {
     "else": {
        'class': 'form-control'
    }
}
SEMESETER_CHOICES = (("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), )

class University(models.Model): 
    name = models.CharField("Üniversite", max_length=255)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Üniversite'
        verbose_name_plural = 'Üniversiteler'
    
class Faculty(models.Model):
    name = models.CharField("Fakülte", max_length=255, null=True, blank=True)
    university = models.ForeignKey(University, on_delete=models.SET_NULL, blank=True, null=True, related_name="faculties")

    class Meta:
        verbose_name = 'Fakülte'
        verbose_name_plural = 'Fakülteler'
        
    def __str__(self):
        return self.name

class Science(models.Model):
    name = models.CharField("Bölüm", max_length=255, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, blank=True, null=True, related_name="sciences")
    university = models.ForeignKey(University, on_delete=models.SET_NULL, blank=True, null=True, related_name="sciences")

    class Meta:
        verbose_name = 'Bölüm'
        verbose_name_plural = 'Bölümler'
    
    def __str__(self):
        return self.name

class Adaptation(models.Model):
    
    class Meta:
        verbose_name = 'İntibak'
        verbose_name_plural = 'İntibaklar'
    
    DG = 'dg'
    YG = 'yg'
    YO = 'yo'
    MT = 'mt'
    
    REASON_CHOCIES = (
        (DG, ("Dikey Geçiş")),
        (YG, ("Yatay Geçiş")),
        (YO, ("Yaz Okulu")),
        (MT, ("Mühendislik Tamamlama")),
    )

    YEAR_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), )
    university = models.ForeignKey(University, on_delete=models.DO_NOTHING, verbose_name="Üniversite")    
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING, verbose_name="Fakülte")
    science = models.ForeignKey(Science, on_delete=models.DO_NOTHING, verbose_name="Bölüm")
    reason_for_coming = models.CharField("Geliş Nedeni", max_length=2, choices=REASON_CHOCIES)
    adaptation_year = models.IntegerField("İntibak Sınıfı", choices=YEAR_CHOICES)
    adaptation_semester = models.IntegerField("İntibak Yarıyılı", choices=SEMESETER_CHOICES)
    decision_date = models.DateField("Karar Tarihi", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=("adaptation"), verbose_name="Öğrenci", unique=True, null=True)      
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    
    def __str__(self):
        return f"{self.user.profile.namesurname} {self.user.username}"
    

class AdapatationClass(models.Model):
    """
    The classes added in system,
    """
    class Meta:
        verbose_name = 'İntibak Dersi'
        verbose_name_plural = 'İntibak Dersleri'
    
    code = models.CharField("Kodu", max_length=20)
    class_name = models.CharField("Dersin Adı", max_length=255)
    semester = models.CharField("Semester", max_length=1, choices= SEMESETER_CHOICES)
    credit = models.IntegerField("Credit")
    akts = models.IntegerField("AKTS")
    is_active = models.BooleanField(("Aktif mi?"), default=True)
    
    def __str__(self):
        return self.code+" - "+self.class_name  

class StudentClass(models.Model):
    """
    The classes can take from user(student),
    """
    class Meta:
        verbose_name = 'Öğrenicin Dersi'
        verbose_name_plural = 'Öğrencinin Dersleri'
        
    code = models.CharField("Kodu", max_length=20)
    class_name = models.CharField("Dersin Adı", max_length=255)
    semester = models.CharField("Semester", max_length=1, choices= SEMESETER_CHOICES)
    credit = models.IntegerField("Credit")
    akts = models.IntegerField("AKTS")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=("student_class"), verbose_name="Öğrenci", default=1)      
    adaptation_class = models.ForeignKey(AdapatationClass, on_delete=models.CASCADE, related_name=("student_classes"), verbose_name="İntibak Dersi",default=1)      

    
    def __str__(self):
        return self.code+" - "+self.class_name
