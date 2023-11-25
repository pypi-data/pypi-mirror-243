#include <algorithm>
#include <cstdint>
#include <sstream>

#include <utils/profiling.hpp>

namespace utils {
/******************************************************************************/
/*                           Scoped Profiling Timer                           */
/******************************************************************************/

ProfilerTimer::ProfilerTimer(std::string name, std::string session)
    : m_Name(std::move(name)), m_Session(std::move(session)) {
    m_TimePointStart = std::chrono::high_resolution_clock::now();
}

ProfilerTimer::~ProfilerTimer() {
    if (!m_Stopped) {
        _Stop();
    }
}

auto ProfilerTimer::_Stop() -> void {
    auto time_point_end = std::chrono::high_resolution_clock::now();

    int64_t time_start =
        std::chrono::time_point_cast<std::chrono::microseconds>(
            m_TimePointStart)
            .time_since_epoch()
            .count();
    int64_t time_end =
        std::chrono::time_point_cast<std::chrono::microseconds>(time_point_end)
            .time_since_epoch()
            .count();
    constexpr double TO_SECONDS = 0.001;
    double time_duration =
        static_cast<double>(time_end - time_start) * TO_SECONDS;

    ProfilerResult result;
    result.name = m_Name;
    result.time_start = time_start;
    result.time_end = time_end;
    result.time_duration = time_duration;

    Profiler::WriteProfileResult(result, m_Session);
    m_Stopped = true;
}

/******************************************************************************/
/*                       Internal profiling session                           */
/******************************************************************************/

ProfilerSessionInternal::ProfilerSessionInternal(const std::string& name)
    : IProfilerSession(name) {
    m_Type = IProfilerSession::eType::INTERNAL;
}

auto ProfilerSessionInternal::Begin() -> void {
    m_Results.clear();
    m_State = IProfilerSession::eState::RUNNING;
}

auto ProfilerSessionInternal::Write(const ProfilerResult& result) -> void {
    m_Results.push_back(result);
}

auto ProfilerSessionInternal::End() -> void {
    m_State = IProfilerSession::eState::IDLE;
}

/******************************************************************************/
/*                    Chrome-tracing profiling session                        */
/******************************************************************************/

ProfilerSessionExtChrome::ProfilerSessionExtChrome(const std::string& name)
    : IProfilerSession(name) {
    m_Type = IProfilerSession::eType::EXTERNAL_CHROME;
}

auto ProfilerSessionExtChrome::Begin() -> void {
    const auto FILE_NAME = m_Name + ".json";
    m_FileWriter.open(FILE_NAME, std::ofstream::out);
    if (!m_FileWriter.is_open()) {
        LOG_CORE_WARN(
            "ProfilerSessionExtChrome::Begin >>> couldn't open session "
            "file {0}",
            FILE_NAME);
        return;
    }

    _WriteHeader();
    m_State = IProfilerSession::eState::RUNNING;
}

auto ProfilerSessionExtChrome::Write(const ProfilerResult& result) -> void {
    if (m_State != IProfilerSession::eState::RUNNING) {
        return;
    }

    std::stringstream json;
    std::string name = result.name;
    std::replace(name.begin(), name.end(), '"', '\'');

    json << ",{";
    json << R"("cat":"function",)";
    json << "\"dur\":" << (result.time_end - result.time_start) << ",";
    json << R"("name":")" << name << "\",";
    json << R"("\"ph\":\"X\",")";
    json << "\"pid\":0,";
    json << "\"tid\":0,";
    json << "\"ts\":" << result.time_start;
    json << "}";

    m_FileWriter << json.str();
    m_FileWriter.flush();
}

auto ProfilerSessionExtChrome::End() -> void {
    if (m_State != IProfilerSession::eState::RUNNING) {
        return;
    }

    _WriteFooter();
    m_FileWriter.close();
    m_State = IProfilerSession::eState::RUNNING;
}

auto ProfilerSessionExtChrome::_WriteHeader() -> void {
    m_FileWriter << R"("{\"otherData\": {},\"traceEvents\":[{}")";
    m_FileWriter.flush();
}

auto ProfilerSessionExtChrome::_WriteFooter() -> void {
    m_FileWriter << "]}";
    m_FileWriter.flush();
}

/******************************************************************************/
/*                             Profiler module                                */
/******************************************************************************/

// s_Instance is not publicly available (singleton-pattern). Disable lint check
// NOLINTNEXTLINE
std::unique_ptr<Profiler> Profiler::s_Instance = nullptr;

auto Profiler::Init(const IProfilerSession::eType& type) -> void {
    if (!s_Instance) {
        s_Instance = std::unique_ptr<Profiler>(new Profiler(type));
    }
    Profiler::BeginSession(DEFAULT_SESSION);
}

auto Profiler::Release() -> void {
    Profiler::EndSession(DEFAULT_SESSION);
    s_Instance = nullptr;
}

auto Profiler::BeginSession(const std::string& session_name) -> void {
    LOG_CORE_ASSERT(s_Instance,
                    "Profiler::BeginSession >>> Profiler module must be "
                    "initialized before using it");
    s_Instance->_BeginSession(session_name);
}

auto Profiler::EndSession(const std::string& session_name) -> void {
    LOG_CORE_ASSERT(s_Instance,
                    "Profiler::EndSession >>> Profiler module must be "
                    "initialized before using it");
    s_Instance->_EndSession(session_name);
}

auto Profiler::WriteProfileResult(const ProfilerResult& result,
                                  const std::string& session_name) -> void {
    LOG_CORE_ASSERT(s_Instance,
                    "Profiler::WriteProfileResult >>> Profiler module must "
                    "be initialized before using it");
    s_Instance->_WriteProfileResult(result, session_name);
}

auto Profiler::GetSessions() -> std::vector<IProfilerSession*> {
    LOG_CORE_ASSERT(s_Instance,
                    "Profiler::GetSessions >>> Profiler module must be "
                    "initialized before using it");
    return s_Instance->_GetSessions();
}

auto Profiler::_BeginSession(const std::string& session_name) -> void {
    if (m_Sessions.find(session_name) == m_Sessions.end()) {
        if (m_ProfilerType == IProfilerSession::eType::INTERNAL) {
            m_Sessions[session_name] =
                std::make_unique<ProfilerSessionInternal>(session_name);
        } else {
            m_Sessions[session_name] =
                std::make_unique<ProfilerSessionExtChrome>(session_name);
        }
    }
    m_Sessions[session_name]->Begin();
}

auto Profiler::_EndSession(const std::string& session_name) -> void {
    if (m_Sessions.find(session_name) == m_Sessions.end()) {
        LOG_CORE_WARN(
            "Profiler::_EndSession() >>> session with name {0} not found",
            session_name);
    } else {
        m_Sessions[session_name]->End();
    }
}

auto Profiler::_WriteProfileResult(const ProfilerResult& result,
                                   const std::string& session_name) -> void {
    if (m_Sessions.find(session_name) == m_Sessions.end()) {
        LOG_CORE_WARN(
            "Profiler::_WriteProfileResult() >>> session with name {0} not "
            "found",
            session_name);
    } else {
        m_Sessions[session_name]->Write(result);
    }
}

auto Profiler::_GetSessions() -> std::vector<IProfilerSession*> {
    std::vector<IProfilerSession*> vec_sessions(m_Sessions.size());
    for (auto& kvpair : m_Sessions) {
        vec_sessions.push_back(kvpair.second.get());
    }
    return vec_sessions;
}

}  // namespace utils
