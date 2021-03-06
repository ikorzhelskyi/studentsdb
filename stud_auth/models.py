from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class StProfile(models.Model):
    """To keep extra user data"""

    class Meta(object):
        verbose_name = _(u"User Profile")
        verbose_name = _(u"Additional User Info")
        verbose_name_plural = _(u"Additional User Info")

    # user mapping
    user = models.OneToOneField(User)

    # extra user data
    mobile_phone = models.CharField(
        max_length=12,
        blank=True,
        verbose_name=_(u"Mobile Phone"),
        default='')

    passport_id=models.CharField(
        max_length=8,
        blank=True,
        verbose_name=_(u'Passport ID'),
        default='',
    )

    address=models.CharField(
        max_length=256,
        blank=True,
        verbose_name=_(u'Address'),
        default='',
    )

    photo=models.ImageField(
        blank=True,
        verbose_name=_(u'Photo'),
    )

    def __unicode__(self):
        return self.user.username