FIELD_CHOICES = (
    ('Air Conditioner', 'Air Conditioner'),
    ('All in One', 'All in One'),
    ('Carpentry', 'Carpentry'),
    ('Electricity', 'Electricity'),
    ('Gardening', 'Gardening'),
    ('Home Machines', 'Home Machines'),
    ('Housekeeping', 'Housekeeping'),
    ('Interior Design', 'Interior Design'),
    ('Locks', 'Locks'),
    ('Painting', 'Painting'),
    ('Plumbing', 'Plumbing'),
    ('Water Heaters', 'Water Heaters'),
)

SERVICE_FIELD_CHOICES = [choice for choice in FIELD_CHOICES if choice[0] != 'All in One']