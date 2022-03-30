from django.contrib.auth import forms as auth_forms, get_user_model
from final_project.accounts.helpers import BootstrapFormMixin
from final_project.accounts.models import Profile
from django import forms

UserModel = get_user_model()


class UserRegistrationForm(BootstrapFormMixin, auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
    )
    picture = forms.URLField()
    date_of_birth = forms.DateField()
    gender = forms.ChoiceField(
        choices=Profile.GENDERS,
    )

    account_balance = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = UserModel
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            picture=self.cleaned_data['picture'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            gender=self.cleaned_data['gender'],
            account_balance=self.cleaned_data['account_balance'],
            user=user,
        )

        if commit:
            profile.save()
        return user
