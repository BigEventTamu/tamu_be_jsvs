/**
 * Created by boredom23309 on 11/16/15.
 */

function addNewField(){
    var total_forms_element = $("#id_serviceformfield_set-TOTAL_FORMS");
    var initial_forms_element = $("#id_serviceformfield_set-INITIAL_FORMS");
    var new_field_form_html = $(".field_table:last").html();
    var cfc = String(parseInt(total_forms_element.attr('value'),10)-1);
    var inc = String(parseInt(cfc,10)+1);
    var endings = ["-id", "-field_label", "-field_type","-required","-help_text","-position"]
    var replace = {
        "find":"serviceformfield_set-"+cfc,
        "replace":"serviceformfield_set-"+inc,
    }
    total_forms_element.value = inc
    for (var i=0; i<endings.length;++i){
        new_field_form_html = new_field_form_html.split(replace['find']+endings[i]).join(replace["replace"]+endings[i])
    }
    new_field_form_html = "<tr class='field_row'><td colspan='2'><table style='' class='field_table'>"+new_field_form_html+"</table></td></tr>";
    $(".field_row:last").after(new_field_form_html);
    total_forms_element.val(String(parseInt(inc,10)+1));
}
function addNewChoice(prefix){
    var prefix = String(prefix);
    var total_forms_element = $("#id_"+prefix+"-TOTAL_FORMS");
    var new_field_form_html = $(".form_"+prefix+":last").html();
    var cfc = String(parseInt(total_forms_element.attr('value'),10)-1);
    var inc = String(parseInt(cfc, 10)+1);
    var replace_list = [
        {
            "find":prefix+"-"+cfc+"-id",
            "replace":prefix+"-"+inc+"-id",
        },
        {
            "find":prefix+"-"+cfc+"-choice",
            "replace":prefix+"-"+inc+"-choice"
        },
    ]
    for(var i=0; i < replace_list.length; ++i){
        new_field_form_html = new_field_form_html.split(replace_list[i]["find"]).join(replace_list[i]["replace"]);
    }
    new_field_form_html = "<tr class='field_row form_"+prefix+"'>"+new_field_form_html+"</tr>";
    $(".form_"+prefix+":last").after(new_field_form_html);
    console.log(new_field_form_html);
    total_forms_element.val(String(parseInt(inc,10)+1));
}
function swapElements(elem1, elem2) {
     elem1.after(elem2);
}
function moveFieldUp(pos_id){
    move_elem = $("#"+pos_id);
    first_elem = $(".old_field:first");
    last_elem = $(".old_field:last");
    if(move_elem.attr('id') == first_elem.attr('id')){console.log("I can't let you do that"); return false;}
    swap_with = move_elem.prev();
    move_elem_pos = $("#"+pos_id.slice(4))
    swap_with_pos = $("#"+swap_with.attr('id').slice(4))

    var temp = swap_with_pos.val();
    swap_with_pos.val(move_elem_pos.val());
    move_elem_pos.val(temp)

    swapElements(move_elem,swap_with);
}
function moveFieldDown(pos_id){
    move_elem = $("#"+pos_id);
    last_elem = $(".old_field:last");
    if(move_elem.attr('id') == last_elem.attr('id')){console.log("I can't let you do that"); return false;}
    swap_with = move_elem.next();
    move_elem_pos = $("#"+pos_id.slice(4))
    swap_with_pos = $("#"+swap_with.attr('id').slice(4))

    console.log("move elem val: " + move_elem.attr('value'))
    console.log("swap with val: " + swap_with.attr('value'))

    var temp = swap_with.attr('value');
    swap_with.attr('value', move_elem.attr('value'));
    move_elem.attr('value', temp);

    console.log("move elem val: " + move_elem.attr('value'))
    console.log("swap with val: " + swap_with.attr('value'))
    console.log("move elem pos val: " + move_elem_pos.val())
    console.log("swap with pos val: " + swap_with_pos.val())

    var temp = swap_with_pos.val();
    swap_with_pos.val(move_elem_pos.val());
    move_elem_pos.val(temp)

    console.log("move elem pos val: " + move_elem_pos.val())
    console.log("swap with pos val: " + swap_with_pos.val())

    swapElements(swap_with, move_elem);
    console.log("move finished")
}
function comp_row(row1, row2){
    console.log(row1);
    console.log(row2);
    if(parseInt(row1.attr('value'),10) > parseInt(row2.attr('value'),10)) return -1
    if(parseInt(row1.attr('value'),10) == parseInt(row2.attr('value'),10)) return 0
    if(parseInt(row1.attr('value'),10) < parseInt(row2.attr('value'),10)) return 1
}
function row_is_smaller(row1, row2){
    if(comp_row(row1, row2) == 1) return true
    return false
}
function sort_field_table(){
    var tbl = document.getElementById("all_fields_table").tBodies[0];
    var store = [];
    for(var i=0, len=tbl.rows.length; i<len; i++){
        var row = tbl.rows[i];
        var sortnr = parseFloat(row.getAttribute('value'));
        if(!isNaN(sortnr)) store.push([sortnr, row]);
    }
    store.sort(function(x,y){
        return x[0] - y[0];
    });
    for(var i=0, len=store.length; i<len; i++){
        tbl.appendChild(store[i][1]);
    }
    store = null;
}
