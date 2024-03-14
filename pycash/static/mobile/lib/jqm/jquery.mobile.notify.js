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
*/
(function($, undefined ) {
$.widget( "mobile.notify", $.mobile.widget, {
    options: {
        duration: 'short',
        type: 'default',
        msg: '',
        style: null,
        onClose: null
    },
   /* _create: function(){
        var self = this,
        o = $.extend(this.options, this.element.data('options')),
        caller = this.element;
        console.log("create");
        // remove any previous dialog
        $('div.ui-notify').remove();
        var thisPage = caller.closest('.ui-page');
        var $el = $("<div class='ui-notify ui-notify-"+o.type+"' style='display: none;'><div class='ui-notify-header'></div><div class='ui-notify-text'>"+o.msg+"</div></div>");
        
        $.extend(self, {
            thisDialog: $el,
            thisPage: thisPage,
            caller: caller
        });
        
    },*/
    _init: function() {
        var self = this,
        o = $.extend(this.options, this.element.data('options')),
        caller = this.element;
        
        var thisPage = caller.closest('.ui-page');
        var $el = $("<div class='ui-notify ui-notify-"+o.type+"' style='display: none;'><div class='ui-notify-header'></div><div class='ui-notify-text'>"+o.msg+"</div></div>");
        
        if (o.style) $el.addClass(o.style);
        
        $.extend(self, {
            thisDialog: $el,
            thisPage: thisPage,
            caller: caller
        });
        
        this.show();
    },    
    show: function() {
        if ( this.thisDialog.is(':visible') ) { return false; }
        
        var self = this,
        o = this.options
      
        var $el = this.thisDialog;

        $el.appendTo(this.thisPage);
        
        $el.css('left', (this.thisPage.width() - $el.outerWidth())/2);
        $el.css('top', ((this.thisPage.height() - $el.outerHeight()/2))/2);
        
        // fade in and fade out after the given time
        var millis = 3000
        if (o.duration === 'short') millis = 2000
        else if (o.duration === 'long') millis = 6000
        else if (! isNaN(o.duration)) millis = parseInt(o.duration)
        else jQuery.error('mobile.notify: options.duration has to be short, long or a integer value')
        
        $el.fadeIn().delay(millis).fadeOut('slow', function() {
            $el.remove();
            if (self.options.onClose && typeof(self.options.onClose) === "function") {
                self.options.onClose(self);
            }
        });
    },
});
    
})( jQuery );

