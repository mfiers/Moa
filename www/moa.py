from mod_python import apache

def handler(req):
      req.log_error('handler')
      req.content_type = 'text/plain'
      req.send_http_header()
      req.write('moa.py\n')
      return apache.OK
