import requests
import json
import time

class Adao:
    post_id = ''
    adao_url = 'https://adnmb3.com'
    trpg_url = 'http://127.0.0.1:12345'
    cookie = {} 
    now_page = 0
    now_reply_data = []
    reply_data = []
    reply_count = 0
    story_scan = {
        'story_start': 0,
        'story_node': 0,
        'story_roll': 0,
        'story_end': 0
    }

    run_status = 0

    def __init__(self, post_id):
        fo = open('store_status.json', 'r')
        store_status = fo.read()
        fo.close()
        arr = json.loads(store_status)
        self.post_id = post_id
        self.run_status = arr['run_status']
        self.cookie = arr['cookie']

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
            # 记录页数
            self.now_page += 1
            res = self.get_reply(show_id, self.now_page)
            self.reply_count = res['replyCount']
            if len(res['replys']) < 20:
                self.now_page -= 1
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

    '''
        [store_start]故事开始
        [store_end]故事结束
        [store_node]故事节点
        [store_roll]roll点或选择
    '''
    def check_first_point(self, check_index, check_word, arr):
        i = check_index + 1
        while i < len(arr):
            if (arr[i]['content'].find(check_word) != -1):
                return i
            i += 1
        return -1

    def check_last_point(self, check_index, check_word, arr):
        check_index = self.check_first_point(check_index, check_word, arr)
        swap = check_index
        while check_index != -1:
            swap = check_index
            check_index = self.check_first_point(check_index, check_word, arr)
        return swap
    
    def set_story_status(self):
        arr = {}
        arr['run_status'] = self.run_status
        arr['cookie'] = self.cookie
        store_status = json.dumps(arr)
        fo = open('store_status.json', 'w')
        fo.write(store_status)
        fo.close

    # run_status = 0
    def run_roll(self):
        if self.run_status != 0:
            return
        data = self.reply_data+self.now_reply_data
        # 获取roll点
        index = self.story_scan['story_roll']
        # 操作 获取roll值并请求
        if index != -1 :
            select = self.get_roll_num(data[index]['content'])
            self.run_story_select(select)
            self.run_status = 1
        return
    
    # run_status = 1
    def run_check_end(self):
        if self.run_status != 1:
            return
        # 确认故事是否到end
        end = self.get_story_node()['Id']
        if end == 1:
            self.run_status = 2
            self.post_reply(self.post_id, '[story_end]')
        else:
            self.run_status = 0
            res = self.get_story_node()
            self.post_reply(self.post_id, '[story_node]'+res['Val'])

        return

    # run_status = 2
    def run_story_reset(self):
        # if self.run_status != 2:
        #     return
        self.run_status = 0
        self.get_json(self.trpg_url+'/run/return?id=0')
        res = self.get_story_node()
        res = self.post_reply(self.post_id, '[story_start]'+res['Val'])
        print(res)
        return

    def story_point_check(self):
        arr = self.reply_data + self.now_reply_data
        # check [story_start]
        self.story_scan['story_start'] = self.check_last_point(self.story_scan['story_start'] - 1, '[story_start]', arr)
        # check [story_node]
        self.story_scan['story_node'] = self.check_last_point(self.story_scan['story_start'], '[story_node]', arr)
        if self.story_scan['story_node'] == -1:
            self.story_scan['story_node'] = self.story_scan['story_start']
        # check [story_roll]
        self.story_scan['story_roll'] = self.check_first_point(self.story_scan['story_node'], '[story_roll]', arr)
        # check [story_end]
        self.story_scan['story_end'] = self.check_first_point(self.story_scan['story_start'], '[story_end]', arr)
        return

    # 更新故事节点
    def run_story_renew(self):
        # 取新内容
        self.get_reply_all(self.post_id)
        # 获取故事节点
        self.story_point_check()
        return

    def get_roll_num(self, content):
        content
        res = {
            0: 2,
            2: 3,
            3: 1
        }
        return res.get(self.get_story_node()['Id'])

    def get_story_status(self):
        res = self.get_json(self.trpg_url+'/run/status_list')
        return res['data']
    
    def get_story_node(self):
        res = self.get_json(self.trpg_url+'/run/now_node_get')
        return res['data']
    
    def run_story_select(self, select):
        res = self.get_json(self.trpg_url+'/run/step?id='+str(select))
        return res['data']

    def run_do(self):
        self.run_story_renew()
        self.run_roll()
        self.run_check_end()
        # self.run_story_reset()
        self.set_story_status()

adao = Adao('30275381')
adao.run_story_reset()
time.sleep(5)
while True:
    adao.run_do()
    print('\nstory_scan:', adao.story_scan)
    time.sleep(5)
    if adao.run_status == 2:
        break
