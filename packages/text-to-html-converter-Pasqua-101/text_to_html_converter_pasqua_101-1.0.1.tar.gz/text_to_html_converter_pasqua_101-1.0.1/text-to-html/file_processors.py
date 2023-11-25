import os
import re
import sys

from . import helper as h


def text_to_html(
    input_path, stylesheet, output_dir, lang, sidebar=None
):  # Takes in all arguments from the command line
    try:
        if os.path.exists(input_path) and os.path.isdir(
            input_path
        ):  # if the user inputted a directory
            h.remove_output_dir(output_dir)
            for filename in os.listdir(input_path):
                extension_check = h.extension_checker(
                    filename
                )  # loops through each file in the directory to check their extension.
                # Returns True if the extensions matches
                if extension_check:
                    input_file = os.path.join(input_path, filename)
                    output_file = h.output_file_creator(input_file, output_dir)

                    # Step 1: if the created output file already exists generate a duplicate
                    if os.path.exists(output_file):
                        output_file = h.generate_duplicate_filename(
                            output_dir, output_file
                        )

                    # Step 2: Start the conversion of the file
                    html_contents = html_processor(
                        input_file, stylesheet, lang, sidebar
                    )

                    # Step 3: Checks to see if the processed input file is a markdown file,
                    # if it is convert any missed Markdown syntax
                    if input_file.endswith(".md"):
                        html_contents = parse_md(html_contents)

                    # Step 4: Write to HTML contents to the output file
                    write_to_html(output_file, html_contents)

            sys.exit(0)

        elif h.extension_checker(input_path) and os.path.isfile(
            input_path
        ):  # if the user enters only a file
            h.remove_output_dir(output_dir)

            input_file = input_path
            output_file = h.output_file_creator(input_file, output_dir)

            # Step 1: Start the conversion of the file
            html_contents = html_processor(input_file, stylesheet, lang, sidebar)

            # Step 2: Checks to see if the processed input file is a markdown file,
            # if it is convert any missed Markdown syntax
            if input_file.endswith(".md"):
                html_contents = parse_md(html_contents)

            # Step 3: Write to HTML contents to the output file
            write_to_html(output_file, html_contents)

            sys.exit(0)

        else:  # if the file/folder entered does not exist print error message
            print(
                "The file/directory name does not exist. Please make sure you entered the correct name"
            )
            sys.exit(-1)

    except Exception as e:  # Throw an error if any kind of error happens
        raise Exception(f"An error occurred: {str(e)}")


def parse_md(html_contents):
    html_contents = re.sub(
        r"\[(.+?)\]\(([^ ]+)\)",  # Regex pattern to match .md link syntax and capture the text to display / the link
        r"<a href=\2>\1</a>",  # Replace all .md links with <a> tags with help from backreferences
        html_contents,
    )

    html_contents = re.sub(
        r"(`{1,3})(.*?)\1", r"<code>\2</code>", html_contents
    )  # Regex to spot code tag in Markdown and convert it to code in HTML

    html_contents = re.sub(
        r"---+", r"<hr>", html_contents
    )  # Regex to spot horizontal rule in Markdown and convert it to HTML

    html_contents = re.sub(
        r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html_contents
    )  # Regex to spot bold in Markdown and convert the text inside it (group 1) to HTML

    return html_contents


def html_processor(input_file, stylesheet, lang, sidebar):
    html_contents = h.html_creator(input_file, stylesheet, lang, sidebar)

    with open(input_file) as file:
        lines = file.readlines()

    in_paragraph = False  # Flag to track if we are inside a paragraph
    for line in lines:
        if (
            not in_paragraph
        ):  # if in_paragraph is set to False, create the beginning of the p tag in html_contents
            # and set in_paragraph to true
            html_contents += "\t\t<p>"
            in_paragraph = True
        if (
            line == "\n"
        ):  # if the current line is a newline close the p tag and append it to then set in_paragraph to False
            html_contents += "</p>\n"
            in_paragraph = False
        else:  # if the code is still in a line with text and is in a paragraph append the line to html_contents
            converted_line = line.replace("\n", "")
            html_contents += f" {converted_line}"
    # Closing the last paragraph if the loop was still in the paragraph when finished
    if in_paragraph:
        html_contents += "</p>\n"

    html_contents += "\t</body>\n</html>"

    return html_contents


def write_to_html(output_file, html_contents):
    with open(output_file, "w") as html:
        html.write(html_contents)
