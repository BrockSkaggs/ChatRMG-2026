import dash_mantine_components as dmc
from dash import dcc, html

from logs import get_logger

logger = get_logger(__name__)


def generate_information_modal(information_modal_id="information-modal"):
    information_modal = dmc.Modal(
        id=information_modal_id,
        title="ChatRMG Information",
        size="xl",
        children=[
            html.H2("About ChatRMG"),
            html.P(
                "ChatRMG is a chat application which utilizes AI models and local company data to answer questions."
            ),
            html.H5("Primary Features"),
            dcc.Markdown(
                """
                - **Chat Interface**: Simple UI and UX for users to interact with the chatbot.
                - **Multiple AI Models**: Pick from a variety of AI models each with accesss to different data sources.
                - **Stored Conversations**: Conversations are stored in a database and can be retrieved later.
                - **User Feedback**: Users can provide feedback on the conversations to help improve ChatRMG.
                """
            ),
            # html.Hr(),
            # html.H4("How to Use DashGPT"),
            # # insert a image of the chat interface
            # html.Img(
            #     src="/assets/images/getting-started-guide.png",
            #     style={"width": "100%", "height": "100%"},
            # ),
        ],
    )

    return information_modal
