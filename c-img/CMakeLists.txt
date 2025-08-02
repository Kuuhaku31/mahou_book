cmake_minimum_required(VERSION 3.14)
project(ImGui_SDL2_Example LANGUAGES CXX)

# ------------------------------------------------------------------------------
# 设置 C++ 标准和编译选项
# ------------------------------------------------------------------------------
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# 设置executable的输出目录
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/../bin)

# 可选：开启调试符号与警告
if(MSVC)
    add_compile_options(/W4 /Zi)
else()
    add_compile_options(-Wall -Wextra -g)
endif()

# ------------------------------------------------------------------------------
# 找到 SDL2 （假设已安装或通过包管理器安装）
# ------------------------------------------------------------------------------
find_package(SDL2 REQUIRED)
include_directories(${SDL2_INCLUDE_DIRS})

# ImGui 自带了几个 SDL + OpenGL 的示例接口实现
# 我们需要 imgui_impl_sdl.cpp、imgui_impl_opengl3.cpp 及对应头文件
set(imgui_SOURCE_DIR "D:/repositories/github/imgui")
set(IMGUI_SOURCES
    ${imgui_SOURCE_DIR}/imgui.cpp
    ${imgui_SOURCE_DIR}/imgui_demo.cpp
    ${imgui_SOURCE_DIR}/imgui_draw.cpp
    ${imgui_SOURCE_DIR}/imgui_tables.cpp
    ${imgui_SOURCE_DIR}/imgui_widgets.cpp
    ${imgui_SOURCE_DIR}/backends/imgui_impl_sdl2.cpp
    ${imgui_SOURCE_DIR}/backends/imgui_impl_opengl3.cpp
)

set(IMGUI_HEADERS
    ${imgui_SOURCE_DIR}/imgui.h
    ${imgui_SOURCE_DIR}/imconfig.h
    ${imgui_SOURCE_DIR}/imgui_internal.h
    ${imgui_SOURCE_DIR}/backends/imgui_impl_sdl2.h
    ${imgui_SOURCE_DIR}/backends/imgui_impl_opengl3.h
)

# ------------------------------------------------------------------------------
# 添加可执行目标
# ------------------------------------------------------------------------------
add_executable(${PROJECT_NAME}
    example_sdl2_opengl3.cpp # 你的主程序
    ${IMGUI_SOURCES}
    ${IMGUI_HEADERS}
)

# ------------------------------------------------------------------------------
# 包含目录
# ------------------------------------------------------------------------------
target_include_directories(${PROJECT_NAME} PRIVATE
    ${imgui_SOURCE_DIR}
    ${imgui_SOURCE_DIR}/backends
)

# ------------------------------------------------------------------------------
# 链接库：SDL2 + OpenGL
# ------------------------------------------------------------------------------
target_link_libraries(${PROJECT_NAME} PRIVATE
    ${SDL2_LIBRARIES}

    # OpenGL：在 Windows 上一般用 opengl32，在 Linux 上用 GL
    $<$<PLATFORM_ID:Windows>:opengl32>
    $<$<PLATFORM_ID:Linux>:GL>
)

# ------------------------------------------------------------------------------
# 平台特定设置（可选）
# ------------------------------------------------------------------------------
if(APPLE)
    find_library(COCOA_LIBRARY Cocoa)
    target_link_libraries(${PROJECT_NAME} PRIVATE ${COCOA_LIBRARY})
endif()
