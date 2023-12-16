import dash
import dash_mantine_components as dmc
import dash_extensions as de

url = 'https://lottie.host/29e771b3-aef8-4a55-ac77-ecfc86022513/GcDkfJmtXj.json'
options = dict(loop=True, autoplay=True)

dash.register_page(
    __name__,
    path="/404",
    title='Mental Health | Not Found'
)


layout = dmc.Container(
    [
        de.Lottie(
            url=url,
            options=options,
            isClickToPauseDisabled=True,
            width='550px',
        )
    ],
    style={
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',
        'height': '70vh',
    },
)