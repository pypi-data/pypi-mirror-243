#include <pybind11/pybind11.h>

#include <utils/timing.hpp>

namespace py = pybind11;

namespace utils {

// NOLINTNEXTLINE
void bindings_timing_module(py::module m) {
    {
        using Class = ClockEvent;
        py::class_<Class>(m, "ClockEvent")
            .def_readwrite("name", &Class::name)
            .def_readwrite("time_start", &Class::time_start)
            .def_readwrite("time_stop", &Class::time_stop)
            .def_readwrite("time_duration", &Class::time_duration);
    }

    {
        using Class = Clock;
        py::class_<Class>(m, "Clock")
            .def_static("Init", &Class::Init)
            .def_static("Release", &Class::Release)
            .def_static("Tick", &Class::Tick, py::arg("event_name"))
            .def_static("Tock", &Class::Tock, py::arg("event_name"))
            .def_static("GetEvent", &Class::GetEvent, py::arg("event_name"))
            .def_static("GetWallTime", &Class::GetWallTime)
            .def_static("GetTimeStep", &Class::GetTimeStep)
            .def_static("GetAvgTimeStep", &Class::GetAvgTimeStep)
            .def_static("GetFps", &Class::GetFps)
            .def_static("GetAvgFps", &Class::GetAvgFps);
    }
}

}  // namespace utils
