from .enum import HeadPack
from .packs import *

def ForceJoin(self):
    p = HeadPack()
    p.name="force_join"
    p.db_config = {'force_join': {'id': 0, 'title': '', 'link': ''}}
    
    def check_is_joind_to_channel(self):
        try:
            if self.context == None:
                return True
            if self.db == None:
                return True
        except:
            return True
        channels = self.db.do('force_join')

        if len(channels) > 0:
            must_be_join = []
            for ch in channels:
                channel_id = ch['link']
                if not self.is_channel_member(channel_id):
                    must_be_join += [ch]
            if len(must_be_join) == 0:
                try:
                    start_bot = self.splited_query_data()[0]
                    if start_bot == 'start_bot':
                        self.delete_message(self.get_msg_id())
                except:
                    pass
                return True
            else:
                try:
                    start_bot = self.splited_query_data()[0]
                    if start_bot == 'start_bot':
                        self.alert(self.text('jonin_alert_pm'))
                        return False,False
                except:
                    pass
                btns = {}
                for i in must_be_join:
                    btns[i['title']] = 'https://t.me/' + \
                        i['link'].replace('@', '')
                txt = self.get_text()
                if '/start' in txt:
                    btns['start_bot'] =txt 
                else:btns['start_bot'] ='/start'
                self.send_message(msg='join_pm', btns = btns,col=1)
                return False,False
        else:
            try:
                start_bot = self.splited_query_data()[0]
                if start_bot == 'start_bot':
                    self.delete_message(self.get_msg_id())
            except:
                pass
            return True
    p.func = check_is_joind_to_channel
    p.pack = Start
    return p
    
def ForceSharePhone(self):
    p = HeadPack()
    p.name="force_share_phone"
    def check_phone(self):
        if self.user('phone') == 0 and not Filters.contact(self.update):
            self.send_message('share_phone', [['share_phone']], share_phone=True)
            return False
        return True
    p.func = check_phone
    p.pack = SharePhone
    return p
    
def CheckLanguage(self):
    p = HeadPack()
    p.name="check_language"
    def check_language(self):
        languages = self.languages
        if self.user('language') == self.defulat_lang_code and languages:
            btn = {k:f"{v}:select_language" for k,v in languages.items()}
            self.send_message(msg='🔘 Select your Language', btns= btn,translat=False)
            return False
        return True
    p.func = check_language
    p.pack = SelectLanguage
    return p