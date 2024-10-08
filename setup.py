from setuptools import setup, find_packages

setup(
    name="mydb",
    version="0.0.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mydb = mydb.mydb:main',  # 'mycli' 명령어를 통해 실행
        ],
    },
    install_requires=[],  # 필요시 의존성 패키지를 추가
)
