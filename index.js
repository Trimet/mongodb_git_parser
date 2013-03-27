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

    // $("dateFrom").change( function(){ orderDate("up") })
    var fields = "&fields="
    $("#submit_button").click( function(){
        var org_name_selected_count = $("#org_name").find("option:selected").size() 
        var i = 1
        if( org_name_selected_count > 1 ){
            fields += "org_name."
            $("#org_name").find("option:selected").each( function(){
                fields += $(this).val()
                if( org_name_selected_count != i){
                    fields += "|"
                } 
                i++;
                alert($(this).val());
            })    
            alert(fields)
        }
        
    })
})