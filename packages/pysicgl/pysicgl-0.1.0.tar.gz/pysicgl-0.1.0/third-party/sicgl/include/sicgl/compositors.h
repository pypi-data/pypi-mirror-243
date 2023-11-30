#pragma once

#include "sicgl/color.h"

// direct compositors
void compositor_direct_set(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_direct_clear(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_direct_none(
    color_t* source, color_t* destination, size_t width, void* args);

// bitwise compositors
void compositor_bitwise_and(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_bitwise_or(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_bitwise_xor(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_bitwise_nand(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_bitwise_nor(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_bitwise_xnor(
    color_t* source, color_t* destination, size_t width, void* args);

// channelwise compositors
void compositor_channelwise_min(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_channelwise_max(
    color_t* source, color_t* destination, size_t width, void* args);

void compositor_channelwise_sum(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_channelwise_diff(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_channelwise_diff_reverse(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_channelwise_multiply(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_channelwise_divide(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_channelwise_divide_reverse(
    color_t* source, color_t* destination, size_t width, void* args);

void compositor_channelwise_sum_clamped(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_channelwise_diff_clamped(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_channelwise_diff_reverse_clamped(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_channelwise_multiply_clamped(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_channelwise_divide_clamped(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_channelwise_divide_reverse_clamped(
    color_t* source, color_t* destination, size_t width, void* args);

// porter-duff alpha compositing
void compositor_alpha_clear(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_alpha_copy(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_alpha_destination(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_alpha_source_over(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_alpha_destination_over(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_alpha_source_in(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_alpha_destination_in(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_alpha_source_out(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_alpha_destination_out(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_alpha_source_atop(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_alpha_destination_atop(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_alpha_xor(
    color_t* source, color_t* destination, size_t width, void* args);
void compositor_alpha_lighter(
    color_t* source, color_t* destination, size_t width, void* args);
