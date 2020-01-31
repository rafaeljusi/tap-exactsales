from setuptools import setup


setup(name="tap-exactsales",
      version="1.0.5",
      description="Singer.io tap for extracting data from the Exactsales API",
      author="Stitch",
      author_email="dev@stitchdata.com",
      url="http://singer.io",
      classifiers=["Programming Language :: Python :: 3 :: Only"],
      py_modules=["tap_exactsales"],
      install_requires=[
          "pendulum==2.0.4",
          "requests==2.21.0",
          "singer-python==5.4.1",
      ],
      entry_points="""
          [console_scripts]
          tap-exactsales=tap_exactsales.cli:main
      """,
      packages=["tap_exactsales",
                "tap_exactsales.streams",
                "tap_exactsales.streams.recents",
                "tap_exactsales.streams.recents.dynamic_typing"],
      include_package_data=True,
)