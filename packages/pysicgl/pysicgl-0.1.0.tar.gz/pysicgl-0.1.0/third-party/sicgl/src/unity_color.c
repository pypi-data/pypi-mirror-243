#include "sicgl/unity_color.h"

#include <errno.h>

#include "sicgl/color.h"

static inline double clamp_double_positive_unity(double val) {
  if (val < 0.0) {
    return 0.0;
  } else if (val > 1.0) {
    return 1.0;
  } else {
    return val;
  }
}

int unity_color_from(color_t color, unity_color_t* unity) {
  int ret = 0;

  if (NULL == unity) {
    ret = -ENOMEM;
    goto out;
  }

  ret = color_components_unity_double(
      color, &unity->red, &unity->green, &unity->blue, &unity->alpha);

out:
  return ret;
}

color_t color_from_unity_color(unity_color_t unity) {
  return color_from_channels(
      color_channel_from_unity_double(unity.red),
      color_channel_from_unity_double(unity.green),
      color_channel_from_unity_double(unity.blue),
      alpha_channel_from_unity_double(unity.alpha));
}

int unity_color_clamp(unity_color_t* unity) {
  int ret = 0;

  if (NULL == unity) {
    ret = -ENOMEM;
    goto out;
  }

  unity->red = clamp_double_positive_unity(unity->red);
  unity->green = clamp_double_positive_unity(unity->green);
  unity->blue = clamp_double_positive_unity(unity->blue);
  unity->alpha = clamp_double_positive_unity(unity->alpha);

out:
  return ret;
}

int unity_color_clamp_alpha(unity_color_t* unity) {
  int ret = 0;

  if (NULL == unity) {
    ret = -ENOMEM;
    goto out;
  }

  unity->alpha = clamp_double_positive_unity(unity->alpha);

out:
  return ret;
}

int unity_color_clamp_color(unity_color_t* unity) {
  int ret = 0;

  if (NULL == unity) {
    ret = -ENOMEM;
    goto out;
  }

  unity->red = clamp_double_positive_unity(unity->red);
  unity->green = clamp_double_positive_unity(unity->green);
  unity->blue = clamp_double_positive_unity(unity->blue);

out:
  return ret;
}

int unity_color_scale(unity_color_t* unity, double factor) {
  int ret = 0;

  if (NULL == unity) {
    ret = -ENOMEM;
    goto out;
  }

  unity->red = unity->red * factor;
  unity->green = unity->green * factor;
  unity->blue = unity->blue * factor;

out:
  return ret;
}

int unity_color_premultiply(unity_color_t* unity) {
  int ret = 0;

  if (NULL == unity) {
    ret = -ENOMEM;
    goto out;
  }

  ret = unity_color_scale(unity, unity->alpha);

out:
  return ret;
}

int unity_color_un_premultiply_alpha(unity_color_t* unity, double alpha) {
  int ret = 0;

  if (NULL == unity) {
    ret = -ENOMEM;
    goto out;
  }

  unity->red = unity->red / alpha;
  unity->green = unity->green / alpha;
  unity->blue = unity->blue / alpha;

out:
  return ret;
}

int unity_color_un_premultiply(unity_color_t* unity) {
  int ret = 0;

  if (NULL == unity) {
    ret = -ENOMEM;
    goto out;
  }

  ret = unity_color_un_premultiply_alpha(unity, unity->alpha);

out:
  return ret;
}
