# -*- coding: utf-8


import re
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def re_decode(src, use_unquote_plus=True):
    '''
    将字符串中形如 \350\275\246 以及 %E5%A4%B4 的部分转化为中文 unicode 
    '''
    if src.find('\\')==-1 and src.find('%')==-1:
        return src
    s1 = src
    # 先将形如 \350\275\246 的部分转化为 %E5%A4%B4 的格式
    # 其中 \xxx 必须有三组才能组成一个 unicode 
    for i in re.findall(r'((\\[0-7]{3}){3})', s1):
        name=''.join(['%%%x' %int(g,8) for g in i[0].split('\\') if g.isdigit()])
        s1 = s1.replace(i[0], name)
    def __decode(x, use_unquote_plus=True):
        '''
        部分解码。注意当且仅当设置了 sys.setdefaultencoding('utf-8') 才生效
        '''
        if use_unquote_plus:
            return urllib.unquote_plus(x.encode('ascii')).decode('utf-8')
        else:
            return urllib.unquote(x.encode('ascii')).decode('utf-8')
    # 尝试整体解码
    try:
        return __decode(s1, use_unquote_plus)
    except:
        pass
    # 将形如 %E5%A4%B4 的部分转化为 unicode 
    # 其中 %xx 必须有三组才能组成一个 unicode 
    # TODO  遇到 \\260\\350\\275\\246 这种的时候 结果会变成 %b0%e8%bd\\246 但更合理的结果应该是 \\260\u8f66 
    for i in re.findall(r'((%[a-fA-F0-9]{2}){3})', s1):
        try:
            s1 = s1.replace(i[0], __decode(i[0], use_unquote_plus))
        except:
            pass
    return s1
if __name__=='__main__':
    # s1 = '\\344 %E6 \\271 %E6%96%B9 \\260 \\350\\275\\246 \\350\\276\\276 \\344\\272\\272'
    # s2 = '%E4%B8%9C %E6%96%B9 %E5%A4%B4 %E6%9D%A1'
    # s3 = s1 + ' ' + s2
    # from pprint import pprint 
    # pprint(re_decode(s1))
    # pprint(re_decode(s2))
    # pprint(re_decode(s3))

    # import codecs
    # from hanziconv import HanziConv
    # with codecs.open('test_redecode.csv', encoding='utf-8') as fin, \
        # codecs.open('test_redecode_out.csv', 'w', encoding='utf-8') as fout:
        # for line in fin:
            # line = line.strip()
            # result = re_decode(line, use_unquote_plus=False)
            # result = HanziConv.toSimplified(result)
            # result = result.strip().replace(' ', '')
            # fout.write(line+'\t'+result+'\n')
    sep = '\t'
    for line in sys.stdin:
        try:
            parts = [i.strip() for i in line.split(sep)]
            useragent = parts[1]
        except: # 输入异常
            continue

        ua_decoded = ''
        try:
            ua_decoded = re_decode(useragent, use_unquote_plus=False)
        except: # 解码异常
            pass

        # try:
            # from hanziconv import HanziConv
            # ua_decoded = HanziConv.toSimplified(ua_decoded)
        # except: # 繁体字转换异常
            # pass

        try:
            sys.stdout.write(sep.join([sep.join(parts),
                ua_decoded]) + '\n')
        except: # 输出异常
            continue

    