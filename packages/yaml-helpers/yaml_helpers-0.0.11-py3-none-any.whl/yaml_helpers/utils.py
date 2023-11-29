from tree_sitter_languages import get_parser

EXPECTED_MAX_ENTITY_LENGTH = 2500
MAX_STRING_LENGTH = 1000


def manage_code_length(input_code, language_type):
    if len(input_code) > EXPECTED_MAX_ENTITY_LENGTH:
        parser = get_parser(language_type)
        tree = parser.parse(bytes(input_code, 'utf8'))
        node_obj = tree.root_node.children[0] # assumes there is only one root entity in input_code
        return rewrite_long_strings(node_obj)
    return input_code


def rewrite_long_strings(node, source_code=None):
    if not source_code:
        source_code = node.text
    modified_code = source_code
    for c in reversed(node.children):
        # Check if the child node is a string
        if c.type in ['string', 'template_string']:
            start_byte = c.start_byte
            end_byte = c.end_byte
            string_content = source_code[start_byte:end_byte]

            # Check if the string length is more than 1000 characters
            if len(string_content) > MAX_STRING_LENGTH:
                # Rewrite the string in the source code
                start_part = string_content[:int(.75*MAX_STRING_LENGTH)]
                end_part = string_content[-int(.25*MAX_STRING_LENGTH):]
                new_string = start_part + b"... [content omitted for brevity] ..." + end_part
                modified_code = modified_code[:start_byte] + new_string + modified_code[end_byte:]

        # Recursively check other nodes
        modified_code = rewrite_long_strings(c, modified_code)

    return modified_code