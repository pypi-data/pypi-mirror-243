#pragma once

#include <memory>
#include <random>
#include <utility>
#include <vector>

#include <math/vec2_t.hpp>

#include <utils/logging.hpp>

namespace utils {

using Vec2 = ::math::Vector2<float>;

class PerlinNoise {
 public:
    /// Initializes the perlin-noise generator module(singleton)
    static auto Init() -> void;

    /// Releases perlin-noise generator module's resources
    static auto Release() -> void;

    /// Configures the noise-generator with the given settings
    static auto Config(size_t num_octaves, float persistance, float lacunarity,
                       float noise_scale) -> void;

    /// Returns the noise value at a given 1d position
    static auto Sample1d(float x_val) -> float;

    /// Returns the noise value at a given 2d position
    static auto Sample2d(float x, float y) -> float;

    /// Returns the noise value at the given 2d position
    static auto Sample2d(const Vec2& xy) -> float;

    /// Default min-range for uniform distribution
    static constexpr float DEFAULT_RAND_MIN = -1e4F;
    /// Default max-range for uniform distribution
    static constexpr float DEFAULT_RAND_MAX = 1e4F;
    /// Default number of octaves of the noise-generator
    static constexpr size_t DEFAULT_NUM_OCTAVES = 4;
    /// Default persistance setting of the noise generator
    static constexpr float DEFAULT_PERSISTANCE = 0.5F;
    /// Default lacunarity setting of the noise generator
    static constexpr float DEFAULT_LACUNARITY = 2.0F;
    /// Default noise-scale setting of the noise generator
    static constexpr float DEFAULT_NOISE_SCALE = 10.0F;

 private:
    /// Configures the noise-generator with the given settings
    auto _Config(size_t num_octaves, float persistance, float lacunarity,
                 float noise_scale) -> void;

    /// Returns the noise value at a given 1d position
    auto _Sample1d(float x) -> float;

    /// Returns the noise value at a given 2d position
    auto _Sample2d(float x, float y) -> float;

    /// Computes the perlin-function at a given 2d position
    auto _Perlin(float x, float y) -> float;

    /// Computes the product with the gradient at a given point (perlin-noise
    /// helper function)
    static auto _DotGrad(size_t hash, float x, float y) -> float;

    /// Computes the fade-function (perlin-noise helper-function)
    static auto _Fade(float t) -> float;

    /// Computes the lerp-function (perlin-noise helper function)
    static auto _Lerp(float a, float b, float t) -> float;

 private:
    // @todo(wilbert): The static-var below are not actually accessible, but
    // could should think about it making it const? (will disable lint for now)

    /// Handle to instance of the noise-generator module(singleton)
    static std::unique_ptr<PerlinNoise> s_Instance;  // NOLINT
    /// Number of octaves used for the noise generator
    size_t m_NumOctaves = DEFAULT_NUM_OCTAVES;
    /// Persistance parameter for the noise generator
    float m_Persistance = DEFAULT_PERSISTANCE;
    /// Lacunarity parameter for the noise generator
    float m_Lacunarity = DEFAULT_LACUNARITY;
    /// Scaler for the generated noise
    float m_NoiseScale = DEFAULT_NOISE_SCALE;
    /// Permutations used for noise generation
    std::vector<size_t> m_Permutations;
    /// Random offsets used for noise generation
    std::vector<Vec2> m_OctavesOffsets;
    /// Create C++ random-engine
    std::default_random_engine m_RandEngine;
    /// Create C++ uniform real distribution
    std::uniform_real_distribution<float> m_RandUnifDist;
};

}  // namespace utils
