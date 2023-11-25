#pragma once

#include <memory>

#include <spdlog/sinks/basic_file_sink.h>
#include <spdlog/sinks/stdout_color_sinks.h>
#include <spdlog/spdlog.h>

#include <utils/common.hpp>

namespace utils {

class Logger {
    // cppcheck-suppress unknownMacro
    NO_COPY_NO_MOVE_NO_ASSIGN(Logger)

    DEFINE_SMART_POINTERS(Logger)

 public:
    /// Available types of loggers
    enum class eType : uint8_t {
        /// Allows to log messages to the console (like printf)
        CONSOLE_LOGGER,
        /// Allows to log messages to a file and save it for later usage
        FILE_LOGGER
    };

    /// Releases the resources allocated by this logger
    ~Logger() = default;

    /// Returns whether or not this logger is properly initialized
    auto ready() const -> bool { return m_Ready; }

    /// Returns the internal type of logger in use
    auto type() const -> eType { return m_Type; }

    /// Returns a mutable reference to the internal core logger
    auto core_logger() -> spdlog::logger&;

    /// Returns an unmutable reference to the internal core logger
    auto core_logger() const -> const spdlog::logger&;

    /// Returns a mutable reference to the internal client logger
    auto client_logger() -> spdlog::logger&;

    /// Returns an unmutable reference to the internal client logger
    auto client_logger() const -> const spdlog::logger&;

 public:
    /// Initialized the logging module given a mode
    static auto Init(eType logger_type = eType::CONSOLE_LOGGER) -> void;

    /// Cleans all resources used by this module
    static auto Release() -> void;

    /// Returns a mutable reference to the unique global instance (singleton)
    static auto GetInstance() -> Logger&;

 public:
    // -------------------------------------------------------------//
    // Core logging fcn calls (exposed to devs for internals usage) //
    // -------------------------------------------------------------//

    template <typename... Args>
    static auto CoreTrace(fmt::basic_string_view<char> fmt, const Args&... args)
        -> void {
        Logger::GetInstance().core_logger().trace(fmt, args...);
    }

    template <typename... Args>
    static auto CoreInfo(fmt::basic_string_view<char> fmt, const Args&... args)
        -> void {
        Logger::GetInstance().core_logger().info(fmt, args...);
    }

    template <typename... Args>
    static auto CoreWarn(fmt::basic_string_view<char> fmt, const Args&... args)
        -> void {
        Logger::GetInstance().core_logger().warn(fmt, args...);
    }

    template <typename... Args>
    static auto CoreError(fmt::basic_string_view<char> fmt, const Args&... args)
        -> void {
        Logger::GetInstance().core_logger().error(fmt, args...);
    }

    template <typename... Args>
    static auto CoreCritical(fmt::basic_string_view<char> fmt,
                             const Args&... args) -> void {
        Logger::GetInstance().core_logger().critical(fmt, args...);
        exit(EXIT_FAILURE);
    }

    template <typename... Args>
    static auto CoreAssert(bool is_not_ok, fmt::basic_string_view<char> fmt,
                           const Args&... args) -> void {
        if (!is_not_ok) {
            return;
        }

        Logger::GetInstance().core_logger().critical(fmt, args...);
        exit(EXIT_FAILURE);
    }

    //---------------------------------------------------------------------//
    // Client logging functionality (exposed to users for their own usage) //
    //---------------------------------------------------------------------//

    template <typename... Args>
    static auto ClientTrace(fmt::basic_string_view<char> fmt,
                            const Args&... args) -> void {
        Logger::GetInstance().client_logger().trace(fmt, args...);
    }

    template <typename... Args>
    static auto ClientInfo(fmt::basic_string_view<char> fmt,
                           const Args&... args) -> void {
        Logger::GetInstance().client_logger().info(fmt, args...);
    }

    template <typename... Args>
    static auto ClientWarn(fmt::basic_string_view<char> fmt,
                           const Args&... args) -> void {
        Logger::GetInstance().client_logger().warn(fmt, args...);
    }

    template <typename... Args>
    static auto ClientError(fmt::basic_string_view<char> fmt,
                            const Args&... args) -> void {
        Logger::GetInstance().client_logger().error(fmt, args...);
    }

    template <typename... Args>
    static auto ClientCritical(fmt::basic_string_view<char> fmt,
                               const Args&... args) -> void {
        Logger::GetInstance().client_logger().critical(fmt, args...);
        exit(EXIT_FAILURE);
    }

    template <typename... Args>
    static auto ClientAssert(bool is_not_ok, fmt::basic_string_view<char> fmt,
                             const Args&... args) -> void {
        if (!is_not_ok) {
            return;
        }

        Logger::GetInstance().client_logger().critical(fmt, args...);
        exit(EXIT_FAILURE);
    }

 private:
    /// Constructor for a logger given its type. Not exposed to user (singleton)
    explicit Logger(eType type);

    /// The unique instance of this logging module
    static Logger::uptr s_Instance;  // NOLINT

    /// Whether or not this logger has been initialized and can be used
    bool m_Ready = false;
    /// The type of logger, could be either write to console or to a file
    eType m_Type = eType::CONSOLE_LOGGER;
    /// The spdlog core logger (should be used for developer traces)
    std::shared_ptr<spdlog::logger> m_CoreLogger = nullptr;
    /// The spdlog client logger (should be used for user/client traces)
    std::shared_ptr<spdlog::logger> m_ClientLogger = nullptr;
};

}  // namespace utils

// NOLINTNEXTLINE
#define LOG_CORE_TRACE(...) ::utils::Logger::CoreTrace(__VA_ARGS__)
// NOLINTNEXTLINE
#define LOG_CORE_INFO(...) ::utils::Logger::CoreInfo(__VA_ARGS__)
// NOLINTNEXTLINE
#define LOG_CORE_WARN(...) ::utils::Logger::CoreWarn(__VA_ARGS__)
// NOLINTNEXTLINE
#define LOG_CORE_ERROR(...) ::utils::Logger::CoreError(__VA_ARGS__)
// NOLINTNEXTLINE
#define LOG_CORE_CRITICAL(...) ::utils::Logger::CoreCritical(__VA_ARGS__)
// NOLINTNEXTLINE
#define LOG_CORE_ASSERT(x, ...) ::utils::Logger::CoreAssert(!(x), __VA_ARGS__)

// NOLINTNEXTLINE
#define LOG_TRACE(...) ::utils::Logger::ClientTrace(__VA_ARGS__)
// NOLINTNEXTLINE
#define LOG_INFO(...) ::utils::Logger::ClientInfo(__VA_ARGS__)
// NOLINTNEXTLINE
#define LOG_WARN(...) ::utils::Logger::ClientWarn(__VA_ARGS__)
// NOLINTNEXTLINE
#define LOG_ERROR(...) ::utils::Logger::ClientError(__VA_ARGS__)
// NOLINTNEXTLINE
#define LOG_CRITICAL(...) ::utils::Logger::ClientCritical(__VA_ARGS__)
// NOLINTNEXTLINE
#define LOG_ASSERT(x, ...) ::utils::Logger::ClientAssert(!(x), __VA_ARGS__)
