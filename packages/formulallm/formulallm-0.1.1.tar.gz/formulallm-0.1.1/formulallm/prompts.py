FIX_CODE_PREFIX =  """ \
SYSTEM MESSAGE:

You are a computer scientist. You will be provided the assembly of a C++ program. You will explain why the program is broken and give solutions to fixing it.

END OF SYSTEM MESSAGE"""

REPAIR_CODE_PREFIX = """ \
SYSTEM MESSAGE:

You are a computer scientist. You will be provided the assembly of a C++ program. You will give repairs of the code in labelled triple backticks.

END OF SYSTEM MESSAGE"""

EXPLAIN_QUERY_PROMPT = """ \
{prompt}

{code}

{output}
"""

REPAIR_QUERY_PROMPT = """ \
{prompt}

{code}

{output}
"""

OUTPUT_RETURN = """ \
{explanation}
"""

REPAIR_OUTPUT_RETURN = """ \
{repair}
"""

FORMULA_CODE_LLM_DESC = """ \
This is a Formula debugging tool. 

To invoke this tool, make sure you call it in a JSON format in the following format:

{
    "prompt": "FORMULA REQUEST HERE",
	"code": "FORMULA CODE HERE",
    "output": "FORMULA INTERPRETER OUTPUT HERE"
}

Make sure you only call this function with a JSON format, otherwise it will not work.
"""

REPAIR_FORMULA_CODE_LLM_DESC = """ \
This is a Formula repair tool. 

To invoke this tool, make sure you call it in a JSON format in the following format:

{
    "prompt": "FORMULA REQUEST HERE",
	"code": "FORMULA CODE HERE",
    "output": "FORMULA INTERPRETER OUTPUT HERE"
}

Make sure you only call this function with a JSON format, otherwise it will not work.
"""