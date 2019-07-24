from django.contrib.auth.models import AbstractUser
from django.db import models, IntegrityError
from django.utils import timezone


class BaseQuerySet(models.QuerySet):
    """The queryset class used to extend the manager for the base class.

        This class enables us to define custom queryset that abstract the business logic
        to within the model layer.
    """
    def update(self, **kwargs):
        if 'updater' in kwargs:
            kwargs['date_updated'] = timezone.now()
            super(BaseQuerySet, self).update(**kwargs)
        else:
            raise IntegrityError('Updater not specified',
                                 'When updating any instance, the updater (User instance/pk) should be provided.')

    def active(self):
        """Queryset to return only the active rows from the model.

            This queryset filters out all the model instances with is_deleted set as true.
        """
        return self.filter(is_deleted=False)

    def remove(self, updater):
        """Queryset to set the is_deleted attribute to true.

            This queryset sets the is_deleted attribute to True, which will be treated
            as a deleted instance by the remaining system.

        """
        return self.update(is_deleted=True, date_updated=timezone.now(), updater=updater)


class BaseModel(models.Model):
    """Base model extended by other models through out the project.

        Here we define all the common fields used by all the models used in the project.
        This way repetition is avoided and custom logic regarding these fields are abstracted
        to with  in the base model.
    """
    # creator = models.ForeignKey(auto_now_add=True, blank=True, related_name='creator_%(class)s_objects')
    # updater = models.ForeignKey(auto_now=True, blank=True, related_name='updater_%(class)s_objects')
    date_added = models.DateTimeField(db_index=True)
    date_updated = models.DateTimeField()

    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Overriding the save methods to extend the logic.

            The update queryset does not call the save method and hence does not cause these modifications to
            be called. In case the update function needs to be called, please add the date_updated
            manually.
        """
        self.date_updated = timezone.now()
        if self.date_added is None:
            self.date_added = timezone.now()

        super(BaseModel, self).save(*args, **kwargs)


class User(AbstractUser, BaseModel):
    """User abstract model inherited from BaseModel.

        Here we define all the custom fields defined by us for users models used in the project.

    """
    linked_in_url = models.CharField(max_length=256, null=True, blank=True)
    twitter_url = models.CharField(max_length=256, null=True, blank=True)
    blog_url = models.CharField(max_length=256, null=True, blank=True)
    status = models.IntegerField(default=0)

    class Meta:
        app_label = 'users_app'
        db_table = "custom_app_user"

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
