from distutils.core import setup, Extension

pkg = 'Extensions.1plus1'
setup (name = 'enigma2-plugin-extensions-1plus1',
       version = '1.0',
       license='GPLv2',
       url='https://github.com/E2OpenPlugins/e2openplugin-1plus1',
       description='1plus1 calculator plugin',
       long_description='A simple arithmetic calculator',
       author='GianricoT',
       packages = [pkg],
       package_dir = {pkg: 'plugin'},
       package_data={pkg: ['*.png']}
)
