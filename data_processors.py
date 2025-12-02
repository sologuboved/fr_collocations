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


def list_to_texts(collocations):
    lines = list()
    for collocation in collocations:
        try:
            mot, trad = collocation.pop('mot'), collocation.pop('trad', None)
        except AttributeError:
            return [collocation]
        if trad:
            lines.append(f"{mot} ~ {trad}\n")
        else:
            lines.append(mot + '\n')
    lines.insert(0, f'-{len(lines)}-\n')
    return batch(lines)
