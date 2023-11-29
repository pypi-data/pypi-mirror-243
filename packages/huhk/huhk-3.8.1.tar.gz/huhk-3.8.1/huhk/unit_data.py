size_names = ("pagesize", "size", "limit", "pageSize", 'page_size')
page_names = ("pageNum", "current", "currentpage", "page", "currentPage", "page_index", "page_no", "page_num")
before_names = ("before", "start")
end_names = ("end", )
page_and_size = size_names + page_names
before_and_end = before_names + end_names
before_and_end_re_str = "|".join(["^" + i for i in before_and_end] + [i + "$" for i in before_and_end])
