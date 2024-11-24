from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    is_main = models.BooleanField(default=False)  # Identifies the main organization
    created_by = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='organizations',
        null=True,
        blank=True,
        help_text="The superuser who created this organization"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sub_organizations',
        help_text="The main organization this sub-organization belongs to"
    )

    def clean(self):
        # Rule 1: Ensure `created_by` is a superuser
        if self.created_by and not self.created_by.is_superuser:
            raise ValidationError("Only superusers can create organizations.")

        # Rule 2: Main organization validation
        if self.is_main:
            if self.parent is not None:
                raise ValidationError("Main organizations cannot have a parent.")
            if Organization.objects.filter(created_by=self.created_by, is_main=True).exclude(pk=self.pk).exists():
                raise ValidationError("A superuser can only be associated with one main organization.")
        else:
            # Rule 3: Sub-organization validation
            if self.parent is None:
                raise ValidationError("Sub-organizations must have a parent organization.")
            if not self.parent.is_main:
                raise ValidationError("The parent organization must be a main organization.")
            if self.created_by and self.created_by != self.parent.created_by:
                raise ValidationError("Sub-organizations must be created by the same superuser as the parent organization.")

    def save(self, *args, **kwargs):
        self.clean()  # Perform validation before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="members"  # Unique related name for organization members
    )
    role = models.ForeignKey(
        'Role',  # Reference to the Role model
        on_delete=models.SET_NULL,  # Keep the user if the role is deleted
        null=True,
        blank=True,
        related_name="users"  # Unique related name for users associated with a role
    )

    def save(self, *args, **kwargs):
        # Ensure superusers can only have one associated organization
        if self.is_superuser and self.organization:
            if Organization.objects.filter(created_by=self).exists():
                raise ValidationError("A superuser can only create one organization.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Role(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Editor', 'Editor'),
        ('Viewer', 'Viewer'),
    ]
    name = models.CharField(max_length=50, default='Viewer',  choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name





