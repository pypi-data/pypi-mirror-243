# pandasfruit

Takes in a pandas dataframe and returns a string containing markdown format where the width of the markdown text is more narrow and is suitable for printing. A more narrow table can fit on a printed page, such as a PDF generated from a Jupyter notebook.

Takes in an optional width parameter (number of characters) and will make the resulting markdown this wide. Else will use a default width of 115.

Also will use a default dictionary of words/abbreviations to shorten column names using the abbreviations instead of the original words. Alternatively, a  user-defined dictionary may be passed in.

See project documentation for more details.
