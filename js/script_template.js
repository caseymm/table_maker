$(document).ready( function () {

    TABLE_HEADER
    for (i in col_list){
        $('.table-header').append('<th title="Field #'+i+'">'+col_list[i]+'</th>');
    }

    get_data();
} );

function get_data(){
    $.ajax({
        url: "json_url_here",
        type: 'get',
        dataType: 'json',
        success: function (data) {
                  $.each(data, function(index, element){
                      CONTENT_HERE

                  })
                  $('#table-1').dataTable({
                      "lengthMenu": [ 100, 75, 50, 25, 10 ]
                  });
        }

      });

}
