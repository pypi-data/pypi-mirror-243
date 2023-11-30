#pragma once

#include "sicgl/color.h"
#include "sicgl/interface.h"
#include "sicgl/screen.h"

typedef void (*blender_fn)(
    color_t* source, color_t* destination, size_t width, void* args);
int sicgl_blend(
    interface_t* interface, screen_t* screen, color_t* sprite,
    blender_fn blender, void* args);
