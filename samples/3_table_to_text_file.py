from outputty import Table
my_table = Table(from_csv='nice-software.csv')
my_table.to_text_file('nice-software.txt')
