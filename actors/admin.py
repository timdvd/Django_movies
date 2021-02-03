from django.contrib import admin
from .models import Actor
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

class ActorAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Actor
        fields = '__all__'

class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image', 'active')
    readonly_fields = ('get_image',)
    form = ActorAdminForm

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Image'

admin.site.register(Actor, ActorAdmin)
