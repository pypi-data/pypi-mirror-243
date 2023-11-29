from distutils.core import setup
setup(
    name="HandTrackingModule",
    packages=["HandTrackingModule"],
    version=0.2,
    license="MIT",
    description="This is a simplified version to do hand tracking from mediapipe",
    author="Harsh Bansal",
    url="https://github.com/Harshbansal8705/HandTrackingModule",
    download_url="https://github.com/Harshbansal8705/HandTrackingModule/archive/refs/tags/0.1.tar.gz",
    keywords=["hand", "track", "detect"],
    install_requires=["opencv-python", "numpy", "mediapipe"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11'
    ]
)