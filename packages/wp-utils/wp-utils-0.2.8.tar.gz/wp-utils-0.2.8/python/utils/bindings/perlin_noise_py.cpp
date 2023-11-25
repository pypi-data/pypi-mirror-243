#include <pybind11/pybind11.h>

#include <utils/perlin_noise.hpp>

namespace py = pybind11;

namespace utils {

// NOLINTNEXTLINE
void bindings_perlin_noise_module(py::module m) {
    {
        using Class = PerlinNoise;
        // NOLINTNEXTLINE
        py::class_<Class>(m, "PerlinNoise")
            .def_static("Init", &Class::Init)
            .def_static("Release", &Class::Release)
            .def_static("Config", &Class::Config)
            .def_static("Sample1d", &Class::Sample1d)
            .def_static("Sample2d",
                        static_cast<float (*)(float, float)>(&Class::Sample2d))
            .def_static("Sample2d",
                        static_cast<float (*)(const Vec2&)>(&Class::Sample2d));
    }
}

}  // namespace utils
