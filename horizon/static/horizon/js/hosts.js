function date_toggle(el) {
    $(el).find('.date-toggle').click(function () {
        if ($(el).children('.date-selector').is(':visible')) {
            $(el).children('.date-selector').hide(300);
        } else {
            $(el).children('.date-selector').show(300);
        }
    });
}

function update_graph(el) {
    $(el).find('.upd_graph').click(function() {
        panel = $(this).closest('.panel')[0];
        loader = $(panel).find('.panel_loader')[0];
        $(loader).show();
        form = $(this).closest('form');
        start = $($(form).find('input[name=start]')[0]).val();
        end = $($(form).find('input[name=end]')[0]).val();
        host_id = $($(form).find('input[name=host_id]')[0]).val();
        panel_class = $($(form).find('input[name=panel_class]')[0]).val();
        url =  $($(form).find('input[name=ajax_url]')[0]).val();
 
        $.ajax({
            url: url,
            data: {
                start: start,
                end: end,
                host_id: host_id,
                panel_class: panel_class,
            },
            success: function(data) {
                tempdiv = document.createElement('div');
                tempdiv.innerHTML = data;
                temptop = $(tempdiv).children('.panel')[0];
                $(panel).replaceWith(temptop);
                date_toggle(temptop);
                update_graph(temptop);
                graph_zoom(temptop);
                $('.datepicker').datepicker();
            }
        });
    });
}

function graph_zoom(el) {
    $(el).find('.metric_graph img').click(function() {
        img = this;
        $('img#zoom_image').attr('src', $(img).attr('src'));
        $('div#graph_zoom div.modal-header h3').html($(img).attr('alt'));
        $("div#graph_zoom").modal('show');
    });
}

$(document).ready(function() {
    $("div#graph_zoom").modal({
        show: false,
        keyboard: true
    });

    $('.datepicker').datepicker();

    $('div.panel').each(function () {
        date_toggle(this);
        update_graph(this);
        graph_zoom(this);
    });
});
