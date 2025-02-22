from pie import *

@task
def build():
    cmd(r"python setup.py bdist_wheel clean --all")


@task
def createVenvs():
    venv(r"venvs\test").create("--system-site-packages")


@task
def setup():
    createVenvs()
    updatePackages()


@task
def test():
    with venv(r"venvs\test"):
        cmd(r"python setup.py build")
        cmd(r"pip uninstall -y agsadmin")
        with open("agsadmin/_version.py") as fin: exec(fin.read(), globals())
        cmd(r"pip install dist/agsadmin-{}-py2.py3-none-any.whl".format(__version__))
        cmd(r"python -m pytest -s tests")


@task
def updatePackages():
    with venv(r"venvs\test"):
        pip(r"install -U pip")
        pip(r"install -U -r requirements.txt")
        pip(r"install -U -r requirements.test.txt")


@task([OptionsParameter('version')])
def upload(version):
    cmd(r'python -m twine upload dist\agsadmin-{}-py2.py3-none-any.whl'.format(version))