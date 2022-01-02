from chesski.backend.engines import test_engines

# Tsting Engines:
# -1000 Games (500 White / 500 Black)
#----------------------------
# Random vs. Random:
# 76 / 861 / 63 --- avg: 324 Moves --- Duration: 26min 29s
#
# Material vs. Random:
# 149 / 849 / 2 --- avg: 196 Moves --- Duration: 15min 10s
#
# Material vs. Material:
# 14 / 970 / 16 --- avg: 158 Moves --- Duration: 8min 48s
#
# Material(+ Checkmate-filter) vs. Random:
# 819 / 181 / 0 --- avg: 117 Moves --- Duration: 10min 4s
#
# Material(+ Checkmate-filter) vs. Material:
# 93 / 890 / 17 --- avg: 147 Moves --- Duration: 8min 6s
#
# Material(+ Checkmate-filter) vs. Material(+ Checkmate-filter):
# 96 / 807 / 97 --- avg: 138 Moves --- Duration: 7min 46s
#
# Material(+ Checkmate-filter + Check_Value = 0.5) vs. Material(+ Checkmate-filter):
#
#
