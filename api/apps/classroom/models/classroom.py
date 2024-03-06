from api.apps.authentication.models.user import (
    Base,
    Student,
    Teacher
)

from django.db import (
    models,
    transaction
)

from dateutil.rrule import (
    rrule,
    WEEKLY
)


class SubjectWeekdayManager(models.Manager):
    @transaction.atomic
    def create_subject_weekday(self, subject_period, weekday, start_time, end_time):
        subject_period_weekday = self.create(
            subject_period=subject_period,
            weekday=weekday,
            start_time=start_time,
            end_time=end_time
        )

        start_date = subject_period.period.start_date
        end_date = subject_period.period.end_date

        for date in rrule(
            WEEKLY,
            dtstart=start_date,
            until=end_date,
            byweekday=weekday
        ):
            Classroom.objects.create(
                subject_period_weekday=subject_period_weekday,
                date=date,
                start_time=start_time,
                end_time=end_time
            )

        return subject_period_weekday


class Period(Base):
    year = models.IntegerField()
    semester = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.year} - {self.semester}'

    class Meta:
        db_table = 'periods'
        ordering = ['created_at']
        verbose_name = 'period'
        verbose_name_plural = 'periods'


class Room(Base):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'rooms'
        verbose_name = 'room'
        verbose_name_plural = 'rooms'


class Subject(Base):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subjects'
        ordering = ['created_at']
        verbose_name = 'subject'
        verbose_name_plural = 'subjects'


class SubjectPeriod(Base):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )
    period = models.ForeignKey(
        Period,
        on_delete=models.CASCADE
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.subject.name} - {self.period.year} - {self.period.semester}'

    class Meta:
        db_table = 'subjects_periods'
        verbose_name = 'subject period'
        verbose_name_plural = 'subjects periods'


class SubjectPeriodStudent(Base):
    subject_period = models.ForeignKey(
        SubjectPeriod,
        on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.subject_period.subject.name} - {self.subject_period.period.year} - {self.subject_period.period.semester}'

    class Meta:
        db_table = 'subjects_periods_students'
        verbose_name = 'subject period student'
        verbose_name_plural = 'subjects periods students'


class SubjectPeriodWeekday(Base):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    DAY_OF_WEEK = (
        (MONDAY, 'Segunda-feira'),
        (TUESDAY, 'Terça-feira'),
        (WEDNESDAY, 'Quarta-feira'),
        (THURSDAY, 'Quinta-feira'),
        (FRIDAY, 'Sexta-feira'),
        (SATURDAY, 'Sábado'),
        (SUNDAY, 'Domingo'),
    )

    subject_period = models.ForeignKey(
        SubjectPeriod,
        on_delete=models.CASCADE
    )
    weekday = models.IntegerField(choices=DAY_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    objects = SubjectWeekdayManager()

    def __str__(self):
        return f'{self.subject_period.subject.name} - {self.subject_period.period.year} - {self.subject_period.period.semester} - {self.weekday}'

    class Meta:
        db_table = 'subjects_periods_weekdays'
        verbose_name = 'subject period weekday'
        verbose_name_plural = 'subjects periods weekdays'


class Classroom(Base):
    CONFIRMED = 'confirmed'
    CANCELED = 'canceled'
    PENDING = 'pending'

    STATUS = (
        (CONFIRMED, 'Confirmada'),
        (CANCELED, 'Cancelada'),
        (PENDING, 'Pendente'),
    )

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField()
    status = models.CharField(
        max_length=255,
        choices=STATUS,
        default=PENDING
    )
    subject_period_weekday = models.ForeignKey(
        SubjectPeriodWeekday,
        on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f'{self.subject_period_weekday.subject_period.subject.name} - {self.subject_period_weekday.subject_period.period.year} - {self.subject_period_weekday.subject_period.period.semester} - {self.subject_period_weekday.weekday} - {self.room.name}'

    class Meta:
        db_table = 'classrooms'
        verbose_name = 'classroom'
        verbose_name_plural = 'classrooms'
