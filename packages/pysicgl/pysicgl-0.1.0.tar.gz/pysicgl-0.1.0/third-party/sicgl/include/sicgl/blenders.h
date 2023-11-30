#include "sicgl/color.h"

// seperable blending
void blend_normal(color_t* memory, color_t* source, size_t width, void* args);
void blend_forget(color_t* memory, color_t* source, size_t width, void* args);
void blend_multiply(color_t* memory, color_t* source, size_t width, void* args);
void blend_screen(color_t* memory, color_t* source, size_t width, void* args);
void blend_overlay(color_t* memory, color_t* source, size_t width, void* args);
void blend_darken(color_t* memory, color_t* source, size_t width, void* args);
void blend_lighten(color_t* memory, color_t* source, size_t width, void* args);
void blend_color_dodge(
    color_t* memory, color_t* source, size_t width, void* args);
void blend_color_burn(
    color_t* memory, color_t* source, size_t width, void* args);
void blend_hard_light(
    color_t* memory, color_t* source, size_t width, void* args);
void blend_soft_light(
    color_t* memory, color_t* source, size_t width, void* args);
void blend_difference(
    color_t* memory, color_t* source, size_t width, void* args);
void blend_exclusion(
    color_t* memory, color_t* source, size_t width, void* args);

// // non-seperable blending
// void blend_hue(color_t* memory, color_t* source, size_t width, void* args);
// void blend_saturation(color_t* memory, color_t* source, size_t width, void*
// args); void blend_color(color_t* memory, color_t* source, size_t width, void*
// args); void blend_luminosity(color_t* memory, color_t* source, size_t width,
// void* args);
