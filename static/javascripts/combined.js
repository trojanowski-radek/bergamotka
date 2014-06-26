/**
 * Created by rtrojan on 19.05.14.
 */


// This class provides methods for Booking application
// =============================================================================
// Admin section scripts
// admin.js
// =============================================================================

var admin = admin || {};
var booking = booking || {};
var news = news || {};

admin.initEventHandlers = function () {

    var $main_content = $('#main-content');

    //NEWS MANAGER
    $('#news-add-btn').on('click', function () {
        $('#news-add-dlg').modal();
    });

    $('#news-add-save-btn').on('click', function () {

        var title = $('#news-add-title').val(),
            content = $('#news-add-content').val(),
            image = $('#news-image-url-placeholder').text(),
            json = {
                'title'     : title,
                'content'   : content,
                'user'      : 1,
                'image'     : image
            };

        var error = false;

        $.each([title, content], function (index, element) {
            if (element == null || element == ''){
                error = true;
            }
        });

        if (error != true) {
            $.postJSON('/news_add', json, function () {
                $.get('admin', function (data) {
                    $main_content.empty();
                    $main_content.html(data);
                    admin.initEventHandlers();
                    $main_content.prepend('<div class="alert alert-success">DODANO nową aktualność: ' + title + '.</div>');
                    afterNewsChange();
                });
            });
        } else {
            $main_content.prepend('<div class="alert alert-danger">BŁĄD: Wszystkie pola są wymagane. Proszę poprawić.</div>');
        }

    });

    var $admin_news_manager_table = $('#admin-news-manager-table');

    $admin_news_manager_table.find('[action=delete]').on('click', function () {
        $.postJSON('news_delete', {id : this.value}, function () {
            $.get('admin', function (data) {
                $main_content.empty();
                $main_content.html(data);
                admin.initEventHandlers();
                afterNewsChange();
            });
        });
    });

    $admin_news_manager_table.parent().find('[action=edit]').on('click', function () {

        var $item = $(this).parent().parent();
        var id = $(this).val();

        $('#news-edit-dlg').modal();

        var title = $item.find('td[rel=title]').text(),
            content = $item.find('td[rel=content]').text(),
            image = $item.find('td[rel=image] > img').attr('src');

        $('#news-edit-title').val(title);
        $('#news-edit-content').text(content);
        //$('#news-edit-image-url-placeholder').text(image);
        $('#news-edit-item-id').text(id);
    });

    $('#news-edit-save-btn').on('click', function () {

        var title = $('#news-edit-title').val(),
            content = $('#news-edit-content').val(),
            image = $('#news-edit-image-url-placeholder').text(),
            id = $('#news-edit-item-id').text(),
            json = {
                'title'       : title,
                'content'     : content,
                'image'       : image,
                'id'          : id
            };

        var error = false;

        $.each([title, content, id], function (index, element) {
            if (element == null || element == ''){
                error = true;
            }
        });

        if (error == true){
            $main_content.prepend('<div class="alert alert-danger">BŁĄD: Wszystkie pola są wymagane. Proszę poprawić.</div>');
        } else {
            $.postJSON('/news_edit', json, function () {
                $.get('admin', function (data) {
                    $main_content.empty();
                    $main_content.html(data);
                    admin.initEventHandlers();
                    $main_content.prepend('<div class="alert alert-success">ZMODYFIKOWANO aktualność: '+title+'.</div>');
                    afterNewsChange();
                });
            });
        }

    });

    $('#news-add-dlg-image-form').find(':button').click(function(){
        var formData = new FormData($('#news-add-dlg-image-form')[0]);
        $.ajax({
            url: '/news_image_upload',  //Server script to process data
            type: 'POST',
            //Ajax events
            success: function(response){
                $('#news-image-url-placeholder').text(response);
                $('#news-add-image-section').html('<div class="alert alert-success">DODANO: '+response+'.</div>');
            },
            error: function(exception){
                alert(exception);
            },
            // Form data
            data: formData,
            //Options to tell jQuery not to process data or worry about content-type.
            cache: false,
            contentType: false,
            processData: false
        });
    });

    $('#news-edit-dlg-image-form').find(':button').click(function(){
        var formData = new FormData($('#news-edit-dlg-image-form')[0]);
        $.ajax({
            url: '/news_image_upload',  //Server script to process data
            type: 'POST',
            //Ajax events
            success: function(response){
                $('#news-edit-image-url-placeholder').text(response);
                $('#news-edit-image-section').html('<div class="alert alert-success">DODANO: '+response+'.</div>');
            },
            error: function(exception){
                alert(exception);
            },
            // Form data
            data: formData,
            //Options to tell jQuery not to process data or worry about content-type.
            cache: false,
            contentType: false,
            processData: false
        });
    });

    //EVENT MANAGER
    //DELETE EVENT
    $('#admin-events-manager-table').find('[action=delete]').on('click', function () {
        $.postJSON('events_delete', {id : this.value}, function () {
            $.get('admin', function (data) {
                $main_content.empty();
                $main_content.html(data);
                admin.initEventHandlers();
                afterEventsChange();
            });
        });
    });

    //EDIT EVENT
    $('#admin-events-manager-table').find('[action=edit]').on('click', function () {

        var $item = $(this).parent().parent(),
            id = $(this).val(),
            cells = $item.find('td'),
            start = cells[1].textContent,
            end = cells[2].textContent,
            title = cells[3].textContent;

        $('#event-edit-dlg').modal();

        $('#calendar-edit-event-title').val(title);

        $('#calendar-edit-event-save-btn').unbind().on('click', function (e) {

            var date = $('#calendar-edit-event-date').val(),
                time_start = $('#calendar-edit-event-time-start').val(),
                time_end = $('#calendar-edit-event-time-end').val(),
                title = $('#calendar-edit-event-title').val(),
                error = false;

            $.each([date, time_start, time_end, title], function (index, element) {
                if (element == null || element == ''){
                    error = true;
                }
            });

            if (error == true){
                $main_content.prepend('<div class="alert alert-danger">BŁĄD: Wszystkie pola są wymagane. Proszę poprawić.</div>');
            } else {

                var json = {
                    'date_start': date+' '+time_start,
                    'date_end'  : date+' '+time_end,
                    'title'     : title,
                    'id'		: id
                };

                $.postJSON('/events_edit', json, function (data) {
                    $.get('admin', function (data) {
                        $main_content.empty();
                        $main_content.html(data);
                        admin.initEventHandlers();
                        afterEventsChange();
                   });
                });
            }
        });
    });

    $('#event-add-btn').on('click', function () {
        $('#event-add-dlg').modal();
    });

    $('#admin-add-event-save-btn').on('click', function () {

        var date = $('#admin-add-event-date').val(),
            time_start = $('#admin-add-event-time-start').val(),
            time_end = $('#admin-add-event-time-end').val(),
            title = $('#admin-add-event-title').val(),
            json = {
                'date_start': date + ' ' + time_start,
                'date_end'  : date + ' ' + time_end,
                'title'     : title,
                'user'      : 1
            };

        var error = false;

        $.each([date, time_start, time_end, title], function (index, element) {
            if (element == null || element == ''){
                error = true;
            }
        });

        if (error == true){
            $main_content.prepend('<div class="alert alert-danger">BŁĄD: Wszystkie pola są wymagane. Proszę poprawić.</div>');
        } else {
            $.postJSON('/events_add', json, function () {
                $.get('admin', function (data) {
                    $main_content.empty();
                    $main_content.html(data);
                    admin.initEventHandlers();
                    $main_content.prepend('<div class="alert alert-success">DODANO: '+title+'.</div>');
                    afterEventsChange();
                });
            });
        }
    });

    //RESERVATIONS MANAGER
    var $admin_reservations_manager_table = $('#admin-reservations-manager-table');

    $admin_reservations_manager_table.find('[action=delete]').on('click', function () {
        $.postJSON('reservations_delete', {id : this.value}, function () {
            $.get('admin', function (data) {
                $main_content.empty();
                $main_content.html(data);
                admin.initEventHandlers();
                afterReservationsChange();
            });
        });
    });

    $admin_reservations_manager_table.parent().find('[action=edit]').on('click', function () {
        var $item = $(this).parent().parent();
        var id = $(this).val();
        $('#reservations-edit-dlg').modal();
        var date_start = $item.find('td[rel=date_start]').text(),
            date_end = $item.find('td[rel=date_end]').text(),
            date = date_start.split(' ')[0],
            time_start = date_start.split(' ')[1],
            time_end = date_end.split(' ')[1],
            title = $item.find('td[rel=title]').text(),
            email = $item.find('td[rel=email]').text(),
            phone = $item.find('td[rel=phone]').text();
        $('#reservations-edit-title').val(title);
        $('#reservations-edit-email').val(email);
        $('#reservations-edit-phone').val(phone);
        $('#reservations-edit-date').val(date);
        $('#reservations-edit-time-start').val(time_start);
        $('#reservations-edit-time-end').val(time_end);
        $('#reservations-edit-item-id').text(id);
    });

    $('#reservations-edit-save-btn').on('click', function () {

        var title = $('#reservations-edit-title').val(),
            email = $('#reservations-edit-email').val(),
            phone = $('#reservations-edit-phone').val(),
            date = $('#reservations-edit-date').val(),
            time_start = $('#reservations-edit-time-start').val(),
            time_end = $('#reservations-edit-time-end').val(),
            id = $('#reservations-edit-item-id').text(),
            json = {
                'title'       : title,
                'email'       : email,
                'phone'       : phone,
                'date'        : date,
                'time_start'  : time_start,
                'time_end'    : time_end,
                'id'          : id
            };

        var error = false;

        $.each([title, email, phone, date, time_start, time_end, id], function (index, element) {
            if (element == null || element == ''){
                error = true;
            }
        });

        if (error != true) {
            $.postJSON('/reservations_edit', json, function () {
                $.get('admin', function (data) {
                    $main_content.empty();
                    $main_content.html(data);
                    afterReservationsChange();
                    admin.initEventHandlers();
                    $main_content.prepend('<div class="alert alert-success">DODANO nową pozycję na karcie dań: ' + title + '.</div>');
                });
            });
        } else {
            $main_content.prepend('<div class="alert alert-danger">BŁĄD: Wszystkie pola są wymagane. Proszę poprawić.</div>');
        }

    });

    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        weekStart : 1,
        autoclose: true
    });

    $('.timepicker').timepicker({showMeridian: false});

    $('.nav-tabs li').click(function(){
        $main_content.find('.alert').remove();
    });

    //DISHES MANAGER
    $('#dishes-add-btn').on('click', function () {
        $('#dishes-add-dlg').modal();
    });

    $('#dishes-add-dlg-image-form').find(':button').click(function(){
        var formData = new FormData($('#dishes-add-dlg-image-form')[0]);
        $.ajax({
            url: '/dishes_image_upload',  //Server script to process data
            type: 'POST',
            //Ajax events
            success: function(response){
                $('#dishes-image-url-placeholder').text(response);
                $('#dishes-add-image-section').html('<div class="alert alert-success">DODANO: '+response+'.</div>');
            },
            error: function(exception){
                alert(exception);
            },
            // Form data
            data: formData,
            //Options to tell jQuery not to process data or worry about content-type.
            cache: false,
            contentType: false,
            processData: false
        });
    });

    $('#dishes-add-save-btn').on('click', function () {

        var title = $('#dishes-add-title').val(),
            ingredients = $('#dishes-add-ingredients').val(),
            price = $('#dishes-add-price').val(),
            type = $('#dishes-add-type').val(),
            image = $('#dishes-image-url-placeholder').text(),
            json = {
                'title'       : title,
                'ingredients' : ingredients,
                'price'       : price,
                'type'        : type,
                'image'       : image
            };

        var error = false;

        $.each([title, price, type, ingredients], function (index, element) {
            if (element == null || element == ''){
                error = true;
            }
        });

        if (error != true) {
            $.postJSON('/dishes_add', json, function () {
                $.get('admin', function (data) {
                    $main_content.empty();
                    $main_content.html(data);
                    admin.initEventHandlers();
                    $main_content.prepend('<div class="alert alert-success">DODANO nową pozycję na karcie dań: ' + title + '.</div>');
                    afterDishesChange();
                });
            });
        } else {
            $main_content.prepend('<div class="alert alert-danger">BŁĄD: Wszystkie pola są wymagane. Proszę poprawić.</div>');
        }

    });

    var $admin_dishes_manager_table = $('#admin-dishes-manager-table');

    $admin_dishes_manager_table.find('[action=delete]').on('click', function () {
        $.postJSON('dishes_delete', {id : this.value}, function () {
            $.get('admin', function (data) {
                $main_content.empty();
                $main_content.html(data);
                admin.initEventHandlers();
                afterDishesChange();
            });
        });
    });

    $admin_dishes_manager_table.parent().find('[action=edit]').on('click', function () {
        var $item = $(this).parent().parent();
        var id = $(this).val();
        $('#dishes-edit-dlg').modal();
        var title = $item.find('td[rel=title]').text(),
            ingredients = $item.find('td[rel=ingredients]').text(),
            price = $item.find('td[rel=price]').text(),
            type = $item.find('td[rel=type]').text(),
            image = $item.find('td[rel=image] > img').attr('src');
        $('#dishes-edit-title').val(title);
        $('#dishes-edit-ingredients').text(ingredients);
        $('#dishes-edit-price').val(price);
        $('#dishes-edit-type').val(type);
        //$('#dishes-edit-image-url-placeholder').text(image);
        $('#dishes-edit-item-id').text(id);
    });

    $('#dishes-edit-dlg-image-form').find(':button').click(function(){
        var formData = new FormData($('#dishes-edit-dlg-image-form')[0]);
        $.ajax({
            url: '/dishes_image_upload',  //Server script to process data
            type: 'POST',
            //Ajax events
            success: function(response){
                $('#dishes-edit-image-url-placeholder').text(response);
                $('#dishes-edit-image-section').html('<div class="alert alert-success">DODANO: '+response+'.</div>');
            },
            error: function(exception){
                alert(exception);
            },
            // Form data
            data: formData,
            //Options to tell jQuery not to process data or worry about content-type.
            cache: false,
            contentType: false,
            processData: false
        });
    });

    $('#dishes-edit-save-btn').on('click', function () {

        var title = $('#dishes-edit-title').val(),
            ingredients = $('#dishes-edit-ingredients').val(),
            price = $('#dishes-edit-price').val(),
            type = $('#dishes-edit-type').val(),
            image = $('#dishes-edit-image-url-placeholder').text(),
            id = $('#dishes-edit-item-id').text(),
            json = {
                'title'       : title,
                'ingredients' : ingredients,
                'price'       : price,
                'type'        : type,
                'image'       : image,
                'id'          : id
            };

        var error = false;

        $.each([title, price, type, ingredients, id], function (index, element) {
            if (element == null || element == ''){
                error = true;
            }
        });

        if (error == true){
            $main_content.prepend('<div class="alert alert-danger">BŁĄD: Wszystkie pola są wymagane. Proszę poprawić.</div>');
        } else {
            $.postJSON('/dishes_edit', json, function () {
                $.get('admin', function (data) {
                    $main_content.empty();
                    $main_content.html(data);
                    admin.initEventHandlers();
                    $main_content.prepend('<div class="alert alert-success">ZMODYFIKOWANO pozycję na karcie dań: '+title+'.</div>');
                    afterDishesChange();
                });
            });
        }

    });

    var afterDishesChange = function () {
        $('#dishes-edit-dlg').modal('hide');
        $('body').removeClass('modal-open');
        $('.modal-backdrop').remove();
        $('#admin-tabs').find('a[rel=dishes]').tab('show');
    };

    var afterNewsChange = function () {
        $('#news-edit-dlg').modal('hide');
        $('body').removeClass('modal-open');
        $('.modal-backdrop').remove();
        $('#admin-tabs').find('a[rel=news]').tab('show');
    };

    var afterEventsChange = function () {
        $('#events-edit-dlg').modal('hide');
        $('body').removeClass('modal-open');
        $('.modal-backdrop').remove();
        $('#admin-tabs').find('a[rel=events]').tab('show');
    };

    var afterReservationsChange = function () {
        $('#reservations-edit-dlg').modal('hide');
        $('body').removeClass('modal-open');
        $('.modal-backdrop').remove();
        $('#admin-tabs').find('a[rel=reservations]').tab('show');
    };

    $('#admin-gallery-add').find(':button').click(function(){
        var formData = new FormData($('#admin-gallery-add')[0]);
        if (formData != null) {
            $('#admin-gallery-add .ajax-loading').show();
            $.ajax({
                url: '/gallery_upload',  //Server script to process data
                type: 'POST',
                //Ajax events
                success: function(response){
                    $('#admin-gallery-tab').find('div.alert.alert-success').remove();
                    $('#admin-gallery-tab').prepend('<div class="alert alert-success">DODANO: '+response+'.</div>');
                    $('#admin-gallery-add .ajax-loading').hide();
                },
                error: function(exception){
                    $('#admin-gallery-add .ajax-loading').hide();
                    alert(exception);
                },
                // Form data
                data: formData,
                //Options to tell jQuery not to process data or worry about content-type.
                cache: false,
                contentType: false,
                processData: false
            });
        } else {
            alert('Proszę wybrać plik.');
        }
    });

    $('.img-to-enlarge').popover({
        html: true,
        trigger: 'hover',
        placement: 'right',
        content: function () {
            return '<img class="img-thumbnail img-responsive" style="float:right" src="'+this.src+'"/>';
        }
    });

};

$(document).ready((function () {
    admin.initLayout = $(function () {
        admin.initEventHandlers();
    });
}));



// This class provides methods for Booking application
// =============================================================================
// Public interface
// booking.js
// =============================================================================

var booking = booking || {};

booking.initEventHandlers = function () {

	//HANDLE CHANGING TABS THROUGH MENU BUTTONS
	$('.navbar-collapse .navbar-nav > li > a').on('click', function (e) {

		var tab = $(this).attr('value').toLowerCase().replace(' ', '');
        var clicked = $(this);

		$.get(tab, function (data) {

			$('#main-content').empty();
			$('#main-content').hide().html(data).fadeIn();
            $('.navbar-collapse .navbar-nav > li').removeClass('active');
            clicked.parent().addClass('active');

			switch (tab) {

				case 'news':
					booking.jumbotronWide();
					news.initEventHandlers();
					break;

				case 'calendar':
					booking.jumbotronHide();
					calendar.initLayout();
					$('#main-content #calendar-add-event').css('padding-top', '0px');
					break;

				case 'reservations':
					booking.jumbotronNarrow();
					reservations.initEventHandlers();
					$('#main-content #calendar-add-event').css('padding-top', '0px');
					break;

				case 'gallery':
					booking.jumbotronHide();
					gallery.initEventHandlers();
					break;

                case 'dishes':
                    booking.jumbotronHide();
                    dishes.initEventHandlers();
                    break;

				case 'about':
					booking.jumbotronWide();
					break;

                case 'admin':
                    booking.jumbotronHide();
                    admin.initEventHandlers();
                    break;
			}
		});
	});

	$('#login-dlg-logon-btn').on( 'click' , function (e) {

	    var email = $('#login-mail').val();
		var password = $('#login-password').val();

		var json = {
			'email'		: email,
			'password'  : password
		};

		$.postJSON('/login', json, function (data) {
			if (Boolean(data.status) == true) {
				alert('Logged.');
			} else {
				alert(data.desc);
			}
		});

	});

	$('#jumbotron-reservation').on( 'click' , function (e) {
		$.get('reservations', function (data) {
			$('#main-content').empty();
			$('#main-content').html(data);
			reservations.initEventHandlers();
			booking.jumbotronNarrow();
			$('#main-content #calendar-add-event').css('padding-top', '0px');
		});
	});

    $("#fb-plugin").hover(function(){
        $(this).stop().animate({right: "0"}, "medium");
    }, function(){
        $(this).stop().animate({right: "-245"}, "medium");
    });

};

$(document).ready( (function() {

	booking.initLayout = $(function () {

    	booking.initEventHandlers();

	});
}));

booking.jumbotronWide = function () {
	$('.jumbotron .btn-lg').show();
    $('.jumbotron').css('display', '');
	//$('.jumbotron').animate({'padding-bottom': '48px', 'padding-top': '48px'} , 500);
};

booking.jumbotronNarrow =  function () {
	$('.jumbotron .btn-lg').hide();
    $('.jumbotron').css('display', '');
	//$('.jumbotron').animate({'padding-bottom': '0px', 'padding-top': '0px'} , 500);
};

booking.jumbotronHide = function () {
	$('.jumbotron .btn-lg').show();
    $('.jumbotron').css('display', 'none');
};


// This class provides methods for Booking application
// =============================================================================
// Calendar section scripts
// calendar.js
// =============================================================================

var calendar = calendar || {};

calendar.initEventHandlers = function () {

	$('.fc-header-left .fc-button').removeClass().addClass('btn btn-primary');
	$('.fc-header-center .fc-button').removeClass().addClass('btn btn-primary');
	$('.fc-header-right .fc-button-today').removeClass().addClass('btn btn-primary');
	$('.fc-header-right .fc-button-prev').removeClass().addClass('btn btn-primary').text('<<');
	$('.fc-header-right .fc-button-next').removeClass().addClass('btn btn-primary').text('>>');

	$('.datepicker').datepicker({
		format: 'yyyy-mm-dd',
		weekStart : 1,
		autoclose: true
	});

	$('.timepicker').timepicker({showMeridian: false});

};

calendar.initLayout = function () {

	calendar.div = '#calendar-div';

	$(calendar.div).fullCalendar({
		theme: false, //Enable theming from jQuery-UI
		firstDay: 1,
		weekMode: 'liquid',

		//SETUP HEADER
		header: {
			left: 'title',
			center: 'month,agendaWeek,agendaDay',
			right: 'today prev,next',
		},

		defaultView: 'agendaWeek',
		allDaySlot: true, //Remove summary slot from agenda view

		//DATASOURCE
		events: '/events_view',

		//SETUP TIME
		defaultEventMinutes: 60,
		firstHour: 7,
		minTime: 6,
		maxTime: 22,
		axisFormat: 'H:mm', //,'h(:mm)tt',
    	timeFormat: {
        	'': 'H:mm{-H:mm}', //h:mm{ - h:mm}'
        	'agenda': 'H:mm{-H:mm}' //h:mm{ - h:mm}'
    	},

		//SETUP BUTTON TEXTS
		buttonText: {
		    prev:     '&lsaquo;', // <
		    next:     '&rsaquo;', // >
		    prevYear: '&laquo;',  // <<
		    nextYear: '&raquo;',  // >>
		    today:    'Dziś',
		    month:    'Miesiąc',
		    week:     'Tydzień',
		    day:      'Dzień'
		},

		//SETUP DISPLAYING NAMES
		monthNames : ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'],
		monthNamesShort : ['Sty', 'Lut', 'Mar', 'Kwi', 'Maj', 'Cze', 'Lip', 'Sie', 'Wrz', 'Paź', 'Lis', 'Gru'],
		dayNames : ['Niedziela', 'Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota'],
		dayNamesShort : ['Nie', 'Pn', 'Wt', 'Śr', 'Czw', 'Pt', 'Sob'],

		//DAY CLICK - MOVE TO DAY AGENDA
		dayClick: function(date, allDay, jsEvent, view) {
        	if (allDay) {
            	// Clicked on the entire day
            	$(calendar.div)
                	.fullCalendar('changeView', 'agendaDay'/* or 'basicDay' */)
                	.fullCalendar('gotoDate', date.getFullYear(), date.getMonth(), date.getDate());
        	}
    	},

    	//EVENT CLICK - CREATE NEW EVENT
		eventClick: function(calEvent, jsEvent, view) {

			$('#event-edit-dlg').modal();

			$('#calendar-edit-event-date').val($.fullCalendar.formatDate( calEvent.start, 'yyyy-MM-dd')).datepicker('update');;
			$('#calendar-edit-event-time-start').val($.fullCalendar.formatDate( calEvent.start, 'HH:mm'));
			$('#calendar-edit-event-time-end').val($.fullCalendar.formatDate( calEvent.end, 'HH:mm'));
			$('#calendar-edit-event-title').val(calEvent.title);

			$('#calendar-edit-event-save-btn').unbind().on('click', function (e) {
				var date = $('#calendar-edit-event-date').val();
				var time_start = $('#calendar-edit-event-time-start').val();
				var time_end = $('#calendar-edit-event-time-end').val();
				var title = $('#calendar-edit-event-title').val();

				var json = {
					'date_start': date+' '+time_start,
					'date_end'  : date+' '+time_end,
					'title'     : title,
					'id'		: calEvent.id
				};

				$.postJSON('/events_edit', json, function (data) {
					if (Boolean(data.status) == true) {
						$(calendar.div).fullCalendar( 'refetchEvents' );
					}
				});
			});
    	}

	});

	calendar.initEventHandlers();

};


// This class provides methods for Booking application
// =============================================================================
// Dishes section scripts
// dishes.js
// =============================================================================

var dishes = dishes || {};

dishes.initEventHandlers = function () {
	$('.img-to-enlarge').popover({
        html: true,
        trigger: 'hover',
        placement: 'right',
        content: function () {
            return '<img class="img-thumbnail img-responsive" style="float:right" src="'+this.src+'"/>';
        }
    });
};

$(document).ready( (function() {
	dishes.initLayout = $(function () {
   		dishes.initEventHandlers();
	});
}));


// This class provides methods for Booking application
// =============================================================================
// Gallery section scripts
// gallery.js
// =============================================================================

var gallery = gallery || {};

gallery.initEventHandlers = function () {
    $('.least-gallery').least();
};

$(document).ready( (function() {
	gallery.initLayout = $(function () {
   		gallery.initEventHandlers();
	});
}));


// This class provides methods for Booking application
// =============================================================================
// News section scripts
// news.js
// =============================================================================

var news = news || {};

news.initEventHandlers = function () {

};

$(document).ready( (function() {
	news.initLayout = $(function () {
   		news.initEventHandlers();
	});
}));


// This class provides methods for Booking application
// =============================================================================
// Reservations interface
// reservations.js
// =============================================================================

var reservations = reservations || {};

reservations.initEventHandlers = function () {

	$('.datepicker').datepicker({
		format: 'yyyy-mm-dd',
		weekStart : 1,
		autoclose: true
	});

	$('.timepicker').timepicker({showMeridian: false});

	$('#reservations-add-btn').on('click', function (e) {

        $('#reservations-form').find('.alert').remove();

		var date = $('#reservation-date').val(),
		    time_start = $('#reservation-time-start').val(),
		    time_end = $('#reservation-time-end').val(),
		    title = $('#reservation-title').val(),
		    phone = $('#reservation-phone').val(),
		    email = $('#reservation-email').val();

        var error = false;

        $.each([date, time_start, time_end, title, phone, email], function (index, element) {
            if (element == null || element == ''){
                error = true;
            }
        });

        if (error == true){
            $('#reservations-form').prepend('<div class="alert alert-danger">BŁĄD: Wszystkie pola są wymagane. Proszę poprawić.</div>');
            return;
        }

        var json = {
            'date_start': date+' '+time_start,
            'date_end'  : date+' '+time_end,
            'title'     : title,
            'email'		: email,
            'phone'     : phone
        };

		$.postJSON('reservations_add', json, function (reserv) {

            $.get('reservations', function (data) {
                $('#main-content').empty();
                $('#main-content').html(data);
                reservations.initEventHandlers();
                booking.jumbotronNarrow();
                if (reserv.status==true) {
                    $('#reservations-form').prepend('<div class="alert alert-success">Rezerwacja zatwierdzona. Data: '+date+' '+time_start+'.</div>');
                }
            });
        });

	});
};

//$(document).ready( (function() {
//	reservations.initLayout = $(function () {
//  		reservations.initEventHandlers();
//	});
//}));

// --------------------------------------------------------------------------
// Helpers
// setup.js
// --------------------------------------------------------------------------

jQuery.extend(jQuery.expr[':'], {
	focus: function(element) {
		return element == document.activeElement;
	}
});

$(document).ready(function(){

	// ===========================================================================
	// Extend jQuery AJAX with new methods
	// ===========================================================================

	/*
	 * Add delete and put HTTP commands
	 */
	jQuery.each(["delete", "put" ], function(i, method ) {
		jQuery[ method ] = function( url, data, callback, type ) {
			// shift arguments if data argument was omitted
			if ( jQuery.isFunction( data ) ) {
				type = type || callback;
				callback = data;
				data = undefined;
			}

			return jQuery.ajax({
				type: method,
				url: url,
				data: data,
				success: callback,
				dataType: type
			});
		};
	});

	/*
	 * Add ability to send JSON data inside POST body
	 */
	jQuery['postJSON'] = function(url, data, callback) {
		return jQuery.ajax({
			type: "POST",
			dataType: "json",
			contentType: "json",
			url: url,
			data: JSON.stringify(data),
			success: function(data){
				if (data != null) {
					if (!data.status) {
						showError(data.desc);
					}
					if (jQuery.isFunction(callback)) {
						callback(data);
					}
				} else {
					showError('Invalid response from the server');
				}
			}
		});
	};

	// ===========================================================================
	// Setup UI
	// ===========================================================================

	// AJAX Setup
	jQuery.ajaxSetup({
		cache: false,
		error : function(x, e){
			var txt = '';
			if(x.status==0){
				return;
			}else if(x.status==404){
				txt = "Requested URL wasn't found.";
			}else if(x.status==401){
				txt = 'You are not authorized to access to this option/page.';
			}else if(x.status==500){
				txt = 'Internal Server Error occured.';
			}else if(e=='parsererror'){
				// Caused by AJAX requests on logout sessions...
				return;
			}else if(e=='timeout'){
				txt = 'Request Timed out.';
			}else {
				if (console) {
					console.error(x.status);
				}
				return;
			}
		}
	});

    var sName = "CookiesAccepted";

    $("#close-cookie-warn").click(function(){
        var oExpire = new Date();
        oExpire.setTime((new Date()).getTime() + 3600000*24*365);
        document.cookie = sName + "=1;expires=" + oExpire;
        $("#cookie-warn").hide("slow");
    });

    var sStr = '; '+ document.cookie +';';
    var nIndex = sStr.indexOf('; '+ escape(sName) +'=');

    if (nIndex === -1) {
        $("#cookie-warn").show();
    }

});