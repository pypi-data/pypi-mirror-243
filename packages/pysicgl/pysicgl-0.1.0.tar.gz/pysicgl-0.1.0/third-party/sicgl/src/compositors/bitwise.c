#include "sicgl/compositors.h"

void compositor_bitwise_and(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    destination[idx] = destination[idx] & source[idx];
  }
}

void compositor_bitwise_or(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    destination[idx] = destination[idx] | source[idx];
  }
}

void compositor_bitwise_xor(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    destination[idx] = destination[idx] ^ source[idx];
  }
}

void compositor_bitwise_nand(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    destination[idx] = ~(destination[idx] & source[idx]);
  }
}

void compositor_bitwise_nor(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    destination[idx] = ~(destination[idx] | source[idx]);
  }
}

void compositor_bitwise_xnor(
    color_t* source, color_t* destination, size_t width, void* args) {
  (void)args;
  for (size_t idx = 0; idx < width; idx++) {
    destination[idx] = ~(destination[idx] ^ source[idx]);
  }
}
