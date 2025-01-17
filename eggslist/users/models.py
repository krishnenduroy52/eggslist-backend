import typing as t

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AnonymousUser as DjangoAnonymousUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField

from eggslist.users import constants, managers
from eggslist.users.user_location_storage import UserLocationStorage

if t.TYPE_CHECKING:
    from eggslist.site_configuration.models import LocationCity


class AnonymousUser(DjangoAnonymousUser):
    def __init__(self, request):
        request.session.create()
        self.id = request.session.session_key
        super().__init__()


class User(AbstractUser):
    email = models.EmailField(verbose_name=_("email address"), unique=True)
    is_email_verified = models.BooleanField(verbose_name=_("is email verified"), default=False)
    phone_number = PhoneNumberField(verbose_name=_("phone number"), null=True, blank=True)
    avatar = ProcessedImageField(
        verbose_name=_("avatar"),
        upload_to="avatars",
        null=True,
        blank=True,
        processors=[ResizeToFill(124, 124)],
        format="JPEG",
        options={"quality": 70},
    )

    is_verified_seller = models.BooleanField(verbose_name=_("is verified seller"), default=False)
    is_verified_seller_pending = models.BooleanField(
        verbose_name=_("is verified seller pending"), default=False
    )
    bio = models.CharField(verbose_name=_("bio"), max_length=1024, null=True, blank=True)
    # Location
    zip_code = models.ForeignKey(
        verbose_name=_("zip code"),
        to="site_configuration.LocationZipCode",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    objects = managers.EggslistUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def user_location(self) -> "LocationCity":
        return UserLocationStorage.get_user_location(self.id)

    @user_location.setter
    def user_location(self, value: "LocationCity"):
        UserLocationStorage.set_user_location(self.id, city_location=value)

    def set_password(self, *args, **kwargs):
        super().set_password(*args, **kwargs)
        self._set_password = True

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class VerifiedSellerApplication(models.Model):
    """
    Verified Seller is not the same thing as email
    verification or password reset verification
    """

    user = models.ForeignKey(
        verbose_name=_("user"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    image = ProcessedImageField(
        verbose_name=_("image"),
        upload_to="seller_verifications",
        null=True,
        format="JPEG",
        options={"quality": 70},
    )
    text = models.TextField(verbose_name=_("text"))
    is_approved = models.BooleanField(verbose_name=_("is_approved"), default=False)
    status = models.IntegerField(
        verbose_name=_("status"), choices=constants.APPLICATION_STATUS, default=constants.PENDING
    )

    class Meta:
        verbose_name = _("verified seller application")
        verbose_name_plural = _("verified seller application")
        ordering = ("status",)

    def __str__(self):
        return f"Verification Application for {self.user.first_name}"


class UserFavoriteFarm(models.Model):
    user = models.ForeignKey(
        verbose_name=_("user"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",
    )
    following_user = models.ForeignKey(
        verbose_name=_("following_user"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    objects = managers.UserFavoriteFarmManager()

    class Meta:
        verbose_name = _("user favorite farm")
        verbose_name_plural = _("user favorite farms")
        ordering = ("-date_created",)
        constraints = (
            models.UniqueConstraint(
                fields=("user", "following_user"), name="favorite_farm_unique_constraint"
            ),
        )


class UserIPLocationLog(models.Model):
    ip_address = models.CharField(verbose_name=_("ip address"), max_length=128)
    determined_city = models.CharField(
        verbose_name=_("determined city"), max_length=128, null=True
    )
