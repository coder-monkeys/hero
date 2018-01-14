import urllib.request
import urllib.parse
import _thread

class AI:

    def __init__(self, question, answer):
        self.question = question
        self.question_type = True
        self.answer = answer
        self.stat = []
        self.count = 0

    def ai_search(self):
        print("-" * 72)
        print("{}\n".format(self.question)) # 输出题目
        self.question = self.format_question(self.question)
        for i in range(len(self.answer)):
            self.stat.append(0)
        _thread.start_new_thread(self.get_count_zhidao, ("https://iask.sina.com.cn/search?searchWord=" + urllib.parse.quote(self.question),))
        _thread.start_new_thread(self.get_count_zhidao, ("http://wenwen.sogou.com/s/?w=" + urllib.parse.quote(self.question),))
        _thread.start_new_thread(self.get_count_zhidao, ("https://wenda.so.com/search/?q=" + urllib.parse.quote(self.question),))
        _thread.start_new_thread(self.get_count_zhidao, ("https://zhidao.baidu.com/search?word=" + urllib.parse.quote(self.question, encoding="gbk"),))
        while True:
            if self.count == 4:
                break
        self.count = 0
        for i in range(len(self.answer)):
            self.count += self.stat[i]  # 计算总数如果为零则发起新搜索
        if self.count == 0:
            print("没有找到答案，启用百度搜索...\n")
            http = "https://www.baidu.com/s?wd=" + urllib.parse.quote(self.question)
            for i in range(len(self.answer)):
                _thread.start_new_thread(self.get_count_baidu, (i, http + urllib.parse.quote("+") + urllib.parse.quote(self.answer[i].replace("《", "").replace("》", "")),))
            while True:
                if self.count == len(self.answer):
                    break
        self.print_answer()

    def get_count_zhidao(self, url):
        headers = ("User-Agent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        try:
            data = opener.open(url).read()
        except:
            print("error: connection reset\n")
            data = str("error")
        else:
            if "zhidao.baidu.com" in url:
                try:
                    data = str(data.decode("gbk").encode("utf-8"), "utf-8")
                except:
                    print("error: unicode decode error\n")
                    data = str("error")
            else:
                data = str(data, "utf-8")
        for i in range(len(self.answer)):
            self.stat[i] += data.count(self.answer[i].replace("《", "").replace("》", ""))
        self.count += 1

    def get_count_baidu(self, sub, url):
        headers = ("User-Agent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        try:
            data = str(opener.open(url).read(), "utf-8")
        except:
            print("error: connection reset\n")
        else:
            self.stat[sub] += int(data.split("百度为您找到相关结果约")[1].split("个")[0].replace(",", ""))
        self.count += 1

    def format_question(self, question):
        # 去除题目编号
        if str.isdigit(question[1:2]):
            question = question[3:]
        else:
            question = question[2:]
        # 去除特殊字符
        for v in ["“", "”", "\"", "？", "?"]:
            question = question.replace(v, "")
        # 排除否定式提问
        for v in ["不是", "不会", "不用", "不宜", "不包括", "不属于", "不正确", "没有", "是错"]:
            if v in question:
                if "不" in v:
                    v = "不"
                question = question.replace(v, "")
                self.question_type = False
        return question

    def print_answer(self):
        self.count = 0
        for i in range(len(self.answer)):
            self.count += self.stat[i] # 计算总数避免除数依然为零
        for i in range(len(self.answer)): # 输出每个答案的权重
            if self.answer[i] in self.question: # 如果问题中包含答案则调整权重
                self.stat[i] = int(self.stat[i] / 3)
            if self.count == 0:
                print("{} (0)".format(self.answer[i]))
            else:
                print("{} ({}%)".format(self.answer[i], int(self.stat[i] / self.count * 100)))
        print("-" * 72)
        if self.count == 0: # 输出建议回答
            print("没有找到答案，蒙一个吧")
        else:
            if self.question_type:
                print("肯定回答：{}".format(self.answer[self.stat.index(max(self.stat))]))
            else:
                print("否定回答：{}".format(self.answer[self.stat.index(min(self.stat))]))
        print("-" * 72)

if __name__ == "__main__":
    pass
