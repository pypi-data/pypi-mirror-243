import requests, json

################################################################################
##
##  Make sure you have a jaguar fwww http server running
##
################################################################################

import os, json

class JaguarHttpClient():

    ''' ctor, takes a http REST endpoint
        url is like "http://192.168.5.100:8080/fwww/"
        url is like "fakeurl"
    '''
    def __init__(self, url):
        if url[-1] != '/':
            url = url + '/'
        self.url = url


    ''' First step is to login and get an auth token
    returns valid token for success or None for failure
    '''
    def login(self, apikey=None):
        if self.url == 'fakeurl/':
            return 'faketoken'

        self.apikey = apikey

        if apikey is None:
            self.apikey = self.getApikey()

        params = { "req": "login", "apikey": apikey }
        response = requests.get(self.url, params=params)
        #print(response.text)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            token = json_data['access_token']
            if token is not None:
                return token
            else:
                return None
        else:
            return None

    ''' makes GET call and returns response
    GET is faster than POST, but request size is limited
    '''
    def get(self, qs, token):
        bearerToken = 'Bearer ' + token
        headers = { "Authorization": bearerToken }
        params = { "req": qs, "token": token }
        response = requests.get(self.url, headers = headers, params = params )
        return response

    ''' makes a POST request and returns response
    '''
    def post(self, qs, token, withfile=False):
        bearerToken = 'Bearer ' + token
        headers = { "Authorization": bearerToken }

        if withfile is True:
            params = { "req": qs, "token": token, "withfile": "yes" }
        else:
            params = { "req": qs, "token": token }

        response = requests.post(self.url, headers = headers, json = params )
        return response

    ### alias for post() since query() normally has large size involving vectors
    def query(self, qs, token, withfile=False):
        return self.post( qs, token, withfile )


    ''' logout is strongly recommended for security reasons
    and resource cleanup
    '''
    def logout(self, token):
        bearerToken = 'Bearer ' + token
        headers = { "Authorization": bearerToken }
        params = { "request": "logout", "token": token }
        requests.get(self.url, headers = headers, params = params )

    ### wrapper
    def getApiKey(self):
        return self.getApikey()


    ''' If apikey is not provided, this tries to get it from $HOME/.jagrc file
    '''
    def getApikey(self):
        try:
            hm = os.getenv("HOME")
            fpath = hm + "/.jagrc"
            f = open(fpath, 'r')
            key = f.read()
            key = key.strip()
            f.close()
            return key
        except Exception as e:
            return ''

    ''' get json from server and parse out the data element
    '''
    def jsonData(self ):
        try:
            j = self.jag.json()
            data = json.loads(j)
            return data['data']
        except Exception as e:
            return ''

    ''' given json string from server, get the data element
    '''
    def getData(self, j):
        try:
            data = json.loads(j)
            return data['data']
        except Exception as e:
            return ''


    ''' post a file to url server index=[1...pos] index is position of the file field
    inside values ('0','1','2','3') in insert statement. Index starts from 1 when invoked. 
    Call this to upload the files, before the insert query
    '''
    def postFile(self, token, filePath, index ):
        try:
            filefp = open(filePath, 'rb');
            if filefp is None:
                return False
        
            ## starts from 0 now
            index = index - 1
            name = 'file_' + str(index)
            files = {name: (filePath, filefp) }
            params = { "token": token }
            bearerToken = 'Bearer ' + token
            headers = { "Authorization": bearerToken }
            response = requests.post(self.url, headers=headers, data=params, files=files)
            filefp.close()
            if response.status_code == 200:
                return True
            return False
        except Exception as e:
            return False 
    
    '''
    get URL for display of files in a browser
    '''
    def getFileUrl(self, token, store, column, zid):
        bearerToken = 'Bearer ' + token
        headers = { "Authorization": bearerToken }
        query = "getfile " + column + " show from " + store + " where zid='" + zid + "'"
        params = { "req": query, "token": token };
        response = requests.get(self.url, headers=headers, params = params)
        if response.status_code == 200:
            json_data = json.loads(resp.text)
            rec = json_data[0]['0']
            return url + "?" + rec
        else:
            return ''
    
    ''' get data from returned select similarity json data
    '''
    def getSimilarityValue(self, jd, i, name):
        try:
            j = jd[i]
            rec = json.loads(j)
            return rec[name]
        except:
            return ''



### example test program
if __name__ == "__main__":
    
    url = "http://192.168.1.88:8080/fwww/"
    jag = JaguarHttpClient( url )
    #apikey = 'my_api_key'
    apikey = jag.getApikey()


    ### login to get an authenticated session token
    token = jag.login(apikey)
    if token == '':
        print("Error login")
        exit(1)
    print(f"session token is {token}")

    ### get some data
    resp = jag.get("help", token)
    print(resp.text)

    j1 = json.loads(resp.text)
    helpjson = j1[0]
    j2 = json.loads(helpjson)
    print(j2['data'])


    q = "drop store vdb.week"
    response = jag.get(q, token)
    print(response.text)
    print(f"drop store {response.text}")

    q = "create store vdb.week ( v vector(512, 'euclidean_fraction_float'), v:f file, v:t char(1024), a int)"
    response = jag.get(q, token)
    print(f"create store {response.text}")


    ### upload file for v:f which is at position 2 
    rc = jag.postFile(token, '/tmp/test1.jpg', 2 )
    print(f"postFile /tmp/test1.jpg {rc}")

    q = "insert into vdb.week values ('0.1,0.2,0.3,0.4,0.5,0.02,0.3,0.5', '/tmp/test1.jpg', 'this is text description: market rebounce', 10 )"
    response = jag.post(q, token, True)
    print(f"insert {response.text}")

    q = "insert into vdb.week values ('0.5,0.2,0.5,0.4,0.1,0.02,0.3,0.7', '/tmp/test1.jpg', 'this is text description: market saturation', 100 )"
    response = jag.post(q, token, True)
    print(f"insert {response.text}")

    q = "select similarity(v, '0.3,0.2,0.8,0.4,0.1,0.1,0.3,0.1', 'topk=3, type=euclidean_fraction_float, with_text=yes, with_score=yes') from vdb.week"
    response = jag.post(q, token)
    jd = json.loads(response.text)

    for i in range(0, len(jd)):
        field = jag.getSimilarityValue(jd, i, 'field')
        vid = jag.getSimilarityValue(jd, i, 'vectorid')
        dist = jag.getSimilarityValue(jd, i, 'distance')
        txt = jag.getSimilarityValue(jd, i, 'text')
        score = jag.getSimilarityValue(jd, i, 'score')
        print(f"field=[{field}]  vectorid=[{vid}]  distance=[{dist}] text=[{txt}] score=[{score}]")

    jag.logout(token)
