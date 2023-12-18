window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        toggle_modal_heatmap: function(n_clicks, opened) {
            if(n_clicks === undefined) {
                return window.dash_clientside.no_update;
            }
            return !opened;
        },
        toggle_modal_sankey: function(n_clicks, opened) {
            if(n_clicks === undefined) {
                return window.dash_clientside.no_update;
            }
            return !opened;
        },
        stop_animate_choropleth: function(n_clicks) {
            if(n_clicks === undefined) {
                return window.dash_clientside.no_update;
            }
            return n_clicks % 2 ? 0 : -1;
        },
        toggle_modal_data_source: function(n_clicks, opened) {
            if(n_clicks === undefined) {
                return window.dash_clientside.no_update;
            }
            return !opened;
        },
        update_disabled_state_select_continent: function(checked) {
            return checked;
        }
    }
});
