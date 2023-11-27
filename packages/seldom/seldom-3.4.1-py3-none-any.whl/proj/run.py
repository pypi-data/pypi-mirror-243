import webbrowser
from loader import loader2


def test_open_url():
    # 调用 base_url 钩子函数
    # 调用 浏览器 访问 baidu_url
    url = loader2("baidu_url")
    print("url-->", url)
    # webbrowser.open_new(url)


if __name__ == '__main__':
    test_open_url()
