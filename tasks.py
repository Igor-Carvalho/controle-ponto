"""Módulo que contém as tarefas locais utilizadas com invoke."""

import invoke


@invoke.task
def collectstatic(ctx, noinput=True, clear=False, verbosity=0, settings='development'):
    """Coleta arquivos estáticos."""
    ctx.run('yarn install', echo=True, pty=True)
    noinput = '--noinput' if noinput else ''
    clear = '--clear' if clear else ''
    cmd = './manage.py collectstatic {} {} --verbosity={} --settings=controle_ponto.settings.{}'
    cmd = cmd.format(noinput, clear, verbosity, settings)
    ctx.run(cmd, echo=True, pty=True)


@invoke.task
def assetsbuild(ctx, noinput=True, clear=False, verbosity=0, settings='development'):
    """Constroe bundles."""
    collectstatic(ctx, noinput, clear, verbosity, settings)
    cmd = './manage.py assets build'
    ctx.run(cmd, echo=True, pty=True)


@invoke.task(default=True)
def run_server(ctx, noinput=True, clear=False, verbosity=0, settings='development'):
    """Executa o servidor web."""
    assetsbuild(ctx, noinput, clear, verbosity, settings)
    cmd = './manage.py runserver 0.0.0.0:8000 --settings=controle_ponto.settings.{}'.format(settings)
    ctx.run(cmd, echo=True, pty=True)


@invoke.task
def test(ctx, package='', settings='test'):
    """Testa as aplicações do projeto (com exceção dos testes funcionais)."""
    cmd = 'coverage run ./manage.py test {} --settings=controle_ponto.settings.{}'.format(package, settings)
    ctx.run(cmd, echo=True, pty=True)
    cmd = 'coverage report'
    ctx.run(cmd, echo=True, pty=True)


@invoke.task
def functional_tests(ctx, package='functional_tests.histories', settings='test'):
    """Executa os testes funcionais."""
    collectstatic(ctx, settings, True)
    cmd = 'coverage run ./manage.py test {} . --settings=controle_ponto.settings.{}'
    cmd = cmd.format(package, settings)
    ctx.run(cmd, echo=True, pty=True)
    cmd = 'coverage report'
    ctx.run(cmd, echo=True, pty=True)
