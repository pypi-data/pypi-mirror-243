from setuptools import setup

import os


pastas = ['mathfox']
origem = r'F:\Brian\Python\Projetos\mathfox\mathfox'
oc = len(origem)-7
for caminho, subpasta, arquivos in os.walk(origem):
    subpasta.pop()
    if not (subpasta == []):
        for pasta in subpasta:
            clista = list(caminho[oc:])
            for posicao, letra in enumerate(clista):
                if letra in r'\ ':
                    clista[posicao] = '.'
            clista = ''.join(clista)
            atual = clista+'.'+pasta
            pastas.append(atual)

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='mathfox',
      version='1.1.1',
      license='MIT License',
      author='Brian Braga Cavalcante',
      long_description=readme,
      long_description_content_type="text/markdown",
      author_email='brianbragacavalcantex@gmail.com',
      keywords='math',
      description=u'A library with math functions to help Python developers with their projects.',
      packages=pastas,
      package_data={'': ['DOCUMENTATION.md']},
      include_package_data=True,
      python_requires='>=3.6',
      )
