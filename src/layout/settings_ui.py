import dash_bootstrap_components as dbc
from aio.chat_settings_aio import ChatSettingsAIO


def generate_settings_offcanvas(settings_offcanvas_id="settings-offcanvas"):
    settings_offcanvas = dbc.Offcanvas(
        children=[
            ChatSettingsAIO("settings-aio")
        ],
        id=settings_offcanvas_id,
        title="ChatRMG Settings",
        is_open=False,
        backdrop=True,
    )

    return settings_offcanvas