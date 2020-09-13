import time
import requests
import json
from lxml import etree

class Adao:
    adao_url = 'https://adnmb3.com'
    cookie = {'_ga':'GA1.2.779298925.1599140706',
          'PHPSESSID':'6cv9engtka2ucfpur7q3hkh1o3',
          'Hm_lvt_e6d1419842221a8d451e9a89cabbcba6':'1599140706,1599532154',
          'memberUserspapapa':'%153k%5D%9Di%A5%2C6%3Cp%A27%FA%B2%98%08%B2%94%F8%23%C8%7D%DD%D5%19%B9%D5qTS%D0%F3n+%AA%A8%9FS1%0E%DA%2B%AF%8F%EC%02%FDW%27%1A%8E%CA%84%29%8C%16%84%AD%28%14%FF%24O',
          '_gid':'GA1.2.703042913.1599798580',
          'userhash':'%8B%E8%CA%D0%CB%89%00%CB%91%FB%07%EA%06%B7%B5%F3%C2+4%12%00%DD%C06',
          'Hm_lpvt_e6d1419842221a8d451e9a89cabbcba6':'1599802975'}

    def get_json(self, url):
        res = requests.get(url)
        content = res.content
        return json.loads(content)

    def get_plate(self):
        plate_url = 'https://adnmb3.com/Api/getForumList'
        adao_plate = self.get_json(plate_url)
        return adao_plate

    def get_show(self, plate_id):
        show_url = 'https://adnmb3.com/Api/showf?'+'id='+plate_id+'&page=0'
        post_head_data = self.get_json(show_url)
        return post_head_data

    def get_reply(self, show_id):
        reply_url = 'https://adnmb3.com/Api/thread?'+'id='+show_id+'&page=0'
        reply_data = self.get_json(reply_url)
        return reply_data

    def post_reply(self, resto, content):
        adao_reply_thread = self.adao_url + '/Home/Forum/doReplyThread.html'
        reply_data = {'resto':resto, 'content':content}
        result = requests.post(adao_reply_thread, data = reply_data, cookies = self.cookie).text
        return result

    def post_post(self, plate, content):
        adao_create_thread = adao_url + '/Home/Forum/doPostThread.html'
        reply_data = {'plate':plate, 'content':content}
        result = requests.post(adao_create_thread, data = reply_data, cookies = self.cookie).text
        return result

    def get_decide_list(self):
        fo = open('decide_list.json', 'r')
        decide_list = fo.read()
        fo.close()
        return decide_list

    def set_decide_node(self, decide_node, decide_content, decide_type, decide_man, date):
        decide_node = {'decide_node':decide_node,
                       'decide_content':decide_content,
                       'decide_type':decide_type,
                       'decide_man':decide_man,
                       'date':date}
        return decide_node

    def append_decide_node(self, decide_list, decide_node):
        if decide_list == '':
            decide_list = []
        else:
            decide_list = json.loads(decide_list)
        decide_list.append(decide_node)
        decide_list = json.dumps(decide_list)
        return decide_list

    def set_decide_list(self, decide_list):
        fo = open('decide_list.json', 'w')
        fo.write(decide_list)
        fo.close()

    def get_store_status(self):
        fo = open('store_status.json', 'r')
        store_status = fo.read()
        fo.close()
        return store_status

    def set_store_status(self, decide_node, decide_status, decide_id, decide_man):
        store_status = {'decide_node':decide_node,
                        'decide_status':decide_status,
                        'decide_id':decide_id,
                        'decide_man':decide_man}
        store_status = json.dumps(store_status)
        fo = open('store_status.json', 'w')
        fo.write(store_status)
        fo.close

text = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>跳转提示</title>
<style type="text/css">
*{ padding: 0; margin: 0; }
body{ background: #fff; font-family: '微软雅黑'; color: #333; font-size: 16px; }
.system-message{ padding: 24px 48px; }
.system-message h1{ font-size: 100px; font-weight: normal; line-height: 120px; margin-bottom: 12px; }
.system-message .jump{ padding-top: 10px}
.system-message .jump a{ color: #333;}
.system-message .success,.system-message .error{ line-height: 1.8em; font-size: 36px }
.system-message .detail{ font-size: 12px; line-height: 20px; margin-top: 12px; display:none}
</style>
<meta name="__hash__" content="a55f18c7c0b239ec51c46861a630fc41_77b6482dbc8de0ba8444e01cee125b40" /></head>
<body>
<div class="system-message">
<h1>:)</h1>
<p class="success">回复成功</p>
<p class="detail"></p>
<p class="jump">
页面自动 <a id="href" href="">跳转</a> 等待时间： <b id="wait">1</b>
</p>
</div>
<script type="text/javascript">
(function(){
var wait = document.getElementById('wait'),href = document.getElementById('href').href;
var interval = setInterval(function(){
	var time = --wait.innerHTML;
	if(time <= 0) {
		location.href = href;
		clearInterval(interval);
	};
}, 1000);
})();
</script>
</body>
</html>
'''

# html = etree.HTML(text)
# result=etree.tostring(html,encoding='utf-8')
# print(result.decode('utf-8'))
# adao = Adao()
# reply_do = adao.post_reply('30275381', 'roll检测测试')
# print(reply_do)
# adao = Adao()
# decide_node = adao.set_decide_node(1, 'important', 123, 123)
# decide_list = adao.get_decide_list()
# print(decide_list, decide_node)
# decide_list = adao.append_decide_node(decide_list, decide_node)
# adao.set_decide_list(decide_list)
# print(decide_list)

post_id = '0'
i = 0
while i < 1:
    space = '  '
    adao = Adao()
    post_data = adao.get_reply('30275381')
    print(post_data['id'], post_data['content'])
    for reply in post_data['replys']:
        if reply['id'] != 9999999:
            print(space+reply['id'], reply['content'])
            if reply['content'].find('roll') != -1 and post_id != reply['id']:
                post_id = reply['id']
                print('find it', reply['id'])

                decide_node = adao.set_decide_node(reply['id'], {'node':1, 'decide':1},'important', reply['userid'], reply['now'])
                decide_list = adao.get_decide_list()
                decide_list = adao.append_decide_node(decide_list, decide_node)
                adao.set_decide_list(decide_list)
                adao.set_store_status(1, 1, reply['id'], reply['userid'])

    decide_list = adao.get_decide_list()
    store_status = adao.get_store_status()
    print(decide_list, store_status)
    # adao.post_reply('30275381', '当前store_status：'+store_status)
    adao.post_reply('30275381', '当前decide_list：'+decide_list)
    time.sleep(1)
    i = i + 1
