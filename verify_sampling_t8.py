#!/usr/bin/env python3
from fractions import Fraction as F
# Numeric examples independently recomputed.
undercoverage=F(1000-900,1000)
item_nonresponse=F(12,100)
processing_error=F(4,200)
unit_nonresponse=F(30,150)
unit_nonresponse_2=F(50,250)
assert undercoverage==F(1,10)
assert item_nonresponse==F(3,25)
assert processing_error==F(1,50)
assert unit_nonresponse==F(1,5)==unit_nonresponse_2
# Error-classification examples.
cases={"omitted_units":"undercoverage","whole_case_refusal":"unit_nonresponse","skipped_question":"item_nonresponse","inaccurate_answer":"measurement_error","wrong_code":"processing_error","wrong_construct":"specification_error"}
assert len(cases)==6
print("PASS numeric rates:",undercoverage,item_nonresponse,processing_error,unit_nonresponse)
print("PASS six classification categories")
