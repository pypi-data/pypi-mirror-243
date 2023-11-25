from .web import web_



class web(web_):
    def set_web_url(self, url):
        result = self._set_web_url(url=url)
        return result
    
    def get_web_url(self):
        result = self._get_web_url()
        return result
    
    def getHtmlText(self, data = {}, header = {}, content_type = "data"):
        result = self._getHtmlText(data=data, header=header, content_type=content_type)
        return result
    
    def postHtmlText(self, data = {}, header = {}, content_type = "data"):
        result = self._postHtmlText(data=data, header=header, content_type=content_type)
        return result
    
    def getHtmlJson(self, data = {}, header = {}, content_type = "data"):
        result = self._getHtmlJson(data=data, header=header, content_type=content_type)
        return result
    
    def postHtmlJson(self, data = {}, header = {}, content_type = "data"):
        result = self._postHtmlJson(data=data, header=header, content_type=content_type)
        return result