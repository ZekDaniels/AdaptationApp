from django.db import models

# Create your models here.

# class Adaptation(models.Model):
#     REASON_CHOCIES = (
#         ('dg',("Dikey Geçiş")),
#         ('yg',("Yatay Geçiş")),
#         ('yo',("Yaz Okulu")),
#         ('mt',("Mühendislik Tamamlama")),
#         )
    
#     reason_for_coming = models.CharField(("Geliş Nedeni"),max_length=2, choices=REASON_CHOCIES)


class University(models.Model):
    
    name = models.CharField("Üniversite", max_length=255)

    def __str__(self):
        return self.name
    
    
class Faculty(models.Model):
    """
    Stores the city info
    """
    university = models.ForeignKey(University, on_delete=models.SET_NULL, blank=True, null=True, related_name="faculties")
    name = models.CharField("Fakülte", max_length=255, null=True, blank=True)

    

