#include <pybind11/pybind11.h>

#include <utils/path_handling.hpp>

namespace py = pybind11;

namespace utils {

void bindings_path_handling_module(py::module m) {
    m.def("GetFilename", &GetFilename, py::arg("filepath"));
    m.def("GetFoldername", &GetFoldername, py::arg("filepath"));
    m.def("GetFolderpath", &GetFolderpath, py::arg("filepath"));
    m.def("GetFilenameNoExtension", &GetFilenameNoExtension,
          py::arg("filepath"));
}

}  // namespace utils
