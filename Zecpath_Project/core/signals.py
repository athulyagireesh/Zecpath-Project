from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Employer, Candidate


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'employer':
            Employer.objects.get_or_create(user=instance)
        elif instance.role == 'candidate':
            Candidate.objects.get_or_create(user=instance)