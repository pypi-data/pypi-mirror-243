# 项目的常用函数

# import
# region
from __future__ import annotations

import datetime
import inspect
import json
import multiprocessing
import os
import random
import re
import sys
import time
import zipfile
from functools import wraps

import editdistance
import selenium
import urllib3
import win32api
import win32con
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# endregion

# 初始化1
# region
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

sys.path.append('D:/Kaleidoscope/')
Logcount = 0
# 不包括 SystemExit，因为默认通过这个来强行中止严重错误
retrylist = [
    Exception, ConnectionRefusedError,
    # pyautogui.FailSafeException,
]
if 'selenium' in sys.modules:
    import selenium

    retrylist += [
        selenium.common.exceptions.ElementClickInterceptedException,
        selenium.common.exceptions.WebDriverException,
        selenium.common.exceptions.NoSuchElementException,
        selenium.common.exceptions.StaleElementReferenceException,
        selenium.common.exceptions.InvalidSessionIdException,
        selenium.common.exceptions.UnexpectedAlertPresentException,

        urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError,
        selenium.common.exceptions.TimeoutException,
        selenium.common.exceptions.NoSuchWindowException,
    ]
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    'cookie': ''
}
chrome_path = r'C:/Program Files/Google/Chrome/Application/chrome.exe'
firefox_path = r'C:/Program Files/Mozilla Firefox/firefox.exe'
edge_path = r'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'


# endregion


# 参考代码
# region
# xpath
# '//div[starts-with(@style,"transform:")]'
# './div[starts-with(@style,"transform:")]'
# ffmpeg
# 合并多个视频
# ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4
# 其中：
# -f concat 指定使用concat协议。
# -safe 0 是因为在某些情况下，ffmpeg可能会因为路径问题报错。这个选项可以确保它正确地解读文件路径。
# -i files.txt 指定输入列表文件。
# -c copy 表示直接复制音频和视频流，而不重新编码。
# 提取视频流
# ffmpeg -i input.mp4 -an -c:v copy video_only.mp4
# 合并视频与音频
# ffmpeg -i video_only.mp4 -i your_audio.wav -shortest -c:v copy -c:a aac output.mp4
# 其中：
# video_only.mp4 是不包含音频的视频文件。
# your_audio.wav 是你的WAV声音文件。
# -shortest 这个选项会确保输出文件的长度与最短的输入流（即视频或音频）相同。
# -c:v copy 表示直接复制视频流，不进行重新编码。
# -c:a aac 表示将音频编码为AAC格式。
# endregion

# 装饰器与语法
# region
def alwaysrun(func):
    """
    除非手动停止，否则绝不停止
    屏蔽除了 KeyboardInterrupt 以外的东西
    确保程序的完全正确，从而关闭一切补救措施
    @param func:
    @return:
    """

    @wraps(func)
    def wrapper(*a, **b):
        def inner1(f, *a, **b):
            while True:
                try:
                    return f(*a, **b)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    pass
                except SystemExit as e:
                    pass

        return inner1(func, *a, **b)

    return wrapper


# 关键字参数多名。用法：@merge_args(target=['target'（可省略）,'...'])
# 所有参数整合到末尾的变量中（排除了 self ）
def manage_args(**merged_keys):
    def decorator(func):
        from functools import wraps
        sig = inspect.signature(func)
        # 这是在函数的定义阶段的操作，所以没有具体值，
        # 即使是 default_values 也是默认值
        # 事实上，_a _b 实际上长度只有 1
        l0 = [p.name for p in list(sig.parameters.values()) if p.kind == p.POSITIONAL_ONLY]
        l1 = [p.name for p in list(sig.parameters.values()) if p.kind == p.POSITIONAL_OR_KEYWORD]
        _a = [p.name for p in list(sig.parameters.values()) if p.kind == p.VAR_POSITIONAL]
        l2 = [p.name for p in list(sig.parameters.values()) if p.kind == p.KEYWORD_ONLY]
        _b = [p.name for p in list(sig.parameters.values()) if p.kind == p.VAR_KEYWORD]
        default_values = {k: v.default for k, v in sig.parameters.items() if
                          k in (l1 + l2) and v.default is not inspect.Parameter.empty}

        @wraps(func)
        def wrapper(*a, **b):
            # 最后还是要通过 *a, **b 的形式传参直接调用被装饰的函数
            a = list(a)
            res = {}
            if len(a) and not len(_a):
                # 调用处省略了键而定义处也没有 *args ，这个时候就需要
                # 手动覆盖关键字参数
                if len(a) > len(l0):
                    res_a = a[len(l0):]
                    a = a[:len(l0)]
                res.update({k: i for k, i in zip(l1 + l2, res_a)})

            # 重写参数名多名
            for dest_key, src_keys in merged_keys.items():
                for src_key in src_keys:
                    if b.get(src_key) is not None:
                        b[dest_key] = b.pop(src_key)
                        break
            res.update(b)
            b = res

            # 调用处没有传参的而定义处具有默认值的，应当
            # 加入 all_args 进行参数传递
            for k, v in default_values.items():
                if not k in b:
                    b.update({k: v})

            # 记录 all_args 到 **b 中进行参数传递
            # 一般认为， all_args 可以有多种表现形式
            for all_args in ['b', 'all_args', 'kwargs']:
                check_lis = l1 + l2 + _b
                if len(check_lis) > 2:
                    check_lis = check_lis[-2:]
                if all_args in check_lis:
                    b = exclude(b, all_args)  # 否则会造成嵌套自身
                    b[all_args] = dict(b)  # 刻印
                    if len(l0 + l1) and 'self' in l0 + l1:  # 处理 self ，不加进去
                        b[all_args] = exclude(b[all_args], 'self')
                    break

            while True:
                try:
                    return func(*a, **b)
                except TypeError as e:
                    # 上次 debug 发现 传 None 会导致以为没传
                    del b[next(iter(b))]
                    continue

        return wrapper

    return decorator


@manage_args(retry_attempts=['repeat'], wait_seconds=['wait'])
def retry(retry_attempts=99, wait_seconds=5,
          ):
    """
    创建一个重试装饰器，基于tenacity库。
    :param retry_attempts: 重试的次数，默认为5次。
    :param wait_seconds: 每次重试的等待时间（秒），默认为2秒。
    :return: 装饰器
    """
    from tenacity import retry, stop_after_attempt, wait_fixed, before, after
    def after_retry(retry_state):
        if retry_state.outcome and retry_state.outcome.exception():
            warn(f"{retry_state.outcome.exception()}  \n{wait_seconds} 秒后自动重启。")

    def decorator_retry(func):
        # 使用tenacity的retry装饰器，配置重试策略
        @retry(stop=stop_after_attempt(retry_attempts), wait=wait_fixed(wait_seconds),
               after=after_retry)
        def wrapper(*args, **kwargs):
            # 执行被装饰的函数
            return func(*args, **kwargs)

        return wrapper

    return decorator_retry


def has_value(interval=2, controller=['not_null', 'complete', 'null'],
              check_lis=['', None, []]):
    # 被装饰的函数会有一个参数 not_null 或者其它名字，
    # 由 controller 传入。当对应变量调用传参为 True 启用
    # checklis 控制判断空值的规则
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            controller_check = any(kwargs.get(key) for key in controller)
            if controller_check:
                while True:
                    result = func(*args, **kwargs)
                    if result not in check_lis:
                        return result
                    else:
                        warn(f'返回了空值 {result} 。重新执行', stacklevel=2)
                    time.sleep(interval)
            else:
                # 如果不满足条件，只执行一次函数
                return func(*args, **kwargs)

        return wrapper

    return decorator


hasvalue = not_null = notnull = \
    has_value


@manage_args(var=['args', 'arg'], check_lis=['l', 'lis'])
def used_arg(var=None, strict=None,
             check_lis=[],
             b=None, **leak):
    """
    非空判断
    @param var:
    @param lis:
    @return:  参数不为空
    """

    def ret():
        if strict:
            Exit(f'变量 {var} （{var} ）\n\t不符合类型断言的要求')
        return False

    if var is None:
        return ret()
    if type(var) in [str, int, bool]:
        if var in check_lis:
            return ret()
    return True


@manage_args()
def enabled_arg(var=None, check_lis=[False, '', 0], b=None, **leak):
    return used_arg(**b)


enabled = enabled_args = \
    enabled_arg


@manage_args(var=['args', 'arg'], type_lis=['lis', '_type', 'type'])
def check_type(var=None, type_lis=None, strict=None,
               b=None, **leak):
    """
    非空判断&类型判断
    @param var:
    @param lis:
    @return:  参数符合预期类型/值
    """

    def ret():
        if strict:
            Exit(f'变量 {var} （{var} ）\n\t不符合类型断言的要求')
        return False

    if not used_arg(var):
        return ret()
    if type_lis is None:
        return True
    if not type(type_lis) in [list]:
        type_lis = [type_lis]
    for item in type_lis:
        if isinstance(item, type) and isinstance(var, item):
            return True
        elif isinstance(var, str) and var in type_lis:
            return True
    return ret()


used_args = used = check_used = used_var = \
    used_arg
check_arg_type = arg_type = is_type = used_type = \
    check_type


def manage_args(**merged_keys):
    def decorator(func):
        from functools import wraps
        sig = inspect.signature(func)
        # 这是在函数的定义阶段的操作，所以没有具体值，
        # 即使是 default_values 也是默认值
        # 事实上，_a _b 实际上长度只有 1
        l0 = [p.name for p in list(sig.parameters.values()) if p.kind == p.POSITIONAL_ONLY]
        l1 = [p.name for p in list(sig.parameters.values()) if p.kind == p.POSITIONAL_OR_KEYWORD]
        _a = [p.name for p in list(sig.parameters.values()) if p.kind == p.VAR_POSITIONAL]
        l2 = [p.name for p in list(sig.parameters.values()) if p.kind == p.KEYWORD_ONLY]
        _b = [p.name for p in list(sig.parameters.values()) if p.kind == p.VAR_KEYWORD]
        default_values = {k: v.default for k, v in sig.parameters.items() if
                          k in (l1 + l2) and v.default is not inspect.Parameter.empty}

        @wraps(func)
        def wrapper(*a, **b):
            # 最后还是要通过 *a, **b 的形式传参直接调用被装饰的函数
            a = list(a)
            res = {}
            if len(a) and not len(_a):
                # 调用处省略了键而定义处也没有 *args ，这个时候就需要
                # 手动覆盖关键字参数
                if len(a) > len(l0):
                    res_a = a[len(l0):]
                    a = a[:len(l0)]
                res.update({k: i for k, i in zip(l1 + l2, res_a)})

            # 重写参数名多名
            for dest_key, src_keys in merged_keys.items():
                for src_key in src_keys:
                    if b.get(src_key) is not None:
                        b[dest_key] = b.pop(src_key)
                        break
            res.update(b)
            b = res

            # 调用处没有传参的而定义处具有默认值的，应当
            # 加入 all_args 进行参数传递
            for k, v in default_values.items():
                if not k in b:
                    b.update({k: v})

            # 记录 all_args 到 **b 中进行参数传递
            #  all_args 可以有多种表现形式
            for all_args in ['b', 'all_args', 'kwargs']:
                check_lis = l1 + l2 + _b
                if len(check_lis) > 2:
                    check_lis = check_lis[-2:]
                if all_args in check_lis:
                    b = exclude(b, all_args)  # 否则会造成嵌套自身
                    b[all_args] = dict(b)  # 刻印
                    if len(l0 + l1) and 'self' in l0 + l1:  # 处理 self ，不加进去
                        b[all_args] = exclude(b[all_args], 'self')
                    break

            return func(*a, **b)

        return wrapper

    return decorator


manageargs = \
    manage_args


# 使用json保存配置文件，进行关键字参数覆盖
def useState(fn):
    @wraps(fn)
    def wrapper(*args, config=True, **kwargs):

        if config:
            config = jsondata(jsonpath(fn.__name__))

            # 获取函数定义时关键字参数默认值
            defaults = fn.__defaults__ or ()
            default_values = dict(
                zip(fn.__code__.co_varnames[:fn.__code__.co_argcount][-len(defaults):], defaults))

            # jsondata config 覆盖
            for k, v in config.data.items():
                if k in default_values:
                    default_values[k] = v

            # 调用处代码覆盖
            default_values.update(kwargs)

            # 构造新的参数列表
            new_args = []
            for arg in args:
                if arg in default_values:
                    new_args.append(default_values[arg])
                    del default_values[arg]
                else:
                    new_args.append(arg)

            # 将剩余的默认值添加到kwargs中
            kwargs.update(default_values)

            # 调用原始函数
            return fn(*new_args, **kwargs)
        else:
            return fn(*args, **kwargs)

    return wrapper


# 只有一个参数，如果有多个，则重复执行函数，或者空参数
def multisingleargs(func):
    @wraps(func)
    def wrapper(*a):
        res = []
        if a in [None, (), []]:
            return func()
        for i in a:
            res.append(func(i))
        return res

    return wrapper


@manage_args(index=['name', 'position', 'pos'])
def listed(index=-1):
    """
    参数可以变为 iterable 以重复执行函数并返回结果。但是参数本身不能是 iterable
    需要注意的是，在元组中还是在字典中取决于调用代码而非定义代码
    @param index:元组的下标或是字典的键
    @return:
    """

    def decorator(func):
        def wrapper(*a, **c):
            import types
            if type(index) in [int]:  # 元组
                if a in [None, (), []]:  # *a 为空，
                    return func(*a, **c)
                if not (type(a[index]) in [list, types.GeneratorType]):  # index 位置不是可迭代对象
                    return func(*a, **c)
                res = []
                if index == -1:  # 处理 index
                    a1 = a[:index]
                    a2 = []
                else:
                    a1 = a[:index]
                    a2 = a[index + 1:]
                for i in a[index]:
                    ret = (func(*a1, i, *a2, **c))
                    if not type(ret) == list:
                        res.append(ret)
                    else:
                        res += ret
                return res

            elif type(index) in [str]:
                if c in [None, (), [], {}] or not index in list(c):  # **c 为空，或者键不存在
                    return func(*a, **c)
                if not (type(c[index] in [list, types.GeneratorType])):  # index 位置不是可迭代对象
                    return func(*a, **c)
                res = []
                c_copy = c.copy()  # 处理 index
                for value in c[index]:
                    c_copy[index] = value
                    ret = func(*a, **c_copy)
                    if not type(ret) == list:
                        res.append(ret)
                    else:
                        res += ret
                return res
            else:
                Exit('index type error')

        return wrapper

    return decorator


# 计算调试时函数的消耗时间
def DebugConsume(func):
    def wrapper(*a, **b):
        def inner1(f, *a, **b):
            ret = f(*a, **b)
            stole = nowstr()
            filename1 = filename(inspect.getframeinfo(
                inspect.currentframe().f_back.f_back)[0])
            # 不加strict 控制台调试时会异常
            filename1 = rmtail(filename1, '.py', strict=False)
            funcname1 = inspect.getframeinfo(
                inspect.currentframe().f_back.f_back)[2]
            funcname2 = None
            try:
                funcname2 = inspect.getframeinfo(
                    inspect.currentframe().f_back.f_back)[3]
                funcname2 = (funcname2[0])
                funcname2 = funcname2[funcname2.find(
                    '.') + 1:funcname2.find('(')]
            except Exception as e:
                pass
            if counttime(stole) > 1:
                delog(
                    f'函数{filename1}.{funcname1}/.{funcname2} 所消耗的时间：{int(counttime(stole))} s')
            return ret

        return inner1(func, *a, **b)

    return wrapper


# 计算运行时函数的消耗时间
def RuntimeConsume(func):
    @wraps(func)
    def wrapper(*a, **b):
        def inner1(f, *a, **b):
            if not get_env_var('debug'):
                stole = nowstr()
            ret = f(*a, **b)
            if get_env_var('debug'):
                return ret
            funcname1 = inspect.getframeinfo(
                inspect.currentframe().f_back.f_back)[2]
            funcname2 = None
            try:
                funcname2 = inspect.getframeinfo(
                    inspect.currentframe().f_back.f_back)[3]
                funcname2 = (funcname2[0])
                funcname2 = funcname2[funcname2.find(
                    '.') + 1:funcname2.find('(')]
            except Exception as e:
                pass
            if counttime(stole) > 1:
                delog(
                    f'函数{funcname1}/{funcname2} 所消耗的时间：{int(counttime(stole))} s')
            return ret

        return inner1(func, *a, **b)

    return wrapper


def consume(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        if elapsed_time > 1:
            delog(f' {func.__name__} ：{int(elapsed_time)} s')
        return result

    return wrapper


# endregion

# 基础数据结构
# region
# 容错
def Eval(a):
    return_map = {
        'false': False,
        'true': True,
        'False': False,
        'True': True,
        'null': None,
        'undefined': None
    }
    if not type(a) in [str]:
        return a
    else:
        if a in return_map:
            return return_map[a]
        else:
            try:
                return eval(a)
            except Exception as e:
                Exit(a)  # 确保已定义 Exit 函数


# 合并字典或列表
def merge(a, b):
    if isinstance(a, list) and isinstance(b, list):
        return a + b  # 合并列表
    elif isinstance(a, dict) and isinstance(b, dict):
        merged_dict = a.copy()
        merged_dict.update(b)
        return merged_dict


# 从字典中排除键
manage_args()


# def add_attribute(obj,*a,b=None,**leak):
def add_attribute(obj, b=None, **leak):
    for i in b.items():
        setattr(obj, key(i), value(i))


def exclude(d, ks):
    if not type(ks) == list:
        ks = [ks]
    return {k: v for k, v in d.items() if k not in ks}


rmkey = exclude


def equals(a, b):
    return a in [Str(b), b, Int(b)]


def deep_copy(a):
    import copy
    if type(a) in [int, str, float, bool]:
        return a
    if type(a) in [list]:
        return copy.deepcopy(a)


def possibility(n):
    import random
    return random.random() < n


def gen_dict(k, v):
    """
    根据两个列表自动生成字典
    @param k:
    @param v:
    @return:
    """
    if not type(k) == list or not type(v) == list:
        Exit('gen_dict的参数必须是列表')
    if not len(k) == len(v):
        Exit('两个列表长度不一致')

    ret = {}
    for i in range(len(k)):
        if not type(i) == str:
            Exit('key必须是字符串')
        ret.update({k[i]: v[i]})
    return ret


def List(s):
    try:
        if s in [None]:
            return []
        return list(s)
    except Exception as e:
        return []


def Str(s):
    """

    @param s:
    @return:
    """
    try:
        if s in [None]:
            return ''
        if type(s) in [WebElement]:
            return s.xpath
        if type(s) in [dict]:
            return dicttojson(s)
        return str(s)
    except Exception as e:
        return ''


class v:
    """
    满足元组、数组的加减
    """

    def __init__(self, *args):
        a = []
        for i in args:
            if type(i) in [list, tuple]:
                for j in i:
                    a.append(j)
            else:
                a.append(i)
        self.data = a

    def __getitem__(self, index):
        if isinstance(index, int):
            if index < 0 or index >= len(self.data):
                raise IndexError("Index out of range")
            return self.data[index]
        else:
            raise TypeError("Invalid index type, should be an integer")

    def __setitem__(self, index, value):
        if isinstance(index, int):
            if index < 0 or index >= len(self.data):
                raise IndexError("Index out of range")
            self.data[index] = value
        else:
            raise TypeError("Invalid index type, should be an integer")

    def __add__(self, other):
        result = []
        if type(other) in [list, tuple]:
            other = v(*other)
        for i in range(len(self.data)):
            result.append(self.data[i] + other.data[i])
        return result

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        result = []
        if type(other) in [list, tuple]:
            other = v(*other)
        for i in range(len(self.data)):
            result.append(-self.data[i] + other.data[i])
        return result

    def __sub__(self, other):
        result = []
        if type(other) in [list, tuple]:
            other = v(*other)
        for i in range(len(self.data)):
            result.append(self.data[i] - other.data[i])
        return result

    def __str__(self):
        s = '   '.join(Str(_) for _ in self.data)
        return f'< {s} >'


def SortedName(l):
    """
    自动排序名字
    @param l:
    @return:
    """
    d = []
    for i in l:
        i, ext = extensionandname(i, exist=False)
        ret = research(r'_\d+$', i)
        if ret:
            d.append((rmtail(i, ret.group()), ret.group(), ext))
            continue
        ret = research(r'\d+$', i)
        if ret:
            d.append((rmtail(i, ret.group()), ret.group(), ext))
            continue
        d.append((i, '', ext))
    d.sort(key=lambda x: (x[0], Int(x[1]), x[2]))
    l = []
    for i in d:
        l.append(i[0] + i[1] + i[2])
    return l


# 实现包括None在内的int转换
def Int(s):
    if s in [None, False, '']:
        return 0
    try:
        return int(s)
    except Exception as e:
        return 0


def Set(l, hashable=True, resort=True, method=None, args=[], kwargs={}):
    """
    当元素包含 not hashable 时，牺牲一部分性能
    当元素只包含 hashable 时，返回具有稳定性的数组
    @param l:
    @param hashable: 是否全是可哈希元素
    @param resort: 是否重排。会牺牲性能
    @param method: 判断元素是否相似的方法。如果不为空，则并非简单的集合处理
    @return:数组
    """
    res = []
    if l == None:
        return []

    # 非简单集合处理
    # count=0
    if not method is None:
        for i, x in enumerate(l):
            for y in l[i + 1:]:
                # count+=1
                # print(count)
                if method(x, y, *args, **kwargs):
                    res.append(x)
                    break
        return list(set(Set(l)) - set(Set(res)))

    # 简单集合处理
    if hashable:
        if resort:
            return list(dict.fromkeys(l))
        else:
            return list(set(l))

    for i in l:
        if i in res:
            continue
        res.append(i)
    return res


def simplinfo(num, author, title, disk=None):
    if disk == None:
        disk = diskname
    return json.dumps({str(num): {'disk': disk, 'author': author, 'title': title}},
                      ensure_ascii=False)


class MyError(Exception):
    """
    一个我希望控制是否终止程序的特殊错误
    一般来说直接停止。除了 alwaysrun
    """
    pass


def jsontodict(s):
    """

    @param s:
    @return: 如果转换失败返回False
    """
    if type(s) == dict:
        return s
    if not type(s) == str:
        Exit('jsontodict 的参数必须是字符串')
    if s == '' or s == None or s == []:
        warn(f'{s, type(s)}')
        return
    try:
        return json.loads(s)
    except Exception as e1:
        warn('解析字符为字典错误', s, e1)
        return False


def dicttojson(s):
    if type(s) == str:
        return s
    try:
        return json.dumps(s, ensure_ascii=False)
        # return str(s)
    except Exception as e:
        warn(e)
        return ''


datatojson = dicttojson


def key(d):
    return keys(d)[0]


def keys(d):
    if d == None:
        return None
    if not type(d) == dict:
        warn(f'用法错误。d的类型为{type(d)}')
    return list(d.keys())


@listed()
def value(d):
    d = jsontodict(d)
    if not type(d) == dict:
        warn(f'用法错误。d的类型为{type(d)}')
    return d[key(d)]


def values(d):
    d = jsontodict(d)
    # ret=[]
    # for i in d:
    #     ret.append(d[i])
    # return ret
    return list(d.values())


# endregion

# 环境变量
# region
os.environ['globals'] = dicttojson({})


# 仅在进程生效
def add_env_path(v=None):
    path_value = os.environ.get('PATH')
    os.environ["PATH"] = path_value + os.pathsep + v


@manage_args(d=['value', 'var'])
def set_env_var(d=None, origin=False,
                b=None, **leak,
                ):
    """

    @param d: 字典。
    @param origin: 是否采用原生。否则在 globals 键名内
    @return:
    """
    if origin:
        for i in d:
            os.environ[i] = d[i]
        return
    newd = jsontodict(os.environ['globals'])
    newd.update(d)
    os.environ['globals'] = dicttojson(newd)


@manage_args(var=['d'])
def save_value(path=None, var=None,
               b=None, **leak):
    import dill
    path = add_ext(varpath(path), '.pkl')
    deletedirandfile(path)
    with createfile(path) as f:
        dill.dump(var, f)


save_var = save_value
save_env_var = \
    set_env_var


def get_env_var(name, origin=False):
    """

    @param name:
    @param origin:
    @return: None/ 值
    """
    if origin:
        return os.environ[name]
    d = jsontodict(os.environ['globals'])
    if name in d:
        return d[name]
    else:
        return


get_env_var


# 获取用户个性化设置
def getsettings(k=None):
    if not type(k) in [str]:
        Exit(f'键错误。{info(k)}')
    f = jsondata(jsonpath('settings'))
    return f.data[k]


# 设置用户个性化设置
def set_settings(d=None):
    f = jsondata('all')
    check_type(var=d, lis=[dict])
    f.data.update(d)
    f.save()


save_settings = setsettings = \
    set_settings


def strict():
    return get_env_var('strict')


set_env_var({'strict': None})


# endregion
# 时间
# region
# 对外只提供类的字符串、类的时间数组、字符串
# timestamp只对内使用

# 字符串
def research(*a):
    return re.search(*a)


def rematch(*a):
    return re.match(*a)


def nowstr(mic=True):
    """
    2023-08-08 09:10:23.841179
    @param mic:
    @return:
    """
    ret = str(datetime.datetime.now())
    if mic:
        return ret
    return ret[:ret.find('.')]


def realtime():
    return f'{str(now().hour).zfill(2)}:{str(now().minute).zfill(2)}:{str(now().second).zfill(2)}'


def now():
    return datetime.datetime.now()


def now_timestamp(int=True):
    if int:
        return Int(time.time())
    else:
        return time.time()


def Now():
    return Time()


# 根据字符串，返回到现在的时间差
def counttime(*args):
    a = []
    for i in args:
        if not type(i) == Time:
            a.append(Time(i))
        else:
            a.append(i)
    if len(a) == 1:
        return a[0].counttime()
    else:
        return a[0].counttime(a[1])

    # if s.find('hms') >= 0:
    #     return time.strftime("%H:%M:%S", time.localtime())
    # if s.find('ms') >= 0:
    #     return time.strftime("%M:%S", time.localtime())
    # if s.find('hm') >= 0:
    #     return time.strftime("%H:%M", time.localtime())
    # if s.find('h') >= 0:
    #     return time.strftime("%H", time.localtime())
    # if s.find('m') >= 0:
    #     return time.strftime("%M", time.localtime())
    # if s.find('s') >= 0:
    #     return time.strftime("%S", time.localtime())
    # if s=='all':
    #     return str(datetime.datetime.nowstr())


class delta_time(datetime.timedelta):
    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], datetime.timedelta):
            delta = args[0]
            return super().__new__(cls, days=delta.days, seconds=delta.seconds,
                                   microseconds=delta.microseconds)
        return super().__new__(cls, *args, **kwargs)

    def __add__(self, other):
        if isinstance(other, delta_time):
            return delta_time(seconds=self.total_seconds() + other.total_seconds())
        elif isinstance(other, datetime.timedelta):
            return delta_time(seconds=self.total_seconds() + other.total_seconds())
        else:
            raise TypeError("Unsupported type for addition with delta_time")

    def __sub__(self, other):
        if isinstance(other, delta_time):
            return delta_time(seconds=self.total_seconds() - other.total_seconds())
        elif isinstance(other, datetime.timedelta):
            return delta_time(seconds=self.total_seconds() - other.total_seconds())
        else:
            raise TypeError("Unsupported type for subtraction with delta_time")

    def __eq__(self, other):
        return self.total_seconds() == other.total_seconds()

    def __lt__(self, other):
        if hasattr(other, 'total_seconds'):
            return self.total_seconds() < other.total_seconds()
        return self.total_seconds() < other

    def __gt__(self, other):
        return self.total_seconds() > other.total_seconds()

    def __le__(self, other):
        return self.total_seconds() <= other.total_seconds()

    def __ge__(self, other):
        return self.total_seconds() >= other.total_seconds()

    def __str__(self):
        days, seconds = divmod(self.total_seconds(), 24 * 3600)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        if days:
            return f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"
        elif hours:
            return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
        elif minutes:
            return f"{int(minutes)}m {int(seconds)}s"
        else:
            return f"{int(seconds)}s"

    def to_string(self):
        return str(self)

    def seconds(self):
        return int(self.total_seconds())

    second = seconds

    def minutes(self):
        return int(self.second() / 60)

    min = minutes

    def hours(self):
        return int(self.second() / 3600)

    def days(self):
        return int(self.days() / 24)


time_delta = delta_time


# 底层维护一个时间类，再由这个时间类导出字符串，进行操作
class Time():
    @manage_args(a=['timestamp','stamp'],hour=['h'],minute=['min','m',],
                month=['mon',],year=['y'],second=['sec','s'])
    def __init__(self,a=None,
                 year=None,month=None,day=None,
                 hour=None,minute=None,second=None,mic=None,
                 b=None, **leak):
        self.reset_to_now()
        if used_type(a,[int,float]):
            self.t = datetime.datetime.fromtimestamp(Int(a))
            return
        if used_type(a,[str]):
            self.t = strtotime(a).t
            return
        if used_type(a,Time):
            self.t = a.t
            return
        if used_type(a,datetime.datetime):
            self.t = a
            return
        if used_type(a,datetime.datetime):
            self.t = a
            return
        def _int(a):
            if a is None:
                return None
            return int(a)
        year,month,day,hour,minute,second,mic=_int(year),_int(month),_int(day),_int(hour),_int(minute),_int(second),_int(mic)
        if used(year):
            self.set_year(year)
        if used(month):
            self.set_month(month)
        if used(day):
            self.set_day(day)
        if used(hour):
            self.set_hour(hour)
        if used(minute):
            self.set_minute(minute)
        if used(second):
            self.set_second(second)
        if used(mic):
            self.set_mic(mic)

    def set_year(self, year):
        self.t = datetime.datetime(
            year=year,                      # 新的年份
            month=self.t.month,             # 保持原始月份
            day=self.t.day,                 # 保持原始日
            hour=self.t.hour,               # 保持原始时
            minute=self.t.minute,           # 保持原始分
            second=self.t.second,           # 保持原始秒
            microsecond=self.t.microsecond  # 保持原始微秒
        )

    def set_month(self, month):
        self.t = datetime.datetime(
            year=self.t.year,
            month=month,  # 新的月份
            day=self.t.day,
            hour=self.t.hour,
            minute=self.t.minute,
            second=self.t.second,
            microsecond=self.t.microsecond
        )

    def set_day(self, day):
        self.t = datetime.datetime(
            year=self.t.year,
            month=self.t.month,
            day=day,  # 新的日期
            hour=self.t.hour,
            minute=self.t.minute,
            second=self.t.second,
            microsecond=self.t.microsecond
        )

    def set_hour(self, hour):
        self.t = datetime.datetime(
            year=self.t.year,
            month=self.t.month,
            day=self.t.day,
            hour=hour,  # 新的小时
            minute=self.t.minute,
            second=self.t.second,
            microsecond=self.t.microsecond
        )

    def set_minute(self, minute):
        self.t = datetime.datetime(
            year=self.t.year,
            month=self.t.month,
            day=self.t.day,
            hour=self.t.hour,
            minute=minute,  # 新的分钟
            second=self.t.second,
            microsecond=self.t.microsecond
        )
    def set_second(self, second):
        self.t = datetime.datetime(
            year=self.t.year,
            month=self.t.month,
            day=self.t.day,
            hour=self.t.hour,
            minute=self.t.minute,
            second=second,  # 新的秒数
            microsecond=self.t.microsecond
        )
    def set_microsecond(self, microsecond):
        self.t = datetime.datetime(
            year=self.t.year,
            month=self.t.month,
            day=self.t.day,
            hour=self.t.hour,
            minute=self.t.minute,
            second=self.t.second,
            microsecond=microsecond  # 新的微秒数
        )
    set_mic=\
    set_microsecond
    def reset_to_now(self):
        self.t=now()

    @staticmethod
    def now():
        return Time()

    def strtotime(s):
        """
        字符串返回时间类
        @return:
        """
        return strtotime(s)

    def istime(*a):
        try:
            return strtotime(a[-1])
        except Exception as e:
            return False

    @classmethod
    def today(cls) -> Time:
        """
        提供给外部接口暴露的方法（一般不通过Time调用）
        可以理解为非时分秒的现在类
        @return:
        """
        self = Time()
        return cls(f'{self.year()}-{self.month()}-{self.day()}')

    @staticmethod
    def todaystr(style='compact') -> str:
        self = Time()
        if style == 'dashed':
            return f'{self.year()}-{self.month()}-{self.day()}'
        if style == 'compact':
            return f'{self.year()}{str(self.month()).zfill(2)}{str(self.day()).zfill(2)}'

    def yesterday(self) -> str:
        t = Time()
        t.add(-24 * 3600)
        return t.today()

    def year(self):
        return str(self.t.year)

    def month(self):
        return str(self.t.month)

    def day(self):
        return str(self.t.day)

    def weekday(self):
        return int(self.t.weekday())

    def second(self):
        return str(self.t.second)

    def min(self):
        return str(self.t.minute)

    def hour(self):
        return str(self.t.hour)

    def mic(self):
        return str(self.t.microsecond)

    def date(self):
        return self.s()[:10]

    def time(self):
        return self.s()[11:19]

    # 重写<，>
    def __lt__(self, other):
        if hasattr(other, 't'):
            return self.t.__lt__(other.t)
        if isinstance(other, int):
            if other < 1619135483:
                other = time_delta(other)
            else:
                other = Time(other)
        return self.t.__lt__(other)

    def __gt__(self, other):
        if hasattr(other, 't'):
            return self.t.__gt__(other.t)
        if isinstance(other, int):
            if other < 1619135483:
                other = time_delta(other)
            else:
                other = Time(other)
        return self.t.__gt__(other)

    def __add__(self, other):
        '''

        @param other: 数字，timedelta，Time，字符串
        @return:
        '''
        if type(other) in [int, float]:
            return Time(self.t.__add__(datetime.timedelta(seconds=other)))
        if type(other) in [str]:
            return Time(self.t.__add__(strtotime(other, delta=True)))
        if type(other) in [datetime.timedelta]:
            return Time(self.t.__add__(other))
        return Time(self.t.__add__(other.t))  # 意义不明

    def __sub__(self, other) -> delta_time | Time:
        '''

        @param other: 数字，timedelta，Time，字符串
        @return: 秒数
        '''
        if type(other) in [int, float]:
            return Time(self.t.__sub__(datetime.timedelta(seconds=other)))
        if type(other) in [datetime.timedelta]:
            return Time(self.t.__sub__(other))
        if type(other) in [str]:
            return Time(self.t.__sub__(strtotime(other, delta=True)))
        if type(other) in [Time, datetime.datetime]:
            return delta_time(self.t.__sub__(Time(other).t))

    def add(self, sec) -> Time:
        if not type(sec) in [int, delta_time]:
            warn(sec)
            sys.exit(-1)
        self.t = Time(self.t.timestamp() + sec)
        return self.s()

    def s(self, mic=False):
        """
        返回时间字符串
        """
        # return f'{str(self.year).zfill(2)}-{str(self.month).zfill(2)}-{str(self.day).zfill(2)} {str(self.hour).zfill(2)}:{str(self.min).zfill(2)}:{str(self.sec).zfill(2)}.{str(self.mic).zfill(6)}'
        if mic:
            return str(self.t)
        else:
            return head(str(self.t), '.', strict=False)

    def __str__(self):
        return self.s()

    # 返回距离现在的时间或者两个时间类的差，返回绝对值（秒）
    def counttime(self, obj=None):
        def do(*a):
            if len(a) == 1:
                s, = a
                return abs(s.t - datetime.datetime.now()).total_seconds()
            if len(a) == 2:
                s1, s2 = a
                return abs(s1.t - s2.t).total_seconds()

        if obj == None:
            return do(self)
        return do(self, obj)

    def stamp(self):
        return self.timestamp()

    def timestamp(self):
        return self.t.timestamp()


today = Time.today
todaystr = Time.todaystr


def strtotime(s=nowstr(), delta=False):
    '''
    字符串返回Time，delta_time
    @param s:
    @param delta:
    @return:
    '''
    import pandas
    if not type(s) == str:
        warn(f'用法错误。s不是字符串而是{info(s)}')
        return

    if delta:
        for i in ['days', 'day', 'years', 'month', 'hour', 'min', 'sec', 'mic']:
            if i in s:
                s = pandas.to_timedelta(s)
                s1, s = splittail(s, i, strict=True)
                return delta_time(**{i.strip('s') + 's': int(s1)})

    def repl1(match):
        y, m, d = match.group(1), match.group(2), match.group(3)
        return f'{y}-{m}-{d}'

    s = resub(r'(\d{4})(\d{2})(\d{2})', repl1, s)
    s = s.strip(' ')
    s = s.replace('/', '-')
    s = s.replace('：', ':')
    index = s.find(":0")
    if index != -1 and index + 2 < len(s) and not s[index + 2].isdigit():
        s = s[:index + 2] + "0" + s[index + 2:]
    match = re.search(r"(?<!\d)0:", s)
    if match:
        index = match.start()
        s = s[:index] + "0" + s[index:]
    s = s.replace('年', '-').replace('月', '-').replace('日', '')
    s = s.replace('时', ':').replace('分', ':').replace('秒', '')

    # 星期（返回的是今日所在这周的）
    if '星期' in s:
        # 0-6
        today = int(now().weekday())
        t = Time()
        if s == '星期一':
            t.add((0 - today) * 24 * 3600)
            s = s.replace('星期一', '')
        if s == '星期二':
            t.add((1 - today) * 24 * 3600)
            s = s.replace('星期二', '')
        if s == '星期三':
            t.add((2 - today) * 24 * 3600)
            s = s.replace('星期三', '')
        if s == '星期四':
            t.add((3 - today) * 24 * 3600)
            s = s.replace('星期四', '')
        if s == '星期五':
            t.add((4 - today) * 24 * 3600)
            s = s.replace('星期五', '')
        if s == '星期六':
            t.add((5 - today) * 24 * 3600)
            s = s.replace('星期六', '')
        if s == '星期日' or s == '星期天':
            t.add((6 - today) * 24 * 3600)
            s = s.replace('星期日', '')
            s = s.replace('星期天', '')
        return t

    # 先处理毫秒
    if '.' in s:
        s, mic = splittail(s, '.')
        mic = int(mic)
    else:
        mic = 0

    # 没有年或者没有时间
    t = rematch(
        r"(\d{4})?-?(\d{1,2})-(\d{1,2})\s?(\d{1,2})?:?(\d{1,2})?:?(\d{1,2})?", s)
    if t:
        year, month, day, hour, min, sec = t.groups()
        if year == None:
            year = now().year
        if hour == None:
            hour = 0
        if min == None:
            min = 0
        if sec == None:
            sec = 0
        if delta:
            return datetime.timedelta(days=int(day), hours=int(hour), minutes=int(min),
                                      seconds=int(sec),
                                      microseconds=mic)
        else:
            return Time(year=year, month=month, day=day, hour=hour, min=min, sec=sec, mic=mic)
    else:
        #     没有日期信息，可以没有秒（那就是时+分）
        t = rematch(r"(\d{1,2}):(\d{1,2}):?(\d{1,2})?", s)
        hour, min, sec = t.groups()
        if sec == None:
            sec = 0
        if delta:
            return datetime.timedelta(hours=int(hour), minutes=int(min), seconds=int(sec),
                                      microseconds=mic)
        else:
            return Time(hour=hour, min=min, sec=sec, mic=mic)

    # 至少五项的字符串
    # if ':'in s and '-'in s:
    #     (year, month, day, hour, min) = (
    #         int(s[0:4]), int(s[s.find('-') + 1:s.rfind('-')]),
    #         int(s[s.rfind('-') + 1:s.find(' ')]), int(s[s.rfind(' ') + 1:s.find(':')]),
    #         int(s[s.find(':') + 1:s.rfind(':')]))
    #     try:
    #         mic = int(s[s.find('.') + 1:])
    #         sec = int(s[s.rfind(':') + 1:s.find('.')])
    #     except Exception as e:
    #         sec = int(s[s.rfind(':') + 1:])
    #         mic = 0
    # else:
    #     # 只有日期字符串
    #     if '-'in s:
    #         lis=s.split('-')
    #         year,month,day=lis[0].strip(' '),lis[1].strip(' '),lis[2].strip(' ')
    #         hour,min,sec,mic=0,0,0,0
    #     else:
    # #         只有时间字符串
    #         year,month,day=today().split('-')
    #         if len(s)<7:
    # #             只有hour, min
    #             hour,min=s.split(':')
    #             sec,mic=0,0
    #         elif len(s)<10:
    # #             没有mic
    #             hour,min,sec=s.split(':')
    #             mic=0
    #         else:
    #             hour,min,res=s.split(':')
    #             sec,mic=res.split('.')


# timestamp构造Time
def timestamptotime(s):
    s = Str(s)
    return datetime.datetime.fromtimestamp(eval(s) / 1000).strftime("%Y-%m-%a %H:%M:%S.%f")


# 工具
# 转换为timestamp
def timestamp(s=None):
    if type(s) == str:
        return time.mktime(time.strptime(s, "%Y-%m-%a %H:%M:%S.%f"))
    if type(s) == Time:
        return Time.timestamp()
    if s == None:
        return time.time()


# 转换为数组（未写完）
def timearr(s=nowstr()):
    # return time.strftime("%Y-%m-%a %H:%M:%S", time.localtime())

    if len(s) > 10:
        (year, month, day, hour, min) = (
            int(s[0:4]), int(s[s.find('-') + 1:s.rfind('-')]
                             ), int(s[s.rfind('-') + 1:s.find(' ')]),
            int(s[s.rfind(' ') + 1:s.find(':')]),
            int(s[s.find(':') + 1:s.rfind(':')]))
        try:
            mic = int(s[s.find('.') + 1:])
            sec = int(s[s.rfind(':') + 1:s.find('.')])
        except Exception as e:
            sec = int(s[s.rfind(':') + 1:])
            mic = 0
        return (year, month, day, hour, min, sec, mic)


# endregion

# 运行时
# region
def mustDebug():
    if not isDebugging():
        Exit('必须在调试模式下运行')


def mustRun():
    if not isRunning():
        Exit('必须在运行模式下运行')


@manage_args(t=['anti_wait_time'])
def sleep(t=9999, silent=None,
          b=None, **leak):
    if not type(t) in [int, float]:
        t = Int(t)
    if t < 0:
        return
    if t > 9999:
        while True:
            delog('无限挂起')
            time.sleep(9999)
    if t >= 10 and not silent:
        delog(f'睡眠 {t} 秒')
    time.sleep(t)


_sleep = sleep


def is_in_jupyter():
    try:
        ipy = get_ipython()
        if "IPKernelApp" in ipy.config:  # 检查是否是 IPython 内核
            return True
        else:
            return False
    except NameError:
        return False


# https://blog.csdn.net/weixin_42133116/article/details/114371614
class ANSIFormatter():
    CSI = '\033['

    # CSI = '\x1b['
    @staticmethod
    def front(n, s=''):
        return (f'{ANSIFormatter.CSI}38;5;{n}m{s}')

    @staticmethod
    def resetfront(s=''):
        return ANSIFormatter.front(39, s)

    @staticmethod
    def background(n, s=''):
        return (f'{ANSIFormatter.CSI}48;5;{n}m{s}')

    @staticmethod
    def resetbackground(s=''):
        return ANSIFormatter.background(49, s)

    @staticmethod
    def font(n, s=''):
        return (f'{ANSIFormatter.CSI}{n}m{s}')

    @staticmethod
    def reset_all(s=''):
        """
        清除格式
        @param s:
        @return:
        """
        return ANSIFormatter.font(0, s)

    reset = reset_all

    def showall(self=None):
        for i in range(0, 256):
            print(i, ANSIFormatter.front(i, f'-------{i}号颜色--------'), ANSIFormatter.reset(),
                  ANSIFormatter.background(i, '\t' * 100), ANSIFormatter.reset())
        for i in range(0, 110):
            print(ANSIFormatter.font(i), f'这是{i}号示例字体', ANSIFormatter.reset())

    listall = showall


class power_shell:
    def __init__(self, coding='utf-8'):
        import subprocess
        cmd = [self._where('PowerShell.exe'),
               "-NoLogo", "-NonInteractive",  # Do not print headers
               "-Command", "-"]  # Listen commands from stdin
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        self.process = subprocess.Popen(cmd,
                                        stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        startupinfo=startupinfo,
                                        text=True)
        self.coding = coding

    def send_command(self, cmd):
        self.process.stdin.write(cmd + "\n")
        self.process.stdin.flush()

    def read_output(self):
        return self.process.stdout.readline()

    def close(self):
        self.process.terminate()

    @staticmethod
    def _where(filename, dirs=None, env="PATH"):
        from glob import glob
        if dirs is None:
            dirs = []
        if not isinstance(dirs, list):
            dirs = [dirs]
        if glob(filename):
            return filename
        paths = [os.curdir] + os.environ[env].split(os.path.pathsep) + dirs
        try:
            return next(os.path.normpath(match)
                        for path in paths
                        for match in glob(os.path.join(path, filename))
                        if match)
        except (StopIteration, RuntimeError):
            raise IOError("File not found: %s" % filename)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class Cmd:
    @manage_args(init_root=['root'])
    def __init__(self, init_root=None, silent=False):
        """

        @param init_root: cmd的初始目录
        """
        import subprocess
        import threading
        # 创建 cmd 进程并设置 stdin, stdout 和 stderr 为 PIPEs，这样我们可以与其交互
        self.process = subprocess.Popen(
            'cmd.exe',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=10
        )

        # 创建读取线程的监听
        self._stop_thread = threading.Event()
        import queue
        self.output = ''
        self.silent = silent
        self.output_queue = queue.Queue()
        self.err_queue = queue.Queue()
        if init_root == None:
            self.send_command(f"cd {projectpath()}", t=0.2)
        else:
            self.send_command(f"{init_root}", t=0.2)
        self.clear_output()
        self._observe()

    def clear_output(self):
        self.output = ''

    clear = clear_output

    @manage_args(command=['cmd'])
    def send_command(self, command='\n', t=5, silent=None):
        """
        执行命令，然后更新输出
        @param command:
        @param t: 读取后续输出的等待时间
        @return:
        """
        command = Str(command)
        if command[-1] != '\n':
            command += '\n'
        self.process.stdin.write(command)
        copyto(command)
        self.process.stdin.flush()
        # self.refresh_output(t=t, silent=silent)

    execute = send_command
    do = execute

    def _observe(self):
        """
        自动执行不外部调用
        持续获得 stdout，stderr
        @return:
        """
        import threading

        def func1(self):
            while not self._stop_thread.is_set():
                line = self.process.stdout.readline().strip()
                if not line == '':
                    self.output_queue.put(line)
                    log(line)
                    self.output += '\n' + line

        def func2(self):
            while not self._stop_thread.is_set():
                line = self.process.stderr.readline().strip()
                if not line == '':
                    self.err_queue.put(line)
                    warn(line, traceback=False)
                    self.output += '\n' + line

        threading.Thread(target=func1, args=(self,)).start()
        threading.Thread(target=func2, args=(self,)).start()

    def execute_at_once(self, command, t=1, silent=None):
        """
        一次性使用这个类
        @param command:
        @param t:
        @param silent: 是否不显示输出
        @return: 这次的输出
        """
        self.send_command(command, t=t, silent=silent)
        ret = self.output
        self.output = ''
        self.close()
        return ret

    def close(self):
        """
        关闭 cmd
        @return:
        """
        self._stop_thread.set()
        self.send_command('exit')
        # self.__del__()

    def __del__(self):
        """

        @return:
        """
        try:
            import signal
            os.kill(self.process.pid, signal.CTRL_C_EVENT)
            self.process.terminate()
        except Exception as e:
            warn(e, traceback=False)
            pass


@manage_args(path=['filename'])
def load_value(path=None, ):
    """从指定的文件中加载变量"""
    import pickle
    f = file(add_ext(varpath(path), '.pkl'), 'rb')
    return pickle.load(f.f)


get_value = get_var = \
    load_value


@manage_args(s=['script'])
def try_to_execute_script(s, t=0, silent=None,
                          b=None, **leak):
    """
    尝试执行一段代码，异常不停止
    @param s: code
    @return:
    """
    frame = inspect.currentframe().f_back
    s = s.strip('\n')
    for p in ['\t', ' ']:
        count = 0
        while s.startswith(p * (count + 1)):
            count += 1
        if count > 0:
            s = s.replace(p * count, '')
    try:
        local_vars = frame.f_locals
        exec(s, globals(), local_vars)
    except Exception as e:
        if not silent:
            warn(f'使用了代码尝试执行功能，但是失败', s, f'{e}', traceback=False)
    finally:
        # 删除frame引用，防止资源泄漏
        del frame


execute_py = execute = \
    try_to_execute_script


@manage_args(path=['module'])
def execute_module(path=None, root=None, pool=None,
                   b=None, **leak):
    """
    执行一个python文件或者把它加入进程池
    @param path: 不能用 list。因为相关功能用 curiser 函数和 pool 参数替代。
    @param root:
    @param pool: 进程池。（异步进程池）
    @return: prompt的输出
    """
    sleep(2)
    import multiprocessing
    add_ext(path, '.py')
    if not ':' in path:
        path = code_path(path)
    if not os.path.exists(path):
        warn(f'{path} 不存在。')
        return
    if not path.endswith('.py'):
        warn(f'{path} 不是python文件。')
        return

    if pool:
        pool.apply_async(_run_module, args=(path,))
    else:
        try:
            p = multiprocessing.Process(target=_run_module, args=(path,))
            p.start()
        except RuntimeError as e:
            warn('需要主程序在if __name__ == "__main__":中运行 run_module 函数。')


run_module = execute_module


def _run_module(file_path):
    """
    因为不是并行，所以是内部函数
    @param file_path:
    @return:
    """
    import runpy
    if not isfile(file_path, exist=True):
        file_path = codepath(file_path)
    delog(f'开始自动执行{file_path}')
    Run()
    runpy.run_path(file_path, run_name="__main__")


def restart(*a, t=3):
    """
    抛出普通的异常以尝试重新运行
    @param a:
    @return:
    """
    warn(*a)
    sleep(t)
    raise (retrylist[0])


def Exit(*a, **b):
    """
    warn+exit
    @param a:
    @return:
    """
    # try
    import sys
    warn(*a, **b)
    sys.exit(-1)


def Debug():
    """
    转到调试模式
    @return:
    """
    set_env_var(d={'debug': True})


def isDebugging():
    return True == get_env_var('debug')


debugging = \
    isDebugging


def Run():
    set_env_var(d={'debug': False})


def isRunning():
    return False == get_env_var('debug')


# endregion

# 特殊功能函数
# region
def probability(a=None, *x):
    if x:
        a = (a, x[0])
    if isinstance(a, (list, tuple)) and len(a) == 2:
        prob = a[0] / a[1]
        return random.random() < prob
    else:
        return random.random() < a


@manage_args()
def bined_args(*args,
               b=None, **leak):
    """
    必须全不为空或全为空
    @return:
    """
    t = False
    for arg in args:
        if is_type(arg, [list]):
            t = any(enabled(arg) for arg in arg) or t
            continue
        else:
            t = enabled(arg) or t
            continue
        if enabled(arg):
            if t:
                Exit(f'有参数未赋值 {args}', traceback=False)


arg_bined = sync_arg = resonate = reso_args = \
    arg_reso = \
    bined_args


@manage_args()
def arg_mutex(*vars, strict=None,
              b=None, **leak):
    """
    检查一组变量的互斥关系。
    @param group1: 第一组变量的列表
    @param group2: 第二组变量的列表
    @return: 如果满足互斥条件，则返回 True；否则返回 False
    """

    def ret():
        if strict:
            Exit(f'使用了互斥变量{b}', traceback=True)
            return False

    used = 0
    check_lis = [None, False, '', 0]
    for var in vars:
        if used_type(var, [list]):
            t = all(var not in check_lis for var in var)
        else:
            t = not var in check_lis
        if t:
            used += 1
        if used == 2:
            return ret()
mutex=arg_mutex

def urltodict(url):
    """

    @param url:
    @return:
    """
    from urllib.parse import urlparse, parse_qs
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    url_dict = {
        "_scheme": parsed_url.scheme,
        "_netloc": parsed_url.netloc,
        "_path": parsed_url.path,
        "_params": parsed_url.params,
        "_fragment": parsed_url.fragment,
        **query_params
    }
    return url_dict


url2params = urltodict


@manage_args(base_url=['base'], paramdict=['dict'])
def dicttourl(base_url, paramdict):
    """

    @param url_dict:
    @return:
    """
    from urllib.parse import urlparse, urlencode, urlunparse
    parsed_url = urlparse(base_url)
    query_params = urlencode(paramdict, doseq=True)
    new_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        query_params,
        parsed_url.fragment
    ))
    return new_url


param2url = dicttourl


def get_ipconfig(filter='ipv4'):
    """

    @param filter: 过滤只显示返回内容中的哪一条
    @return:
    """
    import subprocess
    import re
    try:
        result = subprocess.check_output(['ipconfig'], universal_newlines=True)
    except subprocess.CalledProcessError:
        return ("无法运行ipconfig命令。")

    ipv4_pattern = r'IPv4 Address[.\s]*: (\d+\.\d+\.\d+\.\d+)'
    matches = re.findall(ipv4_pattern, result)

    if matches:
        for match in matches:
            return (match)
    else:
        return ("未找到IPv4地址。")


def get_lock(name=None, interval=2, max_wait=30):
    """
    主机范围
    @param name: 锁名
    @param interval: 检查间隔
    @return:
    """
    name = standarlizedFileName(name)
    while not createfile(path=lockpath(f'{name}'), silent=False):
        sleep(interval)
        max_wait -= 1
        if max_wait < 0:
            warn(f'{name}锁超时了。删除全部锁。')
            deletedirandfile(lockpath())
            createpath(lockpath())
            return
        continue
    return True


getlock = get_lock


def release_lock(name=None):
    """

    @param name:
    @return:
    """
    name = standarlizedFileName(name)
    deletedirandfile(lockpath(f'{name}'))


releaseloc = release_lock


def similarity(a, b, mode=None):
    """
    比较相似度
    @param a:
    @param b:
    @param mode:
    @return:0~1 / bool
    """
    #     计算两个图片的相似度
    if mode in [None, 'image']:
        if type(a) in [str]:
            if type(b) in [str]:
                if isfile(a) and isfile(b):
                    if isimage(a) and isimage(b):
                        return image_similarity(a, b)

    # 计算两个文件的相似度
    elif mode in [None, 'file_operate']:
        pass
    # 计算两个字符串的相似度
    elif mode in ['str', None, 'string']:
        return string_similarity(a, b)


@manage_args(cutoff=['value', 'treshold'])
def similar(a=None, b=None, cutoff=0.7,
            mode=None,
            kwargs=None, **leak) -> bool:
    return similarity(a=a, b=b, mode=mode) >= cutoff


def resize_image(image, new_width, new_height):
    import cv2
    from numpy import ndarray
    if not type(image) in [ndarray]:
        Exit('不是图片。')
    return cv2.resize(image, (new_width, new_height))


@consume
def image_similarity(image1_path, image2_path, samesize=True, silent=None):
    import cv2
    from skimage.metrics import structural_similarity as ssim

    """
    计算两个图片的相似度
    @param a:
    @param b:
    @param samesize:是否要求两个图片大小一致
    @return:
    """
    if image1_path == image2_path:
        warn('比较的两个图片是同一个文件。')
        return True
    # 读取彩色图像文件
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # 如果两幅图片大小不一致
    if not image1.shape == image2.shape:
        if samesize:
            warn('比较的两个图片大小不一致。')
            return 0
        else:
            # 调整第二幅图片的大小, 让它和第一幅图片大小一致
            image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]),
                                interpolation=cv2.INTER_CUBIC)

    # 计算颜色直方图相似度
    hist1 = cv2.calcHist([image1], [0, 1, 2], None, [
        8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist2 = cv2.calcHist([image2], [0, 1, 2], None, [
        8, 8, 8], [0, 256, 0, 256, 0, 256])
    color_similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    # 计算结构相似度
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    structural_similarity, _ = ssim(gray_image1, gray_image2, full=True)

    # 综合考虑颜色和结构相似度
    similarity = (color_similarity + structural_similarity) / 2
    if not silent:
        delog(f'图片\n\t{image1_path}\n\t{image2_path}\n的相似度为 {similarity}')
    return similarity


similar_image = image_similarity


def capture_screenshot(file_path):
    import PIL.ImageGrab
    """
    获取屏幕截图
    @param file_path:
    @return:
    """
    import screeninfo
    file_path = standarlizedPath(file_path)
    createpath(file_path)

    screens = screeninfo.get_monitors()
    for i, screen in enumerate(screens):
        # 获取显示屏的位置和尺寸
        x = screen.x
        y = screen.y
        width = screen.width
        height = screen.height

        # 获取显示屏的截图
        file_path, root = filenameandpath(file_path)
        file_path, _ = extensionandname(file_path, exist=False)
        file_path = root + file_path + f'_{i}.png'
        screenshot = PIL.ImageGrab.grab((x, y, x + width, y + height))
        screenshot.save(file_path)
        break


def info(s):
    # 如果是类，列举属性和方法
    if not type(s) in [int, str, list, dict, float, tuple, ]:
        att = [type(s)]

        for i in dir(s):
            if not i in dir(object):
                att.append(i)
        return att

    if type(s) in [str]:
        # 磁盘
        if len(s) == 1:
            gb = 1024 ** 3  # GB == gigabyte
            try:
                import shutil
                total_b, used_b, free_b = shutil.disk_usage(
                    s.strip('\n') + ':')  # 查看磁盘的使用情况
            except Exception as e:
                Exit(e)
            # log(f'{s.upper()}' + '盘总空间: {:6.2f} GB '.format(total_b / gb))
            # log('\t已使用 : {:6.2f} GB '.format(used_b / gb))
            # log('\t\t空余 : {:6.2f} GB '.format(free_b / gb))
            return (free_b / gb)

        #     文件（夹）
        if isfile(path=s, exist=True) or isdir(path=s, exist=True):
            s = standarlizedPath(s)
            sss = ''
            if isdir(s):
                sss = '夹'
            log(f'路径：{s}（文件{sss}）')
            log(f'创建日期：{createtime(s)}')
            log(f'修改日期：{modifytime(s)}')
            log(f'访问日期：{accesstime(s)}')
            log(f'大小：{size(s)}MB')

            # 是视频
            if tail(s, '.') in ['wmv', 'mp4']:
                t = videolength(s)
                log(f'{filename(s)} 时长{int(t / 60)}:{t - int(t / 60)}')
            return size(s)
    # 其它类型
    elif type(s) in [list, tuple, dict]:
        if len(s) > 3:
            tip(f'{s[0:2]}...{s[-1]}')
        else:
            tip(s)
        tip(f' \' info of runtime variables: \'\n类型：{type(s)} 大小：{int(int(sys.getsizeof(s) / 1024 / 1024 * 100) / 100.0)}MB 内存地址：{id(s)} 长度{len(list(s))}')
    elif type(s) in [int, str, float, ]:
        tip(
            f' \' info of runtime variables: \'\n类型：{type(s)} 大小：{int(sys.getsizeof(s))}Byte 内存地址：{id(s)}')


# 获取屏幕锁
def getscreenlock():
    return getlock('screen')


def releasescreenlock():
    return release_lock('screen')


# 获取剪贴板锁
def getcopylock():
    return getlock('copy')


# 释放剪贴板锁
def releasecopylock():
    return release_lock('copy')


# 翻译
def translate(s, limit=3):
    if len(s) < limit:
        return ''
    hotkey('alt', 'tab')
    getscreenlock()
    getcopylock()
    click(846, 520)
    hotkey('ctrl', 'a')
    copyto(s)
    hotkey('ctrl', 'v')
    hotkey('enter')
    sleep(len(s) / 1000)
    click(1000, 358)
    sleep(0.5)
    hotkey('ctrl', 'a')
    hotkey('ctrl', 'c')
    hotkey('alt', 'tab')
    releasescreenlock()
    releasecopylock()
    return pastefrom()


# 计数工具语法糖
def count(k=''):
    d = get_env_var('count')
    if d == None:
        d = {}
    if k in d:
        n = d[k] + 1
    else:
        n = 1
    d.update({k: n})

    delog({k: n})
    save_env_var(value={'count': d})
    return n


# endregion

# 键鼠
# region
def get_screens():
    from screeninfo import get_monitors
    monitors = get_monitors()
    sorted_monitors = sorted(monitors, key=lambda m: (m.y, m.x))
    monitor_positions = [(m.x, m.y) for m in sorted_monitors]
    monitor_sizes = [(m.width, m.height) for m in sorted_monitors]

    return monitor_positions, monitor_sizes


def get_screen_places():
    return get_screens()[0]


def get_screen_sizes():
    return get_screens()[1]


def wait_keyboard(s=None):
    import keyboard
    keyboard.wait(s)


def scroll(scale):
    """
    滚动鼠标，负数表示向上滚动
    @param scale:
    @return:
    """
    import pyautogui
    flag = scale / abs(scale)
    while abs(scale) > 101:
        scale = abs(scale) - 100
        x = flag * -100
        pyautogui.scroll(int(x))
    return


def get_screen(path):
    import PIL.ImageGrab
    """
    保存当前屏幕截图
    @param path:
    @return:
    """
    path = standarlizedPath(path)
    createpath(path)
    if isdir(path):
        path += f'{Now().s()}.png'
        path = standarlizedFileName(path)
    PIL.ImageGrab.grab().save(path)


desktop_screen = get_screen


def wait_screen(path, t=3, timeout=60):
    """
    等待直到屏幕上出现内容
    @param picpath:
    @param t:
    @return:
    """
    if not ':' in path:
        path = picpath(path)
    if not isfile(path):
        warn(f'图片{path}不存在')
        return False
    while True:
        if locate_on_screen(path):
            # print(locate_on_screen(path))
            return True
        sleep(t)


def openedge(l, browser='edge'):
    """
    打开一系列的网址
    @param l:
    @return:
    """
    hotkey('win')
    typein(browser)
    hotkey('shift')
    hotkey('enter')
    sleep(2)
    if type(l) == str:
        l = [l]
    for url in l:
        hotkey('alt', 'd')
        copyto(url)
        hotkey('ctrl', 'v')
        hotkey('enter')
        if not url == l[-1]:
            hotkey('ctrl', 't')


open_url = openedge
open_urls = openedge


# 键盘输入
def typein(s, strict=False):
    if strict:
        for i in str(s):
            hotkey(i)
    else:
        copyto(s)
        hotkey('ctrl', 'v')
        sleep(0.5)


def copyto(s):
    import pyperclip
    s = Str(s)
    pyperclip.copy(s)
    sleep(0.1)


@manage_args(t=['sleep'])
def copyto_and_paste(s, t=None):
    copyto(s)
    hotkey('ctrl', 'v')
    hotkey('enter')
    _sleep(t)


def pastefrom():
    import pyperclip
    return pyperclip.paste()


# 键盘
@manage_args(t=['sleep'])
def hotkey(*a, t=None):
    import pyautogui
    pyautogui.hotkey(*a)
    _sleep(0.2 + Int(t))


keyb = hotkey


# 文件大小类
class FileSize(float):
    def __new__(cls, path, silent=False):
        if not isfile(path) and not isdir(path):
            if not silent:
                warn(f'{path}不存在')
            return 0
        value = os.path.getsize(path) / 1024
        return super(FileSize, cls).__new__(cls, value)

    def __str__(self):
        size_in_kb = self  # 因为现在 self 就是浮点数
        if size_in_kb < 1024:
            return f"{size_in_kb:.2f} KB"
        else:
            return f"{size_in_kb / 1024:.2f} MB"


def monitor_dir_size(path, *a, **b) -> bool:
    """

    @param path:
    @param interval:
    @param max_time:
    @param silent:
    @return:
    """
    for i in listfile(path):
        monitor_file_size(i, *a, **b)
    for j in listdir(path):
        monitor_dir_size(j, *a, **b)
    log(f'{path} 大小不再变化完成')


@manage_args(interval=['t'])
def monitor_file_size(path: str, interval: int = None,
                      max_time: int = 999, silent=True,
                      b=None, **leak) -> bool:
    """
    监测指定路径文件的大小是否在一段时间内持续变化。
    文件一开始就不存在就跳过。中途消失就返回True。
    中途文件大小不变就返回 False
    @param path:
    @param interval:
    @param maxtime:
    @param silent: 如果文件不存在是否警告。
    @return:
    """
    if interval == None:
        interval = max_time / 5
    if interval > max_time:
        interval = max_time
    最大时间 = max_time
    检查间隔 = interval
    开始时间 = Time.now()
    if not isfile(path, exist=True):
        if not silent:
            warn(f'文件{path}')
        return True
    上次大小 = FileSize(path, silent=True)

    while 最大时间 > Time.now() - 开始时间:
        if not isfile(path):
            return True
        delog(f'文件{path} 大小 {上次大小}')
        sleep(检查间隔)
        if not isfile(path):
            return True
        当前大小 = FileSize(path)

        # 如果文件大小没有变化，返回True
        if 当前大小 == 上次大小:
            return True

        # 更新上次大小以供下一次迭代使用
        上次大小 = 当前大小

    # 如果由于最大时间超出而退出循环，返回False
    return False


def size(a, sum=0, bit=True, mode=None):
    """

    @param a:
    @param sum:
    @param bit:
    @return:
    """
    if mode in [None, 'disk']:
        if type(a) in [str]:
            s = a
            # 磁盘
            if len(s) == 1:  # GB == gigabyte
                try:
                    import shutil
                    total_b, used_b, free_b = shutil.disk_usage(
                        s.strip('\n') + ':')  # 查看磁盘的使用情况
                except Exception as e:
                    Exit(e)
                return FileSize(free_b)

        if mode in [None, 'file']:
            #     文件
            if isfile(s):
                s = standarlizedPath(s)
                return FileSize(s)

        if mode in [None, 'dir']:
            #     文件夹
            if isdir(s):
                sum = 0
                for i in listfile(s):
                    sum += size(i, bit=bit)
                for i in listdir(s):
                    sum += size(i, bit=bit)
                return sum

    if mode in [None]:
        if type(a) in [list, tuple]:
            for i in a:
                sum = size(i, sum, bit=bit)
            return sum
        if type(a) in [dict]:
            sum = size(keys(a), sum, bit=bit)
            for k in keys(a):
                sum = size(a[k], sum, bit == bit)
            return sum
        return sum + sys.getsizeof(a)


# 在屏幕指定位置进行剪贴板复制粘贴并按下回车
def Input(x, y, s):
    import pyperclip
    import pyautogui
    pyperclip.copy(s)
    pyautogui.click(x, y)
    sleep(1)
    pyautogui.hotkey('ctrl' + 'v')
    sleep(0.5)
    pyautogui.hotkey('Enter')
    sleep(1)


# endregion


# 音视频、图片
# region
def merge_audio(video_path=None, root=None,
                audio_paath=None, output_path=None):
    """

    @param video_path:
    @param root:如果不为 None，其它路径需要是相对路径
    @param audio_paath:
    @param output_path:
    @return:
    """
    if not root == None:
        video_path = root + '/' + video_path
        audio_paath = root + '/' + audio_paath
        output_path = root + '/' + output_path
    if output_path == None:
        output_path = filename(video_path)
        output_path = rmext(output_path)

    T = Cmd()
    c = (
        f'ffmpeg -i "{video_path}" -i "{audio_paath}" -c:v copy -c:a aac -strict experimental "{output_path}"')
    copyto(c)
    T.execute(c)


#     拼接图片
def combineimages(inputpath=None, outputpath=None, outputname=None, mode='vertical', reverse=None,
                  filelist=None,
                  cuttop=0, cutbottom=0, cutleft=0, cutright=20):
    """

    @param inputpath:
    @param outputpath:
    @param outputname:
    @param mode:
    @param reverse:
    @param filelist:
    @param cutbottom:
    @param cuttop:
    @param cutleft:
    @param cutright: 总有些傻哔情况有点右侧进度条
    @param cuttop:顶部裁剪
    @return:
    """

    def do(img1, img2, mode='vertical', outputpath=None,
           ratio1=0.3, ratio2=0.3, scale1=70, scale2=70):
        import cv2
        """
        裁剪后自动识别拼接图片
        @param img1:上图片路径(确定？)，是不断扩张的图片。
        @param img2:
        @param mode:
        @param outputpath:
        @param ratio1:
        @param ratio2: 默认地根据图片的长宽比例来设置重合验证长度
        @param scale1: 我也不知道现在有什么用

        @param scale2:与image1的重合验证部分
        @return:
        """
        # 新版 chrome 有进度条，image2 掉顶格2像素变为白色
        image1 = cv2.imread(img1)
        image2 = cv2.imread(img2)[2:, :]
        if image1 is None:
            warn(f'图片读取为空  {img1}')
            return
        if image2 is None:
            warn(f'图片读取为空  {img2}')
            return

        # 原图去掉拼接方向上衔接须裁剪处
        if mode == 'vertical':
            # 允许中断后继续操作，因此有时候不处理image1
            image1 = image1[:image1.shape[0] - cutbottom, :]
            image2 = image2[cuttop:image2.shape[0]:]

        matchimage1 = image1
        # image1 的忽略历史累积部分
        level1 = 0
        if mode == 'vertical':
            if image1.shape[0] > 3000:
                level1 += image1.shape[0] - 2000
                matchimage1 = image1[-2000:, :]
        matchimage2 = image2
        scale1, scale2 = min(scale1, int(matchimage1.shape[0] * ratio1)), min(scale2, int(
            matchimage2.shape[0] * ratio2))
        if mode == 'vertical':
            matchimage2 = matchimage2[:scale2, :]

        # 匹配图去掉垂直于拼接方向的部分
        if mode == 'vertical':
            matchimage1 = matchimage1[:, cutleft:image1.shape[1] - cutright]
            matchimage2 = matchimage2[:, cutleft:image2.shape[1] - cutright]

        # 需要从下到上匹配，所以要翻转
        # 1 是template，是被滑动的图像。
        result_filpped = cv2.matchTemplate(cv2.flip(matchimage2, 0), cv2.flip(matchimage1, 0),
                                           cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(
            cv2.flip(result_filpped, 0))
        if mode == 'vertical':
            max_loc = (max_loc[0], level1 + max_loc[1])
        delog('相似匹配位置', max_loc)
        # look(matchimage1)
        # look(matchimage2)

        if mode == 'vertical':
            if max_val < 0.75 or max_loc == (0, 0):
                warn('图片匹配失败，直接拼接')
                max_loc = (0, image1.shape[0])
            cv2.imwrite(img1, image1[:max_loc[1]])
            image3 = cv2.vconcat([image1[:int(max_loc[1]), :], image2])
            cv2.imwrite(img1, image3)

    if outputpath == None:
        if outputname == None:
            outputpath = parentpath(inputpath) + 'combined.jpg'
        else:
            outputpath = parentpath(inputpath) + outputname
    if filelist == None:
        filelist = []
        l1 = SortedName(listfile(inputpath, full=False))
        for i in l1:
            filelist.append(inputpath + '/' + i)
    if reverse:
        filelist.reverse()
    first = filelist.pop(0)
    for i in filelist:
        do(first, i, )
    if outputpath == None:
        if outputname == None:
            outputname = 'basic.png'
        outputpath = parentpath(inputpath) + outputname
    sleep(2)
    move(first, outputpath)


class pic():
    def __init__(self, path):
        import PIL.Image
        path = standarlizedPath(path)
        self.path = path
        try:
            self.img = PIL.Image.open(path)
            self.width, self.height = self.img.size
            self.type = self.img.format
            self.complete_img_suffix()
        except Exception as e:
            pass

    #         自动补全后缀名
    def complete_img_suffix(self):
        if not '.' in self.path:
            self.img.close()
            newname = self.path + '.' + (self.type.lower())
            rename(self.path, newname)
            self.__init__(newname)

    def __del__(self):
        try:
            self.img.close()
        except Exception as e:
            pass


class img(pic):
    pass


class video():
    def __init__(self, path):
        import cv2
        self.path = path
        self.cap = cv2.VideoCapture(path)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.framecount = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if not self.fps == 0:
            self.duration = self.framecount / self.fps
        self.type = self.path.split('.')[-1]


# 识别图片格式（后缀名）
def imgtype(path):
    import PIL.Image
    img = PIL.Image.open(path)
    return img.format


# 从视频中提取声音
def mp4tomp3(src, tar=None):
    from moviepy.editor import VideoFileClip
    if tar == None:
        tar = f'{removetail(src, "mp4")}mp3'
    src, tar = standarlizedPath(
        src, strict=True), standarlizedPath(tar, strict=True)
    if isdir(src) and isdir(tar):
        for f in listfiletree(src):
            if '.mp4' in f:
                VideoFileClip(f).audio.write_audiofile(
                    f'{tar}\\{filename(f)}.mp3')
        return
    if not isfile(src) and not '.mp4' in src:
        Exit(f'{src}不是mp4文件1')
    VideoFileClip(src).audio.write_audiofile(tar)


videotoaudio = video2audio = mp4tomp3


# 使用ffmpeg剪切视频
@manage_args(inputpath=['src'])
def cutvideo(inputpath, start, end, outputpath=None,
             _type=None,
             b=None, **leak):
    if ' ' in inputpath:
        newapth = inputpath.replace(' ', '')
        rename(inputpath, newapth)
        inputpath = newapth
        warn(f'文件名中有空格，可能会出错。已重命名{inputpath}')
    if not has_ext(inputpath):
        ext = '.mp4'
    else:
        fname, ext = extandname(inputpath)
    if outputpath == None:
        outputpath = fname + '-cut' + ext
    chdir(parentpath(inputpath))
    sourcepath = os.path.abspath(inputpath)
    outputpath = os.path.abspath(outputpath)
    delete(outputpath)
    if _type is None:
        if any(ext in inputpath for ext in ['.mp4', '.flv', '.mkv']):
            _type = 'video'
        else:
            _type = 'audio'
    if _type == 'video':
        command = f'ffmpeg  -i {standarlizedPath(sourcepath)} -vcodec copy -acodec copy -ss {start} -to {end} {outputpath} -y'
    elif _type == 'audio':
        command = f'ffmpeg -i {standarlizedPath(sourcepath)} -ss {start} -to {end} {outputpath} -y'
    delog(f'命令行 {command}')
    os.system('"%s"' % command)


clip_mp3 = cutvideo


# 使用 ffmpeg 剪切音频
@manage_args()
def cutaudio(inputpath=None, start=None,
             end=None, outputpath=None,
             ext='wav',
             b=None, **leak
             ):
    if outputpath == None:
        outputpath = removetail(inputpath, f'.{ext}') + f'-cut.{ext}'
    sourcepath = os.path.abspath(inputpath)
    outputpath = os.path.abspath(outputpath)
    command = f'ffmpeg  -i {standarlizedPath(sourcepath)} -vcodec copy -acodec copy -ss {start} -to {end} {outputpath} -y'
    print(command)
    os.system('"%s"' % command)


# 使用ffmpeg提取音频
# def extractaudio(inputpath, outputpath):
#     sourcepath = os.path.abspath(standarlizedPath(inputpath))
#     command = f'ffmpeg -i {inputpath} -vn -codec copy {outputpath}'
#     print(command)
#     os.system('"%s"' % command)


# 返回音频的秒数
def videolength(s):
    from moviepy.editor import VideoFileClip
    if not isfile(s):
        Exit(s)
    return VideoFileClip(s).duration


# endregion


# 进程池与线程池
# region


class pool():
    def __init__(self, maxworker=10):
        import concurrent.futures
        self.e = concurrent.futures.ThreadPoolExecutor(max_workers=maxworker)

    def doorwait(self, fn, *a):
        # self.e.map(fn,[[*a],])
        self.f = fn
        # print(a)
        self._do(a)
        print(a)

    def _do(self, a):
        self.e.submit(self.f, *a)

    def execute(self, fun, *a):
        self.doorwait(fun, *a)

    def rest(self):
        return len(self.e.as_conpleted())


# endregion

# 文件系统读写 & 数据记录
# region
@manage_args(data=['path'])
def deduplicate(data=None,
                b=None, *leak):
    import pandas as pd
    if used_type(data, [pd.DataFrame]):
        duplicates = data.duplicated()
        return data[~duplicates]
    if is_type(data, [str]):
        data = add_ext(data, '.csv')
        if isfile(path=data, exist=True):
            df = csv2df(data)
            df = deduplicate(data=df, **exclude(b, 'data'))
            deletedirandfile(path=data)
            df2csv(data=df, path=data)


simplify = \
    deduplicate


def csv2df(path):
    import pandas as pd
    return pd.read_csv(path)


@manage_args()
def to_df(with_id=True, data=None,
          b=None, **leak):
    import pandas as pd
    df = pd.DataFrame(data)
    if with_id:
        df.insert(0, 'ID', range(1, 1 + len(df)))
    return df


@manage_args()
def to_csv(data=None, with_id=None, path=None,
           mode='a', duplicate=True,
           b=None, **leak):
    import pandas as pd
    if is_type(data, [list]):
        df = to_df(data=data)
    if is_type(data, [pd.DataFrame]):
        df = data
    path = add_ext(path, 'csv')
    createpath(path)
    if mode == 'a':
        if isfile(path, exist=True):
            existing_df = pd.read_csv(path)
            df = pd.concat([existing_df, df], ignore_index=True)
            if not duplicate:
                df.drop_duplicates(inplace=True)
        df.to_csv(path, index=with_id)


df2csv = df_to_csv = dftocsv = \
    to_csv


def chdir(path=None, exist=True, create=None):
    """

    @param path:
    @param exist: 路径不存在则报错
    @return:
    """
    arg_mutex([create], [exist])
    if create:
        createpath(path)
    if not isdir(path=path, exist=True):
        if exist:
            Exit(f'{path} 不存在')
        else:
            return False
    os.chdir(standarlizedPath(path))


@manage_args()
def get_full_filename(root, filename, recursive=True,
                      interval=2, loop=20,
                      b=None, **leak):
    """
    从文件夹中获取文件名的完整文件名
    @param root:
    @param filename:文件名（不带路径
    @param recursive: 异步
    @return:
    """
    if loop < 3:
        loop = 3
    o_loop = loop
    while True:
        loop -= 1
        for i in listall(root, full=False):
            if filename in i:
                return i
        if not recursive:
            return False
        sleep(interval)
        if loop < 0:
            warn(f'get_full_filename({root},{filename})超时{o_loop}*{interval}')
            return False


set_root_path = set_root = set_work_dir = setworkdir = change_root = \
    chdir


class file():
    def __init__(self, path, mode, encoding=None):
        self.path = path
        self.mode = mode
        self.encoding = encoding
        self.f = open(path, mode, encoding=encoding)

    def look(self):
        look(self.path)

    def Open(self):
        Open(self.path)


@listed()
def json_to_csv(path):
    """
    将自己的记录转换为csv
    @param path:
    @return:
    """


def filenameandpath(s):
    return filename(s), parentpath(s) + '/'


def delete_duplicate(path):
    """
    删除重复文件（(1)(2)(3)(4)...）
    @return:
    """
    path = standarlizedPath(path)
    dlis = []
    if not isdir(path):
        warn(f'{path} 不是已存在路径？')
        return False
    for i in listfile(path):
        i = filename(i)
        i1, i2 = extensionandname(i)
        for j in range(1, 5):
            s = (+f'{path}/{i1}({j}){i2}')
            if isfile(s):
                dlis.append(s)
    log(dlis)
    # deletedirandfile(dlis)


def str_similarity(s1, s2):
    """
    计算两个字符串的相似度
    @param s1:
    @param s2:
    @return:
    """
    if not type(s1) in [str] or not type(s2) in [str]:
        warn('similar 输入的不是字符串')
        return False

    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        dp[i][0] = i
    for j in range(1, n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i]
                [j - 1], dp[i - 1][j - 1])
    return dp[m][n]


def delete_similar(path, new=False):
    """
    删除目录下名称相似的同大小文件和文件夹。保留创建时间更早的。一次只会二选一。
    @param path:
    @param new:是否保留创建时间更晚的
    @return:
    """
    files = listfile(path)
    dirs = listdir(path)
    delete = []
    retain = []

    def func(l):
        for i in l:
            for j in l[l.index(i) + 1:]:
                if i in delete or j in delete:
                    continue
                if size(i) == size(j) and similarity(i, j) / max(len(filename(i)),
                                                                 len(filename(j))) < 0.1:
                    if createtime(i) < createtime(j) and new or createtime(i) > createtime(
                            j) and not new:
                        ii = i
                        jj = j
                    else:
                        ii = j
                        jj = i
                    delete.append(ii)
                    retain.append(jj)
                    break

    func(files)
    func(dirs)
    # out([f'以下是要删除的文件 {len(delete)}\n'] + delete + [f'\n以下是被保留的文件 {len(retain)}\n'] + retain)
    deletedirandfile(delete)


def delete_similar_image(root, ratio=0.97, samesize=False, silent=None):
    """
    删除目录下近似的图片。保留 listfile 的前
    @param root:
    @param ratio: 相似度
    @return:
    """
    lis = [i for i in listfile(root) if isimage(i)]
    dlis = []
    # delete_similar(root)
    lis.sort()
    for x, i in enumerate(lis):
        for j in lis[x + 1:x + 3]:
            if image_similarity(i, j, samesize=samesize, silent=silent) > ratio:
                dlis.append(j)
                break
    deletedirandfile(dlis)
    return dlis


def create_shortcut(source, target=None):
    """

    @param source: 源文件/文件夹
    @param target: 快捷方式位置。默认为在桌面的同名。
    @return:
    """
    import winshell
    if not source[1] == ':':
        source = projectpath(source)
    source = standarlizedPath(source)
    if target == None:
        target = f'C:/Users/username/Desktop/{extensionandname(source)[0]}.lnk'
    if isdir(source):
        folder_shortcut = winshell.shortcut(target)
        folder_shortcut.path = source
        folder_shortcut.write()
    if isfile(source):
        file_shortcut = winshell.shortcut(target)
        file_shortcut.path = source
        # shell = Dispatch('WScript.Shell')
        # file_shortcut.working_directory = shell.SpecialFolders('Desktop')
        file_shortcut.write()


def cleardir(path):
    path = standarlizedPath(path)
    deletedirandfile(path)
    createpath(path + '/')


# 判断路径存在
@manage_args(not_null=['notempty'])
def exists(path, not_null=None,
           b=None, **leak,
           ):
    return os.path.exists(path) and (
            not not_null or (
        not 0 == size(path)
    ))


# 解压zip文件
def unzip(zippath, targetpath=None):
    zfile = zipfile.ZipFile(zippath)
    if targetpath == None:
        targetpath = zippath.replace('.zip', '')
    if isdir(targetpath):
        pass
    else:
        createpath(targetpath)
    for f in zfile.namelist():
        zfile.extract(f, targetpath)
        # zfile.extract(f, targetpath,overwrite=True)
    zfile.close()


def regeneratename(originalname, targetpath, regenerate=None, issame=None, originalpath=None):
    """
    要新建的文件/文件夹已存在时，新命名，并判断是否覆盖。线程不安全。
    @param originalname:原来的名字。不确定目标路径是否存在同样的
    @param targetpath:目标路径
    @param regenerate: 方法。传入旧名字，返回新名字。默认下划线+数字
    @param issame: 方法。判断内容是否相同
    @param originalpath: 如果不为空，说明原来的文件是存在的。就可以使用比较大小作为默认比较内容方法。
    @return: 存在同样的文件/文件夹 ；新的文件/文件夹名
    """
    newname = originalname
    if regenerate == None:
        # 下划线+数字 自动生成新名字
        def regenerate(oldname):
            oldname, ext = extensionandname(oldname, exist=False)
            if not research(r'_\d$', oldname):
                return oldname + '_1' + ext
            originalname, count = splittail(oldname, '_')
            return f'{originalname}_{int(count) + 1}{ext}'

    # 检查目标位置名称是否被占用
    def havename(newname, targetpath):
        return isfile(f'{targetpath}/{newname}') or isdir(f'{targetpath}/{newname}')

    # 检查是否存在同样的文件/文件夹
    def tellsame(newname, targetpath):
        if havename(newname, targetpath):
            if issame == None:
                # 源文件不存在，无法比较大小。默认相同
                if originalpath == None or not exists(originalpath + '/' + originalname):
                    return False
                #     默认比较大小
                return int(size(originalpath + '/' + originalname)) == int(
                    size(targetpath + '/' + newname))
            return issame(newname, targetpath)
        return False

    b = tellsame(newname, targetpath)
    while havename(newname, targetpath):
        newname = regenerate(newname)
        b = tellsame(newname, targetpath) or b
    return b, newname


def extension(*a, **b):
    """
    获取文件的扩展名（后缀名）带点
    """
    return extensionandname(*a, **b)[1]


get_ext = ext = \
    extension


# 判断路径的文件名是否含有扩展名
def has_ext(a):
    a = extension(a, with_dot=False)
    if a:
        return a


def rmextension(fname):
    return extensionandname(fname)[0]


rmext = rmextension


@manage_args(withdot=['with_dot'])
def extensionandname(fname, silent=True,
                     exist=True, parentpath=False,
                     withdot=True, full=None
                     ):
    """
    分割带路径的文件名和.+扩展名
    @param fname:
    @param silent:
    @param exist:
    @param parentpath: 返回是否带路径名
    @param withdot: 返回是否带点

    @param full:
    @return:
    """
    if full == False:
        parentpath = False
        exist = False
    if exist:
        if not isfile(fname, notnull=exist):
            if not silent:
                Exit(f'文件 {fname} 不存在')

    if not '.' in fname:
        if not silent:
            warn(f'文件 {fname} 没有扩展名')
        return fname, ''

    if not parentpath:
        fname = filename(fname)
    ret = fname[0:fname.rfind('.')], fname[fname.rfind('.'):]
    if withdot:
        return ret
    else:
        return ret[0], ret[1][1:]


filenameandext = extandname = splitext = \
    extensionandname


# 移除空文件夹
def rmempty(root, tree=None, silent=False):
    """

    @param root:
    @param tree:  是否处理子文件夹
    @param silent:
    @return:
    """
    dlis = []
    if not tree == False:
        for i in listdir(root):
            if [] == listdir(i) + listfile(i):
                dlis.append(i)
    if not dlis == []:
        if not silent:
            out(dlis)
            warn('确认删除这些空文件夹，输入任意开始删除，否则请立即停止程序。')
            c = input()
        deletedirandfile(dlis)


@listed()
def look(path):
    """
    打开文件或者网页
    @param path:
    @return:
    """
    from numpy import ndarray
    from cv2 import imwrite

    if type(path) in [dict]:
        return look(dicttojson(path))

    # 自定义数据文件
    if type(path) in [pcsv, Csv, txt, rtxt, rjson, cache]:
        try_to_execute_script("""look(parentpath(path.path))""")
        return

    # 图片
    if type(path) in [ndarray]:
        p = cachepath('cv2/look.png')
        createpath(p)
        deletedirandfile([p])
        imwrite(p, path)
        look(p)
        return

    if 'https' in path:
        return openedge(path)

    # 路径
    if isdir(path, exist=True):
        path = standarlizedPath(path)
        return os.startfile(path)
    if not isfile(path, exist=True, notnull=False):
        return warn(f'不存在文件或文件夹{path}')
    try:
        os.startfile(path)
    except Exception as e:
        warn(r'打开失败， {path}')
        Exit(e)


def Open(path):
    return look(path)


# 合法化文件名
def standarlizedFileName(s):
    '_1_171915336a3bc770~tplv-t2oaga2asx-zoom-in-crop-mark 4536 0 0 0.image.webp'
    if s == '':
        return s
    s = re.sub('/|\?|>|<|:|\n|/|"|\*', ' ', s)
    s = re.sub('\|', '丨', s)
    sub = '�'
    s = s.replace('\\', sub)
    s = s.replace('\r', sub)
    s = s.replace('\t', sub)
    s = s.replace('\x08', sub)
    s = s.replace('\x1c', sub)
    s = s.replace('\x14', sub)

    tail = ''
    while not s == '' and s[-1] in [' ', '.']:
        tail = s[-1] + tail
        s = s[:-1]
    tail = tail.replace('.', '。')
    tail = tail.replace(' ', '_')
    s += tail

    head = ''
    while not s == '' and s[0] in [' ', '.']:
        head = s[0] + head
        s = s[1:]
    head = head.replace('.', '。')
    head = head.replace(' ', '_')
    s = head + s
    return s[:224]


def standarlizedPath(s='', strict=False) -> str:
    """
    统一路径格式。并且转化为完整路径。
    或者是返回当前脚本的路径。
    @param s:
    @param strict:
    @return:
    """
    if s == '':
        s = __file__
    s = s.replace('\\', '/')
    is_tail_slash = s[-1] == '/'

    # 规范化每一层文件夹名
    while (' /') in s:
        s = s.replace(' /', '/')
    s = s.strip(' ')
    ss = s
    s = ''
    for i in ss.split('/'):
        if i in ['.', '..', '...']:
            s += i
            continue
        if len(i) == 2 and i[-1] == ':':
            s += i
            continue
        else:
            s += '/' + standarlizedFileName(i)

    try:
        s = os.path.abspath(s)
    except Exception as e:
        Exit(s, e)
    if is_tail_slash:
        s += '/'
    if strict:
        return s.replace('/', '\\')
    return s.replace('\\', '/')


def mix_path(base_path, s=''):
    """
    其它快捷路径的基础方法
    @param base_path:
    @param s:
    @return:
    """
    if s == '':
        return standarlizedPath(base_path)
    if base_path in s or len(s) > 2 and s[1] == ':':
        return standarlizedPath(s)
    if './' in s:
        s = s[2:]
    if not s == '':
        s = '/' + s
    return standarlizedPath(f'{base_path}{s}')


# 隐藏目录
def selfpath(s=''):
    return mix_path(projectpath('self/'), s)


self_path = selfpath


def browser_path(s=''):
    return mix_path(projectpath('browser/'), s)


browserpath = browser_path


def src_path(s=''):
    return mix_path(projectpath('src/'), s)


# 收藏目录


def collectionpath(s=''):
    return mix_path(selfpath('collections&files/'), s)


# 网页爬虫目录
def shotspath(s=''):
    return mix_path(selfpath('collections&files//网页集锦'), s)


# 用户目录
def userpath(s=''):
    if 'C:/' in s:
        return
    return mix_path(f'C:/Users/{user}', s)


# 项目根目录
def projectpath(s=''):
    return mix_path('D:/Kaleidoscope', s)


sys.path.append(projectpath())


# js 脚本目录
def jspath(s=''):
    if not '.js' in s:
        s += '.js'
    return mix_path(codepath('js'), s)


js_path = \
    jspath


# 可执行文件脚本目录
def exec_path(s=''):
    return mix_path(projectpath('executable'), s)


sys.path.append(exec_path())

executable_path = executablepath = \
    exec_path


def varpath(s=''):
    """
    序列化文件目录
    @param s:
    @return:
    """
    return mix_path(projectpath('cache/var'), s)


variable_path = varpath


# 临时文件目录
def cachepath(s=''):
    return mix_path(projectpath('cache'), s)


cache_path = cachepath


def code_path(s=''):
    return mix_path(projectpath('src'), s)


codepath = code_path


def records_path(s=''):
    return mix_path(projectpath('records'), s)


recordpath = records_path
record_path = records_path


def download_path(s=''):
    return mix_path(cachepath('download'), s)


downloadpath = \
    download_path


def lockpath(s=''):
    return mix_path(cachepath('lock'), s)


# 图片目录
def picpath(s=''):
    if not '.' in s[-5:]:
        s = s + '.png'
    return mix_path(projectpath('pic'), s)


imagepath = picpath


# 视频目录
def videopath(s=''):
    if not '.' in s[-5]:
        s = s + '.mp4'
    return mix_path(projectpath('cache'), s)


# 八爪鱼目录
def octopus_path(s=''):
    return mix_path(projectpath('octopus'), s)


# 测试文件目录
def testpath(s=''):
    return mix_path(projectpath('test'), s)


# 用户配置文件目录
def settingspath(s=''):
    return mix_path(projectpath('settings'), s)


def jsonpath(s=''):
    return mix_path(projectpath('json'), s)


# 下属的文件夹和文件
@manage_args()
def listall(path=None, full=False,
            b=None, **leak):
    return listfile(path, full) + listdir(path, full)


# 判断是否是空的文件夹
def isemptydir(path, exist=True):
    path = standarlizedPath(path)
    if exist:
        if not isdir(path):
            warn(f'{path}不是文件夹，请检查路径。')
            return False
    if [] == listfile(path) + listdir(path):
        return True
    else:
        return False


# 访问时间
def accesstime(path):
    path = standarlizedPath(path)
    t = os.path.getatime(path)
    return Time(t)


# 创建时间
def createtime(path):
    path = standarlizedPath(path)
    t = os.path.getctime(path)
    return Time(timestamp=t)


# 修改时间
def modifytime(path):
    path = standarlizedPath(path)
    t = os.path.getmtime(path)
    return Time(timestamp=t)


@manage_args(json_str=['json', 'json_data'])
def out(s=None, d=None, json_str=None,
        silent=False, target='out',
        mode='rewrite'
        ):
    """

    @param s: str
    @param d: dict
    @param json_data: json str
    @param silent:
    @param target:
    @param mode:
    @return:
    """
    global fout
    if used_arg(s):
        f = fout = txt(cachepath(target))
        if mode == 'rewrite':
            f.l = []
            f.save()
            f.add(s, silent=True)
        elif mode == 'a':
            f.add(s, silent=True)
    if used_arg(json_str):
        d = jsontodict(json_str)
    if used_arg(d):
        fout = jsondata(cachepath(target))
        fout.data = d
        fout.save()
    Open(fout.path)


def provisionalout(s, silent=True, path='pout.txt'):
    f = txt(cachepath(path))

    def do(s):
        f.add(s)

    do(s)
    log(f.path)
    if silent == False:
        Open(f.path)


pout = provisionalout


# 在固定文件进行输入
def provisionalin():
    f = txt(desktoppath('pout.txt'))
    return f.l


# 重命名文件或文件夹
def rename(s1, s2, overwrite=True):
    s1 = standarlizedPath(s1)
    s2 = standarlizedPath(s2)
    if overwrite and (isdir(s2, exist=True) or isfile(s2, exist=True, notnull=False)):
        if size(s1) >= size(s2):
            deletedirandfile(s2)
        else:
            deletedirandfile(s1)
            return
    os.rename(standarlizedPath(s1), standarlizedPath(s2))


def isfile(path=None, s=None, notnull=True, exist=True):
    """
    判断是否是存在文件
    @param s:
    @param notnull: 文件不为空
    @return:
    """
    import re
    if not path == None:
        s = path
    s = standarlizedPath(s)
    if not type(s) in [str]:
        warn(f'isfile的参数必须是字符串，而不是{type(s)}')
        return False
    if not exist and re.search(r'\.[a-zA-Z]{1,5}$', s):
        return True
    if os.path.isfile(s):
        if notnull:
            try:
                return not 0 == os.path.getsize(s)
            except:
                pass  # 看一下调用堆栈哪一步是在 try 里，为什么不会断
        return True
    return False


def ispic(s, strict=False):
    import PIL.Image
    """
    判断文件是否是图片
    @param s:
    @param strict: 是否采用开销更大的方法
    @return:
    """
    if not isfile(s):
        return False
    if strict:
        try:
            PIL.Image.open(s)
            return True
        except Exception as e:
            return False
    else:
        if not extension(s, withdot=False) in ['png', 'jpg', 'jpeg', 'bmp', 'gif']:
            return False
    return True


isimage = ispic


@manage_args(s=['path'])
def isdir(s=None, exist=False):
    """
    判断是否是存在文件夹
    @param s:
    @return:
    """
    if not type(s) in [str]:
        return False
    if not exist and not isfile(s, exist=False):
        return True
    return os.path.isdir(s)


# 复制文件夹
def copydir(s1, s2):
    import shutil
    s1, s2 = standarlizedPath(s1), standarlizedPath(s2)
    if isdir(s1):
        shutil.copytree(s1, s2)


def copyfile(s1, s2, overwrite=False):
    """
    复制文件
    @param s1:
    @param s2:
    @param overwrite:
    @return:
    """
    s1, s2 = standarlizedPath(s1), standarlizedPath(s2)
    createpath(s2)
    if overwrite:
        deletedirandfile(f'{pathname(s2)}/{filename(s1)}')

    if isfile(s1):
        import shutil
        shutil.copy(s1, s2)
    #     # s2 是文件名
    #     if len(pathname(s2))+1<len(s2):
    #         s2,newname=pathname(s2),s2
    #         shutil.copy(s1, s2)
    #         rename(f'{s2}/{filename(s1)}', f'{s2}/{newname}')
    #
    #     # s2是路径名
    #     else:
    #         if pathname(s1)==pathname(s2):
    #             warn('复制文件时源和目标再同一目录下，不做任何操作')
    #             return
    #         shutil.copy(s1,s2)
    # else:
    #     warn(f'不存在文件，请检查 {s1}')


@manage_args(s1=['src', 'source', 'ori', 'original'],
             s2=['tar', 'des', 'target', 'desti', 'destination'])
def move(s1=None, s2=None, overwrite=False, silent=True,
         autorename=True, merge=True, skip=None):
    """
    移动文件或文件夹
    @param s1:
    @param s2:
    @param overwrite: 是否覆盖同名文件。如果autorename，同名内容不同文件会重命名而不是覆盖。
    @param autorename: 是否重命名同名文件。如果overwrite，同名同内容文件会直接覆盖而不是重命名。
    @param merge: 是否合并同名文件夹。如果autorename，同名文件夹会重命名而不是合并。
    @param silent:
    @return:
    """
    import shutil
    if isfile(s1, exist=True):
        if isdir(s2, exist=True):
            return move(s1, f'{s2}/{filename(s1)}', overwrite, silent, autorename, merge)
        if isfile(s2, exist=True):
            b, newname = regeneratename(
                filename(s1), parentpath(s2), originalpath=parentpath(s1))
            if overwrite:
                if b:
                    deletedirandfile(s1)
                    delog(f'移动时已有相同文件 {s2}。不移动删除原文件。')
                    return
                # else:
                #     deletedirandfile(s2)
            if autorename:
                if b:
                    delog(f'移动时已有相同文件 {s2}。重命名 {newname}。')
                else:
                    delog(f'移动时已有不同内容文件 {s2}。重命名 {newname}。')

            if not autorename and not overwrite:
                Open(parentpath(s1))
                Open(parentpath(s2))
                warn(f'移动时已有文件。请检查 {s1} {s2}')
            s2 = f'{parentpath(s2)}/{newname}'
        createpath(s2)
        # shutil.move会自动重命名
        shutil.move(standarlizedPath(s1), standarlizedPath(s2))
        return

    if isdir(s1):
        if isfile(s2, exist=False):
            Exit(f'移动文件夹为文件错误。 {s1} {s2}')
        if isdir(s2, exist=False):
            if merge:
                for all in listall(s1, full=True):
                    move(all, f'{s2}/{filename(all)}', overwrite=overwrite, silent=silent,
                         autorename=autorename, merge=merge)
            else:
                # 思路是直接把文件夹当作文件来判断。因此直接copy上面的逻辑
                b, newname = regeneratename(filename(s1), parentpath(s2),
                                            originalpath=parentpath(s1))
                if b and overwrite:
                    delog(f'移动时已有相同文件夹 {s2}。覆盖。')
                else:
                    if autorename:
                        if b:
                            delog(f'移动时已有相同文件夹 {s2}。重命名 {newname}。')
                        else:
                            delog(f'移动时已有不同内容文件夹 {s2}。重命名 {newname}。')
                    if not autorename and not overwrite:
                        Open(parentpath(s1))
                        Open(parentpath(s2))
                        Exit(f'移动时已有文件夹。请检查 {s1} {s2}')
            deletedirandfile(s1)
            return

    shutil.move(standarlizedPath(s1), standarlizedPath(s2))
    if not silent:
        log(f'移动完成：从 {s1} 到 {s2}')


@listed()
def listdir(path, full=True):
    """

    @param path:
    @param full: 是否使用标准路径格式
    @return:
    """
    path = standarlizedPath(path)
    for (root, dirs, files) in os.walk(path):
        ret = dirs
        for i in ['$RECYCLE.BIN', 'System Volume Information']:
            try:
                ret.remove(i)
            except Exception as e:
                pass
        # delog(str(ret))
        if full == False:
            return ret
        ret1 = []
        for i in ret:
            ret1.append(standarlizedPath(root + '/' + i))
        return ret1
    return []


@listed()
def listfile(path, full=True):
    path = standarlizedPath(path)
    for (root, dirs, files) in os.walk(path):
        ret = files
        for i in ['DumpStack.log', 'DumpStack.log.tmp', 'pagefile.sys']:
            try:
                ret.remove(i)
            except Exception as e:
                pass
        if not full:
            return ret
        ret1 = []
        for i in ret:
            ret1.append(standarlizedPath(root + '/' + i))
        # delog(str(ret))
        return ret1
    return []


def listfiletree(path):
    """
    listall
    @param path:
    @return:
    """
    lis = []
    lis += listfile(path)
    for i in listdir(path):
        lis += listfiletree(i)
    return lis


# 直接返回路径的文件夹路径
def pathname(s=None):
    s = standarlizedPath(s)
    return s[:s.rfind('/') + 1]


path_name = pathname


def parentpath(s):
    while s[-1] in ['\\', '/']:
        s = s[:-1]
    return pathname(s)


parent_path = parentpath


# 返回文路径的文件名
def filename(s):
    s = standarlizedPath(s)
    s = s[s.rfind('/') + 1:]
    if s == '':
        warn('空')
        sys.exit(-1)
    return standarlizedFileName(s)


file_name = filename


def add_extension(path, extension, strict=True):
    """
    给路径文件名加上扩展名
    :param path: 原始路径名
    :param extension: 不带"."的扩展名，可以是字符串或列表
    :param strict: 如果疑似已经有扩展名则强制退出
    :return: 加上扩展名的路径名
    """
    path = standarlizedPath(path)
    if extension[0] == '.':
        extension = extension[1:]
    if path.endswith('/'):
        Exit(f'加扩展名时路径不应以/结尾！ {path}')
    if isinstance(extension, str):
        if '.' in path and not path.endswith('.' + extension):
            warn(f'疑似已经有扩展名！ {path}')
            if strict:
                Exit('疑似已经有扩展名！')
        if not f'.{extension}' in path:
            path += f'.{extension}'
            return path
    elif isinstance(extension, list):
        if not any(path.endswith('.' + ext) for ext in extension):
            path += '.' + extension[0]
    return path


add_ext = \
    add_extension


# class table():
#     """
#     add，每次访问全部数据内容要内存开销
#     save，read要磁盘开销
#     决定先不用
#     """
#
#     def sheet(self):
#         """
#         这傻逼 sheet 老是变成None
#         @return:
#         """
#         if self.workbook.worksheets == []:
#             self.workbook.create_sheet('Sheet1')
#         if self.workbook.active == None:
#             return self.workbook.worksheets[0]
#         return self.workbook.active
#
#     def __iter__(self):
#         return self.sheet().iter_rows()
#
#     def __len__(self):
#         return self.sheet()._max_row
#
#     def rows(self):
#         return self.sheet().rows
#
#     def columns(self):
#         return self.sheet().columns
#
#     def __init__(self, path, title=False):
#         """
#         不支持 csv
#         @param path:
#         @param title:默认无表头。None, False 代表无表头。
#         """
#         return
#         import openpyxl
#         self.path = add_extension(standarlizedPath(path), ['xlsx'])
#
#         # 处理title
#         if type(title) in [str]:
#             title = [title]
#         if title in [False, None]:
#             self.title = False
#         elif title == []:
#             self.title = ['']
#         else:
#             self.title = title
#
#         self.workbook = openpyxl.Workbook(self.path)
#         if not isfile(self.path):
#             if self.title:
#                 self.add(self.title)
#
#     def add(self, l):
#         """
#         并行
#         @return:
#         """
#         if type(l) in [dict]:
#             if not self.title:
#                 Exit('无表头，无法添加字典')
#             newl = [l.get(k, None) for k in self.title]
#             self.add(newl)
#         elif type(l) in [list]:
#             self.sheet().append(l)
#             self.save()
#
#     def save(self):
#         self.workbook.save(self.path)


class pcsv():
    """
    pandas 操作 csv，excel
    """

    def __init__(self, path, title=True, duplicate=False, ftype='csv', encoding='utf-8',
                 backup=True, silent=True, frequency=24,
                 dtype=None):
        """

        @param path:
        @param title: True，None，为缺省，False 表示无表头，列表表示表头内容
        @param duplicate: True 表示允许重复
        @param frequency: 备份的小时间隔
        """
        self.silent = silent
        self.dtype = dtype
        self.frequency = frequency
        self.path = add_ext(standarlizedPath(path), [ftype])
        self.duplicate = duplicate
        self.encoding = encoding
        self._has_backup = backup
        self.backup()
        self.recognize_ftype()
        self._make_title(title)
        if not isfile(self.path):
            self._create_new()

        self.get_data()
        if not self.duplicate:
            self.set(save=True)

    def query(self, filters: dict) -> list:
        """
        根据传入的字典进行查询
        列名：键值包含
        @param filters: 字典，其中键名对应column_name，值对应value
        @return: 返回满足所有条件的数据
        """
        mask = True
        if not type(filters) in [dict]:
            Exit('参数类型错误')
        for column_name, value in filters.items():
            mask = mask & (self.data[column_name].isin(
                [Str(value), value, Int(value)]))
            # delog(f'{(self.data[column_name],Str(value),value,Int(value))}')
            # delog(f'{mask}')

        return self.data[mask].to_dict(orient='records')

    def recognize_ftype(self):
        # 处理ftype
        if '.csv' in self.path[-4:]:
            self.ftype = 'csv'
        elif '.json' in self.path[-5:]:
            self.ftype = 'json'

    def add_piece(self, piece_uid, author='', title=''):
        """
        成熟的可执行方法，添加作品信息
        @param author:
        @param title:
        @return:
        """
        self.add({
            'num': piece_uid, 'author': author,
            'title': title, 'disk': diskname
        })

    def merge(self, f):
        """
        合并
        @return:
        """
        import pandas
        if type(f) in [str]:
            f = pcsv(f)
            return self.merge(f)

        if type(f) in [pcsv, Csv]:
            self.data = pandas.concat([self.data, f.data])
            self.save()
            return self

    def backup(self, force=False):
        """
        备份文件
        @param force: 强制备份
        @return:
        """
        if '_backup' in self.path:
            return
        if not self._has_backup:
            return
        if not isfile(self.path):
            return
        root = parentpath(self.path)
        fname = filename(self.path)
        backupname = extensionandname(
            self.path)[0] + '_backup' + extensionandname(self.path)[1]
        backuppath = root + '/' + backupname
        if not isfile(backuppath):
            copyfile(self.path, backuppath)
            return
        if force or modifytime(self.path) > modifytime(backuppath) + 3600 * self.frequency:
            copyfile(self.path, backuppath)

    def clear(self):
        """
        清空所有数据，但保留表头（如果有）
        @return:
        """
        import pandas
        self.data = pandas.DataFrame(columns=self.data.columns)
        self.save()

    def delete(self, d=None, lis=None, save=True):
        """
        如果是 lis 就一整次更改后再文件读写
        @param d:
        @param save: 是否并行
        @return:
        """
        import pandas
        if d == None and lis == None:
            return

        if lis:
            for i in lis:
                self.delete(d=i, save=False)
            self.save()
            return

        if save:
            self.get_data()
        if type(d) in [dict]:
            # 将传入的字典转换为DataFrame
            df_to_delete = pandas.DataFrame([d])
            # 通过判断内容完全相同的行索引来删除行
            common_columns = [col for col in d.keys() if col in self.data.columns]
            matching_rows = self.data[common_columns].eq(d, axis='columns').all(axis=1)
            self.data = self.data.drop(self.data[matching_rows].index)
            warn(f'删除了 {d} 在 {self.path}', traceback=False)

            # 重置索引
            self.data.reset_index(drop=True, inplace=True)
            if save:
                self.save()

    def save(self, data=None, ftype=None, duplicate=None):
        """
        新建文件；保存文件
        @param data:
        @param ftype:
        @param duplicate:  True表示允许重复
        @return:
        """

        import pandas
        path = self.path

        # 新建文件
        if not isfile(path):
            if not hasattr(self, 'data'):
                self.data = pandas.DataFrame(columns=self.title)
            get_lock(self.path)
            self.data.to_csv(path, index=False, encoding=self.encoding)
            release_lock(self.path)
            return
        if duplicate == None:
            duplicate = self.duplicate
        if not duplicate:
            self.set(save=False)

        if ftype == None:
            ftype = self.ftype
        elif not ftype == self.ftype:
            name, extension = extensionandname(self.path, parentpath=True)
            path = standarlizedPath(name + '.' + ftype)
        if not hasattr(self, 'data'):
            self.data = pandas.DataFrame(columns=self.title)
        if data is not None:
            get_lock(self.path)
            data.to_csv(path, index=False, encoding=self.encoding)
            release_lock(self.path)
        elif ftype == 'csv':
            get_lock(self.path)
            self.data.to_csv(path, index=False,
                             encoding=self.encoding, errors='ignore')
            release_lock(self.path)
        elif ftype == 'json':
            self.data.to_json(path, encoding=self.encoding)
        elif ftype == 'excel':
            self.data.to_excel(path, encoding=self.encoding)

    def get(self, set=True):
        """

        @set: 是否导出不唯一
        @return:
        """
        self.get_data()
        if self.data.empty:
            warn('没有数据，get 返回')
            return
        first_row = self.data.iloc[0]  # 获取第一行数据
        self.data = self.data.iloc[1:]  # 删除第一行数据
        self.data = self.data.append(first_row, ignore_index=True)
        self.data.reset_index(drop=True, inplace=True)
        self.save()
        return first_row.to_dict()  # 返回第一行数据

    @consume
    def set(self, save=True):
        """
        不读，去重（忽略 time ），去空，
        似乎开销极低
        @return:
        """
        if hasattr(self, 'data'):
            cols = [col for col in self.data.columns if col != 'time']
            self.data = self.data.drop_duplicates(subset=cols)
        if save:
            self.save()

    def columns(self):
        """
        返回所有列名
        @return:
        """
        return self.title

    def get_columns(self, *a, **b):
        self.get_data()
        return self.columns(*a, **b)

    def _create_new(self):
        """
        创建新文件
        @return:
        """
        import pandas
        path = self.path
        createpath(path)
        if not isfile(path):
            if not hasattr(self, 'data'):
                self.data = pandas.DataFrame(
                    columns=self.title if not self.title in [False, None, [], True] else None)
            self.data.to_csv(path, index=False, encoding=self.encoding)

    def _find_title_from_file(self):
        """
        如果没有文件，就警告并返回
        @return:
        """

    def _make_title(self, title):
        """
        初始化 title
        @return:
        """
        if type(title) in [str]:
            self.title = [title]
        elif title in [False]:
            self.title = title
            return
        elif title in [True, None, []]:
            if hasattr(self, 'data'):
                self.title = self.data.columns.tolist()
            else:
                if isfile(self.path):
                    self.title = False
                    self.get_data()
                    self.title = self.data.values.tolist()[0]
                    self.data = self.data.iloc[1:]
                else:
                    self.title = []
        else:
            self.title = title
        if not 'time' in self.title:
            self.title.append('time')
            if not self.dtype == None:
                self.dtype.update({'time': str})

    @consume
    def get_data(self):
        """
        更新 self.data，并且作为返回值返回
        需要title已经建立。根据 title 读取数据
        @return: pandas.DataFrame
        """
        import pandas
        path = self.path
        usecols = None
        header = None

        if self.title in [False]:
            header = None
        else:
            header = 0  # 第0行是列名

        fail = True
        while fail:
            try:
                get_lock(self.path)
                ret = pandas.read_csv(self.path, na_values=['', 'null', 'Null'],
                                      encoding=self.encoding,
                                      header=header,
                                      dtype=self.dtype,
                                      # errors='replace'
                                      )
                release_lock(self.path)
                if type(self.title) in [list]:
                    for col in self.title:
                        if col not in ret.columns:
                            import numpy
                            ret[col] = numpy.nan
                fail = False
            except Exception as e:
                warn(e)
                sleep(1)
                self.getback()
                pass
        ret.fillna('', inplace=True)
        self.data = ret
        return ret

    def getback(self):
        """
        从备份恢复添加
        @return:
        """
        root = parentpath(self.path)
        fname = filename(self.path)
        backupname = extensionandname(self.path, exist=False)[0] + '_backup' + \
                     extensionandname(self.path, exist=False)[1]
        backuppath = root + '/' + backupname
        if isfile(backuppath):
            self.merge(backuppath)
        return self.get_data()

    getbackup = getback
    get_backup = getback

    def length(self):
        if not hasattr(self, 'data'):
            warn('表格没有数据')
            return 0
        if self.data.empty:
            return 0
        return self.data.shape[0]

    @consume
    def add(self, l, duplicate=None, save=True, isnew=True):
        """
        并行
        需要确保传入的值为纯数字，否则无法去重
        @param l:
        @param duplicate: True 表示允许重复
        @param save: 是否并行读取、保存
        @param isnew: 是否确定是原来不存在的记录（仅供开发者
        @return:
        """
        import pandas
        original_len = self.length()

        if save:
            self.get_data()
        len1 = self.data.shape[0]
        if duplicate == None:
            duplicate = self.duplicate
        if type(l) in [dict]:
            if not self.title:
                Exit('无表头，无法添加字典')
            if not 'time' in l:
                l.update({'time': nowstr(mic=False)})
            self.data = pandas.concat(
                [self.data, pandas.Series(
                    l, index=self.data.columns).to_frame().T],
                ignore_index=True)
        elif type(l) in [list, tuple]:
            self.data = pandas.concat(
                [self.data, pandas.Series(
                    l, index=self.data.columns).to_frame().T],
                ignore_index=True)
        if not duplicate:
            self.set()
        len2 = self.data.shape[0]
        if isnew and len1 == len2:
            warn(f'似乎已有数据{len1} -> {len2}，未新增', traceback=False)
        if not self.silent:
            delog(f'添加后数据量{self.length()}')

        len = self.length()
        if original_len > len + 2:
            print((original_len, len))
            self.getbackup()
            Exit(f'似乎被压缩了。{original_len}->{self.length()}')

    append = add

    def get_column(self, *a, **b):
        self.get_data()
        return self.column(*a, **b)

    @listed()
    def column(self, s=None, set=True, resort=True):
        """
        获取某一列的值
        @set: 是否导出不唯一
        @param s:
        @param set:
        @param sort: 是否原序
        @return:
        """
        if s == None:
            return []

        try:
            ret = self.data[s].tolist()
        except KeyError:
            warn(f'{self.path} 列 {s} 不存在')
            return []
        if set:
            ret = Set(ret, hashable=True, resort=resort)
        return ret

    def rows(self, typ=list):
        """
        返回所有行
        @return:
        """
        if typ == list:
            return self.get_data().values.tolist()
        if typ == dict:
            return self.get_data().to_dict(orient='records')


Csv = pcsv


# class excel(table):
#     pass

@listed()
@manage_args(l=['path'])
def deletedirandfile(l=None, silent=True, rt=True,
                     b=None, **leak):
    """
    删除文件和文件夹
    @param l: 可以是txt路径
    @param silent:
    @param rt: 是否用txt 传入参数
    @return:
    """
    import shutil
    # 删除txt里的文件
    if isfile(l) and l[-4:] in '.txt' and rt:
        f = txt(l)
        dlis = []
        for i in f.l:
            if i in ['\n', '']:
                continue
            dlis.append(i)
        deletedirandfile(dlis)
        return

    # 递归删除dir_path目标文件夹下所有文件，以及各级子文件夹下文件，保留各级空文件夹
    # (支持文件，文件夹不存在不报错)
    def del_files(dir_path):
        if os.path.isfile(dir_path):
            try:
                os.remove(dir_path)  # 这个可以删除单个文件，不能删除文件夹
            except BaseException as e:
                if silent == None:
                    print(e)
        elif os.path.isdir(dir_path):
            file_lis = os.listdir(dir_path)
            for file_name in file_lis:
                tf = os.path.join(dir_path, file_name)
                del_files(tf)
        if silent == None:
            log(dir_path + '  removed.')

    if not type(l) == list:
        l = [l]
    for file in l:
        del_files(file)
    for i in l:
        if os.path.exists(i):
            while True:
                # 循环解决正在访问错误
                try:
                    if isdir(path=i, exist=True):
                        shutil.rmtree(standarlizedPath(i, strict=True))
                    break
                except:
                    warn(f'删除 {i} 错误，正在重试 ...')
                    continue


delete = \
    deletedirandfile


def abstract_path(*a, **b):
    return standarlizedPath(*a, strict=True, **(exclude(b, 'strict')))


strict_path = strictpath = \
    abstract_path


def CreatePath(path):
    """
    只创建空文件夹
    :param path: ’\‘自动转换为‘/’
    :return:成功或者已存在返回路径字符串，否则返回False
    """
    path = pathname(path)
    if os.path.exists(path):
        return path
    try:
        # windows创建文件夹自动删去末尾空格，此时再在原来的带空格路径下操作就会报错
        os.makedirs(path)
        return path
    except Exception as e:
        warn(f'Create {path} Failed.')
        sys.exit(-1)


create_path = CreatePath
createpath = CreatePath


# 文件已存在返回False，成功返回文件对象
def createfile(path=None, encoding=None, silent=None):
    path = standarlizedPath(path)
    root = pathname(path)
    createpath(path)
    name = standarlizedFileName(path[path.rfind('/') + 1:])
    if not path == root + name:
        tip(f'文件名{path}不规范，已重命名为{root + name}')
    path = root + name
    if os.path.exists(path):
        if not silent:
            warn(f'{path} alreay exists. 文件已存在')
        return False
    # try:
    if not encoding == None:
        f = open(path, 'w')
    else:
        f = open(path, 'wb', encoding=encoding)
    # except Exception:
    #     warn(f'创建文件{path}未知失败。{str(Exception)}')
    #     return False
    return f


def file_operate(mode=None, path=None, IOList=None, encoding=None,
                 with_lock=True
                 ):
    """
    所有文件with open的封装的操作过程函数
    @param mode:
    @param path:
    @param IOList:
    @param encoding:
    @return:列表或是open对象
    """
    try:
        path = standarlizedPath(path)
        createpath(path)
        if (IOList == None or IOList == []) and (mode.find('w') > -1 or mode.find('a') > -1):
            warn(f'可能是运行时错误。写未传参。IOList: {info(IOList)} mode: {mode}')
            sys.exit(-1)
        if not os.path.exists(path) and mode.find('r') > -1:
            warn(f'错误。读不存在文件：{path}')
            return False

        get_lock(name=path)
        # 比特流
        if mode == 'rb':
            with open(path, mode='rb') as file:
                release_lock(name=path)
                return IOList + file.readlines()
        # 字符流
        elif mode == 'r':
            with open(path, mode='r', encoding=encoding) as file:
                release_lock(name=path)
                return IOList + file.readlines()
        elif mode == 'w':
            with open(path, mode='w', encoding=encoding) as file:
                release_lock(name=path)
                file.writelines(IOList)
                return file
        elif mode == 'wb':
            try:
                with open(path, mode='wb') as file:
                    if not IOList == None:
                        file.write(IOList)
                    release_lock(name=path)
                    return file
            except Exception as e:
                with open(path, mode='wb') as file:
                    file.writelines(IOList)
                    release_lock(name=path)
                    return file
        elif mode == 'a':
            with open(path, mode='a', encoding=encoding) as file:
                file.writelines(IOList)
                release_lock(name=path)
                return file
    except Exception as e:
        warn('文件读错误', info(IOList))
        release_lock(name=path)
        Exit(e)


def DesktopPath(s=''):
    if 'esktop' in s:
        return
    if './' in s:
        s = s[2:]
    if not s == '':
        s = '/' + s
    if s == 'new':
        s = random.randint(0, 99999)
        s = str(s)
        log(f'桌面新建：{s}')
        return standarlizedPath(f"C:/Users/{user}/Desktop/{s}.txt")

    return standarlizedPath(f"C:/Users/{user}/Desktop{s}")


def desktoppath(s=''):
    return DesktopPath(s)


def desktop(s=''):
    return DesktopPath(s)


class txt():
    """
    读写txt文件。l，可以不是字符串，自动追加空格。
    """

    def __iter__(self):
        return self.l.__iter__()

    def shot(self):
        return list(self.l)

    @DebugConsume
    def __init__(self, path=None, encoding='utf-8', silent=None,
                 ext=None):
        self.silent = silent
        if has_ext(path):
            self.ext = extension(path)
        elif ext:
            self.ext = ext
        else:
            self.ext = 'txt'
        self.mode = 'txt'
        if encoding == None:
            encoding = 'utf-8'
        self.encoding = encoding
        if path == 'new':
            path = desktoppath('new')
        self.path = standarlizedPath(path)
        if not self.path.find('.') > 0:
            self.path += '.' + self.ext
        self.read()

    def content(self):
        return ''.join([i + '\n' for i in self.l])

    def read(self):
        self.l = []
        if not os.path.exists(self.path):
            createfile(self.path, encoding=self.encoding)
            return
        for i in file_operate('r', self.path, IOList=[], encoding=self.encoding):
            self.l.append(str(i).strip('\n'))

    def look(self):
        look(self.path)

    @listed()
    def delete(self, s):
        """
        删除字符串相等的行。自动保存。
        @param s:
        @return:
        """
        for i in self.l:
            if i == s:
                self.l.remove(s)
                self.save()
                return

    @listed()
    def add(self, i, silent=None):
        if silent == None:
            silent = self.silent
        i = str(i)
        for k in i.split('\n'):
            k = str(k)
            # 如果原来是空的，就不另起一行
            if not self.l == []:
                file_operate('a', self.path, ['\n' + k], encoding='utf-8')
            else:
                file_operate('a', self.path, [k], encoding='utf-8')
            self.l.append(str(k))
            if not silent:
                delog(f'txt add {k}')

    def addline(selfself, i):
        txt.add('\n')
        txt.add(i)

    @consume
    def save(self, s='txt saved', silent=False):
        # 强制覆盖写
        if silent == None:
            silent = self.silent
        slist = []
        if self.l == []:
            slist = ['']
        else:
            for i in self.l[:-1]:
                slist.append(str(i) + '\n')
            slist.append(str(self.l[-1]))
        # delog(f'文件写 {self.path}')
        file_operate('w', self.path, slist, encoding=self.encoding)
        if not silent and not self.silent:
            delog(f'{rmtail(tail(self.path), ".txt", strict=False)}({(self.mode)}) - {s}',
                  traceback=False)

    def length(self):
        return len(self.l)

    def clear(self):
        self.l = []
        txt.save(self, '清除')


class markdown(txt):
    def __init__(self, *a, **b):
        self.ext = 'md'
        txt.__init__(self, *a, **b, silent=True)
        self.mark()

    def mark(self):
        marks = []
        is_code = False
        for i in self.l:
            if is_code or i != '':
                if i == '```':
                    is_code = not is_code
                marks.append(True)
            else:
                marks.append(None)

        while None in marks:
            for index, i in enumerate(self.l[1:-1]):
                if marks[index] is None:
                    if marks[index - 1] is True or marks[index + 1] is True:
                        marks[index] = False
                    elif marks[index - 1] is False and marks[index + 1] is False:
                        marks[index] = True

    @staticmethod
    def has_bold(s):
        return '**' in s

    @staticmethod
    def has_list(s):
        return '- ' in s

    @staticmethod
    def plaintext(s):
        s = s.replace('**', '')
        s = s.replace('- [ ] ', '')
        s = s.replace('- [x] ', '')
        s = s.replace('- ', '')
        s = s.replace('~~', '')
        s = s.replace('# ', '')
        s = s.replace('#', '')
        return s


class RefreshTXT(txt):
    # 实现逐行的记录仓库
    # 实现备份
    # 增删都会执行保存操作。
    # 维护内容的唯一性

    @DebugConsume
    def __init__(self, path, encoding=None, silent=None):
        """

        @param path:
        @param encoding:
        @param silent:
        """
        txt.__init__(self, path, encoding, silent)
        self.loopcount = 0
        self.mode = 'Rtxt'
        RefreshTXT.backup(self)
        RefreshTXT.set(self, silent=silent)

    @DebugConsume
    def set(self, silent=None, sort=True):
        """
        维护唯一性
        去重，去空，稳定
        @param silent:
        @param sort: 稳定
        @return:
        """
        while '' in self.l:
            self.l.pop(self.l.index(''))
        if len(self.l) > 20000:
            return
        self.l = Set(self.l)
        if not silent is None:
            txt.save(self, 'Rtxt set', silent=silent)
        else:
            txt.save(self, 'Rtxt set', silent=self.silent)

    def backup(self, strict=False):
        # region
        backupname = self.path.strip('.txt') + '_backup.txt'
        if not os.path.exists(backupname):
            f = txt(backupname, self.encoding)
            f.l = [nowstr()] + self.l
            f.save('create backup')
        else:
            if counttime(txt(backupname).l[0]) <= 3600 * 24 and strict == False:
                return
            RefreshTXT.set(self)
            f = txt(backupname)
            f.l = [nowstr()] + self.l
            f.save('refresh backup')
        # endregion

    @DebugConsume
    def save(self, silent=None):
        """
        并行保存
        @param silent:
        @return:
        """
        if silent == None:
            silent = self.silent
        l1 = self.l
        l2 = rtxt(self.path, silent=silent).l
        self.l = list(set(l1 + l2))
        self.l.sort(key=lambda x: l1.index(x) if x in l1 else len(l1))
        txt.save(self, 'Rtxt 合并保存', silent=silent)

    def get(self, silent=None):
        """
        第一行放最后一行
        @param silent:
        @return: 移动的这一行
        """
        if len(self.l) < 1:
            return None
        self.l = Set(
            rtxt(self.path, encoding=self.encoding, silent=self.silent).l + self.l)
        # self.l= rtxt(path=self.path, encoding=self.encoding, silent=self.silent).l
        if silent == None:
            silent = self.silent
        self.l = self.l[1:] + [self.l[0]]
        self.loopcount -= 1
        txt.save(self, silent=silent)
        return self.l[-1]

    def rollback(self, silent=None):
        if silent == None:
            silent = self.silent
        self.__init__(self.path, self.encoding, silent=self.silent)
        if len(self.l) <= 1:
            return None
        self.l = [self.l[-1]] + self.l[:-1]
        self.loopcount += 1
        self.save(silent=silent)
        return self.l[0]

    @listed()
    def delete(self, i, silent=None):
        if silent == None:
            silent = self.silent
        b = False
        j = dicttojson(i)
        while j in self.l:
            self.l.pop(self.l.index(j))
            b = True
        if not b:
            warn(f'尝试删除但是记录{self.path}中没有以下列表中的任何一个元素 {i}.')
        txt.save(self, f'删除{j}', silent=silent)

    @listed()
    def add(self, i, silent=None):
        if silent == None:
            silent = self.silent
        i = str(i)
        i.strip('\n')
        if not i in self.l:
            self.l.append(i)
            file_operate('a', self.path, ['\n' + i], encoding='utf-8')


class jsondata(file):
    def __init__(self, path, autosave=True):
        """

        @param path:
        @param autosave:
        """
        self.path = standarlizedPath(jsonpath(path))
        self.encoding = 'utf-8'
        self.autosave = autosave
        if not '.json' in self.path:
            self.path += '.json'
        if not isfile(self.path, exist=True):
            json.dump({}, open(mode='w', file=self.path, encoding=self.encoding))

        self.data = json.load(
            open(mode='r', file=self.path, encoding=self.encoding))

    def content(self):
        return self.data

    def remove(self, s):
        if isinstance(s, dict):
            for k in s.keys():
                if k in self.data:
                    del self.data[k]
        elif isinstance(s, str):
            if s in self.data:
                del self.data[s]
        if self.autosave:
            self.save()

    def clear(self):
        self.data = {}
        if self.autosave:
            self.save()

    delete = remove

    def save(self):
        json.dump(self.data, open(
            mode='w', file=self.path, encoding=self.encoding))

    def get(self, s):
        return self.data.get(s)

    def add(self, d: dict):
        """

        @param d:
        @return:
        """
        if type(self.data) in [list]:
            self.data = self.data + [d]
            self.save()
            return
        for key, value in d.items():
            if key in self.data:
                if type(self.data[key]) == list:
                    self.data[key].append(value)
                else:
                    self.data[key] = [self.data[key], value]
            else:
                self.data[key] = value
        if self.autosave:
            self.save()

    def setdata(self, data):
        self.data = data
        self.save()


class Json(txt):
    """
    txt转json，一行一个jsonstr
    """

    def __init__(self, path, encoding=None, silent=None):
        txt.__init__(self, path, encoding)
        self.addtodict()

    # 创建类的字典数据属性
    def addtodict(self):
        self.d = {}
        for i in self.l:
            if i == '':
                continue
            try:
                self.d.update(jsontodict(i))
            except Exception as e:
                warn(self.path)
                warn(f'-{i}-')
                print(type(i))
                print(info(i))
                sys.exit(-1)

    def get(self):
        ret = self.l[0]
        if ret == '':
            self.l.pop(0)
            self.save()
            return Json.get(self)
        return jsontodict(ret)

    def add(self, d):
        txt.add(self, dicttojson(d))
        self.d.update(jsontodict(d))


class RefreshJson(Json, RefreshTXT):
    """
    遵循列表值
    """

    @DebugConsume
    @manage_args()
    def __init__(self, path=None, encoding=None, silent=None, b=None):
        RefreshTXT.__init__(self, **b)
        RefreshJson.depart(self)
        Json.addtodict(self)
        RefreshJson.set(self, silent=silent)
        self.mode = 'Rjson'

        #     非列表的安全检查
        if self.length() > 0 and not list == type(value(jsontodict(self.l[0]))):
            warn(self.l[0])
            Exit(f'{self.path} 似乎不是列表。')

    # depatch
    # segment
    # 有时会产生异常，多行没有换行。分开。

    def findkey(self, value):
        """
        根据值找到键
        @param value:
        @return:  找不到返回False
        """
        for k in self.d:
            v = self.d[k]
            if type(v) == list and value in v or value == v:
                return k
        return False

    def depart(self, silent=None):
        if silent is None:
            silent = self.silent
        addl = []
        dell = []
        for i in self.l:
            if '}{' in i:
                newl = i.split('}{')
                newl[0] = newl[0][1:]
                newl[-1] = newl[-1][:-1]
                addl += newl
                dell.append(i)
        for j in addl:
            RefreshTXT.add(self, '{' + j + '}', silent=silent)
        for i in dell:
            RefreshTXT.delete(self, i, silent=silent)

    # 返回列表，所有的record，一个value对应一个key
    def all(self):
        ret = []
        for i in range(self.length()):
            ret += self.get()
        return ret

    # 返回值的键
    def find(self, v):
        for i in self.all():
            if v == value(i):
                return key(i)

    @DebugConsume
    def get(self, silent=None):
        """
        本地存储值是列表，返回所有键值对（拆开成列表）
        @return: 第一行放最后一行，并返回这一行

        """
        if silent is None:
            silent = self.silent
        dstr = (RefreshTXT.get(self, silent=silent))
        try:
            d = jsontodict(dstr)
        except Exception as e:
            if type(e) in [ValueError] and '}{' in dstr:
                #         先分割
                RefreshJson.depart(self, silent=silent)
                #         在返回全部的列表
                newl = dstr.split('}{')
                newl[0] = newl[0][1:]
                newl[-1] = newl[-1][:-1]
                ret = []
                for j in newl:
                    j = '{' + j + '}'
                    ret += RefreshJson.get(j)
                return ret
            else:
                Exit(f'{e}')
        ret = []
        if value(d) == []:
            return [{key(d): None}]
        for i in value(d):
            ret.append({key(d): i})
        return ret

    def add(self, d, silent=None):
        if silent == None:
            silent = self.silent
        d = jsontodict(d)

        if list == type(value(d)):
            for i in value(d):
                rjson.add(self, {key(d): i}, silent=silent)
            return

        for i in self.l:
            din = jsontodict(i)
            if key(din) == key(d):
                if value(d) in value(din):
                    return
                RefreshTXT.delete(self, dicttojson(din), silent=silent)
                try:
                    din = {key(d): list(Set([value(d)] + value(din)))}
                except Exception as e:
                    print(din)
                    print(d)
                    Exit(e)
                RefreshTXT.add(self, dicttojson(din), silent=silent)
                self.d.update(din)
                return

        d = {key(d): [value(d)]}
        RefreshTXT.add(self, dicttojson(d), silent=silent)
        self.d.update(d)

    @consume
    # 合并相同的键
    def set(self, silent=None):
        if silent == None:
            silent = self.silent
        allkey = []
        for dstr in self.l:
            d = jsontodict(dstr)
            k = key(d)

            if not k in allkey:
                allkey.append(k)
                continue

            dlis = []
            values = []
            for i in self.l:
                ii = jsontodict(i)
                if not key(ii) == k:
                    continue
                dlis.append(i)
                values += value(ii)
                try:
                    values = list(Set(values))
                except Exception as e:
                    print(values)
                    Exit()
            RefreshTXT.delete(self, dlis, silent=silent)
            RefreshJson.add(self, {k: values}, silent=silent)

    def rollback(self):
        d = jsontodict(RefreshTXT.rollback(self))
        ret = []
        for i in value(d):
            ret.append({key(d): i})
        return ret

    @listed()
    @consume
    def delete(self, i, silent=None):
        if silent == None:
            silent = self.silent
        i = jsontodict(i)
        if list == type(value(i)):
            for j in value(i):
                RefreshJson.delete(self, {key(i): j}, silent=silent)
            return

        for j in self.l:
            din = jsontodict(j)
            if not key(din) == key(i):
                continue
            newvalue = value(din)
            if value(i) in newvalue:
                newvalue.remove(value(i))
            newd = {key(din): newvalue}

            RefreshTXT.delete(self, j, silent=silent)
            if not newvalue == []:
                RefreshTXT.add(self, dicttojson(newd), silent=silent)
            else:
                RefreshJson.delete(self, dicttojson(
                    {key(din): []}), silent=silent)
            self.d.update(newd)
            break

    def pieceinfo(self, num, author, title, extra=None):
        diskname = getDiskName()
        if extra in ['', None]:
            return json.dumps({str(num): {'disk': diskname, 'author': author, 'title': title}},
                              ensure_ascii=False)
        else:
            # 有额外信息
            if type(extra) in [dict]:
                din = {'disk': diskname, 'author': author, 'title': title}
                for i in extra:
                    din.update({i: extra[i]})
                ret = {str(num): din}
                return json.dumps(ret, ensure_ascii=False)
            elif type(extra) in [str]:
                return json.dumps({str(num): {'disk': diskname, 'author': author, 'title': title}},
                                  ensure_ascii=False)

    def addpiece(self, num, author, title, extra=None):
        """

        @param num: 作品唯一标识符
        @param author: 作者
        @param title: 标题
        @param extra: 附加信息字符串
        @return:
        """
        piece = jsontodict(self.pieceinfo(num, author, title, extra))
        self.add(piece)

    def adduser(self, uid, author):
        self.add({uid: author})


class cache(txt):
    """
    dict。遵循列表值。
    """

    def __init__(self, path, silent=None, json=True):
        super().__init__(path=path, silent=silent)
        self.silent = silent
        self.path = path
        self.json = json
        self.encoding = 'utf-8'
        self.read()

    def get(self, silent=False, interval=2):
        """
        删除。如果失误直接删除
        @param silent:
        @return:首条。
        """
        if self.silent:
            silent = True
        while True:
            try:
                f = txt(self.path)
                if f.l == []:
                    sleep(interval)
                    return
                if self.json:
                    s = jsontodict(f.l[0])
                    if not s:
                        f.delete(f.l[0])
                        return self.get()
                else:
                    s = f.l[0]
                f.l.pop(0)
                f.save('cache get', silent=silent)
                if s == None:
                    s = self.get()
                return s
            except Exception as e:
                warn(e)
                warn('cache获取失败。正在重试')
                sleep(2)

    def add(self, s, silent=False):
        if self.silent:
            silent = True
        if self.json:
            s = dicttojson(s)
        f = txt(self.path)
        f.add(s, silent=silent)
        f.save(f'cache added{s}', silent=silent)

    def length(self):
        return txt(self.path).length()


def rtxttorjson(path):
    f = txt(path)
    l = f.l
    f.l = []
    f.save()
    for i in l:
        f.l.append(dicttojson({i: []}))
    f.save()


class rtxt(RefreshTXT):
    pass


class rjson(RefreshJson):
    pass


# endregion

#  日志
# region
def show_args(*a, **b):
    # 将位置参数转换为字符串列表，并用', '连接
    args_str = ', '.join(map(str, a))

    # 将关键字参数转换为字符串列表，每个键-值对用'='连接，并用', '连接所有键-值对
    kwargs_str = ', '.join(f"{k}={v}" for k, v in b.items())

    # 合并两个字符串
    print(f"({args_str})  ({kwargs_str})")


def context(step=12, show=False):
    """
    返回程序上下文
    @param step:
    @param show:是否通过txt显示
    @return: d的列表，最深的在最前面
    """
    if step < 0:
        return None
    frame = inspect.currentframe()
    ret = []
    # 调试模式pydev和运行是不一样的
    for i in range(step):
        try:
            frame = frame.f_back
            if not frame == None:
                framed = inspect.getframeinfo(frame)
                d = {}
                d.update({'module': framed.function})
                d.update({'function': framed.function})
                d.update({'func': framed.function})
                d.update({'code': framed.code_context})
                d.update({'code_context': framed.code_context})
                d.update({'file_operate': framed.filename})
                d.update({'filename': framed.filename})
                d.update({'line': framed.lineno})
                d.update({'lineno': framed.lineno})
                if d['code'] == None or d['function'] in ['_call_with_frames_removed',
                                                          'run_code', 'run_ast_nodes',
                                                          'run_cell_async',
                                                          '_run_cell', 'do_add_exec', 'run_cell',
                                                          'runsource',
                                                          'runmodule', 'run', '_run_module_as_main',
                                                          'run_path', '_run_code',
                                                          '_run_module_as_main',
                                                          'add_exec_module', '_run_code_module',
                                                          'add_exec', 'ipython_exec_code', 'Exit'
                                                                                           '_pseudo_sync_runner',
                                                          '_exec', 'execfile', 'main', '<module>'

                                                          ] \
                        or False:
                    continue
                ret.append(d)
        except Exception as e:
            break
    if show:
        f = txt(cachepath('context.txt'))
        f.add(ret)
        f.save()
        look(f.path)
    return ret


stepback = context
traceback = context
backtrace = context


def WARN(s):
    now = Time()
    hotkey('win', 'd')
    win32api.MessageBox(None, s, f'Kaleidoscope{now.time()}', win32con.MB_OK)


@manage_args(content=['message'], total_time=['t', 'duration'])
def desktop_inform(title='未命名', content='无内容', total_time=3,
                   b=None, **leak):
    from win10toast import ToastNotifier
    notifier = ToastNotifier()
    notifier.show_toast(title, content,
                        duration=total_time,
                        # icon_path=picpath('icon.ico'),
                        )


inform = notify = message = \
    desktop_inform


def alert(s=''):
    # t=Time()
    p = pool(1)

    def do():
        win32api.MessageBox(0, s, Time.time(Time()), win32con.MB_OK)

    p.execute(do, )


def console(s, duration=999, text_color='#F08080', font=('Hack', 14), size=28):
    #  每当新的控制台启动后，改内容，然后开新进程，将0改为1，1改为0
    # 控制台每隔一段时间刷新，如果变为0则退出。
    # 新的控制台计时结束后，将1改为0
    import PySimpleGUI
    refreshtime = 0.6
    consoletxt.add({nowstr(): s})
    while 3600 < Now().counttime(Time(key(jsontodict(consoletxt.get())))):
        consoletxt.l.pop(0)
    consoletxt.save()

    # 短暂显示桌面控制台
    def show():
        # 系统默认颜色
        # COLOR_SYSTEM_DEFAULT='1234567890'=='ADD123'
        global win
        outs = ''
        inc = 0
        for i in consoletxt.l:
            outs += f'[{inc}]  {value(i)}\n'
            inc += 1
        layout = [[PySimpleGUI.Text(outs, background_color='#add123', pad=(0, 0),
                                    text_color=text_color, font=font)]]
        win = PySimpleGUI.Window('', layout, no_titlebar=True, keep_on_top=True,
                                 location=(120 * 16 / 3 * 2, 0), auto_close=True,
                                 auto_close_duration=duration,
                                 transparent_color='#add123', margins=(0, 0))
        event, values = win.read(timeout=0)
        sleep(0.3)
        return win

    def func(duration, ):
        delog('1')
        return
        # 更改consolerunning
        # if consolerunning.l[0] == '1':
        #     consolerunning.l[0] == '0'
        #     consolerunning.save()
        # elif consolerunning.l[0] == '0':
        #     consolerunning.l[0] == '1'
        #     consolerunning.save()
        while duration > 0:
            sleep(refreshtime)
            duration -= refreshtime
            show()

    process = multiprocessing.Process(target=func, args=(duration,))
    # process.daemon=True
    process.start()


def Log(s, front=242, font=1, background=238, withtime=True,
        traceback=False, deleted=False, plain_text=None
        ):
    """
    打印单行输出（不处理换行）
    @param s:
    @param front:
    @param font:
    @param background:
    @return:
    """
    if used_arg(plain_text):
        print(plain_text)
    global Logcount
    # 最大的每行字符长度
    if is_in_jupyter():
        m = 75
    else:
        m = 3000
    if deleted:
        font = 9
    try:
        s = str(s)
        if traceback:
            import traceback
            s += traceback.format_exc()
            # for item in stepback()[1:]:
            # s += f"{item['function']}(): {item['code'][0]}"
        if '\n' in s:
            Log(s.split('\n')[0], front, font, background)
            for i in s.split('\n')[1:]:
                Log(i, front, font, background, withtime=False)
            return
        s = s.replace(u'\xa0', u'<?>')
        # 未知字符串
        s1 = ''
        if len(s) > m:
            s1 = s[m:]
            s = s[:m]
        s = s.ljust(m, '\t')
        if Logcount >= 100:
            sss = f'[{Logcount}]' + ANSIFormatter.reset()
        else:
            sss = ANSIFormatter.reset()

        print(sss,
              ANSIFormatter.background(background), ANSIFormatter.front(244),
              realtime() if withtime else '               ',
              ANSIFormatter.front(front), ANSIFormatter.font(
                font), s, ANSIFormatter.reset_all(),
              ANSIFormatter.background(background),
              ANSIFormatter.reset())
        if withtime:
            Logcount += 1
        if not s1 == '':
            Logcount -= 1
            Log(s1[m:], front, font, background)
    except Exception as e:
        warn(f'这条日志输出失败了。原因{e}')


@listed()
def log(*a, **b):
    s = ''
    for i in a:
        s += str(i)
    Log(s, 148, **b)


@listed()
def tip(*a, **b):
    s = ''
    for i in a:
        s += str(i)
    Log(s, 248, 9, **b)


@listed()
def delog(*a, **b):
    if a in [(), [], None]:
        Log('continuing', 75)
        return
    s = a[0]
    s = str(s)
    if not s in [0, -1, 'beign', 'end', 'a', 'z']:
        s = ''
        for i in a:
            s += str(i) + ' '
    if not get_env_var('debug'):
        return
    if s == 0 and type(s) == int:
        delog('is Processing.')
        return
    if s == -1:
        # 手动打终点断点，所以会退出
        delog('已处理。准备退出。')
        sys.exit(0)
        # return
    dic = {
        'begin': 'Announce Begin',
        'end': "Announce End",
        'a': 'Announce Begin',
        'z': "Announce End"
    }
    try:
        if str(s) in dic.keys():
            s = dic.get(s)
    finally:
        Log(s, 75, **b)


@listed()
def warn(*a, traceback=True, plain_text=None
         , b=None, **leak):
    """

    @param plain_text: 链接字符不能放在颜色文本里
    @return:
    """
    s = ''
    for i in a:
        s += str(i)
        if issubclass(type(i), Exception):
            s += str(type(i))
    Log(s, 166, traceback=traceback, plain_text=plain_text)


# endregion


# 字符串
# region
resub = re.sub


def domain_url(url=None):
    from urllib.parse import urlparse
    parsed_url = urlparse(url)
    return parsed_url.netloc


def split(s, *a, **b):
    return s.split(*a, **b)


def compare_strings(s1, s2):
    """
    比较两个字符串，找出第一个不同的字符
    @param s1:
    @param s2:
    @return:
    """
    common = []
    for c1, c2 in zip(s1, s2):
        if c1 == c2:
            common.append(c1)
        else:
            print(
                f"第一个字符不同的位置在 {len(common)}: ('{c1}'         '{c2}'')")
            break
    else:
        if len(s1) != len(s2):
            longer, shorter = (s1, s2) if len(s1) > len(s2) else (s2, s1)
            print(
                f'更长的字符串包含有更多的字符: "{longer[len(common):]}"')
        else:
            print("No differences found.")

    print(f"Common part: {''.join(common)}")


def TellStringSame(s1, s2, ratio=0.8, **b):
    return string_similarity(s1, s2, **b) >= ratio


def string_similarity(s1, s2, stripSpace=True):
    """
    判断两个字符串是否相似
    @param s1:
    @param s2:
    @param ratio:
    @param stripSpace:
    @return:
    """
    if not type(s1) in [str] or not type(s2) in [str]:
        warn(f'你正在比较两个非字符串的字符相似度 {s1} {s2}',
             traceback=False
             )
    s1 = Str(s1)
    s2 = Str(s2)
    if s1 == s2:
        return True
    if stripSpace:
        s1 = s1.replace(' ', '')
        s2 = s2.replace(' ', '')
        s1 = s1.replace('\n', '')
        s2 = s2.replace('\n', '')
        s1 = s1.replace('\t', '')
        s2 = s2.replace('\t', '')
        s1 = s1.replace('\r', '')
        s2 = s2.replace('\r', '')
        s1 = s1.replace('_', '')
        s2 = s2.replace('_', '')
    if len(s1) > 3 and len(s2) > 3:
        if s1.rfind(s2) >= 0 or s2.rfind(s1) >= 0:
            return True
    if len(s1) < 6 or len(s2) < 6 or len(s1) / len(s2) < 0.7 or len(s2) / len(s1) < 0.7 or False:
        return False

    # 计算从s1变到s2的编辑距离
    return 1 - editdistance.eval(s1, s2) / len(s1)


tellstringsame = TellStringSame


# 去除字符串末尾
def Strip(s, tail, strict=False):
    if not type(s) in [str] and type(tail) in [str]:
        warn(f's tail中有不为字符')
        Exit(s, tail)
    if s[-len(tail):] == tail:
        return s[:-len(tail)]
    else:
        return s


# 正则查找
def refind(s, re):
    return re.findall(s, re)


def cuttail(s, mark='_', strict=False):
    """
    分割字符串和末尾
    @param s:
    @param mark:
    @param strict: 不包括mark
    @return:
    """
    if type(s) == list:
        warn('用法错误。')
        sys.exit(-1)
    if mark == None:
        return s
    s, mark = str(s), str(mark)
    t = tail(s, mark, strict=strict)
    if t == s:
        return s, ''  # 没有找到
    return s[:(s.rfind(mark))], t


def splittail(s, mark, strict=None):
    return cuttail(s, mark, strict)


def removetail(l, mark='.', strict=False):
    return cuttail(l, mark, strict=strict)[0]


rmtail = removetail


def gethead(s, mark='/', strict=True):
    """
    截取字符串开头
    找到最左侧匹配，如果没有返回原字符串
    @param s:
    @param mark:
    @param strict:不包括mark
    @return:
    """
    s, mark = str(s), str(mark)
    if mark not in s:
        if strict:
            Exit(f'head失败。字符串 \"{s}\" 中没有预计存在的子串： \"{mark}\"。', (s, mark))
        else:
            return s
    return s[:s.find(mark)]


head = gethead


def gettail(s, mark='/', strict=True, with_mark=False):
    """
    截取字符串末尾
    找到最右侧匹配，如果没有返回原字符串
    @param s:
    @param mark:
    @param strict:不包括mrak
    @return:
    """
    if not type(mark) in [list]:
        mark = [mark]
    for mark in list(mark):
        s, mark = str(s), str(mark)
        if not mark in s:
            if strict:
                warn(stepback(2))
                Exit(f'tail失败。字符串 \"{s}\" 中没有预计存在的子串：  \"{mark}\"。', (s, mark))
            else:
                continue
        if with_mark:
            return s[s.rfind(mark):]
        else:
            return s[s.rfind(mark) + len(mark):]
    return s


tail = gettail


def strre(s, pattern):
    return (re.compile(pattern).findall(s))


# endregion


# 分布式
# region


# 检查磁盘是否可用（待机）
def checkdiskusable(s):
    s = s[0]
    Open(f'{s}:/diskInfo.txt')


@manage_args(dname=['name'], d=['disk'],
             # sepration='-use_root'
             )
def useDisk(dname=None, d=None,
            sepration=True,
            b=None, **leak
            ):
    """
    动态更改操作盘
    更改 path 解析根路径
    @param d:盘符
    @param dname: 字符串表示操作盘唯一标识符，可以列表
    @param strict:非严格模式下，找不到唯一标识符则开始创建
    @param sepration: 路径是否做人机隔离
    @return: 是否成功
    """

    def _use(d):
        if not ':' in d:
            d += ':/'
        if sepration:
            d += '/autom/'
        chdir(d, exist=False, create=False)
        log(f'operating {get_disk().upper()} （{getDiskName()}）')
        return getDiskName()

    global diskname, disknames
    disknames = getsettings('diskNames')
    if d:
        try:
            return _use(d)
        except:
            return False
    if dname in [None, []]:  # 传空参
        return usedisk(d='d', **(exclude(b, 'd')))
    if type(dname) in [list]:
        for dn in dname:
            ret = useDisk(dname=dn)
            if ret:
                return ret
        Exit(f'未找到磁盘 {dname}。')
    if type(dname) in [str, int]:
        for i in ['d', 'e', 'g', 'f', 'h']:
            if getDiskName(d=i) == dname:
                return _use(i)
        return False
    return False


useDisk = usedisk = use_disk = change_disk = switch_disk = \
    useDisk


def confirmRootPath(name):
    return getDiskName() == name


def get_disk():
    """
    获取当前操作盘的分区名
    @return:
    """
    return os.getcwd()[:1]


get_workspace = disk_path = diskpath = \
    os.getcwd
root = getDiskPath = \
    get_disk


def getDiskName(d=None):
    """
    获取唯一标识符
    @return:解析失败则返回False
    """
    if used_arg(d):
        useDisk(d=d)
    diskinfo = RefreshJson(f'{get_workspace()}/diskInfo.txt', silent=True)
    global disknames, diskname
    diskname = diskinfo.d['name'][0]
    disknames.append(diskname)
    return diskname


# endregion

# 爬虫
# region
@manage_args()
def init_edge(*a, b=None, **leak):
    init_browser(type='edge', **b)


ini_edge = init_edge
init_Edge = init_edge


@manage_args()
def init_chrome(*a, b=None, **leak):
    init_browser(type='chrome', **b)


init_Chrome = init_chrome


@manage_args(_type=['Type', 'type'])
def init_browser(_type=None, mine='0',
                 download_path=None, user_data_dir_path=None,
                 b=None, **leak) -> None:
    """
    命令行启动真实浏览器
    @param _type:
    @param mine:
    @param download_path:
    @param b:
    @param leak:
    @return:
    """
    if download_path == None:
        download_path = default_page_download_path
    init_backend()
    # 插件 js 请手动配置
    t = Cmd()
    default_begin_url = 'www.baidu.com'
    url = default_begin_url
    if _type == 'chrome':
        t.execute_at_once((f'\"{chrome_path}\" '
                           f'{url}'
                           f' --user-data-dir=\"{user_data_dir_path}"'
                           f' --download-dir=\"{download_path}\"'
                           ))
    elif _type == 'edge':
        t.execute_at_once((f'\"{edge_path}\" '
                           f'{url}'
                           f' --user-data-dir=\"{user_data_dir_path}"'
                           f' --download-dir=\"{download_path}\"'
                           ))
    # 等待浏览器建立
    # sleep(4)


def check_backend() -> bool:
    import socket
    s = socket.socket()
    s.settimeout(5)
    address = '127.0.0.1'
    port = 12080
    try:
        s.connect((address, port))
    except socket.timeout:
        # print(f"连接到 {address}:{port} 超时")
        return False
    except ConnectionRefusedError:
        # print(f"连接到 {address}:{port} 被拒绝")
        return False
    except Exception as e:
        # print(f"连接到 {address}:{port} 出现错误：{e}")
        return False
    else:
        delog(f"成功连接到后端 {address}:{port}")
        return True
    finally:
        s.close()


def init_backend() -> bool:
    if check_backend():
        return True
    global js_rpc_backend
    # copyto(exec_path())
    look(exec_path())
    Exit(' go 后端未启动，已打开路径请手动启动。')


@manage_args(funcName=['func', 'f'], param=['p', 'params'])
def send_rpc(page=None,
             group='test_group', name='test_name',
             funcName=None, param={},
             time_out=2,
             b=None, **leak
             ):
    import requests
    import json
    url = "http://localhost:12080/go"
    if page:
        group, name = page._type, page.mine
    data = {
        "group": group,
        "name": name,
        "action": "callFunctionByName",
        "param": json.dumps(merge({"funcName": funcName}, param))
    }

    try:
        return jsontodict(requests.post(url, data=data, timeout=max(time_out, 2)).text)['data']
    except  requests.exceptions.ReadTimeout as e:
        warn('脚本请求等待时间过短，请求失败', traceback=False)
    except Exception as e:
        warn(e, traceback=False)
    return send_rpc(**b)


@manage_args(loop=['ragne'])
def checkusers(prefix=None, f=None, suffix=None,
               loop=None,
               b=None, **leak,
               ):
    """

    @param prefix:
    @param f:
    @param suffix:
    @param range:  每次打开的个数
    @return:
    """
    lis = []
    for i in range(loop):
        lis.append(f.get())
    openedge(lis)


# def etree(url=None, xpath=None, proxies=None):
#     return
#     # 导入需要的模块
#     from lxml import etree
#     import requests
#     from fake_useragent import UserAgent
#
#     # 生成随机用户代理
#     ua = UserAgent()
#     headers = {'User-Agent': ua.random}
#
#     # 请求URL并获取内容
#     response = requests.get(url, headers=headers, proxies=proxies)
#     response.raise_for_status()  # 如果请求失败，这将抛出异常
#     content = response.content
#
#     # 使用lxml解析内容
#     tree = etree.HTML(content)
#
#     def count_elements(element):
#         return 1 + sum(count_elements(child) for child in element)
#
#     def tree_length(tree):
#         return count_elements(tree)  # 直接传递 tree
#
#     return tree.xpath(xpath), tree_length(tree)


class VideoDownloader():
    """
    yt-dlp 下载视频
    """

    def __init__(self, url=None, vpn=True, cookie=None, downloadroot=None,
                 silent=True, ):
        self._terminal = Cmd(silent=silent)
        if downloadroot == None:
            downloadroot = cachepath('video')
        if cookie:
            cookie = f'--cookies-from-browser {cookie}'
        else:
            cookie = ''
        if vpn:
            vpn = f'--proxy socks5://127.0.0.1:7890'
        else:
            vpn = ''
        CLI = (f"yt-dlp {vpn} {url} "
               f"--write-info-json --write-thumbnail {cookie} "
               f" -o \"{downloadroot}/%(uploader)s/%(id)s %(title)s/%(title)s.%(ext)s\" "
               f" -o \"thumbnail:{downloadroot}/%(uploader)s/%(id)s %(title)s/%(title)s.%(ext)s\" "
               f" -o \"subtitle:{downloadroot}/%(uploader)s/%(id)s %(title)s/%(title)s.%(ext)s\"  --write-subs "
               )
        copyto(CLI)
        self._terminal.execute(CLI)

    def output(self):
        return self._terminal.output

    def __del__(self):
        self._terminal.close()


def download_video(url, vpn=True, cookie='opera', targetroot=None, silent=True,
                   author=True, title=True, targetname=None, extract_time=5, path=None):
    """
    yt-dlp 下载视频，并且自动移动
    """
    _terminal = Cmd(silent=silent)
    if path:
        if isfile(path, exist=False):
            targetroot, targetname = parentpath(path), filename(path)
        else:
            targetroot = path
    targetroot += '/'
    if cookie:
        cookie = f'--cookies-from-browser {cookie}'
    else:
        cookie = ''
    if vpn:
        vpn = f'--proxy socks5://127.0.0.1:7890'
    else:
        vpn = ''
    downloadroot = cachepath(f'download/yt-dlp/{now_timestamp()}/')
    if author:
        author = '%(uploader)s/'
    else:
        author = ''
    if title:
        title = ' %(title)s'
    else:
        title = ''
    CLI = (f"yt-dlp {vpn} {url} "
           f"--write-info-json --write-thumbnail {cookie} "
           f" -o \"{downloadroot}/{author}/%(id)s{title}/%(title)s.%(ext)s\" "
           f" -o \"thumbnail:{downloadroot}/{author}/%(id)s{title}/%(title)s.%(ext)s\" "
           f" -o \"subtitle:{downloadroot}/{author}/%(id)s{title}/%(title)s.%(ext)s\" --write-subs "
           )
    copyto(CLI)
    _terminal.execute(CLI)

    sleep(extract_time)
    # 这个页面没有视频
    # return False
    monitor_dir_size(downloadroot, t=5)
    target = listdir(f'{downloadroot}')[0]
    fjson = ([i for i in listall(target, full=True) if i.endswith('.json')][0])
    fpic = ([i for i in listall(target, full=True) if i.endswith('.webp') or i.endswith('jpg') or
             i.endswith('png')][0])
    fvideo = ([i for i in listall(target, full=True) if i.endswith('.webm') or
               i.endswith('.mp4')][0])
    deletedirandfile([fjson, fpic])
    if targetname:
        if not '.' in targetname[-5:]:
            targetname += extension(fvideo)
    else:
        targetname = ''
    move(target, targetroot + '/' + filename(target) +
         '/' + targetname, overwrite=True)
    _terminal.close()


# 转到已经打开的edge并保存全部截屏
def getPics(loop, path):
    for i in range(loop):
        hotkey('ctrl', 'shift', 's')
        sleep(1)
        click(1146, 174)
        # 截图生成时间
        sleep(4)
        old = listfile('D:/')
        click(1700, 112)
        # 截图下载时间
        sleep(2)
        new = listfile('D:/')
        for j in new:
            if j in old:
                continue
            else:
                break
        move(j, f'{path}.{gettail(j, ".")}')


def geturls(loop=1, func=None, Type='edge'):
    """
    获取已打开浏览器的所有链接
    @param loop:
    @param func:处理每次get到的url
    @param type:浏览器类型
    @return: 列表
    """
    import pyperclip
    ret = []
    hotkey('alt', 'tab')
    for i in range(loop):
        # click(cachepath(type + 'url.png'), xoffset=80)
        hotkey('alt', 'd')
        hotkey('ctrl', 'c')
        c = pyperclip.paste()
        if func:
            c = func(c)
        ret.append(c)
        hotkey('ctrl', 'w')
    hotkey('alt', 'tab')
    return ret


# 将网页置顶显示
def alertpage(l):
    page = l[0]
    page.switch_to.window(page.window_handles[0])


@manage_args(root=['l', 'page'])
def Element(
        b=None,
        **leak, ):
    res = Elements(**b)
    if res == []:
        return None
    else:
        return res[0]


@manage_args(root=['page', 'l'], xpath=['s'])
def Elements(root=None, xpath=None, depth=3, silent=True,
             method=By.XPATH, strict=True, pre_wait=2,
             complete=True, interval=2,
             b=None, **leak
             ) -> list:
    """

    :param l:根元素
    :param s:字符表达式
    :param complete :区别于单个元素查询，要求全部不为空
    :return:列表，找不到为[]
    """
    # 参数
    # region
    check_arg_type(xpath, [str], strict=True)
    original_xpath = xpath
    for old, new in [
        ('\'', '\"'),
        ('span', '*[name()="span"]'),
        ('//@', '//*/@'),
        ('//text()', '//*/text()'),
        ('/svg', '/*[name()="svg"]')
    ]:
        xpath = xpath.replace(old, new)
    atr = None
    if '/text()' in xpath:
        xpath = Strip(xpath, '/text()')
        atr = 'text'
    if '/@' in xpath:
        xpath, atr = cuttail(xpath, '/@')
    # endregion
    while True:
        ret = root.find_elements(method, xpath)
        if len(ret):
            if atr == None:  # 不是要属性要返回 element，直接返回
                return [obj.__setattr__(method, xpath) or obj for obj in ret]

            # 未加载完全导致返回 '<selenium'
            def completed(l):
                l = l[0]
                if l == None or '<selenium' in str(l):
                    return False
                return True

            if atr not in ['text']:  # text  以外的属性
                l = [i.get_attribute(atr) for i in ret]
                if not completed(l):
                    continue
                return l
            else:  # text 属性
                try:
                    l = [i.text if i.text else i.get_attribute(
                        'text') for i in ret]
                    if strict:
                        if complete and not completed(l):
                            continue  # 整个函数重新执行
                    return l
                except Exception as e:
                    return []
        else:
            if depth < 0:
                if strict:
                    root.save_screenshot(picpath('screen_shot.png'))
                    look(picpath('screen_shot.png'))
                    copyto(xpath)
                    Exit((f'最终未获取到元素。  {original_xpath}'))
                return []
            else:
                sleep(interval)
                return Elements(
                    xpath=original_xpath, depth=depth - 1,
                    **(exclude(b, ['xpath', 'depth'])),
                )


element = Element
elements = Elements


def skip(l, s, method=By.XPATH, strict=False, t=99999):
    """
    简单等待，不做操作，等待人工操作
    t秒后或者元素消失
    :param l:页面
    :param s:字符表达式
    :param method:查找方法
    :param strict:严格模式，找不到元素则报错
    :param t:等待时间
    :return:
    """
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions

    page = l[0]
    sleep(1)
    if Element(l, s, depth=2, silent=True, method=method, strict=strict):
        warn(f'{s} detected. 等待({t})其消失中以继续。。。', traceback=False)
        alertpage([page])
        try:
            WebDriverWait(page, t, 3).until_not(
                expected_conditions.presence_of_element_located(locator=(method, s)))
        except Exception as e:
            page.refresh()
        sleep(2)


def getscrolltop(l):
    page = l[0]
    return page.execute_script('var q=document.documentElement.scrollTop;return(q)')


def scrollwidth(l):
    page = l[0]
    return page.execute_script('var q=document.documentElement.scrollWidth;return(q)')


# 获取页面最大高度（通过滚动条
def scrollheight(l):
    page = l[0]
    return float(page.execute_script('var q=document.documentElement.scrollHeight;return(q)'))


@manage_args()
def requestdownload(path=None, url=None,
                    mode='wb', header={}, t=None,
                    b=None, **leak):
    """

    @param path: 目标路径
    @param url: 源 url
    @param mode:
    @param header:
    @param t:
    @return:
    """
    import requests
    path = standarlizedPath(path)
    CreatePath(path)
    headers.update(**header)
    try:
        with open(path, mode) as f:
            f.write(requests.get(url=url, headers=headers).content)
    except (requests.exceptions.SSLError):
        try:
            with open(path, mode) as f:
                f.write(requests.get(
                    url=url, headers=headers, verify=False).content)
        finally:
            input('SSLError')
            requestdownload(path, mode, url)


@manage_args(download_path=['download_root'])
def _browser(url='', mine=None,
             silent=None, t=100, mute=True,
             _type='edge', download_path=None, method=None,
             manual_manage_webdriver=True,
             clone=None,
             b=None, **leak
             ) -> selenium.webdriver | bool:
    """
    为 js 或是 selenium 启动浏览器。
    @param url:
    @param mine:
    @param silent:
    @param t:
    @param mute:
    @param _type:
    @param download_path:
    @param method:
    @param manual_manage_webdriver: 是否使用第三方管理 webdriver
    @param b:
    @param leak:
    @return:
    """
    user_data_dir_path = standarlizedPath(projectpath(f'browser/userdata/{_type}/{mine}'),
                                          strict=True)
    if method in ['js']:
        return init_browser(download_path=download_path, user_data_dir_path=user_data_dir_path,
                            **(exclude(b, 'download_path')))

    from selenium import webdriver
    options = {
        'edge': lambda: webdriver.EdgeOptions(),
        'chrome': lambda: webdriver.ChromeOptions(),
        'firefox': lambda: webdriver.FirefoxOptions()
    }.get(_type, lambda: webdriver.ChromeOptions())()

    # options.page_load_strategy = 'eager'
    # options.add_experimental_option("autoplay_policy", "user-gesture-required")
    # UA 不受影响
    if download_path == None:
        download_path = default_page_download_path
    if download_path:
        {

        }.get(_type, lambda x: x.add_experimental_option(
            'prefs', {'download.default_directory': download_path}
        ))(options)

    if silent:
        {
            'chrome': lambda: options.add_argument(
                "--headless=new") if mine else options.add_argument('--headless=new')
        }.get(_type, lambda: options.add_argument('headless'))()

    if mute:
        options.add_argument({
                                 'chrome': 'mute-audio',
                             }.get(_type, '--mute-audio'))
        delog('浏览器打开静音')

    sys.path.insert(0, exec_path())
    if manual_manage_webdriver:
        # 手动移动 webdriver.exe 到环境变量中有的地方。例如 executablepath
        # selenium-pypi 官方地址 https://pypi.org/project/selenium/
        # webdriver downloads 在下面列出
        # 其中 chromecriver 地址 https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json
        add_env_path(exec_path())
        pass
    else:
        from webdriver_manager.chrome import ChromeDriverManager
        service = {
            'edge': lambda: None,
            'chrome': lambda: \
                webdriver.chrome.service.Service(ChromeDriverManager().install()),
            'firefox': lambda: webdriver.FirefoxService()
        }.get(_type, ())()

    if mine == True:
        options.add_argument(
            {
                'edge': f'--user-data-dir=C:\\Users\\{user}\\AppData\\Local\\Microsoft\\Edge\\User Data',
                'chrome': f"--user-data-dir=C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data"
            }.get(_type))

    elif mine not in [False, None]:  # 自立的缓存
        command = {
            'edge': f'--user-data-dir=C:\\Users\\{user}\\AppData\\Local\\Microsoft\\Edge\\User Data',
            'chrome': f"--user-data-dir={user_data_dir_path}"
        }.get(_type)
        _path = tail(command, '=')
        # 自动删除不必要数据
        delete((f'{_path}/{i}' for i in
                ['/Default/Code_Cache', '/Default/Cache', '/Default/Service Worker/CacheStorage',
                 '/Crashpad/reports', '/SwReporter',
                 'Profile 1/Cache', 'Profile 1/Service Worker', 'Profile 1/History',
                 '/Profile 1/GPUCache',
                 '/Crashpad']), silent=False)
        options.add_argument(command)

    {
        'chrome': lambda: options.add_experimental_option("excludeSwitches", ["enable-automation"])
    }.get(_type, lambda: None)()

    if manual_manage_webdriver:
        driver = {
            'edge': lambda: webdriver.Edge(options=options),
            'chrome': lambda: webdriver.Chrome(options=options),
        }.get(_type, )()
    else:
        driver = {
            'edge': lambda: webdriver.Edge(service=service, options=options),
            'chrome': lambda: webdriver.Chrome(service=service, options=options),
        }.get(_type, )()

    if not url in ['', None] and not 'http' in url:
        url = 'https://' + url
    driver.set_page_load_timeout(t)
    driver.set_script_timeout(t)
    try:
        if not url in [None, '']:
            driver.get(url)
        return driver
    except selenium.common.exceptions.InvalidArgumentException as e:
        warn(e, url)
        driver.quit()
        warn(f'旧页面未关闭。请关闭。或者是因为{url}中没有http or https请求')
        return False
        # return _chrome(url=url, mine=mine, silent=silent, t=t)


robot_browser = _browser


@manage_args(total=['ran', 'range'])
def getChrome(root=None, total=None,
              b=None, **leak
              ):
    """

    @param root:
    @param total:
    @param b:
    @return:
    """
    return Chrome(root=root, **leak)


default_page_download_path = standarlizedPath(
    cachepath('page_download'), strict=True)


class Browser():
    @manage_args(driver=['page'], mine=['root'], download_path=['download_root'])
    def __init__(self, url=None, download_path=default_page_download_path,
                 silent=False, driver=None, mine=False, family=None,
                 mute=False, clone=None,
                 _js=None, webdriver=None,
                 method=None, _type=None,
                 b=None, **leak):
        """

        @param url:
        @param download_path:
        @param silent:
        @param driver:
        @param mine:
        @param family:
        @param mute:
        @param method:  'page' 'js'
        @param _type:  'chrome' / 'edge' etc
        @param b:
        @param leak:
        """
        arg_mutex(family, mine, clone)
        if used(clone):
            used(url,strict=True)
        if check_type(family, [str]):
            for i in range(100):
                try:
                    return Browser.__init__(self,
                                            mine=f'{family}{i}',
                                            **(exclude(b, ['family', 'mine']))
                                            )
                except selenium.common.exceptions.SessionNotCreatedException as e:
                    pass
            Exit('')
        self.silent = silent
        self._type = self.Type = self.type = _type
        self.mine = mine
        self.method = method
        if self.method in ['js']:
            if download_path == None:
                download_path = strictpath(browser_path(f'download/{_type}/{mine}/'))
        else:
            if download_path == None:
                download_path = default_page_download_path
        self.download_path = download_path
        self.download_root = self.download_path
        if used_type(driver, list):
            self.driver = driver[0]
            return
        else:
            if method in ['js']:
                init_backend()
                if self.test_connect(depth=2):
                    self.driver = None
                    return
            if enabled(clone):
                for i in range(100):
                    try:
                        ret = Browser.__init__(self,
                                               mine=f'blank{i}',
                                               url=domain_url(url) if used_arg(url) else None,
                                               **(exclude(b, ['clone', 'mine', 'url']))
                                               )
                        self.add_cookie(name=f'{clone}')
                        if used_arg(url):
                            self.get(url)
                        return ret
                    except selenium.common.exceptions.SessionNotCreatedException as e:
                        pass
            self.driver = _browser(download_path=download_path, **(exclude(b, 'download_path')))
        if not url == None:
            self.get(url)

    def save_cookies(self, name=None):
        save_var(var=self.driver.get_cookies(),
                 path=browser_path(f'cookies/{self._type}/{self.mine}'))

    export_cookies = \
        save_cookies

    @manage_args()
    def get_cookies(self, name=None,
                    b=None, **leak):
        if used_arg(name):
            path = browser_path(f'cookies/{self._type}/{name}')
        else:
            path = browser_path(f'cookies/{self._type}/{self.mine}')
        path = add_ext(path, '.pkl')
        if not isfile(path=path, exist=True):
            Exit(f'{path} cookie 文件不存在')
        for d in get_var(path=path):
            self.driver.add_cookie(cookie_dict=d)

    add_cookie = load_cookie = \
        get_cookies

    def __del__(self):
        """
        @return:
        """
        try_to_execute_script('self.quit()', silent=True)

    def up_at_once(self):
        """
        立刻返回顶部
        @return:
        """
        self.setscrolltop(0)

    def maximize(self):
        self.driver.maximize_window()

    maxwindow = maximize

    #  爬取论坛的每一页
    def forum(self, url=None, titletail=None, hostname=None,
              func0=None, func1=None, func2=None, func3=None, minsize=(150, 150), t=3,
              scale=200, mine=None, redownload=None,
              saveuid=True, look=True, silent=False):
        """

        @param firsturl:
        @param titletail:
        @param hostname:
        @param func0: 预备检查（比如是否登陆了
        @param func1: 返回当前帖子的Uid
        @param func2: 根据帖子的uid，返回后面的每页的urllist
        @param func3: 检查后面的每页是否被反爬了
        @param minsize:
        @param redownload: 是否重复下载帖子
        @param t:
        @param scale:
        @param saveuid:
        @param look:
        @param silent:
        @return:
        """
        if url == '':
            return
        # uid是否文件夹注入帖子uid前缀
        #     先打开第一页，获取标题，每页数
        page = self
        if not url == None:
            page.get(url)
        sleep(t)
        title = page.title()
        if ' ' + titletail in title:
            title = removetail(title, ' ' + titletail)
        if titletail in title:
            title = removetail(title, titletail)
        if not func0(page):
            return False
        # func1  返回当前帖子的Uid
        uid = func1(page)
        # 检查以前的帖子
        if redownload:
            pastcount = 0
            if exists(shotspath(f'{hostname}/{uid}_{title}')):
                pastcount += 1
                while exists(shotspath(f'{hostname}/{uid}_{title}_{pastcount}')):
                    pastcount += 1
            if exists(shotspath(f'{hostname}/{title}')):
                pastcount += 1
                while exists(shotspath(f'{hostname}/{title}_{pastcount}')):
                    pastcount += 1
            if pastcount == 0:
                pastcount = ''
            else:
                pastcount = f'_{pastcount}'
            delog(pastcount)
        else:
            pastcount = ''
        if saveuid:
            page.save(path=shotspath(f'{hostname}/{uid}_{title}{pastcount}/第1页/'),
                      minsize=minsize,
                      direct=True, look=look, scale=scale, redownload=False)
        else:
            page.save(path=shotspath(f'{hostname}/{title}{pastcount}/第1页/'), minsize=minsize,
                      direct=True, look=look, scale=scale, redownload=False)
        # func2  根据帖子的uid，返回后面的每页的urllist
        urllist = func2([page, uid])
        count = 1
        for url in urllist:
            page.get(url)
            count += 1
            # func3  检查后面的每页是否被反爬了
            func3([page])
            if saveuid:
                page.save(shotspath(f'{hostname}/{uid}_{title}{pastcount}/第{count}页/'),
                          minsize=minsize, direct=True, look=look, scale=scale, redownload=False)
            else:
                page.save(path=shotspath(f'{hostname}/{title}{pastcount}/第{count}页/'),
                          minsize=minsize, redownload=False,
                          direct=True, look=look, scale=scale)

    linkedSpider = forum

    @manage_args()
    @consume
    def download(self, *a, use_global=True,
                 b=None, **leak):
        """
        page_download 的封装
        @param use_global: 是否使用全局的 download_page
        """
        if self.is_js():
            if use_global:
                return download(*a, **b)
            else:
                Exit('未实现')
                # return download(*a, driver=self, **b)
        download(*a, driver=self, **b)

    @manage_args(xpath=['s'])
    def click(self, xpath=None, strict=True, depth=1,
              b=None, **leak
              ) -> bool:
        """
        点击元素或是xpath
        @param a:
        @param strict:
        @param depth:
        @return: 是否成功
        """
        from selenium.webdriver.common.action_chains import ActionChains
        if xpath == None:
            return False

        if type(xpath) in [list]:
            tell = False
            for xpath in list(xpath):
                tell = tell or self.click(strict=False, xpath=xpath,
                                          **(exclude(b, ['strict', 'xpath'])))
                if tell:
                    break
            return tell

        if type(xpath) in [str]:
            if self.is_js():
                return Eval(self.send_rpc(f='click', p={'xpath': xpath}))
            return self.click(self.element(**b))

        elif type(xpath) in [selenium.webdriver.remote.webelement.WebElement]:
            try:
                xpath.click()
                return True
            except Exception as e:
                try:
                    ActionChains(self.driver).move_to_element(
                        to_element=xpath).click().perform()
                    return True
                except Exception as e:
                    return False
                    # warn(['clickelement error！', e])

    def skip(self, s, strict=False, click=False, t=200):
        """
        跳过元素
        @param s: xpath字符串
        @param strict: 这个需要跳过的元素是否一定会出现
        @param click:
        @param t: 该元素未处理的最长等待时间；到后会刷新页面
da      @return:
        """

        if not click:
            return skip([self.driver], s, strict=strict, t=t)
        e = self.element(s, strict=False)
        if not e == None:
            self.click(e)

    @manage_args(path=['file', 'f'])
    def execute_js(self, js=None, path=None):
        if used(js):
            try:
                return self.driver.execute_script(js)
            # except Exception as e:
            except selenium.common.exceptions.WebDriverException:
                # 返回的结果无法序列化？
                outs = tail(js, 'return ')
                before = splittail(js, 'return ')[0]
                cmd = before + 'return JSON.stringify(' + outs + ')'
                return self.driver.execute_script(cmd)
        elif used(path):
            path = jspath(path)
            return self.driver.execute_script(''.join(txt(jspath(path)).l))

    execute_script = executejs = execute = \
        execute_js

    # 应用窗口宽高
    def get_window_size(self):
        if self.is_js():
            return Eval(self.send_rpc(f='Size'))
        return self.driver.get_window_size()['width'], self.driver.get_window_size()['height']

    def nearend(self):
        """
        判断是否接近底部

        @return:
        """
        if self.is_js():
            return Eval(self.send_rpc(f='nearEnd'))
        return (self.getscrolltop() +
                self.get_window_size()[1]) / \
            self.getscrollheight() > 0.999

    nearbottom = nearend
    near_end = nearend

    @manage_args()
    def Down(self, start=0, end=None,
             scale=100, func=None, pause=1,
             args={},
             all_args=None, **leak):
        """
        每次下滚后执行函数。即使已经到底部也会来一次。
        @param start:
        @param end:
        @param scale:
        @param func:一参为迭代返回值，二参为 self ，循环下滚执行。包含返回值累加、去重的逻辑。
        @param pause:
        @param args: func的参数
        @return:[] 或者 None
        """
        self.scroll(h=start)
        ret = []
        while True:
            if (not end == None and self.getscrolltop() < end):
                break
            self.scroll(h=scale + self.getscrolltop())
            sleep(pause)
            if not func == None:
                ret = func(ret, self, **args)
            if self.nearend():
                break
        return ret

    @manage_args(xpath=['s'])
    def new_Down(self, start=0, end=None,
                 scale=100, func=None, pause=1,
                 b=None, **leak):
        """
        每次下滚后执行函数。即使已经到底部也会来一次。
        @param start:
        @param end:
        @param scale:
        @param func:一参为迭代返回值，二参为[self]，循环下滚执行。包含返回值累加、去重的逻辑。
        @param pause:
        @param a: func的参数
        @param b: func的参数
        @return:[] 或者 None
        """
        self.scroll(h=start)
        ret = []
        while True:
            if (not end == None and self.getscrolltop() < end):
                break
            self.scroll(scale + self.getscrolltop())
            sleep(pause)
            if not func == None:
                ret1 = func(self=self, **b)
                if not type(ret1) in [list]:
                    ret1 = [ret1]
                ret = Set(ret + ret1)
            if self.nearend():
                break
        return ret

    @manage_args(s=['xpath'])
    def remove(self, s=None,
               b=None, **leak
               ):
        """
        删去元素
        @param s:
        @return:
        """
        if type(s) in [WebElement]:
            return self.remove(s.xpath)
        if type(s) in [str]:
            self.execute_script(f"var xpath = '{s}';" + """
var iterator = document.evaluate(xpath, document, null, XPathResult.UNORDERED_NODE_ITERATOR_TYPE, null);
var element = iterator.iterateNext();
if (element) {
    element.parentNode.removeChild(element);
}
            """)

    delete = remove

    # 历史后退
    def backward(self):
        if self.is_js():
            return self.send_rpc(f='back')
        self.driver.back()

    # 历史前进
    def forward(self):
        if self.is_js():
            return self.send_rpc(f='forward')
        self.driver.forward()

    # 局内按键
    def hotkey(self, *a):
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.keys import Keys
        for s in a:
            # region
            if s == 'left':
                ActionChains(self.driver).key_down(Keys.ARROW_LEFT).perform()
            elif s == 'right':
                ActionChains(self.driver).key_down(Keys.ARROW_RIGHT).perform()
            elif s == 'up':
                ActionChains(self.driver).key_down(Keys.ARROW_UP).perform()
            elif s == 'down':
                ActionChains(self.driver).key_down(Keys.ARROW_DOWN).perform()
            elif s == 'enter':
                ActionChains(self.driver).key_down(Keys.ENTER).perform()
            elif s == 'esc':
                ActionChains(self.driver).key_down(Keys.ESCAPE).perform()
            elif s == 'backspace':
                ActionChains(self.driver).key_down(Keys.BACKSPACE).perform()
            elif s == 'tab':
                ActionChains(self.driver).key_down(Keys.TAB).perform()
            elif s == 'space':
                ActionChains(self.driver).key_down(Keys.SPACE).perform()
            elif s == 'ctrl':
                ActionChains(self.driver).key_down(Keys.CONTROL).perform()
            elif s == 'alt':
                ActionChains(self.driver).key_down(Keys.ALT).perform()
            elif s == 'shift':
                ActionChains(self.driver).key_down(Keys.SHIFT).perform()
        #     # endregion
        for s in a:
            #         region
            if s == 'left':
                ActionChains(self.driver).key_up(Keys.ARROW_LEFT).perform()
            elif s == 'right':
                ActionChains(self.driver).key_up(Keys.ARROW_RIGHT).perform()
            elif s == 'up':
                ActionChains(self.driver).key_up(Keys.ARROW_UP).perform()
            elif s == 'down':
                ActionChains(self.driver).key_up(Keys.ARROW_DOWN).perform()
            elif s == 'enter':
                ActionChains(self.driver).key_up(Keys.ENTER).perform()
            elif s == 'esc':
                ActionChains(self.driver).key_up(Keys.ESCAPE).perform()
            elif s == 'backspace':
                ActionChains(self.driver).key_up(Keys.BACKSPACE).perform()
            elif s == 'tab':
                ActionChains(self.driver).key_up(Keys.TAB).perform()
            elif s == 'space':
                ActionChains(self.driver).key_up(Keys.SPACE).perform()
            elif s == 'ctrl':
                ActionChains(self.driver).key_up(Keys.CONTROL).perform()
            elif s == 'alt':
                ActionChains(self.driver).key_up(Keys.ALT).perform()
            elif s == 'shift':
                ActionChains(self.driver).key_up(Keys.SHIFT).perform()

    #        # endregion

    def getscrollheight(self):
        if self.is_js():
            return Eval(self.send_rpc(f='Size'))[0]
        return scrollheight([self.driver])

    scrollheight = getscrollheight

    # 应用窗口的高度
    def Height(self):
        if self.is_js():
            self.send_rpc('Size')[1]
        return self.driver.execute_script("return window.innerHeight;")

    def Width(self):
        if self.is_js():
            self.send_rpc('Size')[0]
        if self.is_js():
            self.send_rpc('innerWidth')
        return self.driver.execute_script("return window.innerWidth;")

    def full(self, strict=False):
        """全屏
        @return:
        """
        if self.is_js():
            return
        if strict:
            self.driver.fullscreen_window()
        else:
            self.set_window_size(1920, 1080)

    def fullscreen(self, path=None, scale=100, autodown=True, pause=1, clip=True, clipinterval=0.6,
                   cuttop=0, cutbottom=0, cutleft=0, cutright=0, maxheight=40000, _look=False,
                   overwrite=None):
        """
        往上获取全屏。固定保存在basic.png。
        @param path:路径名而不是文件名
        @param scale: 下滚距离
        @param autodown:是否下滚
        @param pause:不切片上滚时间间隔
        @param clip: 是否切片
        @param cuttop: 顶部固定浮动元素高度
        @param clipinterval: 切片时间间隔
        @param cutbottom: 底部固定浮动元素高度
        @param cutleft: 左边固定浮动元素宽度
        @param cutright: 右边固定浮动元素宽度
        @param maxheight: 最大高度
        @param _look: 是否查看
        @return:
        """
        if path == None:
            path = shotspath(f'其它/{self.title()}/basic.png')
        if not '/basic.png' in path:
            path += '/basic.png'
        path = standarlizedPath(path)
        createpath(path)
        delog(f'将把 {self.url()} 的全屏保存到  {path}')

        if autodown:
            self.down(maxheight=maxheight)
        if clip:
            self.down(maxheight=maxheight)
            # 为了防止图片懒加载跳屏，先上滚一次
            self.up()
            self.down()

            buf = 60
            clipsize = self.Height() - Int(cuttop) - Int(
                cutbottom) - buf
            clipcount = 0
            while True:
                self.scroll(
                    h=max(0, int(self.getscrollheight() - clipsize * clipcount -
                                 self.get_window_size()[
                                     1] + 130)))
                sleep(clipinterval)
                # 50是一般认为clipsize不会小于的值
                clippath = f'{parentpath(path)}/clipped/{extensionandname(path, exist=False)[0]}{clipcount}{extensionandname(path, exist=False)[1]}'
                createpath(clippath)
                self.screen_shot(path=clippath)
                delog(f'已保存部分截图到 {clippath}')
                clipcount += 1
                if self.getscrolltop() == 0:
                    break
            combineimages(parentpath(clippath), outputname='basic.png', mode='vertical',
                          reverse=True,
                          filelist=[f"{parentpath(clippath)}/basic{i}.png" for i in
                                    range(clipcount)],
                          cuttop=cuttop, cutbottom=cutbottom, cutleft=cutleft, cutright=cutright)
            deletedirandfile(parentpath(clippath), silent=True)
        else:
            self.up(scale=scale, pause=pause)
            x, y = max(1080, scrollwidth(
                [self.driver]) + 100), scrollheight([self.driver])
            self.set_window_size(x, y)
            self.driver.get_screenshot_as_file(path)

        if _look:
            look(path)

    # 避开不安全网页警告
    def skipsystemwarn(self):
        if '受到举报的不安全网站' in self.title():
            self.click('//*[@id="moreInformationDropdownLink"]')
            self.click('//*[@id="overrideLink"]')
        time.sleep(1)

    @manage_args()
    def save(self,
             b=None, **leak,
             ):
        config = jsondata('savepage')
        jsondata('_savepage').clear()
        for i in config.data:
            if i in self.url():  # 用 in 的方式来匹配 Url
                jsondata('_savepage').setdata(config.data[i])
        return self._savepage(**(rmkey(b, 'self')))

    @useState
    def _savepage(self, path=None, video=False, minsize=(100, 100),
                  t=3, titletail=None, scale=100,
                  direct=False, look=None,
                  clicktoextend=None, autodown=True, check=False,
                  duplication=False, extrafunc=None,
                  pause=1, windowsize=None,
                  overwrite=True, redownload=True, savevideo=False, clip=True,
                  cuttop=0, cutbottom=0, cutleft=0, cutright=0, clipinterval=2,
                  top=None, bottom=None, left=None, right=None, maxheight=40000,
                  ):
        """
        保存整个网页，自定义参数
        包括截图，图片（大小可过滤），视频（可选），地址默认集锦
        @param path:收藏路径后缀
        @param video:
        @param minsize: 保存图片最小过滤尺寸
        @param t:
        @param titletail:
        @param scale:
        @param direct:
        @param clicktoextend: 可选点击展开
        @param autodown:
        @param check:
        @param duplication: 可选是覆盖还是新建已保存网页的副本
        @param extrafunc: 需要进行的额外操作
        @param pause: 滚动间隔
        @param overwrite: 是否覆盖
        @param redownload: 是否重新下载
        @param savevideo: 是否保存视频
        @param cuttop: 顶部固定浮动元素高度
        @param clipinterval: 切片时间间隔
        @param maxheight:  网页的最大高度
        @param windowsize: 不指定则全屏
        @return:
        """
        # region
        if not None == top:
            cuttop = top
        if not None == bottom:
            cutbottom = bottom
        if not None == left:
            cutleft = left
        if not None == right:
            cutright = right

        if windowsize == None:
            self.full()
        else:
            self.set_window_size(windowsize)
        if minsize in [False, None]:
            minsize = (9999, 9999)

        if path == None:
            path = shotspath(f'其它/{self.title()}/')
        else:
            path = shotspath(path)

        #     附加页面标题到文件夹名
        if not direct:
            sleep(t)
            if not self.title() in path:
                path += self.title()
        if not titletail == None and ' ' + titletail in path:
            path = removetail(path, ' ' + titletail)
        if not titletail == None and titletail in path:
            path = removetail(path, titletail)
        # 没办法，这个空格在不在真的完全是一个玄学
        path += '/'

        # 判断是否新建网页副本
        if not exists(path, notempty=True):
            createpath(path)
        else:
            if not redownload:
                log(f'已存在{path}，将不保存网页')
                return True
            elif not duplication:
                warn(f'已存在 {path}，将覆盖已保存的网页')
                # 遍历文件夹产生从0开始的新序号数字
                count = 0
                while exists(path + str(count)):
                    count += 1
                path = re.sub(r'\\+$', '', path)
                path = path + str(count) + '/'
                createpath(path)

        # 特殊点击展开页面
        if not clicktoextend == None:
            if type(clicktoextend) in (str,):
                self.click(clicktoextend)
                if autodown:
                    self.down()
            else:
                clicktoextend([self])

        # 额外操作
        if not extrafunc == None:
            extrafunc([self])
        # 保存页面截图
        if self._type == 'edge' and not self.silent:
            self.ctrlshifts(path, t)
        else:
            self.fullscreen(f'{path}/basic.png', scale=scale, autodown=autodown, pause=pause,
                            clip=clip,
                            cutright=cutright, cutleft=cutleft, cuttop=cuttop, cutbottom=cutbottom,
                            clipinterval=clipinterval, maxheight=maxheight)

        # 保存页面图片
        self.savepics(path, 7, minsize=minsize)

        # 保存页面视频
        if savevideo:
            self.savevideos(path, 20)

        # 留下url记录
        txt(f'{path}/url.txt').add(self.url())

        log(f'页面已保存到{path}')
        if check:
            try:
                Open(path + '/img')
            except Exception as e:
                pass
        return path

    # 保存页面上的所有图片
    def savepics(self, path=None, t=5, minsize=(100, 100)):
        if self.url() == '':
            return
        res = []
        if path == None:
            path = shotspath(f'/其它/{self.title()}/')
        res = self.elements('//pic', strict=False) + \
              self.elements('//img', strict=False)
        count = 0
        for i in res:
            if i.size['height'] < minsize[1] or i.size['width'] < minsize[0]:
                continue
            count += 1
            url = i.get_attribute('src')
            if url == None:
                url = i.get_attribute('href')
            if url == None:
                Exit(self.url(), '获取图片地址失败')
            #     特殊地址处理
            url = gettail(url, 'blob:', strict=False)
            url = gettail(url, 'data:', strict=False)
            if '<svg' in url:
                continue
            delog(f'图片地址：{url}')

            # 有些图片懒加载
            # if 'data:' in url:
            #     continue

            fname = gettail(url, '/')

            bb = True
            # link里的图片后缀名后面还会有杂七杂八的东西
            for j in ['.jpeg', '.jpg', '.gif', '.png', '.bmp', '.webp']:
                if j in fname:
                    fname = removetail(fname, j) + j
                    bb = False
                    break
            if bb:
                fname += j
            fname = standarlizedFileName(fname)
            dpath = (f'{path}/img/_{count}_{fname}')
            log(f'saving {self.url()}的 {url} 到 {dpath}')
            delog(path)
            try:
                download(url, dpath, t=t)
            except Exception as e:
                warn(f'保存页面上的图片失败，\n{e}')
            p = pic(dpath)

    # 保存页面上的所有视频
    def savevideos(self, path, t=5, minsize=None):
        res = []
        res += self.elements('//video', strict=False)
        count = 0
        for i in res:
            count += 1
            url = i.get_attribute('src')
            if url == None:
                url = i.get_attribute('href')
            if url == None:
                Exit(self.url(), '获取图片地址失败')

            fname = gettail(url, '/')
            b = True
            for j in ['.mp4', 'mp3']:
                if j in fname:
                    fname = removetail(fname, j) + j
                    b = False
                    break
            if b:
                fname = fname + '.mp4'
            fname = standarlizedFileName(fname)
            dpath = f'{path}/video/<{count}>{fname}'
            log(f'saving {self.url()}的 {url} 到 {dpath}')
            download(url, dpath, t=t)

    # 快捷键保存截屏
    def ctrlshifts(self, path=None, t=3):
        """
        快捷键保存截屏
        @param path:
        @param t:
        @return:
        """
        if not self.type in 'edge':
            Exit('不是 edge 浏览器。不能用ctrl+shift+S 保存e')
        self.top()
        self.maxwindow()
        self.down(t=t)
        if path == None:
            path = shotspath(f'/其它/{self.title()}')
        sleep(0.5)
        hotkey('ctrl', 'shift', 's')
        sleep(1)
        lis1 = listfile(userpath('Downloads'))
        click('browser/捕获整页.png')
        sleep(t)
        lis2 = listfile(userpath('Downloads'))
        for i in lis2:
            if not i in lis1:
                break
        move(i, f'{path}/basic.{gettail(i, ".")}')

    # 到上层显示窗口
    def top(self):
        if self.silent == True:
            Exit('静默模式下不显示到上层')
        hotkey('win', 'd')
        self.switchto()

    # 返回窗口列表
    def tabs(self):
        return self.driver.window_handles

    # 新建窗口
    def newwindow(self, url=''):
        if not 'https://' in url:
            url = 'https://' + url
        self.driver.execute_script(f'window.open("{url}")')

    def refresh(self):
        self.driver.refresh()
        sleep(1)

    @not_null(check_lis=[None, ''])
    def url(self):
        if self.is_js():
            ret = self.send_rpc(f='url')
            return ret
        return self.driver.current_url

    @listed()
    def clickelement(self, *a):
        return Edge.click(a)

    def move_mouse(self, *a, strict=False, x=None, y=None, xoffset=None, yoffset=None):
        """
        移动浏览器的鼠标
        @param a:
        @param strict:
        @param x:
        @param y:
        @param xoffset:
        @param yoffset:
        @return:
        """
        s = a[0]
        if s == None:
            return
        from selenium.webdriver.common.action_chains import ActionChains
        if type(s) in [str]:
            ActionChains(self.driver).move_to_element(
                to_element=self.element(s, strict=strict)).click().perform()
            return

        elif type(s) in [selenium.webdriver.remote.webelement.WebElement]:
            try:
                ActionChains(self.driver).move_by_offset(x, y).perform()
                return
            except Exception as e:
                warn(['moveto失败！', e])
        elif not x == None:
            ActionChains(self.driver).move_by_offset(x, y).click().perform()

    # 监测客户端
    # 死循环直到客户端响应 conn 函数
    @manage_args()
    def test_connect(self,
                     depth=0,
                     b=None,
                     **leak):
        if depth < 0:
            return False
        if self.is_js():
            if not 'successfully connected' == self.send_rpc(
                    test=True, f='conn', page=self,
                    **b):
                warn(' js 客户端连接预测试失败。')
                return self.test_connect(depth=depth - 1, **(exclude(b, 'depth')))
            # delog(' js 客户端连接预测试成功。')
            return True
        Exit('？？？ 不是 js 却在调用？')
        return False

    test = conn = \
        test_connect

    @consume
    # 根据多个但只有一个有效的字符串匹配元素，返回第一个
    def element(self, *a, **b):
        ret = self.elements(*a, complete=False, **b)

        if ret == []:
            return None
        else:
            return next((x for x in ret if x is not None), None)

    @manage_args(xpath=['s'])
    def elements(self, xpath=None, depth=2,
                 silent=True, strict=True, root=None,
                 refresh=False, complete=None,
                 interval=1,
                 b=None, **leak
                 ) -> list:
        """
        根据多个但只有一个有效的字符串匹配元素，返回第一组
        @param s:匹配字符串或是元素
        @param depth:
        @param silent:
        @param strict:True表示如果没找到，直接报错
        @param root:根元素。默认是self.driver
        @param refresh:找不到元素是否刷新页面
        @return:
        """
        sync_arg(complete, strict)
        if root == None:
            b['root'] = root = self.driver
        if depth < 0:
            if strict:
                warn(f'最终未找到元素。\n\t {xpath}')
            return []

        try:
            if not type(xpath) == list:
                if self.is_js():
                    ret = self.send_rpc(f='es', p={'xpath': xpath})
                    ret = Eval(ret)
                else:
                    ret = elements(**b)
            else:
                for i in xpath:
                    ret = elements(strict=False, xpath=i, **(exclude(b, 'strict', 'xpath')))
                    if not ret == []:
                        break

            if complete and ret == []:
                sleep(interval)
                ret = Browser.elements(self, **b)
            retl = []
            for i in ret:
                if not type(i) in [WebElement, element]:
                    retl.append(i)
                    continue
                i.url = self.url()
                i.page = self
                i.xpath = xpath
                retl.append(i)
            return retl


        except Exception as e:
            if strict:
                self.look()
            if type(e) in [selenium.common.exceptions.StaleElementReferenceException]:
                return elements(**b)
            Exit(e, traceback=True)
            return []

    Element = element
    Elements = elements

    @manage_args()
    def scroll(self, h=None, xpath=None,
               e=None,
               b=None, **leak):
        """
        下滚或者滚动到元素
        @param h:
        @param ite:
        @return:
        """
        if self.is_js():
            return self.send_rpc(f='scroll', p={'y': h, 'xpath': xpath})
        if used(h):
            if h == -1:
                self.down()
            else:
                setscrolltop([self.driver, h])
            return
        if used(xpath):
            setscrolltop([self.driver, Browser.element(self, xpath).location('y')])
            return
        if arg_type(e, [selenium.webdriver.remote.webelement.WebElement]):
            setscrolltop([self.driver, h.location['y'] - h.size['height']])
            return

    scrollto = scroll_to = scrollTo = \
        scroll

    @consume
    @manage_args()
    def down(self, ratio=1, t=0.3,
             ite=None, maxheight=None, silent=None,
             max_wait=5, b=None,
             **leak):
        """
        一个下滑到底并且再下滑一下的模仿人的动作
        @param ratio: 判断是否到底的 占总高比例
        @param t: 每次执行 doubl_down的过时
        @param ite:
        @param maxheight:
        @param max_wait: 单次的最大下等时间
        @return:
        """
        if silent == None:
            log('滚动中..')
        if self.is_js():
            return self.send_rpc(f='down')
        page = self.driver

        def _tell_end():
            if not self.nearend():
                return False
            if maxheight is None or getscrolltop([page]) <= maxheight:
                return True
            return False

        def double_down():
            """
            只是下滑，但是会往回弹一下，以模拟人的操作
            @param l:
            @param ite:
            @return:
            """
            if self.nearend():
                return
            page = self.driver
            page.execute_script(
                f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
            page.execute_script(
                f'document.documentElement.scrollTop=document.documentElement.scrollHeight-20')
            sleep(t / 2)
            page.execute_script(
                f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
            sleep(t / 2)

        while not _tell_end():
            double_down()
            double_down()
            sleep(t)
            double_down()
            double_down()
            if not _tell_end():
                continue
            sleep(max_wait)

    def getscrolltop(self):
        if self.is_js():
            return Int(self.send_rpc(f='Top'))
        return getscrolltop([self.driver])

    def setscrolltop(self, h):
        if h < 0:
            warn(f'设置目标浏览器高度小于0')
            h = 0
        if self.is_js():
            return self.send_rpc(f='scroll', p={'y': h})
        return setscrolltop([self.driver, h])

    def up(self, scale=250, pause=1):
        """
        向上滚动
        @param scale:上滚距离
        @param pause: 上滚间隔
        @return:
        """
        h = self.getscrolltop()
        while h > 10:
            if h > scale:
                h -= scale
                if h <= 0:
                    h = 0
                delog(h)
                sleep(pause)
            else:
                h = 0
            self.setscrolltop(h)

    # 新建标签页并跳转到标签页
    def open(self, url):
        if self.is_js():
            Exit('不支持')
        if url in [None]:
            Exit(f'url 异常 为{url}')
        url = 'https://' + url.strip('https://')
        self.driver.execute_script(f"window.open('{url}')")
        Edge.switchto(self, )

    def is_js(self):
        return self.method in ['js']

    @manage_args(depth=['retry'])
    def send_rpc(self, *a, depth=4,
                 interval=20, test=None,
                 b=None, **leak):
        """
        有多次尝试
        @param a:
        @param depth:
        @param interval:
        @param test: 是否是 test_conn 调用
        @param b:
        @param leak:
        @return:
        """
        try:
            if depth < 0:
                warn(' send_rpc 失败。', traceback=False)
                if not test:
                    Exit()
                return
            ret = send_rpc(page=self,
                           time_out=interval / (depth),
                           *a, **(exclude(b, 'page')))

            # 异常，chaoshi
            if '黑脸怪：' in ret and 'timeout' in ret:
                warn(f' 黑脸怪 timeout  ', traceback=False)
                sleep(1)
                return self.send_rpc(depth=depth - 1, **(exclude(b, 'depth')))
            elif '没有找到当前组和名字' in ret and '注入了' in ret:
                sleep(1)
                warn(f'客户端 {self._type} {self.mine} 未就绪，重试。。。', traceback=False)
                if test:
                    depth -= 1
                return self.send_rpc(depth=depth, **(exclude(b, 'depth')))
            else:
                return ret
        except Exception as e:
            return send_rpc(**b)

    def get(self, url=None, t=None,
            resethight=False, pre_wait=3, interval=3):
        """

        @param url:
        @param t: 加载后的空白等待时间
        @param resethight: 是否重置浏览器高度
        @param pre_wait:
        @param interval: resetheight down 的间隔
        @return:
        """
        if self.is_js():
            return self.send_rpc(f='get', p={'url': url})

        if resethight:
            self.set_window_size(self.get_width(), 700)
        try:
            if not 'https://' in url and not 'http://' in url:
                url = 'https://' + url
            self.driver.get(url)
            if t:
                sleep(t)
            else:
                sleep(0.4)
        except Exception as e:
            self.look()
            warn(f'geturl 异常，{type(e)}，请尝试 {url}', traceback=False)
            if e in [selenium.common.exceptions.InvalidArgumentException]:
                Exit(f'请检查url = {url} 是否错误。')
            if e in [selenium.common.exceptions.TimeoutException]:
                self.screenshot()
                Exit(f'加载超时，截图退出。')
            raise (e)

        if resethight:
            self.down(t=interval)
            while True:
                old_h = self.getscrollheight()
                self.set_window_size(
                    self.get_width(), self.getscrollheight() - 70)
                sleep(0.2)
                if old_h == self.getscrollheight():
                    self.set_window_size(
                        self.get_width(), self.getscrollheight() + 70)
                    break
            self.up()

    def switchto(self, n=-1):
        if self.is_js():
            return self.send_rpc(f='switchTo', p={'n': n})
        if self.is_js():
            Exit('不支持')
        if type(n) in [int]:
            self.driver.switch_to.window(self.driver.window_handles[n])
        if type(n) in [str]:
            self.driver.switch_to.window(n)

    turn_to = switchto

    def set_window_size(self, *a, **b):
        if self.is_js():
            return
        log(f'扩展窗口至大小：{a, b}')
        if type(a[0]) in [list, tuple]:
            self.driver.set_window_size(*a[0])
        self.driver.set_window_size(*a, **b)

    def set_wnidow_height(self, h):
        self.set_window_size(self.get_width(), h)

    def set_window_width(self, w):
        self.set_window_size(w, self.get_height())

    def elementshot(self, s, path=None, xoffset=None, yoffset=None, moveto=True, overwrite=True,
                    ajax_wait_time=0):
        """
        会改变窗口大小位置
        @param path:
        @param s: 元素，表达式
        @param xoffset:
        @param yoffset:
        @param moveto: 是否移动到元素位置
        @param overwrite:
        @param ajax_wait_time:  moveto 后的等待时间
        @return: 图片路径
        """

        currentheight = self.getscrolltop()
        if path == None:
            path = cachepath('elementshot.png')
        else:
            path = standarlizedPath(path)
            if isfile(path, exist=True):
                if overwrite:
                    warn(f'{path}已存在。即将覆盖下载')
                else:
                    return True
            if not '.png' in path:
                path += '.png'

        if type(s) in [selenium.webdriver.remote.webelement.WebElement]:
            y = int(s.location['y'])
            if not yoffset == None:
                y += yoffset
            if moveto:
                self.scroll(h=y)
                sleep(ajax_wait_time)
                # self.scroll(y+self.getscrolltop())
            else:
                #     强制重新渲染
                self.scroll(h=currentheight)
            if 100 + s.size['height'] > self.get_window_size()[1]:
                self.set_window_size(self.get_window_size()[0],
                                     self.get_window_size()[1] + 100 + s.size['height'])
            file_operate('wb', path, s.screenshot_as_png)
            return path

        if type(s) in [str]:
            return Edge.elementshot(self, self.element(s), path=path)

    # 遇到异常（元素为空时），终止并检查当前页面截图
    def errorscr(self, t=None):
        import pyperclip

        if self.is_js():
            # path=strictpath(self.downloadpath+('/error.png'))
            # self.send_rpc(f='screenshot',p={'path':path})
            return
        else:
            path = cachepath('error.png')
            self.driver.get_screenshot_as_file(path)
            look(path)
            pyperclip.copy(self.driver.current_url)
            Exit(f'{self.url()}   {context(4)}  t={t}')

    error_screen = errscreen = errorscreen = errscr = \
        errorscr

    # 查看当前页面
    @manage_args(a=['xpath'])
    def look(self, a=None):
        if self.is_js():
            return
        path = f'D:/Kaleidoscope/cache/current.png'
        if not a == None:
            self.elementshot(a, path)
            look(path)
            return
        deletedirandfile(path)
        self.driver.get_screenshot_as_file(path)
        look(path)

    # 关闭标签页并跳转到上一个标签页
    def close(self):
        self.driver.close()
        try:
            self.switchto(-1)
        except Exception as e:
            warn(e)

    @has_value()
    @manage_args()
    def title(self, b=None, **leak):
        if self.is_js():
            ret = self.send_rpc(f='title')
            while not ret and not ret == 'None':
                ret = self.send_rpc(f='title')
                sleep(1)
                continue
            return ret
        if self.url() == '':
            Exit('尚未打开任何网页')
        try:
            ret = self.execute_js('return document.title')
            if not ret in ['', None]:
                return standarlizedFileName(ret)
        except Exception as e:
            pass
        try:
            ret = self.driver.title
            if not ret in ['', None]:
                return standarlizedFileName(ret)
        except Exception as e:
            pass
        try:
            ret = self.element(xpath='//title/text()', strict=False,
                               **exclude(b, ['xpath', 'strict']))
            if not ret in ['', None]:
                return standarlizedFileName(ret)
        except Exception as e:
            pass
        try:
            ret = self.execute_js(
                r"return document.getElementsByTagName('title')[0].text")
            if not ret in ['', None]:
                return standarlizedFileName(ret)
        except Exception as e:
            pass
        try:
            ret = self.element(xpath='/html/head/title/text()', strict=False,
                               **exclude(b, ['xpath', 'strict']))
            if not ret in ['', None]:
                return standarlizedFileName(ret)
        except Exception as e:
            pass

    def quit(self):
        if self.is_js():
            return
        if not self.driver == None:
            self.driver.quit()

    @manage_args(path=['target'])
    def screenshot(self, path=None,
                   target_root=None, target_name=None,
                   overwrite=True, pre_wait=True):
        """
        截图并保存。不下滚。
        @return:
        """
        if pre_wait:
            sleep(self.getscrollheight() / 1000 / download_speed)
        if path == None:
            path = cachepath('browser_screenshot.png')
        if overwrite or not isfile(path, exist=True):
            # self.save_var({'pic_download_path': path})
            # _data = self.execute_script(jspath('shot_single_pic'))
            # file_operate('wb', path, _data)
            # 不知道上面写的是什么
            self.driver.get_screenshot_as_file(path)

    get_screenshot = screenshot
    screen_shot = screenshot

    def get_width(self):
        return self.get_window_size()[0]

    def get_height(self):
        return self.get_window_size()[1]


page = \
    Browser


class Edge(Browser):
    @manage_args(driver=['page'], mine=['root'], method=['_type'])
    def __init__(self,
                 driver=None, download_root=None,
                 mine=None, silent=None, method=None,
                 b=None, **leak):
        super().__init__(_type='chrome', **b)


class Chrome(Browser):

    @manage_args(driver=['page'], mine=['root'], method=['_type'])
    def __init__(self,
                 driver=None, download_root=None,
                 mine=None, silent=None, method=None,
                 b=None, **leak):
        super().__init__(_type='chrome', **(exclude(b, '_type')))

    def register(self):
        """
        记录当前在使用mine chrome的context
        @return:
        """
        if get_env_var('debug'):
            return True
        if self.mine == True:
            f = txt(browserpath('ischromeusing.txt'))
            if not f.l == []:
                warn('Chrome 似乎已经在使用了')
                Exit()
            if get_env_var('debug'):
                f.l = context(4)
            else:
                f.l = [
                    '似乎没有关闭上一个带用户缓存的浏览器页面。请确保程序不在用户使用浏览器的情况下使用用户缓存，并且带用户缓存的浏览器同一时间只能存在一个。']
            f.l.append(nowstr())
            f.save()
        return True

    def quit(self):
        if self == None:
            return
        Edge.quit(self)
        #         更改ischromeusing
        f = txt(browser_path('/ischromeusing.txt'))
        if self.mine:
            if not f.l == []:
                f.l = []
        f.save()


@manage_args(pic=['path'])
def click(x=10, y=10, button='left', silent=True,
          interval=0.2, confidence=1, limit=0, gap=0.05,
          grayscale=True, xoffset=0, yoffset=0,
          strict=False, moveto=True, pos=None,
          pic=None,
          moveback=True,
          b=None, **leak,
          ):
    """
    点击屏幕或者识别屏幕内容
    @param x:x为坐标
    @param y:
    @param pos: x,y元组
    @param button: 左键还是右键
    @param silent:
    @param interval:点击完后的等待时间
    @param confidence: 图片识别精确度
    @param limit:图片识别精确度下限
    @param gap: 图片识别精确度下降间隔
    @param grayscale: 是否使用灰度识别图片
    @param xoffset: 图片识别结果的偏移量
    @param yoffset:
    @param strict: 是否严格模式，严格模式下，如果定位不存在，则会返回
    @param moveto:是否移动到
    @param pic:图片路径
    @param moveback:是否移动回来
    @return:是否成功
    """
    import pyautogui
    originallocation = pyautogui.position()
    # 点击图片
    if not pic == None and isfile(path=picpath(pic), exist=True):
        path = picpath(pic)
        # 路径中文名问题
        target = cachepath('locate_screen.png')
        deletedirandfile(target)
        copyfile(path, target, overwrite=True)
        path = target
        pos = locate_on_screen(**b)
        if pos:
            x, y = list(pos)
            click(x + xoffset, y + yoffset)
            if not silent:
                log(x + xoffset, y + yoffset)
            if moveback:
                pyautogui.moveTo(originallocation)
                return True
        #     没找到
        if strict:
            Open(path)
            Exit(path)
        else:
            return False

    if not pos == None:
        (x, y) = pos
    # 点击坐标
    try:
        # 默认xy坐标是在windows UI缩放比例为125%下的，在screenscale.txt中修改当前的缩放比例
        defaultmode = 'center'
        defaultuiscale = 125
        defaultxscale = 1920
        defaultyscale = 1080
        global uiscale, xsize, ysize
        X, Y = x - defaultxscale / 2, y - defaultyscale / 2
        X, Y = int(X / defaultxscale * xsize / defaultuiscale * uiscale), int(
            Y / defaultyscale * ysize / defaultuiscale * uiscale)
        x, y = X + xsize / 2, Y + ysize / 2
        if x == 0:
            x = 1
        if y == 0:
            y = 1
        if moveto:
            pyautogui.click(x, y, button=button)
            delog(f'尝试了点击屏幕 {int(x)}, {int(y)}')
        sleep(interval)
        if not silent:
            print(f'{x}   {y}')
    except Exception as e:
        if type(e) in [pyautogui.FailSafeException]:
            Exit(f'可能是选取点击的坐标过于极端。 x:{x}    y:{y}')
        warn(e)
        sys.exit(-1)


@manage_args(image=['path', 'pic'])
def locate_on_screen(image, confidence=0.8, grayscale=True, limit=0, gap=0.05, xoffset=0, yoffset=0,
                     strict=False, **leak):
    """
    在屏幕上定位图片
    @param image:
    @param confidence:
    @param grayscale:
    @param limit:
    @param gap:
    @param xoffset:
    @param yoffset:
    @param strict:
    @return:  二元组
    """
    import pyautogui
    if not '.png' in image:
        image += '.png'
    path = picpath(image)
    # 路径中文名问题
    target = cachepath('locate_screen.png')
    deletedirandfile(target)
    copyfile(path, target, overwrite=True)
    path = target
    if isfile(path):
        while confidence > limit:
            pos = pyautogui.locateOnScreen(
                path, confidence=confidence, grayscale=grayscale)
            confidence -= gap
            if pos == None:
                continue
            else:
                p = pyautogui.center(pos)
                return v(p.x, p.y)
    #     没找到
    if strict:
        Open(path)
        Exit(path)
    else:
        delog(f'未在屏幕上找到 {path}')
        return False


# 右击屏幕
def rclick(x, y):
    click(x, y, button='cutright')


def setscrolltop(l):
    (page, x) = l
    page.execute_script(f'document.documentElement.scrollTop={x}')


@manage_args(page=['driver'], path=['target'])
@consume
def page_download(url=None, path=None, t=999, silent=True, depth=0,
                  auto=None, redownload=None,
                  overwrite=False, page=None,
                  download_root=None,
                  b=None, **leak,
                  ):
    """
    如果是新开启浏览器实例，下载到固定路径然后移动到目标路径
    如果已有浏览器实例传入，下载到Downloads 路径（需要浏览器配置），然后移动
    浏览器自动重命名 '~' 为 '_'
    @param url:
    @param path: 可以自动识别后缀名。
    @param t:下载和下载后浏览器自动安全检查的时间
    @param silent:
    @param depth:
    @param auto:是否是打开页面即自动下载
    @param overwrite: 覆盖下载或是覆盖移动
    @param redownload: 一定会重新下载。可能覆盖也可能不覆盖
    @param page: 用于下载的浏览器
    @param driver:
    @param download_root: 下载的第一次位置
    @return:True 下载了并且下载成功；False 下载了但是下载失败；字符串 返回检测到的以前的错误命名
    """
    # 参数处理
    # region
    check_type(url, str)
    used_arg(t, strict=True)
    target_path = original_path = path = standarlizedPath(path, strict=True)
    if not used(download_root):
        download_root = default_page_download_path
    if not used(page):
        global default_download_page
        if not 'default_download_page' in globals():
            default_download_page = Chrome(download_root=default_page_download_path,
                                           silent=False, family=f'page_download',
                                           )
        page = default_download_page
    if depth > 5:
        warn(f'多次下载失败后停止，请手动尝试：\n{url}')
        return False
    # 是否多下
    # region
    if not redownload:
        if exists(target_path) and not size(target_path) == 0:
            if not overwrite:
                log(f'{target_path} 已存在，将不下载')
                return True
            else:
                move(target_path, cachepath(f'trashbin/{now()}'))
                warn(f'因为 overwrite， page_download 在下载前先移动删除原来存在的文件。 {path}')
    # endregion
    target_root, target_name = \
        parentpath(target_path), filename(target_path)
    download_name = str(Now().timestamp()).replace('.', '-')

    # 函数定义
    # region
    def _check_and_finish() -> bool:
        if auto:
            lis1 = listfile(download_root)
        download_success = monitor_file_size(path=f'{download_root}/{download_name}.crdownload',
                                             max_time=t, silent=True, **exclude(b, [
                'silent', 'path', 'max_time', 't'
            ]))
        if 'default_download_page' in globals() and not page in [None, default_download_page]:
            page.switchto(previous_page)
        sleep(1)  # ？

        delog(f'正在检测是否下载并移动到了：\n\t\t\t路径 {target_root}  \n\t\t\t文件名{target_name}')

        def warn_and_download_again(s=None, d=None):
            deletedirandfile(d)
            warn(s, traceback=False)
            return download(**(exclude(b, ['t', 'depth'])), t=t * 4, depth=depth + 1)

        for f_name in listfile(download_root):
            f_name = filename(f_name)
            if download_name in f_name and '.crdownload' in f_name:
                return warn_and_download_again(
                    s=f'{Int(t)} s后仍在下载。没有缓存文件存留（自动删除）  {url}',
                    d=f_name)
            if download_name == f_name or '.' in f_name and download_name == rmtail(f_name, '.'):
                if '.htm' in f_name:
                    return warn_and_download_again('下载了  .htm？？？',
                                                   d=f_name)
                _move_target_name = target_name
                if not '.' in target_name and '.' in f_name:  # 传参没有传扩展名但是浏览器下载自动加了
                    _move_target_name = target_name + \
                                        extension(f_name, full=False, withdot=True)
                move(download_root + '/' + f_name,
                     target_root + '/' + _move_target_name,
                     autorename=redownload,
                     overwrite=overwrite)
                return True
        delog(f'depth={depth}')
        warn(f'{t}s后下载失败。没有检测到缓存文件  请手动尝试 {url}', plain_text=url)
        return False

    # endregion
    # 预处理
    # region
    try:
        # 必须 get/open 一次以解决传入的url 会重定向的问题
        if 'default_download_page' in globals() and not page == default_download_page:
            page.open(url)
            previous_page = page.driver.current_window_handle
        else:
            page.get(url)
        if tellstringsame(page.title(depth=0), '403 forbidden'):
            warn(f'这个url已经被服务器关闭  403  ：{url}')
            return False
    except Exception as e:
        # 仍然可以强制下载的报错
        if type(e) in [ZeroDivisionError, ]:
            pass
        elif type(e) in [selenium.common.exceptions.WebDriverException]:
            # 需要重启pagedownload的下载报错
            page.quit()
            return page_download(depth=depth + 1, **exclude(b, 'depth'))
        else:
            Exit(e, type(e))
    # endregion

    # 下载
    # region
    # 如果这个链接打开就能自动下载
    if auto:
        return _check_and_finish()

    sleep(1)  # 等待内容加载
    i = 0
    while i < 10:
        try:
            page.execute_script(js=f"const a1=document.createElement('a');\
            a1.href=window.location.href;\
            a1.download='{download_name}';\
            a1.click();")
            # download_root 必须存在，否则会跳出为另存为
            # delog(f'page_download 正在下载 {url} 到 {download_root}{downloadname}')
            break
        except Exception as e:
            warn('下载重试中...')
            warn(e)
            warn(type(e))
            i += 1
    # endregion
    # 检查
    # region
    download_name = head(s=get_full_filename(download_root, download_name, recursive=True,
                                             loop=int(t / 2), silent=True), mark='.crdownload',
                         strict=False)
    if not download_name:
        warn(f'js执行下载后查找失败，没有检测到下载文件\
         {Str(download_root) + Str(download_name)}\n 下载地址： {url}')
    return _check_and_finish()
    # endregion


download = \
    page_download


def scrshot(l):
    (element, path) = l
    path = standarlizedPath(path)
    if isfile(path):
        warn(f'{path}已存在。即将覆盖下载')
    path = path.strip('.png') + '.png'
    file_operate('wb', path, element.screenshot_as_png)


# endregion

# AI Agent

def QW(s=None, uid=0):
    import random
    from http import HTTPStatus
    import dashscope
    dashscope.api_key = "sk-6ed66e11e21641d88b224a6b7b3814b0"
    response = dashscope.Generation.call(
        model=dashscope.Generation.Models.qwen_max,
        prompt=s if s else txt(recordpath(f'AI/input/{uid}.txt')).content()
    )
    if response.status_code == HTTPStatus.OK:
        ret = (response.output['text'])  # The output text
        # print(response.usage)  # The usage information
    else:
        warn(response.code, response.message)
    return ret


# 初始化2
# region
user = get_env_var('UserNAME', origin=True)
set_env_var(d={'debug': sys.gettrace() is not None})
set_env_var({'strict': None})
download_speed = getsettings('download_speed')  # 下载网速
if useDisk(d='d') == 'HerMAJESTY':
    Debug()
consoletxt = Json('D:/Kaleidoscope/console.txt')
consolerunning = txt(projectpath('ConsoleShow.txt'))
download_list = Csv(projectpath('cache/download_list.csv'))
try:
    uiscale = int(txt(projectpath('ScreenScale.txt')).l[0])
    xsize = int(txt(projectpath('ScreenScale.txt')).l[1])
    ysize = int(txt(projectpath('ScreenScale.txt')).l[2])
except Exception as e:
    warn('ScreenScale未配置，使用默认参数。')
    uiscale = 125
    xsize = 1920
    ysize = 1080


def RuntimeRoot():
    ret = standarlizedPath(__file__)
    ret = ret[:ret.rfind('/')] + '/'
    return ret


tip('MyUtils already loaded')
# endregion
