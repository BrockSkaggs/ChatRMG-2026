import os

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import html
from typing import Literal, Optional

from logs import get_logger

logger = get_logger(__name__)

def generate_chat_controls(
    text_input_id="text-prompt", submit_button_id="submit-prompt"
):
    chat_controls = dbc.InputGroup(
        children=[
            dbc.Textarea(
                id=text_input_id,
                placeholder="Ask me a question...",
                debounce=True,
                style={
                    "border-top-right-radius": 0,
                    "border-bottom-right-radius": 0,
                    "border-top-left-radius": "25px",
                    "border-bottom-left-radius": "25px",
                    "resize": "none",  # Disable textarea resizing by users
                    "overflow-y": "auto",  # Enable vertical scrolling when needed
                },
            ),
            dbc.InputGroupText(
                dmc.Button(
                    DashIconify(icon="mingcute:send-plane-fill"),
                    id=submit_button_id,
                    variant="filled",
                    color='blue',
                    radius="xl",
                    style={"margin-right": "0px", "margin-left": "5px"},
                ),
                # ensure the button is tight within the input group
                style={
                    "padding": "0px",
                    "border-top-right-radius": "25px",
                    "border-bottom-right-radius": "25px",
                    "border-top-left-radius": 0,
                    "border-bottom-left-radius": 0,
                },
            ),
        ]
    )

    disclaimer_text = html.P(
        "Disclaimer: Information provided by DashGPT may be inaccurate; verify all information before use.",
        style={
            "font-size": "0.7rem",
            "font-style": "italic",
            "margin-top": "3px",
            "margin-left": "5px",
            "margin-right": "5px",
            "margin-bottom": "0px"
        },
    )

    chat_controls_with_disclaimer = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(chat_controls, width=12),  # Adjust the width as needed
                    dbc.Col(disclaimer_text, width=12),  # Adjust the width as needed
                ]
            ),
        ]
    )

    return chat_controls_with_disclaimer

def generate_user_textbox(text, name="You"):
    style = {
        "max-width": "80%",
        "width": "max-content",
        "padding": "0px 0px",
        "border-radius": 25,
        "margin-bottom": 20,
    }

    style["margin-left"] = "auto"
    style["margin-right"] = 0

    return dbc.Card(text, style=style, body=True, color="#228be6", inverse=True)

def generate_ai_textbox(output_id, text=""):
    style = {
        "max-width": "80%",
        "width": "max-content",
        "padding": "0px 0px",
        "border-radius": 25,
        "margin-bottom": 20,
    }

    style["margin-left"] = 0
    style["margin-right"] = "auto"
    style['white-space'] = 'pre-line'

    para = html.P(text, id=output_id) if output_id is not None else html.P(text)

    textbox = dbc.Card(
        [para],
        style=style,
        body=True,
        color="lightblue",
        inverse=False,
    )

    return html.Div([textbox])

def generate_related_content_accordion(unique_docs, id="related-source-accordion"):
    # loop to build the anchor/buttons
    related_content = []
    for related_doc in unique_docs:
        # make a markdown element and but the related_doc.page_content in it with an html.HR() below it
        related_content.append(
            html.Div(
                [
                    html.Hr(),
                    html.Strong(f"Source: {related_doc['metadata'].get('source', 'Unknown Source')} Page: {related_doc['metadata'].get('page', 'N/A')}"),
                    html.P(
                        related_doc['page_content'],
                        style={"margin-bottom": "0px"},
                    ),
                ]
            )
        )

    related_sources = dmc.Accordion(
        children=[
            dmc.AccordionItem(
                value="related-topics",
                children=[
                    dmc.AccordionControl("References"),
                    dmc.AccordionPanel(children=related_content),
                ],
            )
        ],
        id=id,
    )

    return related_sources

def gen_thumbs_btn_gradient(thumb: Literal['up', 'down'], is_positive: Optional[bool] = None) -> dmc.Button:
    neutral = {'from': 'grey', 'to': 'grey'}
    if is_positive is None:
        return neutral
    if thumb == 'up' and is_positive:
        return {"from": "green", "to": "#32cd32"}
    elif thumb == 'down' and not is_positive:
        return {"from": "red", "to": "#dc143c"}
    return neutral