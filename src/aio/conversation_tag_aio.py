from dash import html, Input, Output, State, clientside_callback, MATCH, callback, no_update
from dash_bootstrap_components import Collapse
from dash_iconify import DashIconify
from dash_mantine_components import Button, ButtonGroup, TextInput, Textarea
import uuid

from langgraph.checkpoint.postgres import PostgresSaver
from common import gen_postgres_conn_str

from common import chatrmg_engine, create_alchemy_session, get_central_time
from layout.chat_ui import gen_thumbs_btn_gradient
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

        thumbs_up_btn = lambda aio_id: {
            'component': 'ConversationTagAIO',
            'subcomponent': 'thumbs_up_btn',
            'aio_id': aio_id
        }

        thumbs_down_btn = lambda aio_id: {
            'component': 'ConversationTagAIO',
            'subcomponent': 'thumbs_down_btn',
            'aio_id': aio_id
        }

        negative_feedback_collapse = lambda aio_id: {
            'component': 'ConversationTagAIO',
            'subcomponent': 'negative_feedback_collapse',
            'aio_id': aio_id
        }

        negative_feedback_textarea = lambda aio_id: {
            'component': 'ConversationTagAIO',
            'subcomponent': 'negative_feedback_textarea',
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
        with create_alchemy_session(chatrmg_engine) as session:
            app_info = session.query(CheckpointAppInfo).filter_by(thread_id=aio_id).first()
            create_on_txt = ''
            if app_info and app_info.thread_name:
                button_label = app_info.thread_name
                create_on_txt = app_info.created_on_local.strftime("%Y-%m-%d %H:%M:%S")
            else:
                button_label = aio_id
            create_txt = f"Created on: {create_on_txt}" if create_on_txt else "Creation date unknown"

            thumb_up_grad = gen_thumbs_btn_gradient('up', app_info.positive_feedback)
            thumb_dn_grad = gen_thumbs_btn_gradient('down', app_info.positive_feedback) 
            open_neg_feedback_collase = app_info.positive_feedback == False and app_info.negative_feedback_note   
            
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
                            id=self.ids.name_input(aio_id),
                            w="calc(100% - 160px)"
                        ),
                        Button(
                            DashIconify(icon="octicon:thumbsup-16"),
                            id=self.ids.thumbs_up_btn(aio_id),
                            variant="gradient",
                            gradient=thumb_up_grad,
                            radius="xl",
                            style={
                                "margin-right": "3px",
                                "margin-left": "auto",
                                "margin-top": "5px",
                                "width": "40px",
                            },
                            size='compact-md',
                            n_clicks=0,
                            className='ml-2 mr-2'
                        ),
                        Button(
                            DashIconify(icon="octicon:thumbsdown-16"),
                            id=self.ids.thumbs_down_btn(aio_id),
                            variant="gradient",
                            gradient=thumb_dn_grad,
                            radius="xl",
                            style={
                                "margin-top": "5px",
                                "width": "40px",
                            },
                            size='compact-md',
                            n_clicks=0,
                        )
                    ], className='mt-1 d-flex'),
                    Collapse(
                        id=self.ids.negative_feedback_collapse(aio_id),
                        is_open=open_neg_feedback_collase,
                        children=[
                            Textarea(
                                id=self.ids.negative_feedback_textarea(aio_id),
                                placeholder='Please provide additional feedback...',
                                style={'width': '100%', 'margin-top': '10px'},
                                value=app_info.negative_feedback_note if app_info and app_info.negative_feedback_note else ''
                            )
                        ]
                    ),
                    html.Div([
                        html.Span(create_txt, className='text-muted mt-1'),
                        Button('Save', variant='outline', id=self.ids.save_name_btn(aio_id), style={'margin-left': 'auto'})
                    ], className='mt-1 d-flex'),
                ], id=self.ids.edit_collapse(aio_id), is_open=False)
            ], className='mb-3', id=self.ids.tag_container(aio_id))
    
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
        State(ids.thumbs_up_btn(MATCH), 'gradient'),
        State(ids.thumbs_down_btn(MATCH), 'gradient'),
        State(ids.negative_feedback_textarea(MATCH), 'value'),
        prevent_initial_call=True,
    )
    def update_conversation(n_clicks, new_name, edit_collapse_id, 
                                 thumbs_up_gradient, thumbs_down_gradient, negative_feedback):
        cond_new_name = no_update
        with create_alchemy_session(chatrmg_engine) as session:
            thread_id = edit_collapse_id['aio_id']
            app_info = session.query(CheckpointAppInfo).filter_by(thread_id=thread_id).first()
            if app_info:
                if new_name and new_name.strip():
                    cond_name = new_name.strip()
                    app_info.thread_name = cond_name
                    cond_new_name = cond_name
                if thumbs_up_gradient['from'] == 'green':
                    app_info.positive_feedback = True
                    app_info.negative_feedback_note = None
                elif thumbs_down_gradient['from'] == 'red':
                    app_info.positive_feedback = False
                    app_info.negative_feedback_note = negative_feedback.strip() if negative_feedback and negative_feedback.strip() else None
                elif thumbs_down_gradient['from'] == 'grey' and thumbs_up_gradient['from'] == 'grey':
                    app_info.positive_feedback = None
                    app_info.negative_feedback_note = None
                session.commit()
            else:
                raise Exception("ConversationTagAIO: Unable to find CheckpointAppInfo to update conversation info.")
        return cond_new_name, False
    
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

        with create_alchemy_session(chatrmg_engine) as session:
            app_info = session.query(CheckpointAppInfo).filter_by(thread_id=thread_id).first()
            if app_info:
                session.delete(app_info)
                session.commit()
            else:
                raise Exception("ConversationTagAIO: Unable to find CheckpointAppInfo to delete conversation.")

        return {'display': 'none'} #Hide the button after deletion
    
    @callback(
        Output(ids.thumbs_down_btn(MATCH), 'gradient', allow_duplicate=True),
        Output(ids.thumbs_up_btn(MATCH), 'gradient', allow_duplicate=True),
        Output(ids.negative_feedback_collapse(MATCH), 'is_open', allow_duplicate=True),
        Output(ids.negative_feedback_textarea(MATCH), 'value', allow_duplicate=True),
        Input(ids.thumbs_down_btn(MATCH), 'n_clicks'),
        State(ids.thumbs_down_btn(MATCH), 'gradient'),
        prevent_initial_call=True,
    )
    def handle_thumbs_down(clicks, current_gradient):
        target_grad = gen_thumbs_btn_gradient('down', current_gradient['from'] != 'grey' )
        text_area = "" if target_grad['from'] in  ['grey'] else no_update
        return (
            target_grad,
            {"from": "grey", "to": "grey"},
            True, 
            text_area
        )

    @callback(
        Output(ids.thumbs_up_btn(MATCH), 'gradient', allow_duplicate=True),
        Output(ids.thumbs_down_btn(MATCH), 'gradient', allow_duplicate=True),
        Output(ids.negative_feedback_collapse(MATCH), 'is_open', allow_duplicate=True),
        Output(ids.negative_feedback_textarea(MATCH), 'value', allow_duplicate=True),
        Input(ids.thumbs_up_btn(MATCH), 'n_clicks'),
        State(ids.thumbs_up_btn(MATCH), 'gradient'),
        prevent_initial_call=True,
    )
    def handle_thumbs_up(clicks, current_gradient):
        target_grad = gen_thumbs_btn_gradient('up', current_gradient['from'] == 'grey' )
        text_area = "" if target_grad['from'] in ['green', 'grey'] else no_update

        return (
            target_grad,
            {"from": "grey", "to": "grey"},
            False, 
            text_area
        )