from __future__ import unicode_literals
from django.db import models
from core.models import Base
from datetime import datetime


class Report(Base):
    context = models.TextField()
