# 辅助函数 判断字符串中是否含有字母
def is_have_alpha(tmp):
    for i in tmp:
        if i.isalpha():
            return True
            break
    return False