from django.contrib import admin
from .models import Movie, MovieShots, Review, RatingStar, Rating, Genre, Category
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'

class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    list_display = ('title')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="150" height="150"')

    get_image.short_description = 'Image'

class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'slug', 'year', 'draft')
    list_filter = ('category', 'year', 'genre')
    search_fields = ('title', 'category__name', 'genre__name')
    readonly_fields = ('get_image',)
    inlines = [MovieShotsInline, ReviewInline]
    form = MovieAdminForm
    save_on_top = True
    save_as = True
    list_editable = ('draft', )
    fieldsets = (
        (None, {
            'fields': (( 'title', 'tagline' ),)
        }),
        (None, {
            'fields': (('description', 'poster', 'get_image'),)
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'),)
        }),
        ('Actors', {
            'fields': (('actors', 'directors', 'genre', 'category'),)
        }),
        (None, {
            'fields': ('budget', 'fees_in_usa', 'fees_in_world')
        }),
        ('Options', {
            'fields': ('slug', 'draft', 'active')
        }),
    )

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 row has been updated'
        else:
            message_bit = f"{row_update} rows have been updated"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 row has been updated'
        else:
            message_bit = f"{row_update} rows have been updated"
        self.message_user(request, f"{message_bit}")

    publish.short_description = 'Publish'
    publish.allowed_permission = ('change',)

    unpublish.short_description = 'Unpublish'
    unpublish.allowed_permission = ('change',)

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.poster.url}" width="200" height="300"')

    get_image.short_description = 'Image'

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'parent', 'movie', 'id')

admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieShots)
admin.site.register(Review, ReviewAdmin)
admin.site.register(RatingStar)
admin.site.register(Rating)