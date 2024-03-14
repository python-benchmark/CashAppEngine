/*
Copyright (c) 2012 Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

This patch will check for a data-history attribute in forms,
if false, hash wont be created on submit.

The code is extracted from original jquery code and should be kept in sync.
Lines added denoted with // SGT

jqm version 1.2.0

*/
$(function() {
   $( document ).bind( 'pageinit', function(){
         // bind to form submit events, handle with Ajax
         $( document ).undelegate("form", "submit"); // remove jqm handler
         $( document ).on("submit", "form", function( event ) {
             
             function getClosestBaseUrl( ele )
             {
                 // Find the closest page and extract out its url.
                 var url = $( ele ).closest( ".ui-page" ).jqmData( "url" ),
                 base = $.mobile.getDocumentBase().hrefNoHash;
    
                 if ( !url || !$.mobile.path.isPath( url ) ) {
                     url = base;
                 }
    
                 return $.mobile.path.makeUrlAbsolute( url, base);
             }
             
             var $this = $( this );

             if ( !$.mobile.ajaxEnabled ||
                 // test that the form is, itself, ajax false
                 $this.is( ":jqmData(ajax='false')" ) ||
                 // test that $.mobile.ignoreContentEnabled is set and
                 // the form or one of it's parents is ajax=false
                 !$this.jqmHijackable().length ) {
                 return;
             }
    
             var type = $this.attr( "method" ),
                         target = $this.attr( "target" ),
                         url = $this.attr( "action" );
    
             // If no action is specified, browsers default to using the
             // URL of the document containing the form. Since we dynamically
             // pull in pages from external documents, the form should submit
             // to the URL for the source document of the page containing
             // the form.
             if ( !url ) {
                     // Get the @data-url for the page containing the form.
                     url = getClosestBaseUrl( $this );
                     if ( url === $.mobile.getDocumentBase().hrefNoHash ) {
                     // The url we got back matches the document base,
                     // which means the page must be an internal/embedded
                        // page,
                     // so default to using the actual document url as a
                        // browser
                     // would.
                     url = $.mobile.getDocumentUrl().hrefNoSearch;
                 }
             }
    
             url = $.mobile.path.makeUrlAbsolute( url, getClosestBaseUrl( $this ) );
    
             if ( ( $.mobile.path.isExternal( url ) && !$.mobile.path.isPermittedCrossDomainRequest( documentUrl, url ) ) || target ) {
                 return;
             }

             // SGT
             var updateHistory = !$this.is(":jqmData(history='false')");
             
             $.mobile.changePage(
                     url,
                     {
                         changeHash: updateHistory, // SGT
                         type:   type && type.length && type.toLowerCase() || "get",
                         data:   $this.serialize(),
                         transition: $this.jqmData( "transition" ),
                         reverse:    $this.jqmData( "direction" ) === "reverse",
                         reloadPage: true
                     }
             );
             event.preventDefault();
        });
    });
});

