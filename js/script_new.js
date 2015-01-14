$(document).ready( function () {

    var col_list = ['player name', 'stat 1', 'stat 2'];
    for (i in col_list){
        $('.table-header').append('<th title="Field #'+i.split(' ').join('')+'">'+col_list[i]+'</th>');
    }

    get_data();
} );

function get_data(){
    $.ajax({
        url: "football.json",
        type: 'get',
        dataType: 'json',
        success: function (data) {
                  $.each(data, function(index, element){
var playername = '<td>'+element['player name']+'</td>';
var stat1 = '<td>'+element['stat 1']+'</td>';
var stat2 = '<td>'+element['stat 2']+'</td>';
$('tbody').append('<tr>'+playername+stat1+stat2+'</tr>');                      

                  })
                  $('#table-1').dataTable({
                      "lengthMenu": [ 100, 75, 50, 25, 10 ]
                  });
        }

      });

}
