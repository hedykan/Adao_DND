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

    def get_reply(self, show_id, page = '0'):
        reply_url = 'https://adnmb3.com/Api/thread?'+'id='+show_id+'&page='+page
        reply_data = self.get_json(reply_url)
        return reply_data

    def get_reply_all(self, show_id):
        post_data = self.get_reply(show_id)
        post_data_arr = post_data['replys']
        count = int(post_data['replyCount'])
        page =  count // 20
        i = 0
        while i < page:
            post_data = self.get_reply(show_id, str(i + 2))
            post_data_arr.extend(post_data['replys'])
            i = i + 1
        return post_data_arr

    def get_reply_end(self, show_id, end_page):
        post_data = self.get_reply(show_id, str(end_page))
        post_data_arr = post_data['replys']
        count = int(post_data['replyCount'])
        print(end_page)
        page = count // 20
        while end_page < (page + 1):
            post_data = self.get_reply(show_id, str(end_page + 2))
            post_data_arr.extend(post_data['replys'])
            end_page = end_page + 1
        print(end_page)
        return post_data_arr

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

    def set_store_status_arr(self, store_id, store_node, store_speaker, store_stop_id, store_stop_floor, decide_id, decide_man):
        store_status = {'store_id':store_id,
                        'store_node':store_node,
                        'store_speaker':store_speaker,
                        'store_stop_id':store_stop_id,
                        'store_stop_floor':store_stop_floor,
                        'decide_id':decide_id,
                        'decide_man':decide_man}
        return store_status

    def set_store_status(self, store_status_arr):
        store_status = json.dumps(store_status_arr)
        fo = open('store_status.json', 'w')
        fo.write(store_status)
        fo.close

    def set_store_tree_node(self, store_node, parent_node, child_node, store_content):
        store_node = {'store_node':store_node,
                      'parent_node':parent_node,
                      'child_node':child_node,
                      'store_content':store_content}
        return store_node

    def get_store_tree(self):
        fo = open('store_tree.json', 'r')
        store_tree = fo.read()
        fo.close()
        return store_tree

    def roll_set(self, roll_id):
        roll_id = int(roll_id) % 10
        if roll_id >= 0 and roll_id <= 3:
            return 0
        elif roll_id >= 4 and roll_id <= 7:
            return 1
        elif roll_id >= 8 and roll_id <= 9:
            return 2

    def store_node_create(self, store_content):
        store_status_arr = json.loads(self.get_store_status())
        print(store_content)
        self.post_reply(store_status_arr['store_id'], store_content)
        time.sleep(10)
        return

    def store_start(self):
        store_tree_arr = json.loads(self.get_store_tree())
        store_status_arr = json.loads(self.get_store_status())
        if store_tree_arr[store_status_arr['store_node']]['end_status'] == 1:
            store_content = '[store_start]\n'+store_tree_arr[0]['store_content']
            # print(store_content)
            # self.store_node_create(store_content)
            # 查找故事开头
            post_data = self.get_reply_all(store_status_arr['store_id'])
            print(post_data)
            return
            for reply in post_data:
                if reply['id'] != 9999999:
                    if (reply['content'].find('[store_start]') != -1) and (int(reply['id']) > int(store_status_arr['store_stop_floor'])) and (reply['userid'] == store_status_arr['store_speaker']):
                        print(reply)
                        store_status_arr = json.loads(adao.get_store_status())
                        store_status_arr['store_stop_id'] = reply['id']
                        store_status_arr['store_node'] = 0
                        self.set_store_status(store_status_arr)
                        break
        return

    def store_roll(self):
        store_tree_arr = json.loads(self.get_store_tree())
        store_status_arr = json.loads(self.get_store_status())
        post_data = self.get_reply_all(store_status_arr['store_id'])
        for reply in post_data:
            if reply['id'] != 9999999:
                # 找到roll并且id>记录store_stop_floor
                if reply['content'].find('r') != -1 and int(reply['id']) > int(store_status_arr['store_stop_floor']) and reply['userid'] != store_status_arr['store_speaker']:
                    post_id = reply['id']
                    store_node = store_tree_arr[store_status_arr['store_node']]['child_node'][str(self.roll_set(reply['id']))]
                    print('find it', reply['id'])

                    store_stop_floor = reply['id']
                    decide_node = self.set_decide_node(reply['id'], {'node':store_node, 'decide':store_node},'important', reply['userid'], reply['now'])
                    decide_list = self.get_decide_list()
                    decide_list = self.append_decide_node(decide_list, decide_node)
                    self.set_decide_list(decide_list)
                    store_status_arr = self.set_store_status_arr(store_status_arr['store_id'], store_node, store_status_arr['store_speaker'], store_stop_floor, reply['id'], reply['userid'])
                    self.set_store_status(store_status_arr)

                    # 生成故事节点
                    store_status_arr = json.loads(self.get_store_status())
                    store_content = '[store_node]\n'+reply['userid']+' 选择了'+str(store_node)+'选项\n'
                    store_content = store_content+store_tree_arr[store_status_arr['store_node']]['store_content'];
                    self.store_node_create(store_content)

                    # 找到故事节点, 并更新故事停止楼层
                    post_data = self.get_reply_all(store_status_arr['store_id'])
                    for reply in post_data:
                        if reply['id'] != 9999999:
                            if reply['content'].find('[store_node]') != -1 and int(reply['id']) > int(store_status_arr['store_stop_floor']) and reply['userid'] == store_status_arr['store_speaker']:
                                store_status_arr = json.loads(self.get_store_status())
                                store_status_arr['store_stop_floor'] = reply['id']
                                self.set_store_status(store_status_arr)
                                break
                    break
        return

    def store_check_end(self):
        store_tree_arr = json.loads(self.get_store_tree())
        store_status_arr = json.loads(self.get_store_status())
        if store_tree_arr[store_status_arr['store_node']]['end_status'] == 1:
            return True;
        return False

adao = Adao()
layer = 11
r = adao.get_reply_end('30275381', layer)
print(json.dumps(r), '\n')
# i = 0
# for re in r:
#     if re['id'] != 9999999:
#         if re['content'].find('[store_start]') != -1:
#             print(re['id'], i)
#         i = i + 1

# todo: 增加故事结束跳出或重启循环
while False:
    post_id = '0'
    sleep_time = 10
    i = 0
    adao = Adao()
    print('ok')
    adao.store_start()
    while True:
        # 判断当前决定节点
        store_status_arr = json.loads(adao.get_store_status())
        print(store_status_arr['store_node'])
        title_data = adao.get_reply(store_status_arr['store_id'], '1')
        print(title_data['id'], title_data['content'])
        adao.store_roll()
        store_status_arr = json.loads(adao.get_store_status())
        if adao.store_check_end():
            break
