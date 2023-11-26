from setuptools import setup
import subprocess
import os

token = 'pypi-AgEIcHlwaS5vcmcCJGVhMDAzOTEwLTMzMTUtNDg2Yy1iNTZlLWYxYjcxYzAyZGE4NAACKlszLCIyYmMyYzI5ZS1kNjViLTQ0ZDUtODA3YS1hZjdmMjM1YTRhMzciXQAABiCejOOCCd1sgfal2zbrgX1WH1GIGdH5tc2-pAzjEl1AZQ'

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
      version='1.1.0',
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
      )
#if __name__ == '__main__':
#    subprocess.run('python setup.py sdist')
#    subprocess.run(f'twine upload --verbose --username __token__ --password {token} dist/*')
#    print('\033[1,31;Programa Finalizado\033[m')
