#include <string.h>

#include "sicgl/compositors.h"

void compositor_direct_set(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  memcpy(destination, source, width * bytes_per_pixel());
}

void compositor_direct_clear(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)source;
  (void)args;
  memset(destination, 0x00, width * bytes_per_pixel());
}

void compositor_direct_none(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)source;
  (void)destination;
  (void)width;
  (void)args;
}
