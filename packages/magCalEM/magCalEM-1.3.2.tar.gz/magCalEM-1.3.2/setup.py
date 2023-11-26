import setuptools
from setuptools.command.egg_info import egg_info

class egg_info_ex(egg_info):
    """Includes license file into `.egg-info` folder."""

    def run(self):
        # don't duplicate license into `.egg-info` when building a distribution
        if not self.distribution.have_run.get('install', True):
            # `install` command is in progress, copy license
            self.mkpath(self.egg_info)
            self.copy_file('LICENSE.txt', self.egg_info)

        egg_info.run(self)


with open("README.md", 'r', encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="magCalEM",
    version="1.3.2",
    author="Joshua L. Dickerson",
    author_email="jdickerson@mrc-lmb.cam.ac.uk",
    description="A program to calibrate the pixel size of cryoEM data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    license="MIT",
    license_files = ('LICENSE.txt',),
    install_requires=['PyQt5', 'numpy', 'mrcfile', 'opencv-python', 'matplotlib', 'scipy', 'numba', 'psutil', 'scikit-image', 'pandas', 'lmfit'],
    cmdclass = {'egg_info': egg_info_ex},
)
