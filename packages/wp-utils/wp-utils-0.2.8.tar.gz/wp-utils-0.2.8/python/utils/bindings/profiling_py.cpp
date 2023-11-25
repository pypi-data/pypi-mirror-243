#include <pybind11/pybind11.h>

#include <utils/profiling.hpp>

namespace py = pybind11;

namespace utils {

// NOLINTNEXTLINE
void bindings_profiling_module(py::module m) {
    {
        using Enum = IProfilerSession::eType;
        py::enum_<Enum>(m, "SessionType", py::arithmetic())
            .value("INTERNAL", Enum::INTERNAL)
            .value("EXTERNAL_CHROME", Enum::EXTERNAL_CHROME);
    }

    {
        using Class = ProfilerTimer;
        py::class_<Class>(m, "ProfilerTimer")
            .def(py::init([](const std::string& timer_name,
                             const std::string& session_name) -> Class::uptr {
                return Class::CreateUnique(timer_name, session_name);
            }));
    }

    {
        using Class = Profiler;
        py::class_<Class>(m, "Profiler")
            .def_static("Init", &Class::Init, py::arg("type"))
            .def_static("Release", &Class::Release)
            .def_static("BeginSession", &Class::BeginSession, py::arg("name"))
            .def_static("EndSession", &Class::EndSession, py::arg("name"));
    }
}

}  // namespace utils
