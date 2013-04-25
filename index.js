$(document).ready( function(){
    /// Открытие ссылок для загрузки ///
    $(".orderItem").click( function(){
        $(".orderDownload").hide()
        // alert(0)
        $(this).find(".orderDownload").each( function(){
            // alert(1)
            $(this).show()
        })

    })  
    $.datepicker.setDefaults( $.datepicker.regional[ "ru-RU" ] )
    $(".dateInput").datepicker()
    $(".dateInputClosed").datepicker()

    // $("dateFrom").change( function(){ orderDate("up") })
    var fields = "&fields="
    $("#submit_button").click( function(){
        var org_subname_selected_count = $("#org_subname").find("option:selected").size() 
        var i = 1
        if( org_subname_selected_count > 1 ){
            fields += "org_subname."
            $("#org_subname").find("option:selected").each( function(){
                fields += encodeURIComponent($(this).val())
                if( org_subname_selected_count != i){
                    fields += "|"
                } 
                i++;
                alert($(this).val());
            })    
            alert(fields)
        }

        var initiator_selected_count = $("#initiator").find("option:selected").size() 
        var i = 1
        if( initiator_selected_count > 1 ){
            fields += "initiator."
            $("#initiator").find("option:selected").each( function(){
                fields += encodeURIComponent($(this).val())
                if( initiator_selected_count != i){
                    fields += "|"
                } 
                i++;
                alert($(this).val());
            })    
            alert(fields)
        }
        window.location = "show_issues.py?sort=created"+fields
    })
    $("#add_sort").click( function(){
        $("#sort_select").find("option:selected").each( function(){
            // alert( $("#sort").val().indexOf($(this).val()) )
            if($("#sort").val().indexOf($(this).val())==-1){
                if($("#sort").val().length > 1){
                    var new_val = $("#sort").val() + "," + $(this).val()
                    $("#sort").val(new_val)    
                } else {
                    var new_val = $("#sort").val() + $(this).val()
                    $("#sort").val(new_val) 
                }
                
            }
        })
        
    })
})
