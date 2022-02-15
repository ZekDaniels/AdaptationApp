from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max

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
    NYG = 'nyg'
    EYG = 'eyg'
    YO = 'yo'
    MT = 'mt'
    
    REASON_CHOCIES = (
        (DG, ("Dikey Geçiş")),
        (NYG, ("Notla Yatay Geçiş")),
        (EYG, ("Ek Madde 1 Yatay Geçiş")),
        (YO, ("Yaz Okulu")),
        (MT, ("Mühendislik Tamamlama")),
    )
    SEMESETER_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8"), )
    YEAR_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), )
    university = models.ForeignKey(University, on_delete=models.DO_NOTHING, verbose_name="Üniversite")    
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING, verbose_name="Fakülte")
    science = models.ForeignKey(Science, on_delete=models.DO_NOTHING, verbose_name="Bölüm")
    reason_for_coming = models.CharField("Geliş Nedeni", max_length=3, choices=REASON_CHOCIES)
    adaptation_year = models.IntegerField("İntibak Sınıfı", choices=YEAR_CHOICES, default=1)
    adaptation_semester = models.IntegerField("İntibak Yarıyılı", choices=SEMESETER_CHOICES, default=1)
    decision_date = models.DateField("Karar Tarihi", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=("adaptation"), verbose_name="Öğrenci", unique=True, null=True, blank=False)      
      
    is_closed =  models.BooleanField(("Kapalı mı?"), default=False)
    result_note = models.TextField("Sonuç Bilgisi", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.user.profile.namesurname} {self.user.username}"

    def get_username(self):
        return self.user.username

    def get_name_surname(self):
        return self.user.profile.namesurname

    def get_is_confirmated_all(self):
        if self.student_classes.exists():
            for student_class in self.student_classes.all():
                if not student_class.get_confirmation():
                    return False
            return True 
        else:    
            return False  
            
    def get_adaptation_class_list(self):

        adaptation_class_list = []
        for student_class in self.student_classes.all():
            if not student_class.adaptation_class in adaptation_class_list:
                adaptation_class_list.append(student_class.adaptation_class)
        return adaptation_class_list 

    def get_adaptation_class_list_akts_sum(self):

        sum = 0
        for adaptation_class in self.get_adaptation_class_list():
            sum += adaptation_class.akts

        return sum
       

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

    def get_own_student_classes(self, adaptation):
        return self.student_classes.filter(adaptation=adaptation)

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
    )
    class Meta:
        verbose_name = 'Öğrenicin Dersi'
        verbose_name_plural = 'Öğrencinin Dersleri'
        unique_together = (("code"), ("adaptation_class") )
        ordering = ['adaptation_class', 'semester', 'code']

        
        
    code = models.CharField("Ders Kodu", max_length=20)
    class_name = models.CharField("Dersin Adı", max_length=255)
    semester = models.PositiveIntegerField("Dönem", choices= SEMESETER_CHOICES, default=1)
   
    teorical = models.PositiveIntegerField("Teorik", default = 0)
    practical = models.PositiveIntegerField("Pratik", default = 0)
    credit = models.FloatField("Kredi", null=True, blank=True)
    akts = models.PositiveIntegerField("AKTS", null=True, blank=True)
    grade = models.FloatField("Not", choices=GRADE_CHOICES, default=2.0)
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

    def get_confirmation(self):
        if self.adaptation_class.confirmation.exists():
            if self.adaptation_class.confirmation.filter(adaptation=self.adaptation).first() is not None:
                return {"exists":True, "id": self.adaptation_class.confirmation.filter(adaptation=self.adaptation).first().id}
            else:
                return False
        else:
            return False

class AdaptationClassConfirmation(models.Model):

    adaptation_class = models.ForeignKey(AdapatationClass, on_delete=models.CASCADE, related_name=("confirmation"), verbose_name="İntibak Dersi")      
    adaptation = models.ForeignKey(Adaptation, on_delete=models.CASCADE, related_name=("confirmations"), verbose_name="İntibak")      

    class Meta:
        verbose_name = 'İntibak Dersi Onayı'
        verbose_name_plural = 'İntibak Dersi Onayları'
        unique_together = (("adaptation"), ("adaptation_class") )

    def __str__(self):
        return f"{self.adaptation_class} {self.adaptation.user.profile}"