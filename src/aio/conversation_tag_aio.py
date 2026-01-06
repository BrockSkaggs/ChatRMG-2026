from dash import html, Input, Output, State, clientside_callback, MATCH, callback, no_update
from dash_bootstrap_components import Collapse
from dash_mantine_components import Button, ButtonGroup, TextInput
import uuid

class ConversationTagAIO(html.Div):
    
    class ids:
        conversation_btn = lambda aio_id: {
            'component': 'ConversationTagAIO',
            'subcomponent': 'conversation_btn',
            'aio_id': aio_id 
        }

        edit_btn = lambda aio_id: {
            'component': 'ConversationTagAIO',
            'subcomponent': 'edit_btn',
            'aio_id': aio_id 
        }

        edit_collapse = lambda aio_id: {
            'component': 'ConversationTagAIO',
            'subcomponent': 'edit_collapse',
            'aio_id': aio_id 
        }

        name_input = lambda aio_id: {
            'component': 'ConversationTagAIO',
            'subcomponent': 'name_input',
            'aio_id': aio_id 
        }

        save_name_btn = lambda aio_id: {
            'component': 'ConversationTagAIO',
            'subcomponent': 'save_name_btn',
            'aio_id': aio_id        
        }

    ids = ids

    #Use the conversation id as the aio_id
    def __init__(self, aio_id=None):
        if aio_id is None:
            aio_id = str(uuid.uuid4())
        
        super().__init__(
            id=f"ConversationTagAIO{aio_id}",
            children=[self._gen_layout(aio_id)]
        )

    def _gen_layout(self, aio_id: str):
        return html.Div([
            ButtonGroup([
                Button(aio_id, variant='outline', id=self.ids.conversation_btn(aio_id)),
                Button('Edit', variant='outline', id=self.ids.edit_btn(aio_id))
            ]),
            Collapse([
                html.Div([
                    TextInput(
                        placeholder='Conversation name...',
                        id=self.ids.name_input(aio_id)
                    ),
                    Button('Save', variant='outline', id=self.ids.save_name_btn(aio_id))
                ], className='mt-1 d-flex')                
            ], id=self.ids.edit_collapse(aio_id), is_open=False)
        ], className='mb-2')
    
    clientside_callback(
        """
        function(n_clicks, is_open) {
            return !is_open;
        }
        """,
        Output(ids.edit_collapse(MATCH), 'is_open', allow_duplicate=True),
        Input(ids.edit_btn(MATCH), 'n_clicks'),
        State(ids.edit_collapse(MATCH), 'is_open'),
        prevent_initial_call=True,
    )


    @callback(
        Output(ids.conversation_btn(MATCH), 'children'),
        Output(ids.edit_collapse(MATCH), 'is_open'),
        Input(ids.save_name_btn(MATCH), 'n_clicks'),
        State(ids.name_input(MATCH), 'value'),
        prevent_initial_call=True,
    )
    def update_conversation_name(n_clicks, new_name):
        if new_name and new_name.strip():
            #TODO: Will need to persist this to a data store.
            return new_name.strip(), False
        return no_update, no_update