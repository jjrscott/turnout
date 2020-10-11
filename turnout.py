import argparse
import json
import os
import re

parser = argparse.ArgumentParser(description="Turnout converts a JSON file representing a vote into a square chart.",
epilog="""

JSON files have the format:

{
  "choices": [
    {
      "color": "<SVG color value>",
      "title": "<First place>",
      "value": <First place percentage or absolute count>
    },
    {
      "color": "<SVG color value>",
      "title": "<Second place>",
      "value": <Second place percentage or absolute count>
    }
  ],
  "title": "<title of chart>",
  "total": <Total elegible to vote. Choice values will be treated as an absolute count>
  "turnout": <Percentage of those eligible to vote who did so. Choice values will be treated as percentage>
}

See the examples folder for examples.

""",
                             formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('input_path', nargs='+', help="")
parser.add_argument('-output', help="location of resulting SVG files (default: same as source)")
parser.add_argument('-size', default=600, type=int, help="Size of the SVG file canvas (default: 600)")

args = parser.parse_args()

canvas_size = args.size
chart_size = canvas_size / 1200 * 1000
chart_padding = (canvas_size - chart_size) / 2
small_size = max(2, chart_size/1000 * 10)
stroke_width = max(1, chart_size/1000 * 6)


def svg_rect(*args, **kwargs):
    buffer = ""
    buffer += "<rect"
    for key in kwargs:
        buffer += ' %s="%s"' % (key.replace('_', '-'), kwargs[key])
    buffer += " />"
    return buffer

def svg_text(*args, **kwargs):
    if canvas_size <= 100:
        return ""
    buffer = ""
    buffer += "<text"
    for key in kwargs:
        buffer += ' %s="%s"' % (key.replace('_', '-'), kwargs[key])
    buffer += ">"
    buffer += " ".join(args)
    buffer += "</text>"
    return buffer

for input_path in args.input_path:
    with open(input_path, 'r') as file:
        data=json.load(file)

    with open(input_path, 'w') as file:
        json.dump(data, file, sort_keys=True, indent=4)

    if 'total' in data:
        votes = 0
        for choice in data['choices']:
            votes += choice['value']
        for choice in data['choices']:
            choice['value'] = choice['value'] / votes
        data['turnout'] = votes / data['total']
    else:
        for choice in data['choices']:
            choice['value'] /= 100
        data['turnout'] /= 100

    output_path = os.path.splitext(input_path)[0] + '.svg'

    if args.output:
        output_path = os.path.join(args.output, os.path.basename(output_path))

    turnout_width = data['turnout']* chart_size + chart_padding
    absent_width = canvas_size - turnout_width

    output = """<?xml version="1.0" encoding="UTF-8"?>
    <svg viewBox="0 0 {canvas_size} {canvas_size}"  xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">

        <defs>
          <mask id="border">{border_mask}</mask>
          <mask id="turnout">{turnout_mask}</mask>
          <mask id="absent">{absent_mask}</mask>
        </defs>

        <rect width="{canvas_size}" height="{canvas_size}" fill="#F2F2F2" />


    """.format(canvas_size = canvas_size,
                chart_size = chart_size,
                border_mask = svg_rect(x=chart_padding ,y=chart_padding, width=chart_size, height=chart_size, fill="white", rx=small_size),
                turnout_mask = svg_rect(x=0 ,y=0, width=turnout_width, height=canvas_size, fill="white"),
                absent_mask = svg_rect(x=turnout_width ,y=0, width=absent_width, height=canvas_size, fill="white"),
                )

    output += svg_text(data['title'],
                       x=canvas_size / 2,
                       y=chart_padding/2,
                       text_anchor="middle",
                       font_size=max(4, chart_size/1000 * 48),
                       font_weight="bold",
                       dominant_baseline="middle",
                       fill="#484848",
                       font_family="sans-serif")
    output += "\n"
    output += svg_text("VOTE SHARE",
                       x=0,
                       y=0,
                       text_anchor="middle",
                       transform="translate(%s %s) rotate(-90)" % (chart_padding/2, canvas_size/2),
                       font_size=max(3, chart_size/1000 * 18),
                       dominant_baseline="middle",
                       letter_spacing=max(1, chart_size/1000 * 5),
                       fill="#484848",
                       font_family="sans-serif")
    output += "\n"
    output += svg_text("TURNOUT",
                       x=canvas_size / 2,
                       y=canvas_size - chart_padding/2,
                       text_anchor="middle",
                       font_size=max(3, chart_size/1000 * 18),
                       dominant_baseline="middle",
                       letter_spacing=max(1, chart_size/1000 * 5),
                       fill="#484848",
                       font_family="sans-serif")
    output += "\n"
    output += svg_text("Graphics by jjrscott",
                       x=0,
                       y=0,
                       text_anchor="middle",
                       transform="translate(%s %s) rotate(-90)" % (canvas_size - chart_padding/2, canvas_size/2),
                       font_size=max(3, chart_size/1000 * 18),
                       dominant_baseline="middle",
                       fill="#484848",
                       font_family="sans-serif")
    output += "\n"
    y = chart_padding
    for choice in data['choices']:
        output += svg_rect(x=chart_padding,
                           y=y,
                           width=data['turnout'] * chart_size,
                           height = choice['value']* chart_size,
                           fill=choice['color'],
                           mask="url(#border)")

        output += "\n"
        if 'title' in choice:
            output += svg_text(
                choice['title'],
                x = (data['turnout']* chart_size + chart_padding + chart_padding)/2,
                y = y + choice['value']* chart_size/2, chart_padding = chart_padding,
                text_anchor="middle",
                font_size=max(3, chart_size/1000 * 36),
                dominant_baseline="middle",
                fill="#FFFFFFEE",
                font_weight="bold",
                font_family="sans-serif")
            output += "\n"
        y += choice['value']* chart_size

    output += svg_rect(x=chart_padding,
                       y=chart_padding,
                       width=chart_size,
                       height=chart_size,
                       fill="none",
                       rx=small_size,
                       stroke_width=stroke_width,
                       stroke="#484848",
                       mask="url(#turnout)")
    output += "\n"
    output += svg_rect(x=chart_padding,
                       y=chart_padding,
                       width=chart_size,
                       height=chart_size,
                       fill="none",
                       rx=small_size,
                       stroke_width=stroke_width,
                       stroke="#484848",
                       stroke_dasharray="{0} {0}".format(small_size),
                       mask="url(#absent)")
    output += "\n"
    output += "</svg>"
    output += "\n"

    with open(output_path, "w") as text_file:
        text_file.write(output)
