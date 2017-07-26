from django.db import models
from accounts.models import StudentProfile
from subforums import models as forum_models


class Subject(models.Model):
    title = models.CharField(max_length=255)
    credit = models.IntegerField()
    subject_id = models.CharField(max_length=8)
    short_name = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        # Auto create a subforum for this subject
        super(Subject, self).save(*args, **kwargs)
        subforum = forum_models.Subforum.objects.get_or_create(subject=self)[0]
        subforum.title = self.title
        subforum.short_name = self.short_name
        subforum.save()

    class Meta:
        db_table = 'Subjects'

    def __str__(self):
        return self.title


class Mark(models.Model):
    PASS = 'PS'
    NOT_PASS = 'NP'

    MARK_STATUS = (
        (PASS, 'PASS'),
        (NOT_PASS, 'NOT PASS'),
    )

    student = models.ForeignKey(StudentProfile, related_name='marks')
    subject = models.ForeignKey(Subject, related_name='mark')
    mid_term_mark = models.FloatField()
    final_mark = models.FloatField()
    status = models.CharField(max_length=2, choices=MARK_STATUS,
                              default=NOT_PASS)
    avg_mark = models.FloatField()

    class Meta:
        db_table = 'Marks'

    def __str__(self):
        return '{}\'s {} mark'.format(self.student.name, self.subject.title)