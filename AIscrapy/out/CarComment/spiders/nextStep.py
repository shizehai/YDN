
    def $name$(self, response):
        item = copy.deepcopy(response.meta['item'])
        page = response.meta['page']
        keyword=item['keyword']
        last_url_=response.meta['url_']
        $res_meta_keys$
        # response文本预处理
        soup = BeautifulSoup(response.text)
        lines = soup.find(class_="result").find_all(class_="list-dl")

        count = len(lines)
        # 翻页
        $turn_page$
        items = []
        for line in lines:
            page=1
            # 解析 item 数据
            $line_keys$
            
        $to_next_step$
