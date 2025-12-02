from telegram.constants import MessageLimit


def batch(lines):
    messages = list()
    message = line = ''
    while lines:
        message += line
        line = lines.pop(0)
        if len(message + line) >= MessageLimit.MAX_TEXT_LENGTH:
            messages.append(message)
            message = ''
    message += line
    messages.append(message)
    return messages


def list_to_texts(collocations, with_tag):
    lines = list()
    for collocation in collocations:
        try:
            line, trad = collocation.pop('mot'), collocation.pop('trad', None)
        except AttributeError:
            return [collocation]
        if trad:
            line += f" ~ {trad}"
        if with_tag:
            line += f" *{collocation.pop('tag')}"
        lines.append(line + '\n')
    if not with_tag:
        lines.insert(0, f'-{len(lines)}-\n')
    return batch(lines)
