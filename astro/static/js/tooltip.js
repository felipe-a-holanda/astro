$(function() {

    $( document ).tooltip({
        track: true,
        position: {
            my: "left top+20 center",
            at: "right center"
        }
    });
    
    function enable_tooltip(obj){
        $(obj).tooltip({
        items: ":not([disabled])",
        content: function(){var title = $( this ).find( "title" ),
                content;
            if ( title.length ) {
                title.attr( "data-rect", $( this ).attr( "id" ) )
                    .appendTo( "body" );
            } else {
                title = $( "[data-rect='" +
                          $( this ).attr( "id" ) + "']" );
            }
            return title.html();},
        track: true, 
        position: { 
            my: "left top+20 center", 
            at: "right center" },
        show: {
          delay: 0
        }
    });
    }
    
    enable_tooltip("rect");
    enable_tooltip("circle");
    enable_tooltip("line");
    enable_tooltip("path");
    
    
});
