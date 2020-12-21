from django import forms

class LoginForm(forms.Form):
    username = forms.EmailField(
        max_length=150,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username and not password:
            raise forms.ValidationError('You have to insert your username and password!')


class CVForm(forms.Form):
    POSITION_CHOICE = (
        ('Backend', 'Backend'),
        ('Frontend', 'Frontend')
    )

    name = forms.CharField(max_length=256, required=True)
    email = forms.EmailField(max_length=256, required=True)
    phone = forms.CharField(max_length=14, required=True)
    full_address = forms.CharField(max_length=512)
    name_of_university = forms.CharField(max_length=512, required=True)
    graduation_year = forms.IntegerField(max_value=2020, min_value=2015, required=True)
    cgpa = forms.FloatField(max_value=4.0, min_value=2.0)
    experience_in_months = forms.IntegerField(max_value=100, min_value=0)
    current_work_place_name = forms.CharField(max_length=256)
    applying_in = forms.ChoiceField(choices=POSITION_CHOICE)
    expected_salary = forms.IntegerField(max_value=60000, min_value=15000, required=True)
    field_buzz_reference = forms.CharField(max_length=256, required=True)
    github_project_url = forms.URLField(max_length=512)
    cv_file = forms.FileField()

    def clean(self):
        cleaned_data = super(CVForm, self).clean()