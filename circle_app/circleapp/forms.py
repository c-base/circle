from django import forms
from django.contrib.auth import authenticate

from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from simplemathcaptcha.fields import MathCaptchaField

from circleapp.models import *


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    user_cache = None

    def clean(self):
        self.user_cache = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if self.user_cache is None:
            raise forms.ValidationError('No such username/password exists.')
        elif not self.user_cache.is_active:
            raise forms.ValidationError('This account has been blocked.')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

class MemberForm(forms.Form):
    #class Meta:
      #fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        #self.helper.form_class = 'blueForms'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.form_read_only = True
        self.helper.form_id = 'id-itemform'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    username = forms.CharField(max_length=255)
    captcha = MathCaptchaField()

class AlienTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('headline', 'summary')

      #fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AlienTopicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        #self.helper.form_class = 'blueForms'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.form_read_only = True
        self.helper.form_id = 'id-topicform'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Abschicken'))

    headline = forms.CharField(max_length=255)
    summary = forms.CharField(widget=forms.Textarea)
    email = forms.CharField(max_length=255)
    captcha = MathCaptchaField()

class MemberTopicForm(forms.Form):
    #class Meta:
      #fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MemberTopicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        #self.helper.form_class = 'blueForms'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.form_read_only = True
        self.helper.form_id = 'id-topicform'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Abschicken'))

    headline = forms.CharField(max_length=255)
    summary = forms.CharField(widget=forms.Textarea)

