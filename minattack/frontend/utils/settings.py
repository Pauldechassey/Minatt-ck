from minattack.frontend.utils import settings


def init_globals():
    global SELECTED_AUDIT_ID
    global SELECTED_AUDIT_STATE
    SELECTED_AUDIT_ID = -1
    SELECTED_AUDIT_STATE = -1


def set_AUDIT_STATE(new_state: int):
    try:
        if new_state < 0 and new_state > 4:
            settings.SELECTED_AUDIT_STATE = new_state
        else:
            raise Exception("ERROR : Cannot set a state < 0 and > 4")
    except Exception as e:
        print(e)


def load_image():
    global LOGO_PRINCIPAL
    global LOGO_WINDOW
    global LOGO_DECONNEXION
    LOGO_PRINCIPAL = ":/images/logo.png"
    LOGO_WINDOW = ":/images/icon_app.png"
    LOGO_DECONNEXION = ":/images/deconnexion.png"
