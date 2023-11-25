#include <catch2/catch.hpp>
#include <utils/logging.hpp>

// NOLINTNEXTLINE
TEST_CASE("Testing logging module", "[Logging]") {
    SECTION("Init and Release") {
        // Should be able to initialize without exceptions thrown
        ::utils::Logger::Init();
        // The logger should be READY by now
        REQUIRE(::utils::Logger::GetInstance().ready() == true);
        // By default, the logger is initialized to console-logger
        REQUIRE(::utils::Logger::GetInstance().type() ==
                ::utils::Logger::eType::CONSOLE_LOGGER);
        // Should be able to log some messages to the console
        LOG_CORE_TRACE("Just a simple core TRACE log");
        LOG_CORE_INFO("Just a simple core INFO log");
        LOG_CORE_WARN("Just a simple core WARN log");
        LOG_CORE_ERROR("Just a simple core ERROR log");
        LOG_CORE_ASSERT(2 + 2 == 4, "Just a simple core ASSERT statement");

        LOG_TRACE("Just a simple client TRACE log");
        LOG_INFO("Just a simple client INFO log");
        LOG_WARN("Just a simple client WARN log");
        LOG_ERROR("Just a simple client ERROR log");
        LOG_ASSERT(1 + 3 == 4, "Just a simple client ASSERT statement");
        // Should be able to release without exceptions being thrown
        ::utils::Logger::Release();

        // Should be able to initialize again; will create new spdloggers
        // internally
        ::utils::Logger::Init(::utils::Logger::eType::FILE_LOGGER);
        // The logger should be READY by now
        REQUIRE(::utils::Logger::GetInstance().ready() == true);
        // The logger should be initialized to file-logger
        REQUIRE(::utils::Logger::GetInstance().type() ==
                ::utils::Logger::eType::FILE_LOGGER);
        // Should be able to log to a file
        LOG_CORE_TRACE("Just a simple core TRACE log");
        LOG_CORE_INFO("Just a simple core INFO log");
        LOG_CORE_WARN("Just a simple core WARN log");
        LOG_CORE_ERROR("Just a simple core ERROR log");
        LOG_CORE_ASSERT(2 + 2 == 4, "Just a simple core ASSERT statement");

        LOG_TRACE("Just a simple client TRACE log");
        LOG_INFO("Just a simple client INFO log");
        LOG_WARN("Just a simple client WARN log");
        LOG_ERROR("Just a simple client ERROR log");
        LOG_ASSERT(1 + 3 == 4, "Just a simple client ASSERT statement");
        // Should be able to release without exceptions being thrown
        ::utils::Logger::Release();
    }
    SECTION("Auto initialization") {
        // Should be fine to call the logger directly. If no instance, it should
        // be created on the fly to allow the log call to work
        LOG_CORE_TRACE(
            "Should be able to log directly. Creates a console logger");
        REQUIRE(::utils::Logger::GetInstance().ready() == true);
        REQUIRE(::utils::Logger::GetInstance().type() ==
                ::utils::Logger::eType::CONSOLE_LOGGER);
        ::utils::Logger::Release();
    }
}
