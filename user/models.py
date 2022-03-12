from django.db import models
from django.contrib.auth.models import User
from django.db import transaction

from user.utils import resize_image
# Create your models here.

class Profile(models.Model):
    """
    This model represents the profile info of Internal Personals.
    """
    normal_education = 'n.ö'
    secondary_education = 'i.ö'
    student = "student"
    commission_member = "commission_member"
    commission_lead = "commission_lead"
    admin = "admin"
    
    EDUCATION_TIME_CHOICES = ((normal_education, ('Normal Öğretim')), (secondary_education, ('İkinci Öğretim')))
    USER_ROLE_CHOICES = ((student, ('Öğrenci')), (commission_member, ('İntibak Komisyonu Üyesi')), (commission_lead, ('İntibak Komisyonu Lideri')),(admin,("Yönetici")))
       
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_image = models.ImageField(("Profil Resmi"), upload_to='images/profiles/', null=True, blank=True,
                              help_text=("Lütfen kare profil resminizi kare olacak şekilde yükleyin, yoksa fotoğrafınız kırpılacaktır."))
    namesurname = models.CharField(("Ad Soyad"), max_length=200, default="")
    phone_number = models.CharField(("Telefon Numarası"), max_length=50, blank=False, null=True)
    address = models.TextField(("Adres"), blank=True, null=True)
    user_role = models.CharField(("Kullanıcı Rolü"), max_length=17, choices=USER_ROLE_CHOICES, default=student)
    student_number = models.CharField(("Okul Numarası"), max_length=9, blank=True, null=True)
    identification_number = models.CharField(("TC Kimlik No"), max_length=11, blank=True, null=True)
    education_time = models.CharField(("Öğretim"), max_length=4, choices=EDUCATION_TIME_CHOICES, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    __image=None

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profiller'

    def __init_(self, *args, **kwargs):
        super().__init_(*args, **kwargs)
        self.__image = self.user_image

    def __str__(self):
        model_text = f"{self.namesurname} | {self.user.username}"
        if self.is_allowed_user():
            model_text = f"{model_text} {self.get_user_role_display()}"
        return model_text

    def save(self, *args, **kwargs):
        """
        Crop image before sending to Amazon, thanks to:
        https://blog.soards.me/posts/resize-image-on-save-in-django-before-sending-to-amazon-s3/
        https://bhch.github.io/posts/2018/12/django-how-to-editmanipulate-uploaded-images-on-the-fly-before-saving/
        """
        # check if the image field is changed
        if self.user_image and self.user_image != self.__image:
            self.user_image = resize_image(self.user_image, 512, 512)

        with transaction.atomic():

            if self.is_allowed_user():
                self.user.is_staff = True
                self.user.is_admin = True
                self.user.is_superuser = True
                self.user.save()

            super().save(*args, **kwargs)

    @staticmethod
    def get_read_only_fields():
        return ['student_number','birthday']

    def is_allowed_user(self):
        allowed_user_roles = (Profile.admin, Profile.commission_member, Profile.commission_lead)
        is_allowed_user = self.user_role in allowed_user_roles
        return is_allowed_user

    def is_allowed_simple(self):
        allowed_simple_roles = (Profile.admin, Profile.student)
        is_allowed_simple = self.user_role in allowed_simple_roles
        return is_allowed_simple
