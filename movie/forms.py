from django import forms
from .models import Review, RatingStar, Rating
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

class ReviewForm(forms.ModelForm):

    captcha = ReCaptchaField()

    class Meta:
        model = Review
        fields = ('text', 'captcha')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'name': 'text', 'id':"contactcomment"}),
        }

class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=Rating.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ('star',)