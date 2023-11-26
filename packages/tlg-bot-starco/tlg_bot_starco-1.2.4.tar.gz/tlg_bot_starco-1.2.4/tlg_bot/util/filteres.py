from telegram.ext.filters import MessageFilter,UpdateFilter,BaseFilter
from.enum import Role


class match_text(MessageFilter):
    def __init__(self, target) -> None:
        super(match_text, self).__init__()
        self.target = target

    def filter(self, message):
        return self.target == message.text

class IsReplied(MessageFilter):
    def __init__(self,*args) -> None:
        super(IsReplied, self).__init__()
    def filter(self, message):
        out = message.reply_to_message!=None and message.chat.id==message.reply_to_message.chat.id
        return out

class special_user(MessageFilter):
    def __init__(self, target) -> None:
        super(special_user, self).__init__()
        self.target = target

    def filter(self, message):
        return self.target == message.from_user.id
    
class match_btn(MessageFilter):
    def __init__(self, target,super_self) -> None:
        super(match_btn, self).__init__()
        self.target = target
        self.super_self = super_self

    def filter(self, message):
        res = self.super_self.replace_btn_label(self.target, main_word= message.text) == message.text
        return res

class RoleFilter(UpdateFilter):
    def __init__(self, *super_self) -> None:
        super(RoleFilter, self).__init__(*super_self)
        # self.super_self = super_self
        print(super_self)

    # def filter(self,*args):
    #     print(self.super_self.user('role') , self.super_self.role)
    #     return self.super_self.user('role') in self.super_self.role




class RoleFilter(UpdateFilter):
    """Represents a filter that has been inverted.

    Args:
        f: The filter to invert.

    """

    __slots__ = ('f',)

    def __init__(self, f,*args):
        self.f = f

    def filter(self, update) -> bool:
        super_self = self.f
        u_id = update.message.from_user.id
        try:
            user = super_self.db.do('users',condition=f"id={u_id}")
            if user:
                res = user[0]['role'] in super_self.role
                return res
            return Role.USER.value in super_self.role
        except Exception as e:super_self.debug.debug(e)
        return True