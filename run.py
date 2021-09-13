import requests
import json


class Adao:
    adao_url = 'https://adnmb3.com'
    cookie = {
        'userhash': '%8B%E8%CA%D0%CB%89%00%CB%91%FB%07%EA%06%B7%B5%F3%C2+4%12%00%DD%C06'
    }
    page = 0
    reply_data = []
    now_reply_data = []
    last_node = ''
    last_node_index = 0

    # 请求JsonRes
    def get_json(self, url):
        res = requests.get(url)
        content = res.content
        return json.loads(content)

    # 请求a岛接口
    def get_reply(self, show_id, page=0):
        reply_url = self.adao_url+'/Api/thread?' + \
            'id='+show_id+'&page='+str(page)
        reply_data = self.get_json(reply_url)
        return reply_data

    def get_reply_all(self, show_id):
        while True:
            self.page += 1
            res = self.get_reply(show_id, self.page)
            if len(res['replys']) < 20:
                self.now_reply_data = []
                for reply in res['replys']:
                    if reply['id'] != 9999999:
                        self.now_reply_data.append(
                            {"id": reply['id'], "content": reply['content']})
                break
            for reply in res['replys']:
                if reply['id'] != 9999999:
                    self.reply_data.append(
                        {"id": reply['id'], "content": reply['content']})

    # 回帖
    def post_reply(self, resto, content):
        adao_reply_thread = self.adao_url + '/Home/Forum/doReplyThread.html'
        reply_data = {'resto': resto, 'content': content}
        result = requests.post(
            adao_reply_thread, data=reply_data, cookies=self.cookie).text
        return result

    def check_point(self, check_word, arr):
        i = self.last_node_index + 1
        while i < len(arr):
            if (arr[i]['content'].find(check_word) != -1):
                self.last_node_index = i
                return i
            i += 1
        return -1
    def set_store_status(self):
        arr = {}
        arr['last_node'] = self.last_node
        arr['last_node_index'] = self.last_node_index 
        # arr['reply_data'] = self.reply_data
        # arr['now_reply_data'] = self.now_reply_data
        store_status = json.dumps(arr)
        fo = open('store_status.json', 'w')
        fo.write(store_status)
        fo.close


adao = Adao()
adao.get_reply_all('30275381')
adao.set_store_status()