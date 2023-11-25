from setuptools import setup, find_packages

setup(
    name="rafetch",
    version="1.0.3",
    author="Tanjibul Hasan Rafi",
    author_email="rafitanjibulhasan@gmail.com",
    description="A simple system information tool for Ubuntu",
    packages=find_packages(),
    install_requires=[
        'distro',
        'platform',
        'subprocess',
        'os',
        're',
        'random',
        'cv2',
        'socket',
        'psutil',
        'getpass',
        'cpuinfo',
        'colorama',
    ],
    entry_points={
        "console_scripts": [
            "rafetch=rafetch.rafetch:main",
        ],
    },
    keywords=['python', 'fetch', 'linux', 'ubuntu', 'systeminfo', 'neofetch'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ],
)
