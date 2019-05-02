# Birth, PersonNewForm, BirthForm
GENDER_CHOICES = (
    ('U', 'Unknown'),
    ('M', 'Male'),
    ('F', 'Female'),
)

# Child, FamilyForm
REL_CHOICES = (
    ('B', 'Biological'),
    ('A', 'Adopted'),
    ('F', 'Foster'),
    ('S', 'Sealing'),
)

# FamilyForm
NBR_CHOISES = [(str(x), str(x)) for x in range(1, 21)]

# DateTime, PersonNewForm
QUALIFIERS_CHOICES = (
    ('EXC', 'Exactly'),
    ('ABT', 'About'),
    ('CAL', 'Calculated'),
    ('EST', 'Estimated'),
    ('AFT', 'After'),
    ('BEF', 'Before'),
    ('BET', 'Between'),
    ('FROM', 'Beginning'),
    ('TO', 'Ending'),
)

# DateTime
CALENDAR_CHOICES = (
    ('Gregorian', 'Gregorian'),
    ('Julian', 'Julian'),
    ('Hebrew', 'Hebrew'),
    ('French', 'French'),
    ('Roman', 'Roman'),
    ('unknown', 'unknown'),
)

# DateTime
DAY_CHOISES = (
    ('None', 'Day'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),

)
MONTH_CHOISES = (
    ('None', 'Month'),
    ('1', '1'),
    ('2', '2'),
)
YEAR_CHOISES = (
    ('None', 'Year'),
    ('1999', '1999'),
    ('2000', '2000'),
)
HOUR_CHOISES = (
    ('None', 'Hour'),
    ('1', '1'),
    ('2', '2'),
)
MINUTE_CHOISES  = (
    ('None', 'Minute'),
    ('10', '10'),
    ('20', '20'),
)


def link_inc(obj):
    if obj:
        obj.link += 1
        obj.save()


def link_dec(obj):
    if obj:
        if obj.link > 1:
            obj.link -= 1
            obj.save()
        elif getattr(obj, 'note', False):
            obj.link = 0
            obj.save()
        else:
            obj.delete()
