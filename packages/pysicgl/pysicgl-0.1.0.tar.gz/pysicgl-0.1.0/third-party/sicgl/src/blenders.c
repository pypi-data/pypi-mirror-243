#include "sicgl/blenders.h"

#include <math.h>

#include "sicgl/private/minmax.h"
#include "sicgl/unity_color.h"

// some tools for color channel manipulation
static inline double channel_color_multiply(double memory, double source) {
  return memory * source;
}

static inline double channel_color_screen(double memory, double source) {
  return memory + source - memory * source;
}

static inline double channel_color_dodge(double memory, double source) {
  if (source == 1.0) {
    return 1.0;
  } else if (memory == 0.0) {
    return 0.0;
  } else {
    return min(1.0, memory / (1.0 - source));
  }
}

static inline double channel_color_burn(double memory, double source) {
  if (memory == 1.0) {
    return 1.0;
  } else if (source == 0.0) {
    return 0.0;
  } else {
    return 1.0 - min(1.0, (1.0 - memory) / source);
  }
}

static inline double channel_color_hard_light(double memory, double source) {
  if (source <= 0.5) {
    return channel_color_multiply(memory, (2.0 * source));
  } else {
    return channel_color_screen(memory, (2.0 * source) - 1.0);
  }
}

static inline double channel_color_soft_light(double memory, double source) {
  if (source <= 0.5) {
    return memory - ((1 - (2 * source)) * memory * (1 - memory));
  } else {
    double d;
    if (memory < 0.25) {
      d = (((16 * memory) - 12) * memory + 4) * memory;
    } else {
      d = sqrt(memory);
    }
    return memory + ((2 * (source - 1)) * (d - memory));
  }
}

static inline color_t color_multiply(unity_color_t Cmem, unity_color_t Csrc) {
  Cmem.red = Cmem.red * Csrc.red;
  Cmem.green = Cmem.green * Csrc.green;
  Cmem.blue = Cmem.blue * Csrc.blue;
  unity_color_clamp(&Cmem);
  return color_from_unity_color(Cmem);
}

static inline color_t color_screen(unity_color_t Cmem, unity_color_t Csrc) {
  Cmem.red = channel_color_screen(Cmem.red, Csrc.red);
  Cmem.green = channel_color_screen(Cmem.green, Csrc.green);
  Cmem.blue = channel_color_screen(Cmem.blue, Csrc.blue);
  unity_color_clamp(&Cmem);
  return color_from_unity_color(Cmem);
}

// separable blending
void blend_normal(color_t* memory, color_t* source, size_t width, void* args) {
  // do nothing - normal blending ignores the source and keeps only the memory
  (void)memory;
  (void)source;
  (void)width;
  (void)args;
}

void blend_forget(color_t* memory, color_t* source, size_t width, void* args) {
  // forget will ignore the memory value and use only the backdrop
  // however the alpha component of the memory is retained
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    color_t mem = memory[idx];
    color_t src = source[idx];
    memory[idx] = color_from_channels(
        color_channel_red(src), color_channel_green(src),
        color_channel_blue(src), color_channel_alpha(mem));
  }
}

void blend_multiply(
    color_t* memory, color_t* source, size_t width, void* args) {
  (void)args;
  unity_color_t Cmem, Csrc;
  for (size_t idx = 0; idx < width; idx++) {
    unity_color_from(memory[idx], &Cmem);
    unity_color_from(source[idx], &Csrc);
    memory[idx] = color_multiply(Cmem, Csrc);
  }
}

void blend_screen(color_t* memory, color_t* source, size_t width, void* args) {
  (void)args;
  unity_color_t Cmem, Csrc;
  for (size_t idx = 0; idx < width; idx++) {
    unity_color_from(memory[idx], &Cmem);
    unity_color_from(source[idx], &Csrc);
    memory[idx] = color_screen(Cmem, Csrc);
  }
}

void blend_overlay(color_t* memory, color_t* source, size_t width, void* args) {
  blend_hard_light(source, memory, width, args);
}

void blend_darken(color_t* memory, color_t* source, size_t width, void* args) {
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    color_t src = source[idx];
    color_t mem = memory[idx];
    memory[idx] = color_from_channels(
        min(color_channel_red(src), color_channel_red(mem)),
        min(color_channel_green(src), color_channel_green(mem)),
        min(color_channel_blue(src), color_channel_blue(mem)),
        min(color_channel_alpha(src), color_channel_alpha(mem)));
  }
}

void blend_lighten(color_t* memory, color_t* source, size_t width, void* args) {
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    color_t src = source[idx];
    color_t mem = memory[idx];
    memory[idx] = color_from_channels(
        max(color_channel_red(src), color_channel_red(mem)),
        max(color_channel_green(src), color_channel_green(mem)),
        max(color_channel_blue(src), color_channel_blue(mem)),
        max(color_channel_alpha(src), color_channel_alpha(mem)));
  }
}

void blend_color_dodge(
    color_t* memory, color_t* source, size_t width, void* args) {
  (void)args;
  unity_color_t Cmem, Csrc;
  for (size_t idx = 0; idx < width; idx++) {
    unity_color_from(memory[idx], &Cmem);
    unity_color_from(source[idx], &Csrc);
    Cmem.red = channel_color_dodge(Cmem.red, Csrc.red);
    Cmem.green = channel_color_dodge(Cmem.green, Csrc.green);
    Cmem.blue = channel_color_dodge(Cmem.blue, Csrc.blue);
    unity_color_clamp(&Cmem);
    memory[idx] = color_from_unity_color(Cmem);
  }
}

void blend_color_burn(
    color_t* memory, color_t* source, size_t width, void* args) {
  (void)args;
  unity_color_t Cmem, Csrc;
  for (size_t idx = 0; idx < width; idx++) {
    unity_color_from(memory[idx], &Cmem);
    unity_color_from(source[idx], &Csrc);
    Cmem.red = channel_color_burn(Cmem.red, Csrc.red);
    Cmem.green = channel_color_burn(Cmem.green, Csrc.green);
    Cmem.blue = channel_color_burn(Cmem.blue, Csrc.blue);
    unity_color_clamp(&Cmem);
    memory[idx] = color_from_unity_color(Cmem);
  }
}

void blend_hard_light(
    color_t* memory, color_t* source, size_t width, void* args) {
  (void)args;
  unity_color_t Cmem, Csrc;
  for (size_t idx = 0; idx < width; idx++) {
    unity_color_from(memory[idx], &Cmem);
    unity_color_from(source[idx], &Csrc);
    Cmem.red = channel_color_hard_light(Cmem.red, Csrc.red);
    Cmem.green = channel_color_hard_light(Cmem.green, Csrc.green);
    Cmem.blue = channel_color_hard_light(Cmem.blue, Csrc.blue);
    unity_color_clamp(&Cmem);
    memory[idx] = color_from_unity_color(Cmem);
  }
}

void blend_soft_light(
    color_t* memory, color_t* source, size_t width, void* args) {
  (void)args;
  unity_color_t Cmem, Csrc;
  for (size_t idx = 0; idx < width; idx++) {
    unity_color_from(memory[idx], &Cmem);
    unity_color_from(source[idx], &Csrc);
    Cmem.red = channel_color_soft_light(Cmem.red, Csrc.red);
    Cmem.green = channel_color_soft_light(Cmem.green, Csrc.green);
    Cmem.blue = channel_color_soft_light(Cmem.blue, Csrc.blue);
    unity_color_clamp(&Cmem);
    memory[idx] = color_from_unity_color(Cmem);
  }
}

void blend_difference(
    color_t* memory, color_t* source, size_t width, void* args) {
  (void)args;
  unity_color_t Cmem, Csrc;
  for (size_t idx = 0; idx < width; idx++) {
    unity_color_from(memory[idx], &Cmem);
    unity_color_from(source[idx], &Csrc);
    Cmem.red = fabs(Cmem.red - Csrc.red);
    Cmem.green = fabs(Cmem.green - Csrc.green);
    Cmem.blue = fabs(Cmem.blue - Csrc.blue);
    unity_color_clamp(&Cmem);
    memory[idx] = color_from_unity_color(Cmem);
  }
}

void blend_exclusion(
    color_t* memory, color_t* source, size_t width, void* args) {
  (void)args;
  unity_color_t Cmem, Csrc;
  for (size_t idx = 0; idx < width; idx++) {
    unity_color_from(memory[idx], &Cmem);
    unity_color_from(source[idx], &Csrc);
    Cmem.red = Cmem.red + Csrc.red - 2.0 * Cmem.red * Csrc.red;
    Cmem.green = Cmem.green + Csrc.green - 2.0 * Cmem.green * Csrc.green;
    Cmem.blue = Cmem.blue + Csrc.blue - 2.0 * Cmem.blue * Csrc.blue;
    unity_color_clamp(&Cmem);
    memory[idx] = color_from_unity_color(Cmem);
  }
}

// // non-seperable blending
// void blend_hue(color_t* memory, color_t* source, size_t width, void* args);
// void blend_saturation(color_t* memory, color_t* source, size_t width, void*
// args); void blend_color(color_t* memory, color_t* source, size_t width, void*
// args); void blend_luminosity(color_t* memory, color_t* source, size_t width,
// void* args);
