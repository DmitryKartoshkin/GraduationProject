from rest_framework.test import APIClient
import pytest
from model_bakery import baker
from ProductOrderingService.models import User
from django.core.management import call_command
from app import settings


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def data_factory():
    def factory(*args, **kwargs):
        return baker.make(*args, **kwargs)
    return factory




