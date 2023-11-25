#include <utils/perlin_noise.hpp>

namespace utils {

// @todo(wilbert): The variables below are not actually accessible, but
// could should think about it making it const? (will disable lint for now)
std::unique_ptr<PerlinNoise> PerlinNoise::s_Instance = nullptr;  // NOLINT

auto PerlinNoise::Init() -> void {
    // Initialize singleton (can't use make_unique for now, as const is private)
    if (!s_Instance) {
        s_Instance = std::make_unique<PerlinNoise>();
    }

    // Initialize uniform distribution
    s_Instance->m_RandUnifDist = std::uniform_real_distribution<float>(
        DEFAULT_RAND_MIN, DEFAULT_RAND_MAX);

    s_Instance->m_NumOctaves = DEFAULT_NUM_OCTAVES;
    s_Instance->m_Persistance = DEFAULT_PERSISTANCE;
    s_Instance->m_Lacunarity = DEFAULT_LACUNARITY;
    s_Instance->m_NoiseScale = DEFAULT_NOISE_SCALE;

    s_Instance->m_OctavesOffsets.clear();
    for (size_t i = 0; i < s_Instance->m_NumOctaves; i++) {
        s_Instance->m_OctavesOffsets.emplace_back(
            s_Instance->m_RandUnifDist(s_Instance->m_RandEngine),
            s_Instance->m_RandUnifDist(s_Instance->m_RandEngine));
    }

    // Initialize the permutation vector with ken perlin's reference permutation
    // and double it to avoid overflow
    // clang-format off
    s_Instance->m_Permutations = {
        151, 160, 137, 91,  90,  15,  131, 13,  201, 95,  96,  53,  194, 233,// NOLINT
        7,   225, 140, 36,  103, 30,  69,  142, 8,   99,  37,  240, 21,  10,// NOLINT
        23,  190, 6,   148, 247, 120, 234, 75,  0,   26,  197, 62,  94,  252,// NOLINT
        219, 203, 117, 35,  11,  32,  57,  177, 33,  88,  237, 149, 56,  87,// NOLINT
        174, 20,  125, 136, 171, 168, 68,  175, 74,  165, 71,  134, 139, 48,// NOLINT
        27,  166, 77,  146, 158, 231, 83,  111, 229, 122, 60,  211, 133, 230,// NOLINT
        220, 105, 92,  41,  55,  46,  245, 40,  244, 102, 143, 54,  65,  25,// NOLINT
        63,  161, 1,   216, 80,  73,  209, 76,  132, 187, 208, 89,  18,  169,// NOLINT
        200, 196, 135, 130, 116, 188, 159, 86,  164, 100, 109, 198, 173, 186,// NOLINT
        3,   64,  52,  217, 226, 250, 124, 123, 5,   202, 38,  147, 118, 126,// NOLINT
        255, 82,  85,  212, 207, 206, 59,  227, 47,  16,  58,  17,  182, 189,// NOLINT
        28,  42,  223, 183, 170, 213, 119, 248, 152, 2,   44,  154, 163, 70,// NOLINT
        221, 153, 101, 155, 167, 43,  172, 9,   129, 22,  39,  253, 19,  98,// NOLINT
        108, 110, 79,  113, 224, 232, 178, 185, 112, 104, 218, 246, 97,  228,// NOLINT
        251, 34,  242, 193, 238, 210, 144, 12,  191, 179, 162, 241, 81,  51,// NOLINT
        145, 235, 249, 14,  239, 107, 49,  192, 214, 31,  181, 199, 106, 157,// NOLINT
        184, 84,  204, 176, 115, 121, 50,  45,  127, 4,   150, 254, 138, 236,// NOLINT
        205, 93,  222, 114, 67,  29,  24,  72,  243, 141, 128, 195, 78,  66,// NOLINT
        215, 61,  156, 180};// NOLINT
    // clang-format on
    s_Instance->m_Permutations.insert(s_Instance->m_Permutations.end(),
                                      s_Instance->m_Permutations.begin(),
                                      s_Instance->m_Permutations.end());
}

auto PerlinNoise::Release() -> void { s_Instance = nullptr; }

auto PerlinNoise::Config(size_t num_octaves, float persistance,
                         float lacunarity, float noise_scale) -> void {
    LOG_CORE_ASSERT(s_Instance,
                    "PerlinNoise::Config >>> Must initialize perlin-noise "
                    "module before using it");
    s_Instance->_Config(num_octaves, persistance, lacunarity, noise_scale);
}

auto PerlinNoise::Sample1d(float x) -> float {
    LOG_CORE_ASSERT(s_Instance,
                    "PerlinNoise::Sample1d >>> Must initialize perlin-noise "
                    "module before using it");
    return s_Instance->_Sample1d(x);
}

auto PerlinNoise::Sample2d(float x, float y) -> float {
    LOG_CORE_ASSERT(s_Instance,
                    "PerlinNoise::Sample2d >>> Must initialize perlin-noise "
                    "module before using it");
    return s_Instance->_Sample2d(x, y);
}

auto PerlinNoise::Sample2d(const Vec2& xy) -> float {
    LOG_CORE_ASSERT(s_Instance,
                    "PerlinNoise::Sample2d >>> Must initialize perlin-noise "
                    "module before using it");
    return s_Instance->_Sample2d(xy.x(), xy.y());
}

auto PerlinNoise::_Config(size_t num_octaves, float persistance,
                          float lacunarity, float noise_scale) -> void {
    m_NumOctaves = num_octaves;
    m_Persistance = persistance;
    m_Lacunarity = lacunarity;
    m_NoiseScale = noise_scale;

    m_OctavesOffsets.clear();
    for (size_t o = 0; o < m_NumOctaves; o++) {
        m_OctavesOffsets.emplace_back(
            s_Instance->m_RandUnifDist(s_Instance->m_RandEngine),
            s_Instance->m_RandUnifDist(s_Instance->m_RandEngine));
    }
}

auto PerlinNoise::_Sample1d(float x) -> float { return _Sample2d(x, 0.0F); }

auto PerlinNoise::_Sample2d(float x, float y) -> float {
    float ampl = 1.0F;
    float freq = 1.0F;
    float noise_value = 0.0F;

    for (size_t i = 0; i < m_NumOctaves; i++) {
        float sample_x = freq * (x / m_NoiseScale) + m_OctavesOffsets[i].x();
        float sample_y = freq * (y / m_NoiseScale) + m_OctavesOffsets[i].y();
        noise_value += ampl * _Perlin(sample_x, sample_y);
        ampl *= m_Persistance;
        freq *= m_Lacunarity;
    }
    return noise_value;
}

auto PerlinNoise::_Fade(float t) -> float {
    constexpr float KA = 6.0F;
    constexpr float KB = -15.0F;
    constexpr float KC = 10.0F;
    return t * t * t * (t * (t * KA + KB) + KC);
}

auto PerlinNoise::_Lerp(float a, float b, float t) -> float {
    return (1 - t) * a + t * b;
}

auto PerlinNoise::_DotGrad(size_t hash, float x, float y) -> float {
    constexpr auto MASK_LSB = 0xf;
    // Get the LSB from the hash to get the gradient direction
    const auto HASH_LSB = hash & MASK_LSB;
    // hash results for (x+y) direction
    constexpr auto GRAD_DIR_00_0 = 0x0;
    constexpr auto GRAD_DIR_00_1 = 0x4;
    constexpr auto GRAD_DIR_00_2 = 0x8;
    constexpr auto GRAD_DIR_00_3 = 0xc;
    // hash results for (-x+y) direction
    constexpr auto GRAD_DIR_01_0 = 0x1;
    constexpr auto GRAD_DIR_01_1 = 0x5;
    constexpr auto GRAD_DIR_01_2 = 0x9;
    constexpr auto GRAD_DIR_01_3 = 0xd;
    // hash results for (x-y) direction
    constexpr auto GRAD_DIR_10_0 = 0x2;
    constexpr auto GRAD_DIR_10_1 = 0x6;
    constexpr auto GRAD_DIR_10_2 = 0xa;
    constexpr auto GRAD_DIR_10_3 = 0xe;
    // hash results for (-x-y) direction
    constexpr auto GRAD_DIR_11_0 = 0x3;
    constexpr auto GRAD_DIR_11_1 = 0x7;
    constexpr auto GRAD_DIR_11_2 = 0xb;
    constexpr auto GRAD_DIR_11_3 = 0xf;
    // Because we are in 2d, there are just 4 options for the gradient vectors
    // and so, just 4 options for the dot product
    switch (HASH_LSB) {
        case GRAD_DIR_00_0:
        case GRAD_DIR_00_1:
        case GRAD_DIR_00_2:
        case GRAD_DIR_00_3:
            return x + y;
        case GRAD_DIR_01_0:
        case GRAD_DIR_01_1:
        case GRAD_DIR_01_2:
        case GRAD_DIR_01_3:
            return -x + y;
        case GRAD_DIR_10_0:
        case GRAD_DIR_10_1:
        case GRAD_DIR_10_2:
        case GRAD_DIR_10_3:
            return x - y;
        case GRAD_DIR_11_0:
        case GRAD_DIR_11_1:
        case GRAD_DIR_11_2:
        case GRAD_DIR_11_3:
            return -x - y;
    }

    return 0.0F;
}

auto PerlinNoise::_Perlin(float x, float y) -> float {
    // Calculate unit square position in grid (wrap around by 256)
    const size_t X_INDX = static_cast<size_t>(std::floor(x)) & 255;
    const size_t Y_INDX = static_cast<size_t>(std::floor(y)) & 255;

    // Calculate relative position [0-1] inside unit-square
    const float X_F = x - std::floor(x);
    const float Y_F = y - std::floor(y);

    // Smooth using easing-function for smooth interpolation
    const float U = _Fade(X_F);
    const float V = _Fade(Y_F);

    const size_t HASH_00 = m_Permutations[m_Permutations[X_INDX] + Y_INDX];
    const size_t HASH_01 = m_Permutations[m_Permutations[X_INDX] + Y_INDX + 1];
    const size_t HASH_10 = m_Permutations[m_Permutations[X_INDX + 1] + Y_INDX];
    const size_t HASH_11 =
        m_Permutations[m_Permutations[X_INDX + 1] + Y_INDX + 1];

    const float D_00 = _DotGrad(HASH_00, X_F, Y_F);
    const float D_01 = _DotGrad(HASH_01, X_F, Y_F - 1.0F);
    const float D_10 = _DotGrad(HASH_10, X_F - 1.0F, Y_F);
    const float D_11 = _DotGrad(HASH_11, X_F - 1.0F, Y_F - 1.0F);

    return _Lerp(_Lerp(D_00, D_10, U), _Lerp(D_01, D_11, U), V);
}

}  // namespace utils
