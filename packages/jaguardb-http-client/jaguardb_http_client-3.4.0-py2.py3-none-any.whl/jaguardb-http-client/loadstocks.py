import requests, json, sys
from sentence_transformers import SentenceTransformer


sys.path.append('/mnt/ssd/home/dev2/src/pip_packaging/jaguardb_http_client/jaguardb-http-client/jaguardb-http-client')
#import JaguarHttpClient
from JaguarHttpClient import JaguarHttpClient


def loadStocks():
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


    q = "drop table vdb.daily"
    response = jag.get(q, token)
    print(response.text)
    print(f"drop store {response.text}")

    q = "create store vdb.daily ( key: zid zuid, value: v vector(1024, 'cosine_fraction_float'), v:f file, v:t char(1024) )"
    response = jag.get(q, token)
    print(f"create store {response.text}")

    # 0 -- 334
    mdir = '/mnt/ssd/home/dev2/fwww/htdocs/dia/'
    model = SentenceTransformer('BAAI/bge-large-en')

    #for i in range(0, 335):
    for i in range(0, 300):
        fpath = mdir + 'main_' + str(i) + '_price.txt'

        f = open(fpath, "r")
        text = f.read();
        text = text.strip()
        f.close()

        sentences = [ text ]
        embeddings = model.encode(sentences, normalize_embeddings=False)
        comma_sepstr = ",".join( [str(x) for x in embeddings[0] ])

        ### upload file for v:f which is at position 2 
        rc = jag.postFile(token, fpath, 2 )

        q = "insert into vdb.daily values ('" + comma_sepstr + "', '" + fpath + "', '" + text + "' )"
        response = jag.post(q, token, True)

        fpath = mdir + 'overlap_' + str(i) + '_price.txt'

        f = open(fpath, "r")
        text = f.read();
        text = text.strip()
        f.close()

        sentences = [ text ]
        embeddings = model.encode(sentences, normalize_embeddings=False)
        comma_sepstr = ",".join( [str(x) for x in embeddings[0] ])

        ### upload file for v:f which is at position 2 
        rc = jag.postFile(token, fpath, 2 )

        q = "insert into vdb.daily values ('" + comma_sepstr + "', '" + fpath + "', '" + text + "' )"
        response = jag.post(q, token, True)




    qpath = '/mnt/ssd/home/dev2/ui/query_price.txt'
    #f = open(fpath, "r")
    f = open(qpath, "r")
    qt = f.read();
    qt = qt.strip()
    f.close()

    #sentences = [ text ]
    sentences = [ qt ]
    embeddings = model.encode(sentences, normalize_embeddings=False)
    comma_sepstr = ",".join( [str(x) for x in embeddings[0] ])

    q = "select similarity(v, '" + comma_sepstr + "', 'topk=3, type=cosine_fraction_float, with_score=yes') from vdb.daily"
    response = jag.post(q, token)
    #print(response.text)

    jd = json.loads(response.text)

    page = "<html><head><title>10x10</title></head>\n"
    page += "<body style='font-size: 12pt; color: #555;'>\n"
    page += "<br><br>\n"
    page += "<table align=center width=700 style='border-radius: 4px; box-shadow: 0 0 12px rgba(150, 150, 150, 0.5);'>\n"
    page += "<tr bgcolor='#f8f8f8'><td>Rank</td><td>Distance</td><td>Score</td><td>URL</td></tr>\n"

    for i in range(0, len(jd)):
        fd= json.loads( jd[i] )
        field = fd['field']
        vid = fd['vectorid']
        zid = fd['zid']
        score = fd['score']
        dist = fd['distance']
        #print(f"field={field} vid={vid} zid={zid}")

        q = "select v:f as vf from vdb.daily where zid='" + zid + "'"
        response = jag.get(q, token)
        #print(response.text)
        j2 = json.loads( response.text )
        #print(j2[0])
        j3 = json.loads( j2[0] )
        #print(j3)
        fname = j3['vf']

        sp = fname.split('.')
        html = 'http://192.168.1.88:8080/dia/' + sp[0] + ".html"

        #print(f"field=[{field}]  vectorid=[{vid}] zid=[{zid}]  distance=[{dist}] score=[{score}] fname=[{fname}] html={html}")
        print(f"zid=[{zid}]  distance=[{dist}] score=[{score}] html= {html} ")
        href = "<a href='" + html + "' style='color: #555;' target=_blank>" + html + "</a>"
        page += "<tr><td>" + str(i) + "</td><td>" + dist + "</td><td>" + score + "</td><td>" + href + "</td></tr>\n"


    page += "</table>\n"
    page += "</body>\n"
    page += "</html>\n"

    f = open("/mnt/ssd/home/dev2/fwww/htdocs/dia/result.html", "w")
    f.write(page)
    f.close()

    print("Result is  http://192.168.1.88:8080/dia/result.html")


    jag.logout(token)



if __name__ == "__main__":
    loadStocks()
    
