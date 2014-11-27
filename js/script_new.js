$(document).ready( function () {

    var col_list = ['player', 'team', 'att'];
    for (i in col_list){
        $('.table-header').append('<th title="Field #'+i+'">'+col_list[i]+'</th>');
    }

    get_data();
} );

function get_data(){
    $.ajax({
        url: "passing_stats.json",
        type: 'get',
        dataType: 'json',
        success: function (data) {
                  $.each(data, function(index, element){
var player = '<td>'+element['player']+'</td>';
var team = '<td>'+element['team']+'</td>';
var att = '<td>'+element['att']+'</td>';
$('tbody').append('<tr>'+player+team+att+'</tr>');

                  })
                  $('#table-1').dataTable({
                      "lengthMenu": [ 100, 75, 50, 25, 10 ]
                  });
        }

      });

}
