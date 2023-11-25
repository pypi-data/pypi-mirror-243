#include <pybind11/pybind11.h>

#include <utils/logging.hpp>

namespace py = pybind11;

namespace utils {

// NOLINTNEXTLINE
void bindings_logging_module(py::module m) {
    {
        using Enum = Logger::eType;
        constexpr auto EnumName = "LoggerType";  // NOLINT
        py::enum_<Enum>(m, EnumName, py::arithmetic())
            .value("CONSOLE_LOGGER", Enum::CONSOLE_LOGGER)
            .value("FILE_LOGGER", Enum::FILE_LOGGER);
    }

    {
        using Class = Logger;
        constexpr auto ClassName = "Logger";  // NOLINT
        py::class_<Class>(m, ClassName)
            .def_property_readonly("ready", &Class::ready)
            .def_property_readonly("type", &Class::type)
            .def_static("Init", &Class::Init,
                        py::arg("type") = Logger::eType::CONSOLE_LOGGER)
            .def_static("Release", &Class::Release)
            .def_static("GetInstance", &Class::GetInstance,
                        py::return_value_policy::reference)
            .def_static("CoreTrace",
                        [](const std::string& msg) { LOG_CORE_TRACE(msg); })
            .def_static("CoreInfo",
                        [](const std::string& msg) { LOG_CORE_INFO(msg); })
            .def_static("CoreWarn",
                        [](const std::string& msg) { LOG_CORE_WARN(msg); })
            .def_static("CoreError",
                        [](const std::string& msg) { LOG_CORE_ERROR(msg); })
            .def_static("CoreCritical",
                        [](const std::string& msg) { LOG_CORE_CRITICAL(msg); })
            .def_static("CoreAssert",
                        [](bool is_ok, const std::string& msg) {
                            LOG_CORE_ASSERT(is_ok, msg);
                        })
            .def_static("Trace", [](const std::string& msg) { LOG_TRACE(msg); })
            .def_static("Info", [](const std::string& msg) { LOG_INFO(msg); })
            .def_static("Warn", [](const std::string& msg) { LOG_WARN(msg); })
            .def_static("Error", [](const std::string& msg) { LOG_ERROR(msg); })
            .def_static("Critical",
                        [](const std::string& msg) { LOG_CRITICAL(msg); })
            .def_static("Assert",
                        [](const bool& is_ok, const std::string& msg) {
                            LOG_ASSERT(is_ok, msg);
                        });
    }
}

}  // namespace utils
