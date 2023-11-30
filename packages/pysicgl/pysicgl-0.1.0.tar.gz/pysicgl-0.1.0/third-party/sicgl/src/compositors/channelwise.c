#include "sicgl/compositors.h"
#include "sicgl/private/minmax.h"
#include "sicgl/unity_color.h"

void compositor_channelwise_min(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    color_t src = source[idx];
    color_t dest = destination[idx];
    destination[idx] = color_from_channels(
        min(color_channel_red(src), color_channel_red(dest)),
        min(color_channel_green(src), color_channel_green(dest)),
        min(color_channel_blue(src), color_channel_blue(dest)),
        min(color_channel_alpha(src), color_channel_alpha(dest)));
  }
}

void compositor_channelwise_max(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    color_t src = source[idx];
    color_t dest = destination[idx];
    destination[idx] = color_from_channels(
        max(color_channel_red(src), color_channel_red(dest)),
        max(color_channel_green(src), color_channel_green(dest)),
        max(color_channel_blue(src), color_channel_blue(dest)),
        max(color_channel_alpha(src), color_channel_alpha(dest)));
  }
}

void compositor_channelwise_sum(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    color_t src = source[idx];
    color_t dest = destination[idx];
    destination[idx] = color_from_channels(
        color_channel_red(src) + color_channel_red(dest),
        color_channel_green(src) + color_channel_green(dest),
        color_channel_blue(src) + color_channel_blue(dest),
        color_channel_alpha(src) + color_channel_alpha(dest));
  }
}

void compositor_channelwise_diff(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    color_t src = source[idx];
    color_t dest = destination[idx];
    destination[idx] = color_from_channels(
        color_channel_red(src) - color_channel_red(dest),
        color_channel_green(src) - color_channel_green(dest),
        color_channel_blue(src) - color_channel_blue(dest),
        color_channel_alpha(src) - color_channel_alpha(dest));
  }
}

void compositor_channelwise_diff_reverse(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    color_t src = source[idx];
    color_t dest = destination[idx];
    destination[idx] = color_from_channels(
        color_channel_red(dest) - color_channel_red(src),
        color_channel_green(dest) - color_channel_green(src),
        color_channel_blue(dest) - color_channel_blue(src),
        color_channel_alpha(dest) - color_channel_alpha(src));
  }
}

void compositor_channelwise_multiply(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  unity_color_t src, dest;
  for (size_t idx = 0; idx < width; idx++) {
    unity_color_from(source[idx], &src);
    unity_color_from(destination[idx], &dest);
    dest.red = src.red * dest.red;
    dest.green = src.green * dest.green;
    dest.blue = src.blue * dest.blue;
    dest.alpha = src.alpha * dest.alpha;
    destination[idx] = color_from_unity_color(dest);
  }
}

void compositor_channelwise_divide(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  unity_color_t src, dest;
  for (size_t idx = 0; idx < width; idx++) {
    unity_color_from(source[idx], &src);
    unity_color_from(destination[idx], &dest);
    dest.red = src.red / dest.red;
    dest.green = src.green / dest.green;
    dest.blue = src.blue / dest.blue;
    dest.alpha = src.alpha / dest.alpha;
    destination[idx] = color_from_unity_color(dest);
  }
}

void compositor_channelwise_divide_reverse(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  unity_color_t src, dest;
  for (size_t idx = 0; idx < width; idx++) {
    unity_color_from(source[idx], &src);
    unity_color_from(destination[idx], &dest);
    dest.red = dest.red / src.red;
    dest.green = dest.green / src.green;
    dest.blue = dest.blue / src.blue;
    dest.alpha = dest.alpha / src.alpha;
    destination[idx] = color_from_unity_color(dest);
  }
}

void compositor_channelwise_sum_clamped(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    color_t src = source[idx];
    color_t dest = destination[idx];
    destination[idx] = color_from_channels(
        color_channel_clamp(color_channel_red(src) + color_channel_red(dest)),
        color_channel_clamp(
            color_channel_green(src) + color_channel_green(dest)),
        color_channel_clamp(color_channel_blue(src) + color_channel_blue(dest)),
        color_channel_clamp(
            color_channel_alpha(src) + color_channel_alpha(dest)));
  }
}

void compositor_channelwise_diff_clamped(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    color_t src = source[idx];
    color_t dest = destination[idx];
    destination[idx] = color_from_channels(
        color_channel_clamp(color_channel_red(src) - color_channel_red(dest)),
        color_channel_clamp(
            color_channel_green(src) - color_channel_green(dest)),
        color_channel_clamp(color_channel_blue(src) - color_channel_blue(dest)),
        color_channel_clamp(
            color_channel_alpha(src) - color_channel_alpha(dest)));
  }
}

void compositor_channelwise_diff_reverse_clamped(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    color_t src = source[idx];
    color_t dest = destination[idx];
    destination[idx] = color_from_channels(
        color_channel_clamp(color_channel_red(dest) - color_channel_red(src)),
        color_channel_clamp(
            color_channel_green(dest) - color_channel_green(src)),
        color_channel_clamp(color_channel_blue(dest) - color_channel_blue(src)),
        color_channel_clamp(
            color_channel_alpha(dest) - color_channel_alpha(src)));
  }
}

void compositor_channelwise_multiply_clamped(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  unity_color_t src, dest;
  for (size_t idx = 0; idx < width; idx++) {
    unity_color_from(source[idx], &src);
    unity_color_from(destination[idx], &dest);
    dest.red = src.red * dest.red;
    dest.green = src.green * dest.green;
    dest.blue = src.blue * dest.blue;
    dest.alpha = src.alpha * dest.alpha;
    unity_color_clamp(&dest);
    destination[idx] = color_from_unity_color(dest);
  }
}

void compositor_channelwise_divide_clamped(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  unity_color_t src, dest;
  for (size_t idx = 0; idx < width; idx++) {
    unity_color_from(source[idx], &src);
    unity_color_from(destination[idx], &dest);
    dest.red = src.red / dest.red;
    dest.green = src.green / dest.green;
    dest.blue = src.blue / dest.blue;
    dest.alpha = src.alpha / dest.alpha;
    unity_color_clamp(&dest);
    destination[idx] = color_from_unity_color(dest);
  }
}

void compositor_channelwise_divide_reverse_clamped(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  unity_color_t src, dest;
  for (size_t idx = 0; idx < width; idx++) {
    unity_color_from(source[idx], &src);
    unity_color_from(destination[idx], &dest);
    dest.red = dest.red / src.red;
    dest.green = dest.green / src.green;
    dest.blue = dest.blue / src.blue;
    dest.alpha = dest.alpha / src.alpha;
    unity_color_clamp(&dest);
    destination[idx] = color_from_unity_color(dest);
  }
}
