from math import ceil


def prepare_pagination_link(link_base: str, pagination, employees_number: int) -> str:
    links = ''
    page_size = pagination['page_size']
    offset = pagination['offset']
    if offset != 0:
        page_number = 1
        relation = 'rel=\"first\"'
        links += link_base.format(page_number, page_size, relation)
    prev_page_number = int(offset / page_size)
    if prev_page_number != 1:
        page_number = prev_page_number
        relation = 'rel=\"prev\"'
        links += link_base.format(page_number, page_size, relation)
    page_number = offset / page_size + 1
    next_page_number = page_number + 1
    last_page_number = ceil(employees_number / page_size)
    if next_page_number < last_page_number:
        page_number = next_page_number
        relation = 'rel=\"next\"'
        links += link_base.format(page_number, page_size, relation)
    if page_number < last_page_number:
        page_number = last_page_number
        relation = 'rel=\"last\"'
        links += link_base.format(page_number, page_size, relation)
    return links
