/* Additional JavaScript for marketplace. */
$(document).ready(function() {
    $('.app_instance button').click(function() {
        $('.app_instance button').removeClass('active btn-primary');
        $(this).addClass('active btn-primary');
    });

    $(document).on('show', '.modal', function(evt) {
        // Get selected version value
        version = $('select#version-select').val();
        // Get selected version text
        version_text = $('select#version-select option:selected').text();
        // Get selected zone
        zone = $('select#zone-select').val();
        // Get selected zone text
        zone_text = $('select#zone-select option:selected').text();
        // Get selected instance
        flavor = $($('div.app_instance button.btn-primary')[0]).attr('id');
        // Get selected flavor text
        flavor_text =  $($('div.app_instance button.btn-primary')[0]).text();
        // Get security group
        sec_grp = $('select#sec_grp-select').val();
        // Get security group text
        sec_grp_text = $('select#sec_grp-select option:selected').text();
        // Get keypair
        keypair = $('select#keypair-select').val();
        // Get keypair text
        keypair_text = $('select#keypair-select option:selected').text();

        // Update form variables
        $('form#start_application_form input#id_version').val(version);
        $('form#start_application_form input#id_flavor').val(flavor);
        $('form#start_application_form input#id_zone').val(zone);
        $('form#start_application_form input#id_sec_grp').val(sec_grp);
        $('form#start_application_form input#id_keypair').val(keypair);
        // Update disply text
        $('dl.start_app_dl span#sel_version').text(version_text);
        $('dl.start_app_dl span#sel_flavor').text(flavor_text);
        $('dl.start_app_dl span#sel_zone').text(zone_text);
        $('dl.start_app_dl span#sel_sec_grp').text(sec_grp_text);
        $('dl.start_app_dl span#sel_keypair').text(keypair_text);
    });
});
