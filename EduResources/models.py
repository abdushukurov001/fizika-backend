from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class Classes(models.Model):
    name = models.CharField(max_length=200)


    class Meta:
        verbose_name = "Sinf"
        verbose_name_plural = "Sinflar"

    def __str__(self):
        return self.name




class Lessons(models.Model):
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='lessons')
    lesson = models.CharField(max_length=300, verbose_name="Mavzu nomi")
    title = models.CharField(max_length=200)
    description = models.TextField()
    videoUrl = models.URLField()

    class Meta:
        verbose_name = "Mavzu"
        verbose_name_plural = "Mavzular"

    def __str__(self):
        return self.lesson
    

    


class Test(models.Model):
    resource = models.ForeignKey(Lessons, on_delete=models.CASCADE,  related_name='tests')
    question = models.TextField()
    option1 = models.CharField(max_length=300, verbose_name="Variant 1")
    option2 = models.CharField(max_length=300, verbose_name="Variant 2")
    option3 = models.CharField(max_length=300, verbose_name="Variant 3")
    option4 = models.CharField(max_length=300, verbose_name="Variant 4")
    correct_option = models.PositiveSmallIntegerField(
        choices=[(1, 'Variant 1'), (2, 'Variant 2'), (3, 'Variant 3'),(4, 'Variant 4')],
        verbose_name="To'g'ri variant"
    )


    class Meta:
        verbose_name = "Test savoli"
        verbose_name_plural = "Test savollari"

    def __str__(self):
        return f"{self.resource.title} - Savol #{self.question}"
    




class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  verbose_name="Foydalanuvchi")
    test = models.ForeignKey(Test, on_delete=models.CASCADE,  verbose_name="Test")
    selected_option = models.PositiveSmallIntegerField(
        choices=[(1, 'Variant 1'), (2, 'Variant 2'), (3, 'Variant 3'), (4, 'Variant 4')],
        verbose_name="Tanlangan variant"
    )
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javob")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Vaqti")
    

    class Meta:
        verbose_name = "Test natijasi"
        verbose_name_plural = "Test natijalari"
        unique_together = ['user', 'test']  

   
    def save(self, *args, **kwargs):
        self.is_correct = (self.selected_option == self.test.correct_option)
        super().save(*args, **kwargs)
        self.update_statistics()

    def update_statistics(self):
        """ Foydalanuvchining mavzu bo‘yicha statistikani yangilaydi """
        lesson = self.test.resource  # Test qaysi mavzuga tegishli ekanligini olamiz
        user = self.user

        statistic, created = TestStatistic.objects.get_or_create(user=user, lesson=lesson)

        # Jami testlar sonini yangilaymiz
        statistic.total_tests = Test.objects.filter(resource=lesson).count()

        # To'g'ri javoblar sonini yangilaymiz
        statistic.correct_answers = TestResult.objects.filter(
            user=user, test__resource=lesson, is_correct=True
        ).count()

        # Foizni hisoblaymiz
        statistic.update_percentage()















class TestStatistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, verbose_name="Mavzu")
    total_tests = models.PositiveIntegerField(default=0, verbose_name="Jami testlar")
    correct_answers = models.PositiveIntegerField(default=0, verbose_name="To'g'ri javoblar")
    percentage = models.FloatField(default=0, verbose_name="Test foizi")

    class Meta:
        unique_together = ['user', 'lesson']

    def update_percentage(self):
        """ Test natijalariga asoslangan holda foizni yangilaydi """
        if self.total_tests > 0:
            self.percentage = (self.correct_answers / self.total_tests) * 100
        else:
            self.percentage = 0
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} - {self.percentage:.2f} %"







