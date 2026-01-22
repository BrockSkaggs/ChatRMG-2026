from dash import html, Input, Output, State, clientside_callback, MATCH, callback, no_update
from dash_bootstrap_components import Collapse
from dash_mantine_components import Button, ButtonGroup, TextInput, HoverCard, HoverCardTarget, HoverCardDropdown, Text
import uuid

from langgraph.checkpoint.postgres import PostgresSaver
from common import gen_postgres_conn_str

from common import dashgpt_engine, create_alchemy_session, get_central_time
from orm_models.checkpoint_app_info import CheckpointAppInfo

#TODO: Add delete conversation/thread functionality - https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.postgres.PostgresSaver.delete_thread
#TODO: Add ability for user to see creation date

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

        delete_btn = lambda aio_id: {
            'component': 'ConversationTagAIO',
            'subcomponent': 'delete_btn',
            'aio_id': aio_id
        }

        tag_container = lambda aio_id: {
            'component': 'ConversationTagAIO',
            'subcomponent': 'tag_container',
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
        with create_alchemy_session(dashgpt_engine) as session:
            app_info = session.query(CheckpointAppInfo).filter_by(thread_id=aio_id).first()
            create_on_txt = ''
            if app_info and app_info.thread_name:
                button_label = app_info.thread_name
                create_on_txt = app_info.created_on_local.strftime("%Y-%m-%d %H:%M:%S")
            else:
                button_label = aio_id
            create_txt = f"Created on: {create_on_txt}" if create_on_txt else "Creation date unknown"

        return html.Div([
            ButtonGroup([                
                Button(button_label, variant='outline', id=self.ids.conversation_btn(aio_id), style={'flex':'1'}),
                Button('Edit', variant='outline', id=self.ids.edit_btn(aio_id), w=80),
                Button('Delete', variant='outline', id=self.ids.delete_btn(aio_id), w=80)
            ], w='100%', style={'display':'flex'}),
            Collapse([
                html.Div([
                    TextInput(
                        placeholder='Conversation name...',
                        id=self.ids.name_input(aio_id)
                    ),
                    Button('Save', variant='outline', id=self.ids.save_name_btn(aio_id))
                ], className='mt-1 d-flex'),
                html.Span(create_txt, className='text-muted mt-1')
            ], id=self.ids.edit_collapse(aio_id), is_open=False)
        ], className='mb-2', id=self.ids.tag_container(aio_id))
    
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
        State(ids.edit_collapse(MATCH), 'id'),
        prevent_initial_call=True,
    )
    def update_conversation_name(n_clicks, new_name, edit_collapse_id):
        if new_name and new_name.strip():
            cond_new_name = new_name.strip()
            thread_id = edit_collapse_id['aio_id']
            with create_alchemy_session(dashgpt_engine) as session:
                app_info = session.query(CheckpointAppInfo).filter_by(thread_id=thread_id).first()
                if app_info:
                    app_info.thread_name = cond_new_name
                else:
                    raise Exception("ConversationTagAIO: Unable to find CheckpointAppInfo to update conversation name.")                    
                session.commit()            
            return cond_new_name, False
        return no_update, no_update
    
    @callback(
        Output(ids.tag_container(MATCH), 'style'),
        Input(ids.delete_btn(MATCH), 'n_clicks'),
        State(ids.delete_btn(MATCH), 'id'),
        prevent_initial_call=True,
    )
    def delete_conversation(_, del_btn_id):
        thread_id = del_btn_id['aio_id']
        with PostgresSaver.from_conn_string(gen_postgres_conn_str(False)) as checkpointer:
            checkpointer.delete_thread(thread_id)

        with create_alchemy_session(dashgpt_engine) as session:
            app_info = session.query(CheckpointAppInfo).filter_by(thread_id=thread_id).first()
            if app_info:
                session.delete(app_info)
                session.commit()
            else:
                raise Exception("ConversationTagAIO: Unable to find CheckpointAppInfo to delete conversation.")

        return {'display': 'none'} #Hide the button after deletion