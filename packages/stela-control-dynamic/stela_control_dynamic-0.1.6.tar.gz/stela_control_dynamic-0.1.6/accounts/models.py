from django.db import models
from django.utils.safestring import mark_safe
# Create your models here.
from geolocation.models import City, Country
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)   
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superusuario debe ser asignado a is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superusuario debe ser asignado a is_superuser=True.')
        
        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError(_('Debes suministrar un email'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          **other_fields)
        user.set_password(password)
        user.save()
        
        return user

class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    email_sender = models.EmailField(_('email'), null=True)
    username = models.CharField(max_length=150, unique=True, verbose_name=_('username'))
    full_name = models.CharField(max_length=150, verbose_name=_("Full Name"))
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    # delivery details
    cloud_id=models.CharField(max_length=150, unique=True, null=True)
    image = models.ImageField(verbose_name=_("Avatar"), upload_to='profile/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, default="No Phone")
    zip = models.CharField(max_length=50, blank=True, null=True)
    country_profile = models.ForeignKey(Country, verbose_name=_('Country'), on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=150, verbose_name=_('Address'))
    city_profile = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    #User Status
    meta_token = models.CharField(max_length=1000, default="no_token")
    meta_status = models.CharField(max_length=50, default="not_logged_in")
    meta_id = models.CharField(max_length=150, default="noID")
    is_active = models.BooleanField(_('Activation'), help_text=_("Control of user status"), default=False)
    is_staff = models.BooleanField(default=False,)
    is_subscribed = models.BooleanField(default=False,)
    is_business = models.BooleanField(default=False,)
    is_suspended = models.BooleanField(default=False,)
    yearly_subscriber = models.BooleanField(default=False,)
    cloud_services = models.BooleanField(default=False,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    newsletter = models.BooleanField(default=False, help_text=_("If you accept, we will keep you informed of all our promotions and offers."))
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username']

    class Meta:
        verbose_name = 'Accounts'
        verbose_name_plural = 'Accounts'
    
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    def __str__(self):
        return self.username

