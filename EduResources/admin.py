from django.contrib import admin
from django.utils.html import format_html
from .models import Classes, Lessons, Test, TestResult, TestStatistic

class TestInline(admin.TabularInline):
    model = Test
    extra = 1

@admin.register(TestStatistic)  
class TestStatisticsAdmin(admin.ModelAdmin):  
    list_display = ('user', 'lesson', 'total_tests', 'correct_answers', 'percentage')
    list_filter = ('user', 'lesson')

@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'classes')
    list_filter = ('classes',)
    search_fields = ('lesson',)
    


 
    
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('short_question', 'resource_link', 'correct_option_display')
    list_filter = ('resource__classes',)  # resource orqali classes'ga murojaat qilish
    search_fields = ('question', 'resource__title')
    list_per_page = 20

    def short_question(self, obj):
        return obj.question[:50] + "..." if len(obj.question) > 50 else obj.question
    short_question.short_description = "Savol"

    def resource_link(self, obj):
        if obj.resource:
            return format_html(
                '<a href="?resource__id__exact={}">{}</a>',
                obj.resource.id,
                obj.resource.title
            )
        return "❌ Resurs yo‘q"
    resource_link.short_description = "Mavzu (Darslik)"
    resource_link.allow_tags = True

    def correct_option_display(self, obj):
        return format_html('<span style="color: green;">Variant {}</span>', obj.correct_option)
    correct_option_display.short_description = "To'g'ri javob"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('resource')  # Lessons bilan bog'lanish


# Classes Admin
@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ('name', 'lesson_count')
    search_fields = ('name',)
    
    def lesson_count(self, obj):
        return obj.lessons.count()
    lesson_count.short_description = "Darslar soni"

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test_info', 'selected_option_display', 'is_correct_display', 'created_at')
    list_filter = ('is_correct', 'test__resource__classes', 'test__resource__title')  # test orqali classes'ga murojaat qilish
    search_fields = ('user__username', 'test__question', 'test__resource__title')
    readonly_fields = ('created_at',)

    def test_info(self, obj):
        resource_title = getattr(obj.test.resource, 'title', '❌ Resurs yo‘q')
        return f"{resource_title} - {obj.test.question[:30]}..."
    test_info.short_description = "Test ma'lumoti"

    def selected_option_display(self, obj):
        return f"Variant {obj.selected_option}"
    selected_option_display.short_description = "Tanlangan javob"

    def is_correct_display(self, obj):
        return format_html(
            '<span style="color: {}">{}</span>',
            'green' if obj.is_correct else 'red',
            "✅ To'g'ri" if obj.is_correct else "❌ Noto'g'ri"
        )
    is_correct_display.short_description = "Natija"