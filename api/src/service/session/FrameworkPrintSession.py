def printSession(self,commandList) :
    if self.session :
        print(f'{self.globals.TAB}api-key : {commandList[0]}')
        print(f'{self.globals.TAB}session-api-list :')
        for api in self.session.api_list :
            print(f'{self.globals.TAB * 2}{api.key} : {api.class_name}')
    else :
        self.globals.error(self.__class__, '''session is currently inactive''', self.globals.NOTHING)
