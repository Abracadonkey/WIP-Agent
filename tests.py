from functions.run_python_file import run_python_file 


result1 = run_python_file("calculator", "main.py")
result2 = run_python_file("calculator", "main.py", ["3 + 5"])
result3 = run_python_file("calculator", "tests.py")
result4 = run_python_file("calculator", "../main.py")
result5 = run_python_file("calculator", "nonexistent.py")





print(result1, result2, result3, result4, result5)
