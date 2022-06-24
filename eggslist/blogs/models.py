from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from eggslist.utils.models import NameSlugModel, TitleSlugModel


class BlogCategory(NameSlugModel):
    class Meta:
        verbose_name = _("blog category")
        verbose_name_plural = _("blog categories")


class BlogArticle(TitleSlugModel):
    image = models.ImageField(verbose_name=("image"), null=True, blank=True)
    author = models.ForeignKey(
        verbose_name=_("author"), to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        verbose_name=_("category"), to="BlogCategory", on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(verbose_name=_("date created"), auto_now_add=True)
    body = models.TextField(verbose_name=_("body"))

    class Meta:
        verbose_name = _("blog article")
        verbose_name_plural = _("blog articles")