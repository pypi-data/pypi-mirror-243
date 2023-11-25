#pragma once

#include <cstdint>
#include <cstdlib>
#include <memory>
#include <string>
#include <vector>

namespace utils {

/// Divides a given string into substrings using the given character separator
///
/// \param txt          String to be splitted into substrings
/// \param separator    Character separator used for the splitting process
/// \return Vector of strings that form the initial string, after splitting
/// using the separator
auto Split(const std::string &txt, char separator = '/')
    -> std::vector<std::string>;

/// Gets the string representation of the hex-address of a given pointer
///
/// \param ptr  Pointer from whom to get the hex-address representation
/// \return String representation of the hex-address of the pointer
auto PointerToHexAddress(const void *ptr) -> std::string;

/// Returns a string with the contents of a given file
auto GetFileContents(const char *filepath) -> std::string;

}  // namespace utils

//----------------------------------------------------------------------------//
//       Use make_unique extension if the compiler is c++11 or older          //
//----------------------------------------------------------------------------//
#if __cplusplus <= 201103L

// make_unique implementation from Stephan T. Lavavej
// post:
// https://stackoverflow.com/questions/7038357/make-unique-and-perfect-forwarding
// url: https://isocpp.org/files/papers/N3656.txt
#include <cstddef>
#include <type_traits>
#include <utility>

namespace std {
template <class T>
struct _Unique_if {                        // NOLINT
    typedef unique_ptr<T> _Single_object;  // NOLINT
};

template <class T>
struct _Unique_if<T[]> {                     // NOLINT
    typedef unique_ptr<T[]> _Unknown_bound;  // NOLINT
};

template <class T, size_t N>
struct _Unique_if<T[N]> {       // NOLINT
    typedef void _Known_bound;  // NOLINT
};

template <class T, class... Args>  // NOLINTNEXTLINE
typename _Unique_if<T>::_Single_object make_unique(Args &&...args) {
    return unique_ptr<T>(new T(std::forward<Args>(args)...));
}

template <class T>
typename _Unique_if<T>::_Unknown_bound make_unique(size_t n) {  // NOLINT
    typedef typename remove_extent<T>::type U;                  // NOLINT
    return unique_ptr<T>(new U[n]());
}

template <class T, class... Args>  // NOLINTNEXTLINE
typename _Unique_if<T>::_Known_bound make_unique(Args &&...) = delete;
}  // namespace std

#endif /* checks that we're using c++11 or older */

//----------------------------------------------------------------------------//
//  Function-name helper macro, directive depends on the compiler being used  //
//----------------------------------------------------------------------------//
#if defined(__GNUC__)
// NOLINTNEXTLINE @todo(wilbert): might be possible to change to constexpr?
#define __FUNCTION_NAME__ __PRETTY_FUNCTION__
#elif defined(__clang__)
#define __FUNCTION_NAME__ __FUNCTION__
#elif defined(_MSC_VER)
#define __FUNCTION_NAME__ __FUNCSIG__
#endif

//----------------------------------------------------------------------------//
//              Smart pointer helper macros for class-declarations            //
//----------------------------------------------------------------------------//
// Macros based on helper-macros from habitat-sim repo
// repo: https://github.com/facebookresearch/habitat-sim
// snippet-url:
// https://github.com/facebookresearch/habitat-sim/blob/3d810b9c006976be8bd15b4ca8cf5170c5ad398d/src/esp/core/esp.h#L108
// NOLINTNEXTLINE @todo(wilbert) might be possible to change to contexpr?
#define DEFINE_SMART_POINTERS(Classname)                                  \
 public:                                                                  \
    using ptr = std::shared_ptr<Classname>;                               \
    using cptr = std::shared_ptr<const Classname>;                        \
    using uptr = std::unique_ptr<Classname>;                              \
    using cuptr = std::unique_ptr<const Classname>;                       \
    template <typename... Targs>                                          \
    static inline auto Create(Targs &&...args)->ptr {                     \
        return std::make_shared<Classname>(std::forward<Targs>(args)...); \
    }                                                                     \
    template <typename... Targs>                                          \
    static inline auto CreateUnique(Targs &&...args)->uptr {              \
        return std::make_unique<Classname>(std::forward<Targs>(args)...); \
    }

//----------------------------------------------------------------------------//
//                    RAII Rule of five helper-macro                          //
//----------------------------------------------------------------------------//
// Macro based on helper macro from drake repo:
// https://github.com/RobotLocomotion/drake/blob/master/common/drake_copyable.h
// NOLINTNEXTLINE
#define NO_COPY_NO_MOVE_NO_ASSIGN(Classname)                 \
 public:                                                     \
    Classname(const Classname &) = delete;                   \
    auto operator=(const Classname &)->Classname & = delete; \
    Classname(Classname &&) = delete;                        \
    auto operator=(Classname &&)->Classname & = delete;

// NOLINTNEXTLINE
#define DEFAULT_COPY_AND_MOVE_AND_ASSIGN(Classname)           \
    Classname(const Classname &) = default;                   \
    auto operator=(const Classname &)->Classname & = default; \
    Classname(Classname &&) = default;                        \
    auto operator=(Classname &&)->Classname & = default;
