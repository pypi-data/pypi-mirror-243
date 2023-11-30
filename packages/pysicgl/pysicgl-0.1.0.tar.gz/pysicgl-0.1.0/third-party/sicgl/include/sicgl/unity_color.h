#include <stdbool.h>

#include "sicgl/color.h"

typedef struct _unity_color_t {
  double red;
  double green;
  double blue;
  double alpha;
} unity_color_t;

int unity_color_from(color_t color, unity_color_t* unity);
color_t color_from_unity_color(unity_color_t unity);

int unity_color_clamp(unity_color_t* unity);
int unity_color_clamp_alpha(unity_color_t* unity);
int unity_color_clamp_color(unity_color_t* unity);

int unity_color_scale(unity_color_t* unity, double factor);

int unity_color_premultiply(unity_color_t* unity);
int unity_color_un_premultiply_alpha(unity_color_t* unity, double alpha);
int unity_color_un_premultiply(unity_color_t* unity);
