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
$(function(){
    $(document).on("pageshow", function(event, ui) {
		createSwipeMenu();
    });
    $('body').on('tap', function(e){
        // if the triggering object is a button, fire it's tap event
        if (e.target.className.indexOf('aSwipeBtn') >= 0) {
            $(e.target).trigger('click');
        }
        // remove any existing buttons
        $('.divSwipe').remove();
    });
})

function createSwipeMenu() {
    $("li[swipe-options]:visible").each(function() {
		$('.divSwipe').remove();
        var $li = $(this);
        var options = $li.attr("swipe-options");
        var opts = $.parseJSON(options);
		// add swipe event to the list item, removing it first (if it exists)
        var direction = 'swipe'+opts.direction;
        var fn = function(e){
            $('.divSwipe').remove();
            e.stopPropagation();
            e.preventDefault();              
			// create buttons and div container
			var $divSwipe = $('<div class="divSwipe"></div>');
			$li.prepend($divSwipe);
			$.each(opts.buttons, function(index, obj) {
	             var $b = $('<a>'+obj.value+'</a>').attr({
	                    'class': 'aSwipeBtn ui-btn-up-'+obj.style,
	             });
			    if ("javascript:" == obj.href.substring(0,11)) {
			        var func = obj.href.substring(11);
			        $b.on('click', function(){eval(func)});
			    } else {
					$b.attr('href', obj.href);
			    }
				$divSwipe.prepend($b);	
			});
			// insert buttons into divSwipe
			$divSwipe.height($li.innerHeight());
			$divSwipe.show(100);
			// add escape route for swipe menu
		};
        $li.off(direction, fn).on(direction, fn);
    });
}
