def split_sql(query, pattern=';', limit=-1):
    need = [pattern, 0, 0]
    inComma = False
    need_line_end = False
    queries = []
    item = ""
    i = 0
    while i < len(query):
        try:
            c = query[i]
            # 0. add limit
            if limit > 0 and len(queries) == limit and len(item) == 0:
                queries.append(query[i:])
                break
            # 1. normally split
            if not inComma and c == pattern:
                if len(item) > 0:
                    queries.append(item)
                item = ""
                continue
            # 2. add char
            item += c
            # deal with \\
            if c == '\\':
                if i + 1 < len(query):
                    item += query[i + 1]
                    i += 1
                continue
            # 3. pack multi chars
            pack = [c, 0, 0]
            single_comma = False
            # 3.1 normal string supported
            pack_len = 1 if c == '\'' or c == '\"' or c == '`' else 0
            # 3.2.1 comment: single/multi line(s) comment
            next = query[i + 1] if i + 1 < len(query) else 0
            if (c == '-' and next == '-') or (not inComma and c == '/' and next == '*'):
                pack[1] = next
                pack_len = 2
                single_comma = c == '-'
                item += query[i + 1]
                i += 1
            elif inComma and c == '*' and next == '/':
                pack[0] = next
                pack[1] = c
                pack_len = 2
                item += query[i + 1]
                i += 1
            if c == '`':
                # `` && ```
                while pack_len <= 3 and i + 1 < len(query) and query[i + 1] == c:
                    pack[pack_len] = c
                    pack_len += 1
                    item += c
                    i += 1
            # 4. single comment end
            if inComma and need_line_end and c == '\n':
                inComma = False
                continue
            # 5. else nothing special
            if pack_len == 0:
                continue
            # 6. check comma start
            if not inComma:
                # 6.1 set comma start
                need[:] = pack[:]
                need_line_end = single_comma
                inComma = True
            else:
                # 6.2 comma match check
                match = True
                for k in range(3):
                    if pack[k] != need[k]:
                        match = False
                        break
                if match:
                    inComma = False
        finally:
            i += 1
    if len(item) > 0:
        queries.append(item)
    return queries
