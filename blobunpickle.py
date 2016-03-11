import cgi
import webapp2
import logging
import pickle
import pprint

MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/convert" method="post">
      <pre>
First get the blob column data from your sql table in hex format.
e.g. 
mysql> select hex(attrs) from mytable
+--------------------------------------------------------------------------+
| hex(attrs)                                                               |
+--------------------------------------------------------------------------+
| 286470300a532761270a70310a5327666f6f20626172270a70320a7349310a49310a732e |
+--------------------------------------------------------------------------+
1 row in set (0.00 sec)
Copy (ctrl+c) the hex string.
Paste (ctrl+v) the hex string in the box below.
Click convert.
      </pre>
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Convert"></div>
    </form>
    
    <div>
    <small><i>If you like this tool, send improvement requests to: a n i a p t e AT g m a i l DOT c o m</i></small>
    </div>

  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)

class Convert(webapp2.RequestHandler):
    def post(self):
        blob = self.request.get('content').strip()
        logging.info('convert: blob: %s', blob)
        
        self.response.write('<html><body>')
        
        self.response.write('<pre>You pasted this: ')
        self.response.write(cgi.escape(blob))
        self.response.write('</pre>')
        
        self.response.write('<pre>After conversion: ')       
        self.response.write('<pre>')
        
        obj = pickle.loads(blob.decode('hex'))
        pp = pprint.PrettyPrinter()
        out = pp.pformat(obj)

        self.response.write(cgi.escape(out))
        self.response.write('</pre>')
        
        self.response.write('</body></html>')

        logging.info('convert: out: %s', str(obj))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/convert', Convert),
], debug=True)

