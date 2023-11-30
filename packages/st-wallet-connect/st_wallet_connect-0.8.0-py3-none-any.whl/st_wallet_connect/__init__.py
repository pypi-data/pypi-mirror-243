import streamlit.components.v1 as components
import os
import streamlit as st

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True

if not _RELEASE:
    _st_wallet_connect = components.declare_component(
        "st_wallet_connect",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _st_wallet_connect = components.declare_component("st_wallet_connect", path=build_dir)



def web3Modal(
    key=None,
    default="connect",
    img_path=None,
    componentHeight=None,
    button_text=None,
    provider="MetaMask",  # 3 Provider MetaMask , walletConnect , coinbase   
    amount=None,
    recipient=None,
    message=None,
    contractAddress=None,
    contractABI=None,
):
    provider = provider.upper()
    component_value = _st_wallet_connect(
        key=key,
        default=default,
        img_path=img_path,
        componentHeight=componentHeight,
        button_text=button_text,
        provider=provider,
        amount=amount,
        recipient=recipient,
        message=message,
        contractAddress=contractAddress,
        contractABI=contractABI
    )
    return component_value


# hide_streamlit_style = """
# <style> MainMenu {visibility: hidden;}
# footer {display: none !important}
# iframe {height: 10vh !important;}
# iframe {width: 35vh !important;}
# .css-z5fcl4 {padding: 0px !important}
# .css-13f0yma {gap: 0px !important}
# .main + div + div + div {gap: 0px !important}
# .css-18ni7ap {visibility: hidden;}
# .css-164nlkn {display: none;}
# .e1tzin5v0 {gap: 0px !important;}
# .css-18e3th9 {padding: 0;}
# .css-qri22k {display: none;}
# .css-k1vhr4 {overflow: unset !important;}
# </style> """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)


#monkeypatch streamlit
st.wallet_connect = web3Modal