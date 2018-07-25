import requests, ast

url = 'https://portfoliotest.infrontservices.com/portfolio'

class UserLists:
    def __init__(self, username, password, url=None):
        self.username = username
        self.password = password
        self.url = 'https://portfoliotest.infrontservices.com/portfolio'
        if url:
            self.url = url

    def get_user_lists(self):
        r = requests.get(self.url, auth=(self.username, self.password))
        outdict = dict(ast.literal_eval(r.text))
        if outdict['error_code'] != 0:
            print('Status code: ' + str(r.status_code))
            print('Internal error code: ' + str(outdict['error_code']))
            print('Error message: ' + str(outdict['error_message']))
        else:
            print('Lists and Portfolios fetched for user "' + self.username + '"')
        out = {}
        for i in outdict['md_list_all_response']:
            urli = url + '?list=' + str(i['list']).replace(" ", "%20")
            p = requests.get(urli, auth=(self.username, self.password))
            resp = ast.literal_eval(p.text)
            out[i['list']] = resp['md_get_user_list_response']
        return out


#test
a = UserLists('greni','sander')
yolo = a.get_user_lists()
