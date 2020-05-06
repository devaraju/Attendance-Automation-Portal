from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

from .models import Student, Faculty

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff and not instance.is_superuser:
            Faculty.objects.create(user=instance)
        elif not instance.is_staff:
            Student.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.is_staff and not instance.is_superuser:
        instance.faculty.faculty_id = instance.username
        instance.faculty.save()
        faculty_group,_ = Group.objects.get_or_create(name='Faculty')
        faculty_group.user_set.add(instance)
        
    elif not instance.is_staff:
        instance.student.student_id = instance.username
        instance.student.save()
