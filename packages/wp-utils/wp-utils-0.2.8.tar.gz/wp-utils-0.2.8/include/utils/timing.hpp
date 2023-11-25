#pragma once

#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <unordered_map>

#include <utils/logging.hpp>

/// Number of frames used for averaging-window
constexpr size_t NUM_FRAMES_FOR_AVG = 100;
/// Name of the default event to keep track of (wall-time)
constexpr const char* MAIN_EVENT = "walltime";

namespace utils {

struct ClockEvent {
    /// Unique identifier of the event
    std::string name;
    /// Starting time-stamp of the event
    double time_start;
    /// Finishing time-stamps of the event
    double time_stop;
    /// Total duration(in seconds) of the event
    double time_duration;

    /// Returns the string representation of the event
    auto ToString() const -> std::string;
};

class Clock {
    DEFINE_SMART_POINTERS(Clock)

 public:
    /// Buffer-type used for storing times used in averaging-window
    using BufferArray = std::array<float, NUM_FRAMES_FOR_AVG>;

    /// Initialize the clock module(singleton)
    static auto Init() -> void;

    /// Releases this module(singleton) and its resources
    static auto Release() -> void;

    /// Starts tracking the time, until a Tock() is received
    static auto Tick(const std::string& event_name = MAIN_EVENT) -> void;

    /// Stop the tracking of time (started by a Tick()) and updates internal
    /// state
    static auto Tock(const std::string& event_name = MAIN_EVENT) -> void;

    /// Returns a given event by its name
    static auto GetEvent(const std::string& event_name) -> ClockEvent;

    /// Returns the current time (in seconds) since the initialization of the
    /// clock module
    static auto GetWallTime() -> float;

    /// Returns the time-step (delta-time in seconds) in between the last
    /// tick-tock request
    static auto GetTimeStep() -> float;

    /// Returns the average time-step (average delta-time in seconds) so far
    /// (since the clock module initialization)
    static auto GetAvgTimeStep() -> float;

    /// Returns the fps computed for the last tick-tock request
    static auto GetFps() -> float;

    /// Returns the average fps recorded since the initialization of the clock
    /// module
    static auto GetAvgFps() -> float;

    /// Returns the index of the current time-step in the times-buffer
    static auto GetTimeIndex() -> size_t;

    /// Returns all elements currently being processed in the time-steps window
    static auto GetTimesBuffer() -> BufferArray;

    /// Returns all elements currently being processed in the fps window
    static auto GetFpsBuffer() -> BufferArray;

 public:
    Clock() = default;

 private:
    /// Starts tracking the time of a step
    auto _Tick(const std::string& event) -> void;

    /// Stops the tracking of time of the current step, and updates internal
    /// state
    auto _Tock(const std::string& event) -> void;

    /// Returns the time-stamp in seconds since the start of the epoch
    static auto _TimeStampNow() -> double;

 private:
    /// Handle to instance of clock module (singleton)
    static Clock::uptr s_Instance;  // NOLINT
    /// Current wall time (in seconds)
    float m_TimeCurrent = 0.0F;
    /// Delta-time in between tick-tock calls (in seconds)
    float m_TimeStep = 0.0F;
    /// Average delta-time in between tick-tock calls (in seconds)
    float m_TimeStepAvg = 0.0F;
    /// Index used for average calculation and indexing in the times and fps
    /// buffers
    size_t m_TimeIndex = 0;
    /// Buffer of time values in the averaging window
    BufferArray m_TimesBuffer{};
    /// Buffer of fps-values in the averaging window
    BufferArray m_FpsBuffer{};
    /// Dictionary used to store the events by name
    std::unordered_map<std::string, ClockEvent> m_ClockEvents;
};

}  // namespace utils
