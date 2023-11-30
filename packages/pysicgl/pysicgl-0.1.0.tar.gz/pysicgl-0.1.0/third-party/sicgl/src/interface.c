#include "sicgl/interface.h"

#include <errno.h>
#include <stdbool.h>
#include <stddef.h>

#include "sicgl/debug.h"
#include "sicgl/private/minmax.h"

int sicgl_interface_get_pixel_offset(
    interface_t* interface, uext_t offset, color_t* color) {
  int ret = 0;
  if (NULL == interface->memory) {
    goto out;
  }
  if (NULL == color) {
    goto out;
  }
  if (offset >= interface->length) {
    goto out;
  }
  *color = interface->memory[offset];
out:
  return ret;
}

int sicgl_interface_get_pixel(
    interface_t* interface, uext_t u, uext_t v, color_t* color) {
  int ret = 0;
  if (NULL == interface->memory) {
    goto out;
  }
  if (NULL == interface->screen) {
    goto out;
  }
  if (u >= interface->screen->width) {
    goto out;
  }
  if (v >= interface->screen->height) {
    goto out;
  }
  size_t offset = interface->screen->width * v + u;
out:
  ret = sicgl_interface_get_pixel_offset(interface, offset, color);
  return ret;
}
