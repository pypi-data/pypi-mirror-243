#pragma once

#include <string>

#include <utils/common.hpp>

namespace utils {

/// Gets the stripped filename from an absolute full-path
///
/// \param filepath     Absolute path from which to strip the filename
/// \return String representing the filename stripped from the given fullpath
auto GetFilename(const std::string &filepath) -> std::string;

/// Gets the stripped foldername from an absolute full-path
///
/// \param filepath     Absolute path from which to strip the foldername
/// \return String representing the foldername stripped from the given fullpath
auto GetFoldername(const std::string &filepath) -> std::string;

/// Gets the folderpath (path with removed filename) from an absolute full-path
///
/// \param filepath     Absolute path from which to strip the folderpath
/// \return String representing the folderpath stripped from the given fullpath
auto GetFolderpath(const std::string &filepath) -> std::string;

/// Gets the stripped filename from an absolute full-path, and removes the file
/// extension
///
/// \param filepath     Absolute path from which to strip the filename
/// \return String representing the filename (without extension) stripped from
/// the given fullpath
auto GetFilenameNoExtension(const std::string &filepath) -> std::string;

}  // namespace utils
