from conan import ConanFile


class MyAppConan(ConanFile):
    name = "my-app"
    version = "1.0"
    settings = "os", "compiler", "build_type", "arch"
    requires = "zlib/1.3.1", "bzip2/1.0.8"
    tool_requires = "cmake/3.27.9", "ninja/1.12.1"
    generators = "CMakeToolchain", "CMakeDeps"
