"""Fábricas da aplicação core."""

import factory
from django.contrib import auth


class UserFactory(factory.django.DjangoModelFactory):
    """Fábrica de usuários."""

    username = factory.Faker('first_name')
    password = factory.Faker('ean')

    class Meta:
        """Meta opções da fábrica."""

        model = auth.get_user_model()
        django_get_or_create = ('username', 'email')

    @factory.lazy_attribute
    def email(self):
        """Email aleatório."""
        return '{}@domain.com'.format(self.username)
