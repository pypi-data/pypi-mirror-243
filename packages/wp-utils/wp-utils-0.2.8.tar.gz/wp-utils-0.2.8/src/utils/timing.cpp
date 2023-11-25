#include <chrono>
#include <memory>

#include <utils/timing.hpp>

namespace utils {

auto ClockEvent::ToString() const -> std::string {
    std::string str_rep;
    str_rep += "event   : " + name + "\n\r";
    str_rep += "start   : " + std::to_string(time_start) + "\n\r";
    str_rep += "stop    : " + std::to_string(time_stop) + "\n\r";
    str_rep += "duration: " + std::to_string(time_duration) + "\n\r";
    return str_rep;
}

// NOLINTNEXTLINE : using singleton here (instance is not publicly available)
std::unique_ptr<Clock> Clock::s_Instance = nullptr;

auto Clock::Init() -> void {
    if (!s_Instance) {
        s_Instance = std::make_unique<Clock>();
    }

    // All these book-keeping variables are associated with the main event
    s_Instance->m_TimeCurrent = 0.0;
    s_Instance->m_TimeStep = 0.0;
    s_Instance->m_TimeStepAvg = 0.0;
    s_Instance->m_TimeIndex = 0;
    for (size_t i = 0; i < NUM_FRAMES_FOR_AVG; i++) {
        s_Instance->m_TimesBuffer[i] = 0.0;
        s_Instance->m_FpsBuffer[i] = 0.0;
    }
    s_Instance->m_ClockEvents.clear();
    /// Initialize main clock-event (default event that the clock keeps track
    /// of)
    s_Instance->m_ClockEvents[MAIN_EVENT] = ClockEvent();
    s_Instance->m_ClockEvents[MAIN_EVENT].name = MAIN_EVENT;
    s_Instance->m_ClockEvents[MAIN_EVENT].time_start =
        s_Instance->_TimeStampNow();
    s_Instance->m_ClockEvents[MAIN_EVENT].time_stop =
        s_Instance->_TimeStampNow();
    s_Instance->m_ClockEvents[MAIN_EVENT].time_duration = 0.0;
}

auto Clock::Release() -> void { s_Instance = nullptr; }

auto Clock::Tick(const std::string& event_name) -> void {
    LOG_CORE_ASSERT(
        s_Instance,
        "Clock::Tick >>> Must initialize clock-module before using it");
    s_Instance->_Tick(event_name);
}

auto Clock::Tock(const std::string& event_name) -> void {
    LOG_CORE_ASSERT(
        s_Instance,
        "Clock::Tock >>> Must initialize clock-module before using it");
    s_Instance->_Tock(event_name);
}

auto Clock::GetEvent(const std::string& event_name) -> ClockEvent {
    LOG_CORE_ASSERT(
        s_Instance,
        "Clock::GetEvent >>> Must initialize clock-module before using it");
    if (s_Instance->m_ClockEvents.find(event_name) ==
        s_Instance->m_ClockEvents.end()) {
        LOG_CORE_WARN(
            "Clock::GetEvent >>> event named {0} wasn't found on the set of "
            "registered clock-events",
            event_name);
        return {event_name, 0.0, 0.0, 0.0};
    }
    return s_Instance->m_ClockEvents.at(event_name);
}

auto Clock::GetWallTime() -> float {
    LOG_CORE_ASSERT(
        s_Instance,
        "Clock::GetWallTime >>> Must initialize clock-module before using it");
    return s_Instance->m_TimeCurrent;
}

auto Clock::GetTimeStep() -> float {
    LOG_CORE_ASSERT(
        s_Instance,
        "Clock::GetTimeStep >>> Must initialize clock-module before using it");
    return s_Instance->m_TimeStep;
}

auto Clock::GetAvgTimeStep() -> float {
    LOG_CORE_ASSERT(s_Instance,
                    "Clock::GetAvgTimeStep >>> Must initialize clock-module "
                    "before using it");
    return s_Instance->m_TimeStepAvg;
}

auto Clock::GetFps() -> float {
    LOG_CORE_ASSERT(
        s_Instance,
        "Clock::GetFps >>> Must initialize clock-module before using it");
    return 1.0F / s_Instance->m_TimeStep;
}

auto Clock::GetAvgFps() -> float {
    LOG_CORE_ASSERT(
        s_Instance,
        "Clock::GetAvgFps >>> Must initialize clock-module before using it");
    return 1.0F / s_Instance->m_TimeStepAvg;
}

auto Clock::GetTimeIndex() -> size_t {
    LOG_CORE_ASSERT(
        s_Instance,
        "Clock::GetTimeIndex >>> Must initialize clock-module before using it");
    return s_Instance->m_TimeIndex;
}

auto Clock::GetTimesBuffer() -> Clock::BufferArray {
    LOG_CORE_ASSERT(s_Instance,
                    "Clock::GetTimesBuffer >>> Must initialize clock-module "
                    "before using it");
    return s_Instance->m_TimesBuffer;
}

auto Clock::GetFpsBuffer() -> Clock::BufferArray {
    LOG_CORE_ASSERT(
        s_Instance,
        "Clock::GetFpsBuffer >>> Must initialize clock-module before using it");
    return s_Instance->m_FpsBuffer;
}

auto Clock::_Tick(const std::string& event_name) -> void {
    if (m_ClockEvents.find(event_name) == m_ClockEvents.end()) {
        m_ClockEvents[event_name] = ClockEvent();
        m_ClockEvents[event_name].name = event_name;
    }
    m_ClockEvents[event_name].time_start = _TimeStampNow();
}

auto Clock::_Tock(const std::string& event_name) -> void {
    if (m_ClockEvents.find(event_name) == m_ClockEvents.end()) {
        LOG_CORE_WARN(
            "Clock::_Tock >>> tried calling _Tock() with a non-started "
            "clock-event \"{0}\"",
            event_name);
        return;
    }
    m_ClockEvents[event_name].time_stop = _TimeStampNow();
    m_ClockEvents[event_name].time_duration =
        m_ClockEvents[event_name].time_stop -
        m_ClockEvents[event_name].time_start;
    if (event_name == MAIN_EVENT) {
        // @todo(wilbert): check why we couldn't use double in all sides here
        m_TimeStep =
            static_cast<float>(m_ClockEvents[MAIN_EVENT].time_duration);
        m_TimeCurrent += m_TimeStep;
        m_TimeStepAvg =
            m_TimeStepAvg +
            (m_TimeStep - m_TimesBuffer[m_TimeIndex]) / NUM_FRAMES_FOR_AVG;
        m_TimesBuffer[m_TimeIndex] = m_TimeStep;
        m_FpsBuffer[m_TimeIndex] = 1.0F / m_TimeStep;
        m_TimeIndex = (m_TimeIndex + 1) % NUM_FRAMES_FOR_AVG;
    }
}

auto Clock::_TimeStampNow() -> double {
    constexpr auto TO_SECONDS = 0.001;
    auto time_stamp_chrono = std::chrono::high_resolution_clock::now();
    auto time_stamp =
        static_cast<double>(
            std::chrono::time_point_cast<std::chrono::milliseconds>(
                time_stamp_chrono)
                .time_since_epoch()
                .count()) *
        TO_SECONDS;
    return time_stamp;
}

}  // namespace utils
