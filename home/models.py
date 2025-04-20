from django.db import models



class AboutModel(models.Model):
    description = models.TextField(max_length=400)

    class Meta:
        verbose_name = "Biz haqimizda"
        verbose_name_plural = "Biz haqimizda"
    
    def __str__(self):
        return self.description


class WhyUsModel(models.Model):
    image = models.ImageField(upload_to='whyUs_img')
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=180)

    class Meta:
        verbose_name = "Nima uchun biz"
        verbose_name_plural = "Nima uchun biz"
    
    def __str__(self):
        return self.title
    



class TypeModel(models.Model):
    image = models.ImageField(upload_to='type_image')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=170)
    item = models.JSONField(default=list)

    class Meta:
        verbose_name = "Fizika turi"
        verbose_name_plural = "Fizika turlari"
    
    def __str__(self):
        return self.title



class UserExperienceModel(models.Model):
    image = models.ImageField(upload_to='user_experience_image')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)

    class Meta:
        verbose_name = "Foydalanuvchi tajribasi"
        verbose_name_plural = "Foydalanuvchi tajribasi"
    
    def __str__(self):
        return self.title



class ContactModel(models.Model):
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        verbose_name = "Kontakt va ijtimoiy tarmoq"
        verbose_name_plural = "Kontakt va ijtimoiy tarmoqlar"

    def __str__(self):
        return f"{self.phone} - {self.email}"
    


class SocialMedia(models.Model):
    contact = models.ForeignKey(ContactModel, on_delete=models.CASCADE, related_name='socials')
    name = models.CharField(max_length=50)
    url = models.URLField()
    icon = models.ImageField(upload_to='social_icons' )  

    def __str__(self):
        return self.name
    


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kontakt xabar"
        verbose_name_plural = "Kontact xabarlar"

    def __str__(self):
        return f"{self.name} - {self.phone}"