#include <iostream>
#include <stdexcept>

#include <utils/logging.hpp>

namespace utils {

// NOLINTNEXTLINE
Logger::uptr Logger::s_Instance = nullptr;

Logger::Logger(eType type) : m_Type(type) {
    spdlog::set_pattern("%^[%T] %n: %v%$");
    switch (m_Type) {
        case ::utils::Logger::eType::CONSOLE_LOGGER: {
            m_CoreLogger = spdlog::stdout_color_mt("CORE");
            m_CoreLogger->set_level(spdlog::level::trace);
            m_ClientLogger = spdlog::stdout_color_mt("USER");
            m_ClientLogger->set_level(spdlog::level::trace);
            break;
        }
        case ::utils::Logger::eType::FILE_LOGGER: {
            try {
                m_CoreLogger =
                    spdlog::basic_logger_mt("CORE", "./core_logs.txt");
                m_CoreLogger->set_level(spdlog::level::trace);
                m_ClientLogger =
                    spdlog::basic_logger_mt("USER", "./user_logs.txt");
                m_ClientLogger->set_level(spdlog::level::trace);
            } catch (const spdlog::spdlog_ex& ex) {
                std::cout << "Logger initialization FAILED: " << ex.what()
                          << '\n';
            }
            break;
        }
    }
    m_Ready = true;

    std::cout << "Initialized Logging module :)\n";
}

auto Logger::GetInstance() -> Logger& {
    if (Logger::s_Instance == nullptr) {
        // By default, if not initialized, use a console logger
        Logger::s_Instance =
            std::unique_ptr<Logger>(new Logger(Logger::eType::CONSOLE_LOGGER));
    }
    return *Logger::s_Instance;
}

auto Logger::Init(eType logger_type) -> void {
    if (Logger::s_Instance == nullptr) {
        Logger::s_Instance = std::unique_ptr<Logger>(new Logger(logger_type));
    }
}

auto Logger::Release() -> void {
    Logger::s_Instance = nullptr;
    spdlog::drop_all();
}

auto Logger::core_logger() -> spdlog::logger& {
    if (m_CoreLogger == nullptr) {
        throw std::runtime_error(
            "Logger::core_logger >>> Should initialize the logger before using "
            "the internal spdlog capabilities");
    }
    return *m_CoreLogger;
}

auto Logger::core_logger() const -> const spdlog::logger& {
    if (m_CoreLogger == nullptr) {
        throw std::runtime_error(
            "Logger::core_logger >>> Should initialize the logger before using "
            "the internal spdlog capabilities");
    }
    return *m_CoreLogger;
}

auto Logger::client_logger() -> spdlog::logger& {
    if (m_ClientLogger == nullptr) {
        throw std::runtime_error(
            "Logger::client_logger >>> Should initialize the logger before "
            "using the internal spdlog capabilities");
    }
    return *m_ClientLogger;
}

auto Logger::client_logger() const -> const spdlog::logger& {
    if (m_ClientLogger == nullptr) {
        throw std::runtime_error(
            "Logger::client_logger >>> Should initialize the logger before "
            "using the internal spdlog capabilities");
    }
    return *m_ClientLogger;
}

}  // namespace utils
