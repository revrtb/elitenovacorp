$(function() {


    $(document).ready(function () {
        $(document).ajaxStart(function () {
            $("#loading").show();
        }).ajaxStop(function () {
            $("#loading").hide();
        });
    });

    $('#btnLogin').click(function() {
 
        $.ajax({
            url: '/dashboard',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('tbody tr').click(function(event) {
        tr = event.target.closest('tr');
        $('#modal_text').text('<script type="text/javascript" src="https://www.revrtb.com/cbmpop?id='+tr.id+'"></script>');
        $('#modal_url').text($(tr).attr('url'));
        $('#modal_feed_url').text($(tr).attr('feed_url'));
        var dt_val = "--"
        if ($(tr).attr('dt') != 'None') {
            dt_val = $(tr).attr('dt');
        }
        $('#modal_notify_dt').text("Publisher notified on: "+dt_val);
        $('#myModal').modal('toggle');
    });

    $('.editItem').click(function(event) {
        tr = event.target.closest('tr');
        event.stopPropagation();

        $.ajax({
            url: '/get_publisher',
            data: {'feedid': tr.id},
            //data: {'subid': tr.id},
            type: 'POST',
            success: function(response) {
                data = response['data'];
               if (data != null) {
                $('#id').val(data[0]);
                $('#name').val(data[1]);
                $('#subid').val(data[2]);
                $('#feedid').val(data[3]);
                $('#feedauth').val(data[4]);
                $('#delay').val(data[5]);
                $('#max').val(data[6]);
                $('#period').val(data[7]);
                $('#def_url').val(data[8]);
                $('#email').val(data[9]);
               }
               $('#headerText').text('Edit publisher info');
               $('#editModal').modal('toggle');
            },
            error: function(error) {
                console.log(error);
            }
        });
        
     });

    $('.delItem').click(function(event) {
        tr = event.target.closest('tr');
        event.stopPropagation();

        $.ajax({
            url: '/delete_publisher',
            data: {'feedid': tr.id},
            type: 'POST',
            success: function(response) {
                data = response['data'];
                if (data) {
                    location.reload();
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
        
     });

    $('.sendItem').click(function(event) {
        tr = event.target.closest('tr');
        event.stopPropagation();

        if ($(tr).attr('email') == '' || $(tr).attr('email') == undefined) {
            alert("Email is not set");
        }
        $.ajax({
            url: '/notify_publisher',
            data: {
                    'html_code': '<script type="text/javascript" src="https://www.revrtb.com/cbmpop?id='+tr.id+'"></script>',
                    'direct_url': $(tr).attr('url'),
                    'pub_name': $(tr).attr('pub_name'),
                    'feed_url': $(tr).attr('feed_url'),
                    'email': $(tr).attr('email'),
                    'id': tr.id
                  },
            type: 'POST',
            success: function(response) {
                data = response['data'];
                if (data) {
                    location.reload();
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
        
     });

    $('#newPub').click(function(event) {
                $('#name').val('');
                $('#subid').val('');
                $('#feedid').val('');
                $('#feedauth').val('');
                $('#delay').val('');
                $('#max').val('');
                $('#period').val('');
                $('#def_url').val('');
                $('#email').val('');
                $('#id').val('');
                $('#headerText').text('Create new publisher');
        $('#editModal').modal('toggle');
    });

    $('#saveBtn').click(function(event) {
        data = {
                    'name' : $('#name').val(),
                    'subid' : $('#subid').val(),
                    'feedid' : $('#feedid').val(),
                    'feedauth' : $('#feedauth').val(),
                    'delay' : $('#delay').val(),
                    'max' : $('#max').val(),
                    'period' : $('#period').val(),
                    'default_url' : $('#def_url').val(),
                    'email' : $('#email').val()
                }
        var id = $('#id').val();
        if (id != '') {
            data['id'] = id;
        }
        for (var f in data) {
            if (f != 'default_url' && f != 'email' && data[f] == '') {
                alert('All fields are required except "Def URL" and "Email"');
                return false;
            }
        }

        $.ajax({
            url: '/save_publisher',
            data: data,
            type: 'POST',
            success: function(response) {
                if (response['data']) {
                    location.reload();
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
        
     });

});
