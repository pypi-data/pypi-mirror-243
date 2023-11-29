from ..base import Base
from ..classes import Conversation
from .enum import Pack,Node
from .filteres import match_btn,match_text
from telegram.ext import Filters



def Start(self:Conversation):
    
    def act(self,*args):
        self.send(msg = 'start_pm', btns = self.menu_keys)
        return -1

    p = Pack()
    p.name = 'start'

    e1 = Node()
    e1.command = 'start'
    e1.command_filters = match_text('/start')
    e1.callback=act

    e2=Node()
    e2.pattern = self.check_inline_keyboards('/start')
    e2.callback = act
    p.entry=[e1,e2]
    return p

def SharePhone(self:Conversation):
    p = Pack()
    p.name = 'share_phone'
    e=Node()
    e.filters = Filters.contact
    def act(self,*args):
        contact = self.update.effective_message.contact
        phone = contact.phone_number
        self.db.do('users', {'id': self.id, 'phone': int(phone)}, condition=f"id={self.id}")
        self.send_message('phone_shared', self.menu_keys)
        return -1
    e.callback = act
    p.entry=[e]
    return p
            
def SelectLanguage(self:Conversation):
    p = Pack()
    p.name = 'select_language'
    e=Node()
    e.pattern = self.check_inline_keyboards('select_language',self)
    
    def act(self:Conversation,*args):
        lang_id = int(self.splited_query_data()[1])
        self.db.do('users', {'id': self.id, 'language': lang_id}, condition=f"id={self.id}")
        self.delete_message(self.get_msg_id())
        self.user_info=self.get_user_info_from_db([])
        self.send('✅ The language has been set', self.menu_keys,translat=False)
        return -1
    e.callback = act
    p.entry=[e]
    return p
            
def Referral(self:Conversation):
    p = Pack()
    p.name = 'Referral'
    p.db_config={'users':{'presenter':0}}

    e1 = Node()
    e1.btn = self.menu_keys
    e1.filters = match_btn('referral',self)
    
    def referral_text(self:Base,*args):
        msg=self.text('referral_text',slash=True)+'\n\n'
        msg+=f'https://t.me/{self.super_self.bot_username}?start=ref{self.id}\n\n'
        msg+=f"{self.text('invited')} : {len(self.db.do('users', condition=f'presenter={self.id}'))}"

        self.send(msg= msg,btns=self.menu_keys,translat=False)
        return -1
    e1.callback =referral_text

    e2 = Node()
    e2.btn = self.menu_keys
    e2.command = 'start'
    e2.command_filters=Filters.regex('/start ref\d+')
    def referral_action(self,*args):
        try:
            presenter = int(self.get_text().split(' ')[-1].replace('ref',''))
        except:
            try:
                presenter = int(self.splited_query_data()[1].split(' ')[-1].replace('ref',''))
            except:
                presenter=0
        try:
            submited_presenter = int(self.user('presenter'))
        except:
            submited_presenter = 0
        if submited_presenter==0 and presenter!=self.id:
            self.db.do('users', {'presenter': presenter},condition=f"id={self.id}")
            self.send('new_subset_text', chat_id=presenter)
        self.send('start_pm', self.menu_keys)
        return -1
    
    e2.callback=referral_action

    e3 = Node()
    e3.btn = self.menu_keys
    e3.pattern = self.check_inline_keyboards('/start ref',regex=True)
    e3.callback=referral_action


    p.entry=[e1,e2,e3]
    return p






#************** not completed********************
def SupportAdmin(self:Conversation):
    p = Pack()
    p.name = 'SupportAdmin'
    p.db_config={'support': {'id':0,'u_id': 0, 'msg_id': 0, 'response_id': 0, 'responser_id': 0, 'extra': '', 'status': 0, 'time': 0}}
    e=Node()
    e.filters = match_btn('support',self)

    def show_message_from_user(self:Conversation, item):
        try:

            lnk = None
            u_username = self.user('username')
            if u_username != None:
                lnk = f'https://t.me/{u_username}'
            try:
                name = self.user('name')[:13]
            except:
                name = 'info'
            btn = {
                'send_reply': f"{item['id']}",
                'user_info': f"{item['u_id']}",
                'mark_read': f"{item['id']}",
                'show_response': f"{item['id']}",
                'perv_sup_pm': f"{item['id']}:{item['u_id']}",
                'next_sup_pm': f"{item['id']}:{item['u_id']}",
            }
            tbtn = btn.copy()
            tbtn[name] = f"shinfo:{item['id']}"
            if lnk:
                tbtn['pv'] = lnk
            
            try:
                self.copy_message(from_chat_id=item['u_id'],message_id=item['msg_id'],chat_id=self.id,btns=tbtn)
            except:
                try:
                    btn['info'] = f"shinfo:{item['time']}"
                    if lnk:
                        btn['pv'] = lnk
                        self.copy_message(from_chat_id=item['u_id'],message_id=item['msg_id'],chat_id=self.id,btns=tbtn)
                except:
                    self.send('unreadable_message'+f"\n/user_{item['u_id']}", btn)
                    self.db.do('support', {'status': 1},condition=f"id={item['id']}")
        except Exception as e:
            self.send_message('unreadable_message'+f"\n/user_{item['u_id']}\nerror")
            self.db.do('support', {'status': 1},condition=f"id={item['id']}")
            self.debug.debug(e)


    def unreaded_messages(self:Conversation, *args):
        unreaded_messages = self.db.do('support', condition=f"status=0")
        self.send('wait', self.menu_btn)
        try:
            if not unreaded_messages:
                self.send('no_item', self.menu_keys)
            else:
                for item in unreaded_messages:
                    self.show_message_from_user(item)
        except Exception as e:
            self.debug.debug(e)
        return -1
    e.callback = unreaded_messages
    p.entry=[e]
    return p


    
    