$(document).ready( function () {

    var col_list = ['aircraft', 'airport', 'number', 'date', 'remains collected?', 'remains to smithsonian?', 'remarks', 'fowl size', 'species'];
    for (i in col_list){
        $('.table-header').append('<th title="Field #'+i.split(' ').join('')+'">'+col_list[i]+'</th>');
    }

    get_data();
} );

function get_data(){
    $.ajax({
        url: "bird_strikes.json",
        type: 'get',
        dataType: 'json',
        success: function (data) {
                  $.each(data, function(index, element){
var aircraft = '<td>'+element['aircraft']+'</td>';
var airport = '<td>'+element['airport']+'</td>';
var number = '<td>'+element['number']+'</td>';
var date = '<td>'+element['date']+'</td>';
var remainscollected = '<td>'+element['remains collected?']+'</td>';
var remainstosmithsonian = '<td>'+element['remains to smithsonian?']+'</td>';
var remarks = '<td>'+element['remarks']+'</td>';
var fowlsize = '<td>'+element['fowl size']+'</td>';
var species = '<td>'+element['species']+'</td>';
$('tbody').append('<tr>'+aircraft+airport+number+date+remainscollected+remainstosmithsonian+remarks+fowlsize+species+'</tr>');                      

                  })
                  $('#table-1').dataTable({
                      "lengthMenu": [ 100, 75, 50, 25, 10 ]
                  });
        }

      });

}
