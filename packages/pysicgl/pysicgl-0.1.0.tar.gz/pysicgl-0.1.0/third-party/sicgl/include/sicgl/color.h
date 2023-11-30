#pragma once

#include <stddef.h>
#include <stdint.h>

// colors are represented as a system int
// https://github.com/oclyke/sicgl/issues/24
// if necessary the user can change this definition
typedef int color_t;

// size of a color_t variable in bytes (must be positive... duh)
static inline int bytes_per_pixel(void) {
  return (sizeof(color_t) / sizeof(uint8_t));
}

// tools to get individual color channels
static inline color_t color_channel_alpha(color_t color) {
  return ((color >> 24U) & 0xff);
}
static inline color_t color_channel_red(color_t color) {
  return ((color >> 16U) & 0xff);
}
static inline color_t color_channel_green(color_t color) {
  return ((color >> 8U) & 0xff);
}
static inline color_t color_channel_blue(color_t color) {
  return ((color >> 0U) & 0xff);
}

// tools to assemble color channels
static inline color_t color_from_channels(
    color_t red, color_t green, color_t blue, color_t alpha) {
  return (
      (((alpha & 0xff) << 24U) | (red & 0xff) << 16U) | ((green & 0xff) << 8U) |
      ((blue & 0xff) << 0U));
}

// tool to clamp a color channel to its valid range
static inline color_t color_channel_clamp(color_t channel) {
  if (channel > 255) {
    return 255;
  } else if (channel < 0) {
    return 0;
  } else {
    return channel;
  }
}

// tools to convert color channel to floating precision
static inline double color_channel_as_unity_double(color_t channel) {
  return (double)channel / 255.0;
}

static inline color_t color_channel_from_unity_double(double channel) {
  return (color_t)(channel * 255);
}

static inline double alpha_channel_as_unity_double(color_t channel) {
  return 1.0 - ((double)channel / 127.0);
}

static inline color_t alpha_channel_from_unity_double(double channel) {
  return (color_t)((1.0 - channel) * 127);
}

static inline int color_components_unity_double(
    color_t color, double* red, double* green, double* blue, double* alpha) {
  int ret = 0;

  if (NULL != red) {
    *red = color_channel_as_unity_double(color_channel_red(color));
  }

  if (NULL != green) {
    *green = color_channel_as_unity_double(color_channel_green(color));
  }

  if (NULL != blue) {
    *blue = color_channel_as_unity_double(color_channel_blue(color));
  }

  if (NULL != alpha) {
    *alpha = alpha_channel_as_unity_double(color_channel_alpha(color));
  }

  return ret;
}
