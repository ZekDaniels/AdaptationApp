from django.db import models
from django.contrib.auth.models import User

from user.utils import resize_image
# Create your models here.

class Profile(models.Model):
    """
    This model represents the profile info of Internal Personals.
    """
    normal_education = 'n.ö'
    secondary_education = 'i.ö'
    student = "student"
    teacher = "teacher"
    admin = "admin"
    
    EDUCATION_TIME_CHOICES = ((normal_education, ('Normal Öğretim')), (secondary_education, ('İkinci Öğretim')))
    USER_ROLE_CHOICES = ((student, ('Öğrenci')), (teacher, ('İntibak Komisyonu Üyesi')),(admin,("Yönetici")))
       
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(("Profil Resmi"), upload_to='images/profiles/', null=True, blank=True,
                              help_text=("Lütfen kare profil resminizi kare olacak şekilde yükleyin, yoksa fotoğrafınız kırpılacaktır."))
    namesurname = models.CharField(("Ad Soyad"), max_length=200, default="")
    phone_number = models.CharField(("Telefon Numarası"), max_length=50, blank=False, null=True)
    address = models.TextField(("Adres"), blank=True, null=True)
    user_role = models.CharField(("Kullanıcı Rolü"), max_length=7, choices=USER_ROLE_CHOICES, default=student)
    student_number = models.CharField(("Okul Numarası"), max_length=9, blank=True, null=True)
    education_time = models.CharField(("Öğretim"), max_length=4, choices=EDUCATION_TIME_CHOICES, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profiller'

    def __init_(self, *args, **kwargs):
        super().__init_(*args, **kwargs)
        self.__image = self.image

    def __str__(self):
        return f"{self.namesurname} | {self.user.username}"

    def save(self, *args, **kwargs):
        """
        Crop image before sending to Amazon, thanks to:
        https://blog.soards.me/posts/resize-image-on-save-in-django-before-sending-to-amazon-s3/
        https://bhch.github.io/posts/2018/12/django-how-to-editmanipulate-uploaded-images-on-the-fly-before-saving/
        """
        # check if the image field is changed
        if self.image and self.image != self.__image:
            self.image = resize_image(self.image, 512, 512)
        super().save(*args, **kwargs)

    @staticmethod
    def get_read_only_fields():
        return ['student_number','birthday']