from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.core.validators import MinValueValidator

STYLES = {
     "else": {
        'class': 'form-control'
    }
}

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
    SEMESETER_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8"), )
    YEAR_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), )
    university = models.ForeignKey(University, on_delete=models.DO_NOTHING, verbose_name="Üniversite")    
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING, verbose_name="Fakülte")
    science = models.ForeignKey(Science, on_delete=models.DO_NOTHING, verbose_name="Bölüm")
    reason_for_coming = models.CharField("Geliş Nedeni", max_length=2, choices=REASON_CHOCIES)
    adaptation_year = models.IntegerField("İntibak Sınıfı", choices=YEAR_CHOICES)
    adaptation_semester = models.IntegerField("İntibak Yarıyılı", choices=SEMESETER_CHOICES)
    decision_date = models.DateField("Karar Tarihi", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=("adaptation"), verbose_name="Öğrenci", unique=True, null=True, blank=False)      
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    is_closed =  models.BooleanField(("Kapalı mı?"), default=False)

    
    def __str__(self):
        return f"{self.user.profile.namesurname} {self.user.username}"


    def get_username(self):
        return self.user.username

    def get_name_surname(self):
        return self.user.profile.namesurname

class AdapatationClass(models.Model):
    """
    The classes added in system,
    """
    SEMESETER_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8"), )
    EDUCATION_TIME_CHOICES = (("n.ö", "Normal Öğretim"),("i.ö", "İkinci Öğretim"))
    class Meta:
        verbose_name = 'İntibak Dersi'
        verbose_name_plural = 'İntibak Dersleri'
        ordering = ['semester','class_name', 'code']
    
    code = models.CharField("Ders Kodu", max_length=20, unique=True)
    class_name = models.CharField("Dersin Adı", max_length=255)
    class_name_english = models.CharField("Dersin İngilizce Adı", max_length=255, null=True, blank=True)
    semester = models.IntegerField("Dönem", choices= SEMESETER_CHOICES)
    teorical = models.PositiveIntegerField("Teorik", default = 0)
    practical = models.PositiveIntegerField("Pratik", default = 0)
    credit = models.FloatField("Kredi")
    akts = models.PositiveIntegerField("AKTS")
    education_time = models.CharField("Öğretim", max_length=3, default="n.ö", choices=EDUCATION_TIME_CHOICES)
    is_active = models.BooleanField(("Aktif mi?"), default=True)

    turkish_content = models.TextField("Türkçe İçerik")
    english_content = models.TextField("İngilizce İçerik", null=True, blank=True)
    
    def __str__(self):
        return self.code+" - "+self.class_name+" - "+ self.get_education_time_display()

    def get_sum(self):
        return self.teorical + self.practical

class StudentClass(models.Model):
    """
    The classes can take from user(student),
    """
    SEMESETER_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8"), )

    
    GRADE_CHOICES = (
        (4.0, ("AA")),
        (3.5, ("BA")),
        (3.0, ("BB")),
        (2.5, ("CB")),
        (2.0, ("CC")),
        (1.5, ("DC")),
        (1.0, ("DD")),
        (0.5, ("FD")),
        (0, ("FF")),
    )
    class Meta:
        verbose_name = 'Öğrenicin Dersi'
        verbose_name_plural = 'Öğrencinin Dersleri'
        unique_together = (("code"), ("adaptation_class") )
        
        
    code = models.CharField("Ders Kodu", max_length=20)
    class_name = models.CharField("Dersin Adı", max_length=255)
    semester = models.PositiveIntegerField("Dönem", choices= SEMESETER_CHOICES, default=1)
   
    teorical = models.PositiveIntegerField("Teorik", default = 0)
    practical = models.PositiveIntegerField("Pratik", default = 0)
    credit = models.FloatField("Kredi", null=True, blank=True)
    akts = models.PositiveIntegerField("AKTS", null=True, blank=True)
    grade = models.FloatField("Not", choices=GRADE_CHOICES, default=4.0)
    adaptation = models.ForeignKey(Adaptation, on_delete=models.CASCADE, related_name=("student_classes"), verbose_name="İntibak", null=True, blank=False)      

    turkish_content = models.TextField("Türkçe İçerik")
    english_content = models.TextField("İngilizce İçerik", null=True, blank=True)


    adaptation_class = models.ForeignKey(AdapatationClass, on_delete=models.CASCADE, related_name=("student_classes"), verbose_name="İntibak Dersi")      

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.code+" - "+self.class_name+" --> "+ self.adaptation_class.class_name
    
    
    def get_max_grade(self):
        candidate_classes = StudentClass.objects.filter(adaptation_class=self.adaptation_class)
        candidate_classes.aggregate(Max('grade'))
        max_grade_class = candidate_classes.order_by('-grade').first()
        return max_grade_class.get_grade_display()

    def get_sum(self):
            return self.teorical + self.practical
       

    def get_adaptation_class_sum(self):
        return self.adaptation_class.get_sum()