# Method takes in a pd.df and an optional desired width for the returned markdown version
# of the df. Returns a reformatted df in markdown format where the width of the markdown
# is equal to or slightly less than the desired with. If desired width is not specified, a
# default width of 115 characters is achieved (this default width is suitable for printing
# to a Letter-sized PDF with landscape orientation). Function also optionally takes in a
# dictionary of abbreviations that is used in place of the standard abbreviations
# dictionary (format: {'word_1_to_abbreviate': 'abbreviation_1',
# 'word_2_to_abbreviate': 'abbreviation_2', ...}).
#
# To achieve the more-narrow markdown version of the df, first column names are shortened
# using the default abbreviations dictionary (or the optional user-provided dictionary).
# Keywords in column names are replaced with abbreviations. Note that column names may
# contain words separated by either underscores or spaces.

# If, after wrapping column names, the width of the markdown is still greater than the
# desired markdown width, the columns are iteratively wrapped to increasingly shorter
# widths until the desired width of the markdown is achieved.

def shorten_df_for_printing(df, desired_width=115, abbreviations=None):

    import textwrap

    # Define default dictionary of abbreviations which will be accessed below.
    if abbreviations is None:
        abbreviations = {
            'foobar': 'fbr',
            'person': 'prsn',
            'number': 'nbr',
            'name': 'nm',
            'street': 'st',
            'address': 'adrs',
            'clean': 'cln'
        }

    # Get list of col names in original df.
    existing_columns = list(df)

    # Create list of new column names. Empty for now.
    new_column_names = []

    for col in existing_columns:
        # Iterate over the existing columns in original df.

        existing_col_name = col

        # Split this original column name into words. If column contains underscores,
        # split on underscores. Else split on spaces.
        if '_' in existing_col_name:
            split_character = '_'
        else:
            split_character = ' '

        existing_col_name_words = existing_col_name.split(split_character)

        # Create a list of new words for the new column name. Empty for now.
        new_col_name_words = []

        for word in existing_col_name_words:
            # Iterate over the original list of words in this column.

            abbreviation_found = False

            # For this word in the original column name, iterate over each word in our
            # abbreviations dictionary.
            for key, value in abbreviations.items():

                # Test if this word in the original column is the same as a key word in
                # the abbreviations dictionary.
                if word == key:
                    # This word in the original column is in the abbreviations dict.

                    # The new word (abbreviation) from the dict.
                    new_word = abbreviations[key]

                    # Add the new word (abbreviation) to the new list of words for this
                    # column.
                    new_col_name_words.append(new_word)

                    # Set flag indicating we found an abbreviation for this word in the
                    # new column.
                    abbreviation_found = True

            # Test if we found an abbreviation for this word in the original column name.
            if not abbreviation_found:
                # We did NOT find an abbreviation for this word in the original col name.

                # Append the *original* word for the column to the set of new words for
                # the column.
                new_col_name_words.append(word)

        # Now that we have gone through all original words in this col and replaced those
        # that had abbreviations with the given abbreviation OR just replaced the original
        # word with itself, take this set of "new" words and join them into a new name for
        # the col.
        new_col_name = split_character.join(new_col_name_words)

        # Append the *new* column name to the running set of new column names.
        new_column_names.append(new_col_name)

    # Take the original list of col names for the df and the new list of col names for the
    # df and zip them together. Take the zip object and place it into a dictionary that
    # can be used to rename the df cols.
    col_rename_mapping = dict(zip(existing_columns, new_column_names))

    # Rename the original df cols using the new mapping and return the new df.
    new_df = df.rename(columns=col_rename_mapping)

    # Convert the new df to markdown (a string).
    markdown_string_for_display = new_df.to_markdown(tablefmt='grid')

    # Get the width of the markdown after shortening the col names by using abbreviations.
    markdown_first_line_len = markdown_string_for_display.find('\n')

    # Next check the width of each column header and if the width of the given column
    # header is greater than the max width of the contents of the column. If so, wrap the
    # column header to the width of the contents of the column.
    for col in list(new_df):

        # Get the width of this column header.
        col_header_width = len(col)

        # Get the max width of the contents of this col.
        max_col_width = new_df[col].str.len().max()

        if col_header_width > max_col_width:
            # The width of the column header is greater than the max width of the contents
            # of the column.

            # Because column names may have words separated by underscores instead of
            # spaces, conditionally first replace all underscores with spaces.
            if '_' in col:
                new_col_name = col.replace('_', ' ')
            else:
                new_col_name = col

            # Wrap the column header to the width of the contents of the column.
            new_col_name = '\n'.join(
                textwrap.wrap(text=new_col_name, width=max_col_width)
            )

            # Conditionally replace the spaces with underscores.
            if '_' in col:
                new_col_name = new_col_name.replace(' ', '_')

            # Replace the original column name with the wrapped column name.
            new_df = new_df.rename(columns={col: new_col_name})

    # If the width of the markdown is greater than 115 characters, wrap all of the df
    # columns at 99.5 percent of the width of the widest col and then test if the width of
    # the markdown is less than or equal to 115 characters. If not, decrease n by 1/2 of 1
    # percent and wrap cells again and test markdown width again. Repeat until markdown
    # width is less than or equal to 115 characters.
    n_percent = 99.5
    while markdown_first_line_len > desired_width:

        # Start by getting the greatest width of all cols. Set to 0 since we don't know
        # the greatest width yet.
        greatest_width = 0

        # Iterate over all cols
        for col in list(new_df):

            # Get the max width of the contents of this col.
            this_col_width = new_df[col].str.len().max()

            # If this col is longer than all other cols so far, use its width as the max
            # width.
            if this_col_width > greatest_width:
                greatest_width = this_col_width

        # Function to wrap each col at n percent of the greatest width. Returns a new
        # series for the given coll
        def wrap_col_at_n_pct_of_widest_col(this_col):

            percent_as_decimal = n_percent / 100

            new_wrap_length = round(greatest_width * percent_as_decimal)

            return this_col.str.wrap(new_wrap_length)

        # Wrap all columns to the given width.
        new_df = new_df.apply(lambda c: wrap_col_at_n_pct_of_widest_col(c))
        markdown_string_for_display = new_df.to_markdown(tablefmt='grid')

        # Get the width of the markdown after wrapping the cols.
        markdown_first_line_len = markdown_string_for_display.find('\n')

        # Decrease n by 1/2 of 1 percent.
        n_percent = n_percent - 0.5

    return markdown_string_for_display
