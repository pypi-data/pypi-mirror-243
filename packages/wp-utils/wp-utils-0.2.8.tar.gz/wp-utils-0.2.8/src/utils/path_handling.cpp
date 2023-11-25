#include <sstream>

#include <utils/path_handling.hpp>

namespace utils {

auto GetFilename(const std::string &filepath) -> std::string {
    return Split(filepath, '/').back();
}

auto GetFoldername(const std::string &filepath) -> std::string {
    auto path_parts = Split(filepath, '/');
    if (path_parts.size() < 2) {
        return "./";
    }

    return path_parts[path_parts.size() - 2];
}

auto GetFolderpath(const std::string &filepath) -> std::string {
    auto path_parts = Split(filepath, '/');
    if (path_parts.size() < 2) {
        return "./";
    }

    std::stringstream ss;
    for (size_t i = 0; i < path_parts.size() - 1; ++i) {
        ss << path_parts[i] << "/";
    }

    return ss.str();
}

auto GetFilenameNoExtension(const std::string &filepath) -> std::string {
    return Split(Split(filepath, '/').back(), '.').front();
}

}  // namespace utils
