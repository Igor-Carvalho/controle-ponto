"""
Módulo contendo testes funcionais.

Testes funcionais estão separados dos testes de aplicação já que estão relacionados ao projeto em si e não
a uma aplicação específica.
"""

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver import Firefox


class FunctionalTests(LiveServerTestCase):
    """Base para os testes funcionais."""

    @classmethod
    def setUpClass(cls):
        """Class fixtures."""
        super(FunctionalTests, cls).setUpClass()
        get_user_model().objects.create_user('user', 'user@domain.com', 'pass')

    def setUp(self):
        """Inicializa serviços necessários para execução dos testes funcionais."""
        self.driver = Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def tearDown(self):
        """Finaliza serviços."""
        self.driver.close()

    def get_live_url(self, url_name):
        """Obtém url_name em relação ao servidor de testes."""
        return '{}{}'.format(self.live_server_url, reverse(url_name))


class LoginTest(FunctionalTests):
    """Testes para página de login."""

    def test_título_login(self):
        """Verifica o título da página de login."""
        self.driver.get(self.get_live_url('dashboard'))

        self.assertEqual(self.driver.title, 'Login')

        self.driver.find_element_by_id('login').send_keys('user')

        self.driver.find_element_by_id('password').send_keys('pass')

        self.driver.find_element_by_id('loginButton').click()

        self.assertEqual(self.driver.title, 'Bem vindo')
        self.driver.find_element_by_id('userDropdown').click()
        self.driver.find_element_by_id('logoutLink').click()

        self.driver.switch_to.alert.accept()
