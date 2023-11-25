#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace utils {

extern void bindings_logging_module(py::module m);
extern void bindings_path_handling_module(py::module m);
extern void bindings_timing_module(py::module m);
extern void bindings_perlin_noise_module(py::module m);
extern void bindings_profiling_module(py::module m);

}  // namespace utils

// NOLINTNEXTLINE
PYBIND11_MODULE(utils_bindings, m) {
    utils::bindings_logging_module(m);
    utils::bindings_path_handling_module(m);
    utils::bindings_timing_module(m);
    utils::bindings_perlin_noise_module(m);
    utils::bindings_profiling_module(m);
}
