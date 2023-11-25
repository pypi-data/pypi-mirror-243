
#include <cstdint>
#include <cstring>
#include <type_traits>
#include <stdexcept>

#include <utils/obj_loader.hpp>

namespace utils {

auto ParseObjFromString(const std::string &obj_geom_str,
                        const std::string &obj_mtl_str) -> VertexData {
    tinyobj::ObjReader obj_reader;
    obj_reader.ParseFromString(obj_geom_str, obj_mtl_str);
    return _ParseObjFromReader(obj_reader);
}

auto ParseObjFromFile(const std::string &obj_file) -> VertexData {
    tinyobj::ObjReader obj_reader;
    obj_reader.ParseFromFile(obj_file);
    return _ParseObjFromReader(obj_reader);
}

auto _ParseObjFromReader(const tinyobj::ObjReader &obj_reader) -> VertexData {
    if (!obj_reader.Valid()) {
        throw std::runtime_error(
            "Something went wrong while trying to parse OBJ file");
    }

    VertexData ret;
    const auto &attrib = obj_reader.GetAttrib();
    static_assert(std::is_same<float, tinyobj::real_t>::value,
                  "Should work with same single precision f32");

    if (!obj_reader.GetShapes().empty()) {
        for (const auto &shape : obj_reader.GetShapes()) {
            for (const auto &index : shape.mesh.indices) {
                auto index_vertex_base =
                    static_cast<std::uint64_t>(3 * index.vertex_index);
                ret.vertices.emplace_back(
                    attrib.vertices[index_vertex_base + 0],
                    attrib.vertices[index_vertex_base + 1],
                    attrib.vertices[index_vertex_base + 2]);

                auto index_normal_base =
                    static_cast<std::uint64_t>(3 * index.normal_index);
                ret.normals.emplace_back(attrib.normals[index_normal_base + 0],
                                         attrib.normals[index_normal_base + 1],
                                         attrib.normals[index_normal_base + 2]);

                auto index_texcoord_base =
                    static_cast<std::uint64_t>(2 * index.texcoord_index);
                ret.texcoords.emplace_back(
                    attrib.texcoords[index_texcoord_base + 0],
                    attrib.texcoords[index_texcoord_base + 1]);
            }
        }
    }

    return ret;
}

}  // namespace utils
