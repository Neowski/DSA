from database import add_set, add_card, get_sets

def add_word(conn, set_name, word, definition):
    if set_name and word and definition:
        sets = get_sets(conn)
        if set_name not in sets:
            set_id = add_set(conn, set_name)
        else:
            set_id = sets[set_name]
        add_card(conn, set_id, word, definition)
