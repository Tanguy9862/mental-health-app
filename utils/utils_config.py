# FIGURE:
FIG_CONFIG_WITHOUT_DOWNLOAD = {
    'displayModeBar': False,
    'scrollZoom': False,
    'showTips': False,
}

FIG_CONFIG_WITH_DOWNLOAD = {
        'displaylogo': False,
        'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d',
                                   'autoScale2d', 'resetScale2d', 'hoverClosestCartesian',
                                   'hoverCompareCartesian', 'toggleSpikelines', 'sendDataToCloud'],
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'mental_health_figure',
        }
}

HOVERLABEL_TEMPLATE = dict(
    bgcolor='rgba(11, 6, 81, 0.8)',
    bordercolor='rgba(11, 6, 81, 0.8)',
    font=dict(
        color='white'
    )
)
BG_TRANSPARENT = 'rgba(0,0,0,0)'


# LAYOUT:
HIDE = {'display': 'none'}
MAIN_TITLE_COLOR = '#4e3a8e'
STORAGE_SESSION = 'session'
