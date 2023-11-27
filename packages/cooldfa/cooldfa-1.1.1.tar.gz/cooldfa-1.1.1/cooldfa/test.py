from cooldfa import DFA, preset_words


# dfa算法
example = DFA('123', '234', '56', 'end')
text = '1--2--3--4--5--6--7--8--9--end--'

assert example.has_any(text) is True
assert example.find_one(text) == '1--2--3'
assert example.find_all(text) == ['1--2--3', '5--6', 'end']
assert example.sub(text, '*') == '*******--4--****--7--8--9--***--'
assert example.sub(text, '*', compress=True) == '*--4--*--7--8--9--*--'


# 使用内置的敏感词库
example = DFA(
    *preset_words.politics,  # 政治类
    *preset_words.sex,  # 色情类
    *preset_words.violence,  # 暴力类
    *preset_words.url,  # 网址
    *preset_words.others,  # 其它
    *['123', '234', '56', 'end']
)


# 记录测试结果
name = 'cooldfa'
print(f'[测试通过] {name}')