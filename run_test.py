from chesski.backend.engines import test_engines

# Tsting Engines:
# -1000 Games (500 White / 500 Black)
# -------------------------------------------------------------------
#       vs. Random
#--------------------------------------------------------------------
# Random:
# 506.5
# 76 / 861 / 63 --- avg: 324 Moves --- Duration: 16min 58s
#
# Material:
# 569.5
# 141 / 857 / 2 --- avg: 202 Moves --- Duration: 11min 20s
#
# Material(+ Draw Avoid):
# 636.0
# 273 / 726 / 1 --- avg: 303 Moves --- Duration: 42min 43s
#
# Material(+ Checkmate-filter):
# 903.5
# 809 / 189 / 2 --- avg: 115 Moves --- Duration: 12min 14s
#
# Material(+ Checkmate-filter + Draw Avoid):
# 934
# 871 / 126 / 3 --- avg: 127 Moves --- Duration: 20min 58s
#
# Material(+ Autoqueen):
#
# 222 / 774 / 4 --- avg: 171 Moves --- Duration: 14min 25s
#
# -------------------------------------------------------------------
#       vs. Material
#--------------------------------------------------------------------
# Material(+ Checkmate-filter):
# 536.5
# 102 < / 869 / 29 --- avg: 146 Moves --- Duration: 7min 2s
#
# Material(+ Checkmate-filter + Draw Avoid):
# 566.5
# 149 / 835 / 16 --- avg: 178 Moves --- Duration: 14min 28s
#
# -------------------------------------------------------------------
#       vs. Material(+ Checkmate-filter)
#--------------------------------------------------------------------
# Material(+ Checkmate-filter + Draw Avoid):
# 513.5
# 137 / 753 / 110 --- avg: 156 Moves --- Duration: 13min 3s
#
