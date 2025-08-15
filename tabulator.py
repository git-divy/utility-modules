import prettytable

html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Export</title>
    
    <!-- Modern font from Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;700&display=swap" rel="stylesheet">
    
    <style>
        body {{
            background-color: #121212;
            color: #eaeaea;
            font-family: 'Fira Code', monospace;
            
        }}

        pre {{
            font-size: 1rem; /* Larger font size */
            line-height: 1.6;
            background: #1e1e1e;
            padding: 20px;
            border-radius: 10px;
            overflow-x: auto;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        }}
    </style>
</head>
<body>
    <pre>{0}</pre>
</body>
</html>
"""


def tabulate(
    datax,
    width=25,
    pagination=False,
    result_perpage_on_pagination=25,
    dump=False,
    export=False,
):
    if len(datax) == 0:
        datax = [{"NO DATA": "-"}]
    flag = False
    if pagination and len(datax) > result_perpage_on_pagination:
        data = datax[:result_perpage_on_pagination]
        datax = datax[result_perpage_on_pagination:]
        flag = True
    else:
        data = datax

    if isinstance(data, dict):
        data = [data]
    keys = list(data[0].keys())
    table = prettytable.PrettyTable()
    table.field_names = list(keys)

    for item in data:

        row = []
        for key in keys:
            value = item.get(key, None)
            if value is None:
                value = "-"
            str_val = ""

            if isinstance(value, list):
                str_val = ", ".join(map(str, value))
            else:
                str_val = str(value)

            if len(str_val) <= (len(key) + width):
                row.append(str_val)
            else:
                row.append(str_val[: len(key) + width - 3] + "...")

        table.add_row(row)

    table.align = "l"
    if dump:
        return table.get_string()
    else:
        print(table)

    if export:
        with open(f"export.html", "w") as fl:
            fl.write(html.format(table))

    if flag:
        try:
            input("Press Enter for Next Page --> ")
        except KeyboardInterrupt as k:
            print("Keyboard Interrupt")
            exit()
        tabulate(datax, width, pagination, result_perpage_on_pagination)
