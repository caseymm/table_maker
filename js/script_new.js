$(document).ready( function () {

    var col_list = ['name', 'team', 'date'];
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
var name = '<td>'+element['name']+'</td>';
var team = '<td>'+element['team']+'</td>';
var date = '<td>'+element['date']+'</td>';
$('tbody').append('<tr>'+name+team+date+'</tr>');                      

                  })
                  $('#table-1').dataTable({
                      "lengthMenu": [ 100, 75, 50, 25, 10 ]
                  });
        }

      });

}
