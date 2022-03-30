"""
FINAL PROJECT

STEP 1)

    CREATE new app 'accounts'
    INCLUDE IT IN 'settings.py'
    MOVE IT INTO THE MAIN PROJECT FOLDER
    MAKE 'urls.py' file and do the -> urlpatterns = () + include in main urls

STEP 2)
    CREATE AND CONNECT DATA_BASE

STEP 3)
    FIX THE STATIC/MEDIAS DIRECTORIES -> COPY FROM PREVIOUS FILES

STEP 4)
    START MAKING THE REGISTER/LOGIN/LOGOUT VIEWS
    ! IMPORTANT TO START ASAP BECAUSE YOU WILL BE DELETING THE USER TABLE IN THE DATA_BASE

    - CREATE REGISTER VIEW + HTML
    class UserRegistrationView(views.CreateView):
        form_class = auth_form.UserCreationForm
        template_name = 'auth_accounts/register.html'
        success_url = 'index.html'

    ^^^ this is the most basic view for registration you can use
    YOU CAN MIGRATE DIRECTLY IF THIS IS ENOUGH, IF NOT CONTINUE TO MAKE IT CUSTOM

    MEANWHILE YOU CAN CREATE A HOMEVIEW TO VISUALISE WHATEVER
    CRTL + / TO COMMENT THE AUTH_PASSWORD_VALIDATORS in 'settings.py' SO YOU CAN WORK WITH EASIER PASSWORDS

    TO CUSTOMISE:
    IMPORT UserModel = get_user_model()
    CREATE: class UserRegistrationForm(auth_form.UserCreationForm):
                class Meta:
                model = UserModel
                fields = ('username',)
            ^^^ now customise this form

    and your REGISTER VIEW changes to this:

    class UserRegistrationView(views.CreateView):
        form_class = -> UserRegistrationForm <- THE DIFF IS HERE
        template_name = 'auth_accounts/register.html'
        success_url = reverse_lazy('index')

STEP 5)
    LOGIN AND LOGOUT VIEWS
        CREATE: class UserLoginView(auth_views.LoginView):
                    template_name = 'auth_accounts/login.html'

                    def get_success_url(self):
                        return reverse_lazy('index')

                ^^^ to login + html hrefs/urls/etc...

        CREATE: class UserLogoutView(auth_views.LogoutView):
                    def get_next_page(self):
                        return reverse_lazy('index')

                ^^^ to logout + html hrefs/urls/etc...

    ^^^ this is the most basic register/login/logout structure

    STEP 5.1) MAKE CUSTOM USER AND AUTO LOGIN AFTER REGISTER

    > > > AUTO LOGIN:
        def form_valid(self, *args, **kwargs):
            result = super().form_valid(*args, **kwargs)
            # user => self.object
            # request => self.request
            login(self.request, self.object)
            return result

        ^^^ ADD TO REGISTER VIEW

    > > > EXTENDING THE USER MODEL

    CREATE:

    1)    class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
                pass <- add all the fields like email/is_staff/date_joined... essentials for login
                DO NOT INCLUDE FIRST/LAST NAME/IMAGE/ ETC
                custom user model MUST have objects = Custom Manager as shown
                check out 'accounts/managers' for Custom Manager
                check out 'accounts/models line 9 - 26 for Custom User


    2)    AUTH_USER_MODEL = 'accounts.AppUser'

    3) DROP ALL TABLES AND MIGRATE ANEW

    YOU NOW HAVE A CUSTOM USER MODEL

    NOTE: THIS APP USES LOGIN WITH EMAIL

    4) CHECK 'accounts.forms' line 10-45 for FORM for first/last name/etc abe kato se
    registrirash da populvash first/late name i tn ima i BootStrapMixin

    BRUH GO CHECK GROUPS IN DJANGO FOR DIFF PERMISSIONS
"""