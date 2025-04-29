def insert_after_first_line(text, symbols):
    lines = text.split('\n')
    if len(lines) == 0:
        return text
    # Вставляем символы после первой строки
    lines.insert(1, symbols)
    return '\n'.join(lines)