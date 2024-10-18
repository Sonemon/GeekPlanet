from django import forms

from geekplanet.models import User, Anime, Review


class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=False
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name",
            "bio", "profile_picture", "password1", "password2"
        )
        widgets = {
            "bio": forms.Textarea(attrs={
                "rows": 5,
                "cols": 50,
                "placeholder": "Write something about yourself...",
                "class": "form-control",
            }),
            "profile_picture": forms.ClearableFileInput(attrs={
                "class": "form-control-file",
                "accept": "image/*",
            }),
        }

    def __init__(self, *args, **kwargs):
        self.is_update = kwargs.pop("is_update", False)
        super().__init__(*args, **kwargs)

        if self.is_update:
            self.fields.pop("username")
            self.fields.pop("email")
            self.fields["password1"].required = False
            self.fields["password2"].required = False
        else:
            self.fields["password1"].required = True
            self.fields["password2"].required = True

    def clean_password2(self):
        if not self.is_update:
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data.get("password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        if not self.is_update:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AnimeForm(forms.ModelForm):
    class Meta:
        model = Anime
        fields = "__all__"
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["content", "rating", "character"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "rating": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 10}),
            "character": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "content": "Review:",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rating"].initial = 1
