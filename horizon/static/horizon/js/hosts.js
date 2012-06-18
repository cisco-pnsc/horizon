$(document).ready(function() {
    /*
    $('li.host_icon').hover(
        function() {
            elem = this;
            $(elem).find('dl').show();
        },
        function() {
            elem = this;
            $(elem).find('dl').hide();
        }
    );
    */
    $('span.badge').tooltip();
    $('span.label').tooltip();
    $('span.hosts_filter span.label').tooltip();

    $('span.hosts_filter span.label').click(function() {
        span = this;
        cl = $(span).attr('id');
        $('span.hosts_filter span.label').removeClass('label-success');
        $(span).addClass('label-success');
        $('ul#host_list li').each(function() {
            if (cl == 'all_hosts') {
                $(this).show();
            } else {
                if ($(this).hasClass(cl)) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            }
        });
    });
    
    $('div.int_selector span.label').click(function() {
        $('div.int_selector span.label').removeClass('label-success');
        $(this).addClass('label-success');
        url = $(this).attr('alt');
        $.ajax({
            url: url,
            type: "GET",
            success: function(data) {
                $('img#net_graph').attr('src', data.graph);
                $('span#pkts_sent').html(data.stats[0].tx);
                $('span#pkts_recv').html(data.stats[0].rx);
                $('span#bandwidth').html(data.stats[0].bandwidth);
                $('span#net_used').html(data.stats[0].used);
                $("div#net_load div.progress").removeClass().
                 addClass('progress').addClass(data.stats[0].class);
                $("div#net_load div.bar").css('width', data.stats[0].used +'%');
            }
        });
    });

    $('div.core_selector span.label').click(function() {
        $('div.core_selector span.label').removeClass('label-success');
        $(this).addClass('label-success');
        url = $(this).attr('alt');
        $.ajax({
            url: url,
            type: "GET",
            success: function(data) {
                $('img#cpu_graph').attr('src', data.graph);
                $('span#cpu_used').html(data.stats[0].cpu_load);
                $("div#cpu_load div.progress").removeClass().
                 addClass('progress').addClass(data.stats[0].cpu_class);
                $("div#cpu_load div.bar").css('width', data.stats[0].cpu_load +'%');
            }
        });
    });
});
