from dash import html
from dash_bootstrap_components import Select
import uuid

class ChatSettingsAIO(html.Div):
    
    class ids:
        model_select = lambda aio_id: {
            'component': 'ChatSettingsAIO',
            'subcomponent': 'model_select',
            'aio_id': aio_id 
        }

        conversation_div = lambda aio_id: {
            'component': 'ChatSettingsAIO',
            'subcomponent': 'conversation_div',
            'aio_id': aio_id 
        }
    
    ids = ids

    def __init__(self, aio_id=None):
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        super().__init__(
            id=f"ChatSettingsAIO{aio_id}",
            children=[self._gen_layout(aio_id)]
        )

    def _gen_layout(self, aio_id: str):
        return html.Div([
            html.H6('Select Model'),
            Select(
                id=self.ids.model_select(aio_id),
                options=[
                    {"label": "Information Technology", "value": "it-rag"},
                    {"label": "Multiplier", "value": "multiplier"}
                ],
                value='multiplier',
            ),
            html.Hr(),
            html.H6('Chat History'),
            html.Div([], id=self.ids.conversation_div(aio_id))
        ])
