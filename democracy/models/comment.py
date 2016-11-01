from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from djgeojson.fields import GeometryField

from .base import BaseModel


class BaseComment(BaseModel):
    parent_field = None  # Required for factories and API
    parent_model = None  # Required for factories and API
    title = models.CharField(verbose_name=_('title'), blank=True, max_length=255)
    content = models.TextField(verbose_name=_('content'), blank=True)
    geojson = GeometryField(blank=True, null=True, verbose_name=_('location'))
    authorization_code = models.CharField(verbose_name=_('authorization code'),  max_length=32, blank=True)
    author_name = models.CharField(verbose_name=_('author name'), max_length=255, blank=True, null=True)
    plugin_identifier = models.CharField(verbose_name=_('plugin identifier'), blank=True, max_length=255)
    plugin_data = models.TextField(verbose_name=_('plugin data'), blank=True)
    label = models.ForeignKey("Label", verbose_name=_('label'), blank=True, null=True)
    n_votes = models.IntegerField(
        verbose_name=_('vote count'),
        help_text=_('number of votes given to this comment'),
        default=0,
        editable=False
    )
    n_unregistered_votes = models.IntegerField(
        verbose_name=_('unregistered vote count'),
        help_text=_('number of unregistered votes'),
        default=0,
        editable=False
    )
    voters = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('voters'),
        help_text=_('users who voted for this comment'),
        related_name="voted_%(app_label)s_%(class)s",
        blank=True
    )

    class Meta:
        abstract = True

    @property
    def parent(self):
        """
        :rtype: Commentable|None
        """
        return getattr(self, self.parent_field, None)

    @property
    def parent_id(self):
        """
        :rtype: int|str|None
        """
        return getattr(self, "%s_id" % self.parent_field, None)

    def save(self, *args, **kwargs):
        if not (self.plugin_data or self.content or self.label):
            raise ValueError("Comments must have either plugin data, textual content or label")
        if not self.author_name and self.created_by_id:
            self.author_name = (self.created_by.get_display_name() or None)
        return super(BaseComment, self).save(*args, **kwargs)

    def recache_n_votes(self):
        n_votes = self.voters.all().count() + self.n_unregistered_votes
        if n_votes != self.n_votes:
            self.n_votes = n_votes
            self.save(update_fields=("n_votes", "n_unregistered_votes"))

    def recache_parent_n_comments(self):
        if self.parent_id:  # pragma: no branch
            self.parent.recache_n_comments()


def comment_recache(sender, instance, using, created, **kwargs):
    """
    :type instance: BaseComment
    """
    if created or instance.deleted:
        instance.recache_parent_n_comments()
    else:
        instance.recache_n_votes()


def recache_on_save(klass):
    assert issubclass(klass, BaseComment)
    post_save.connect(comment_recache, sender=klass)
    return klass
