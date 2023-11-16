from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampedModel(models.Model):
    """An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields with UUID as primary_key field.
    """

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class ScalingConfigSetting(TimeStampedModel):
    "Configuration setting for support workers scaling"

    scale_up_threshold = models.IntegerField(
        _("Number of tasks in queues to add support workers."), default=100
    )
    scale_down_threshold = models.IntegerField(
        _("Number of tasks in queues to remove support workers."), default=0
    )
    consumption_rate = models.IntegerField(
        _(
            "Tasks support workers should consume in a minute to process all tasks in the queue in 5-7 minutes"
        ),
        default=300,
    )
    min_support_workers = models.IntegerField(
        _("Minimum support workers ECS can launch"), default=1
    )
    max_support_workers = models.IntegerField(
        _("Maximum support workers ECS can launch"), default=9
    )

    @classmethod
    def get_latest_object(self):
        return self.objects.latest()

    def __str__(self):
        return f"Scaling Config Setting Object {self.id}"

    class Meta:
        verbose_name = _("Support worker scaling config setting")
        get_latest_by = ["created_at"]  # order the objects by timestamp in descending
        ordering = ("-created_at",)
