from parameters_generator import (generate_column_params, generate_row_params,
                                  generate_border, generate_column_params,
                                  generate_column_width, generate_header_params,
                                  generate_blank_col_row_params)


def full_imager(words):
    table_params = generate_column_params()
    font_size = table_params["font_size"]
    font_name = table_params["font_name"]
    # dict
    row_params = generate_row_params(font_size)
    is_partial_border = table_params["is_partial_border"]
    is_border = table_params["is_border"]
    # obiekt Border
    border = generate_border(table_params["line_style"], is_border, is_partial_border)
    column_type = table_params["columns_type"]
    # dict
    row_params = generate_row_params(font_size)
    
    total_cols_width = 0
    for col number:
        # dict
        column_params = generate_column_params(column_type)
        
        # word_generator and number_generator use values from column_params
        words = full_lister(..., column_params) # dla kolumny
        
        word_max_length = maksymalna dl slowa w kolumnie
        # dict
        column_width = generate_column_width(font_size, word_max_length)
        total_cols_width += column_width
        for row number:
            ...
            cell.border = Border
            ...
    if table_params["is_different_header"]:
        # dict
        header_params = generate_header_params()
        font_size = header_params["font_size"]
        font_bold = header_params["font_bold"]
        font_italic = header_params["font_italic"]
        border = generate_border(header_params["line_style",] is_border=is_border, is_partial_border=is_partial_border)
        zmien parametry peirwszego wiersza
        
    blank_shape = generate_blank_col_row_params(table_params['rows_number'],
                                                row_params['row_height'],
                                                table_params['columns_number'],
                                                total_cols_width)
    fill the rest of the space with white