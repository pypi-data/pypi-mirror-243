from .base import *
from time import time
class Conversation(Base):
    def __init__(self,role:list[Role],super_self, defulat_lang_code=0,languages:dict[str:int]={},*args, **kwargs) -> None:
        super().__init__(super_self,defulat_lang_code=defulat_lang_code,languages=languages,*args, **kwargs)
        self.element_name=None
        self.nodes:list[ConversationNode] =[]
        if not isinstance(role,list):
            role=[role]
        self.role=role

        self.init_setter()
        self.init_pagination()
        self.init_menu()


    def not_fount(self,*args):
        self.send('not_fount',self.menu_keys)
        return -1
    ############### init_setter###################
    def init_setter(self):
        e = Node()
        e.filters = ~Filters.contact & IsReplied()
        e.callback = self.setter_entry
        self.node('setter',entry=[e])

    def setter_entry(self, *args):
        if (self.super_self.edit_mode or self.get_setting('edit_mode')) and (self.user('editor') == 1 or self.is_super_admin() or self.id in self.super_self.editors_id):
            try:
                self.setter()
            except Exception as e:
                self.debug.debug(e)
            return  -1

    ############### init_pagination###################

    def init_pagination(self):
        e1 = Node()
        e1.pattern = self.check_inline_keyboards('next_page:pagination',regex=True)
        e1.callback = self.pagination_entry

        e2 = Node()
        e2.pattern = self.check_inline_keyboards('back_page:pagination',regex=True)
        e2.callback = self.pagination_entry
        self.node('setter',entry=[e1,e2])

    def pagination_entry(self, *args):
        order = self.splited_query_data()[0]
        if 'pagination_iter' in self.context.user_data:
            if order == 'next_page':
                self.userdata('pagination_iter',
                              self.userdata('pagination_iter')+1)
            elif order == 'back_page':
                self.userdata('pagination_iter',
                              self.userdata('pagination_iter')-1)
            try:
                msg = self.pagination_msg_maker()
                btn = self.pagination_btn_maker()
                self.edit_message_text(new_msg=msg,message_id=self.get_msg_id(),btns=btn,chat_id=self.id)
            except Exception as e:
                self.debug.debug(e)
                self.delete_message(self.get_msg_id())
        else:
            self.delete_message(self.get_msg_id())
        return -1
    ############### init_menu###################
    def init_menu(self):
        e = Node()
        e.filters = match_btn(self.back_menu_key,self)
        e.callback =self.menu
        self.node('menu',entry=[e])

    
    
class Scheduler:
    def __init__(self,super_self) -> None:
        self.super_self = super_self
        self.schecdaul_info={}

    def allow(self,name):
        now = int(time())
        item = self.schecdaul_info.get(name,{})
        last_run = item.get('last_run',0)
        first_run = item.get('first_run',0)
        run_evry_sec = item.get('run_evry_sec',0)
        if last_run==0:
            self.schecdaul_info[name]['last_run']=now
            if first_run:
                return True
        else:
            if now%run_evry_sec==0 or now - last_run > run_evry_sec:
                self.schecdaul_info[name]['last_run']=now
                return True
                
        return False

    def add(self,func,run_evry_sec:int,first_run=False):
        '''
            function with input self
        '''
        name = str(func.__name__)
        self.schecdaul_info[name] = {'func':func,'run_evry_sec':run_evry_sec,'first_run':first_run,'last_run':0}
    
    def run(self):
        while True:
            for name , dict_val in self.schecdaul_info.items():
                try:
                    if self.allow(name):
                        dict_val['func'](self.super_self)
                except Exception as e:self.super_self.debug.debug(e)
            sleep(1)

