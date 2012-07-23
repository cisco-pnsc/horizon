$(document).ready(function() {

    $("div#graph_zoom").modal({
        show: false,
        keyboard: true
    });

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
    
    $('div#int_selector span.label').click(function() {
        $('div#int_selector span.label').removeClass('label-success');
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

    $('div#core_selector span.label').click(function() {
        $('div#core_selector span.label').removeClass('label-success');
        $(this).addClass('label-success');
        url = $(this).attr('alt');
        $.ajax({
            url: url,
            type: "GET",
            success: function(data) {
                $('img#cpu_graph').attr('src', data.graph);
                $('span#cpu_used').html(data.stats.cpu_load);
                $("div#cpu_load div.progress").removeClass().
                 addClass('progress').addClass(data.stats.cpu_class);
                $("div#cpu_load div.bar").css('width', data.stats.cpu_load +'%');
            }
        });
    });

    $('div#mem_selector span.label').click(function() {
        $('div#mem_selector span.label').removeClass('label-success');
        $(this).addClass('label-success');
        url = $(this).attr('alt');
        $.ajax({
            url: url,
            type: "GET",
            success: function(data) {
                $('img#mem_graph').attr('src', data.graph);
                $("span#mem_cap").html(data.stats.total_mem);
                $("span#mem_used").html(data.stats.mem_used);
                $("span#mem_usage").html(data.stats.mem_usage);
                $("div#mem_load div.progress").removeClass().
                  addClass('progress').addClass(data.stats.mem_class);
                $("div#mem_load div.bar").css('width', data.stats.mem_usage +'%');
            }
        });
    });
    
    $('div#part_selector span.label').click(function() {
        $('div#part_selector span.label').removeClass('label-success');
        $(this).addClass('label-success');
        url = $(this).attr('alt');
        $.ajax({
            url: url,
            type: "GET",
            success: function(data) {
                $('img#part_graph').attr('src', data.graph);
                $("span#part_size").html(data.stats.total);
                $("span#part_used").html(data.stats.used);
                $("span#part_usage").html(data.stats.usage);
                $("div#part_load div.progress").removeClass().
                  addClass('progress').addClass(data.stats.class);
                $("div#part_load div.bar").css('width', data.stats.usage +'%');
            }
        });
    });

    $('div#disk_selector span.label').click(function() {
        $('div#disk_selector span.label').removeClass('label-success');
        $(this).addClass('label-success');
        url = $(this).attr('alt');
        $.ajax({
            url: url,
            type: "GET",
            success: function(data) {
                $('img#disk_graph').attr('src', data.graph);
                $("span#part_size").html(data.stats.total);
                $("span#disk_tps").html(data.stats.tps);
                $("span#disk_kbr").html(data.stats.kb_read);
                $("span#disk_kbw").html(data.stats.kb_written);
            }
        });
    });

    $('div.metric_graph img').click(function() {
        img = this;
        $('img#zoom_image').attr('src', $(img).attr('src'));
        $('div#graph_zoom div.modal-header h3').html($(img).attr('alt'));
        $("div#graph_zoom").modal('show');
    });
});
