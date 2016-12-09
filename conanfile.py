from conans import ConanFile, CMake, tools
import os


class IlmBaseConan(ConanFile):
    name = "IlmBase"
    version = "2.2.0"
    license = "BSD"
    url = "https://github.com/Mikayex/conan-ilmbase.git"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "namespace_versioning": [True, False]}
    default_options = "shared=True", "namespace_versioning=True"
    generators = "cmake"

    def source(self):
        tools.download("http://download.savannah.nongnu.org/releases/openexr/ilmbase-%s.tar.gz" % self.version,
                       "ilmbase.tar.gz")
        tools.untargz("ilmbase.tar.gz")
        os.unlink("ilmbase.tar.gz")
        tools.replace_in_file("ilmbase-%s/CMakeLists.txt" % self.version, "PROJECT ( ilmbase )",
                              """PROJECT ( ilmbase )
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

        # Remove tests compilation
        tools.replace_in_file("ilmbase-%s/CMakeLists.txt" % self.version, "ADD_SUBDIRECTORY ( HalfTest )", "")
        tools.replace_in_file("ilmbase-%s/CMakeLists.txt" % self.version, "ADD_SUBDIRECTORY ( IexTest )", "")
        tools.replace_in_file("ilmbase-%s/CMakeLists.txt" % self.version, "ADD_SUBDIRECTORY ( ImathTest )", "")

    def build(self):
        cmake = CMake(self.settings)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else "-DBUILD_SHARED_LIBS=OFF"
        namespace_versioning = "-DNAMESPACE_VERSIONING=ON" if self.options.namespace_versioning else "-DNAMESPACE_VERSIONING=OFF"
        cmake_flags = [shared, namespace_versioning, '-DCMAKE_INSTALL_PREFIX="%s"' % self.package_folder]

        self.run('cmake ilmbase-%s %s %s' % (self.version, ' '.join(cmake_flags), cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        cmake = CMake(self.settings)
        self.run("cmake --build . --target install %s" % cmake.build_config)

    def package_info(self):
        parsed_version = self.version.split('.')
        version_suffix = "-%s_%s" % (parsed_version[0], parsed_version[1]) if self.options.namespace_versioning else ""

        self.cpp_info.includedirs = ['include', 'include/OpenEXR']
        self.cpp_info.libs = ["Imath" + version_suffix, "IexMath" + version_suffix, "Half", "Iex" + version_suffix,
                              "IlmThread" + version_suffix]

        if not self.settings.os == "Windows":
            self.cpp_info.cppflags = ["-pthread"]
