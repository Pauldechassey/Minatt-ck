from minattack.frontend.utils import settings


def init_globals():
    global SELECTED_AUDIT_ID
    global SELECTED_AUDIT_STATE
    global SELECTED_RAPPORT_PATH
    SELECTED_AUDIT_ID = -1
    SELECTED_AUDIT_STATE = -1
    SELECTED_RAPPORT_PATH = ""


def load_image():
    global LOGO_PRINCIPAL
    global LOGO_WINDOW
    global LOGO_DECONNEXION
    LOGO_PRINCIPAL = ":/images/logo.png"
    LOGO_WINDOW = ":/images/icon_app.png"
    LOGO_DECONNEXION = ":/images/deconnexion.png"
