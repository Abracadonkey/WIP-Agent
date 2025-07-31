from functions.get_files_info import get_files_info 

def test():
    result1 = get_files_info("calculator", ".") 
    result2 = get_files_info("calculator", "pkg") 
    result3 = get_files_info("calculator", "/bin") 
    result4 = get_files_info("calculator", "../") 
    return result1, result2, result3, result4
