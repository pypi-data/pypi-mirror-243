# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enet']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0', 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'econnect',
    'version': '0.0.10',
    'description': 'Paquete para uso de los desarrolladores cubanos que les facilita el uso de funciones del portal cautivo Nauta.',
    'long_description': '# EConnect-module\n\nEsto es un paquete de Python que permite a los desarrolladores cubanos interactuar de manera facil y sencilla con el Portal Cautivo de Etecsa.\n\n# Caracteristicas\n- Verificación de conexión.\n- Inicio de Sesión.\n- Guardado de datos para el cierre de manera local.\n- Obtención de tiempo disponible.\n- Cierre de sesión.\n- Cierre de sesion de forma local con los datos guardados por el usuario\n\n[Repositorio del proyecto aqui](https://guides.github.com/features/mastering-markdown/)\npara los que se interesen en el código.<br>\n[Documentacion del paquete](https://github.com/TheMrAleX/econnect/blob/main/README.md) para una ayuda de como usar el paquete correctamente.',
    'author': 'Alejandro Pérez',
    'author_email': 'alejandroperezsantana55@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
