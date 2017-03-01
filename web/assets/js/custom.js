function countdown_init() {
		
		if($('#header-countdown').length) {
			var $obj=$('#header-countdown');
			var hideseconds=( $obj.data('hideseconds') ? true : false );
				
			var label_days=$obj.data('days');
			var label_hrs=$obj.data('hrs');
			var label_min=$obj.data('min');
			var label_sec=$obj.data('sec');
			
			var txt=$obj.text().replace( /^\s+/g, '').replace( /\s+$/g, '');
			var tmp=txt.split(' ');
			if(tmp.length == 2) {
				var tmp_d=tmp[0].split('-');
				var tmp_h=tmp[1].split(':');
				if(tmp_d.length == 3 && tmp_h.length == 3) {
					var monthNames = ["zero", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
					tmp_d[1]=parseInt(tmp_d[1]);
					if(isNaN(tmp_d[1])) {
						$obj.remove();
						return;
					}
					var timeGMT=$obj.data('gmt');
					if(typeof(timeGMT) == 'undefined' || timeGMT == '0') {
						timeGMT='';
					}
					var finaldate = new Date(monthNames[tmp_d[1]] + ' ' + tmp_d[2] + ', ' + tmp_d[0] + ' ' + tmp_h[0] + ':' + tmp_h[1] + ':' + tmp_h[2] + ' GMT'+timeGMT);
					$obj.html('').show();
					var $days=$('<div class="box-value" />');
					var $hrs=$('<div class="box-value" />');
					var $min=$('<div class="box-value" />');
					if(!hideseconds) {
						var $sec=$('<div class="box-value" />');
					}
					var $days_box=$('<div class="countdown-box box-days" />').append($days).append('<div class="box-label">'+label_days+'</div>').appendTo($obj);
					var $hrs_box=$('<div class="countdown-box box-hrs" />').append($hrs).append('<div class="box-label">'+label_hrs+'</div>').appendTo($obj);
					var $min_box=$('<div class="countdown-box box-min" />').append($min).append('<div class="box-label">'+label_min+'</div>').appendTo($obj);
					if(!hideseconds) {
						var $sec_box=$('<div class="countdown-box box-sec" />').append($sec).append('<div class="box-label">'+label_sec+'</div>').appendTo($obj);
					}

					var now=new Date();
					if(finaldate > now) {
					
						$obj.countdown(finaldate);
	
						if(!jQuery('html').hasClass('touch') || !jQuery(window).data('mobile-view')) {
							
							var last_offset={
								totalDays: 0,
								hours: 0,
								minutes: 0,
								seconds: 0
							}
							var transformY=83; // %
							
							$obj.on('update.countdown', function(event) {
								$days.text(event.offset.totalDays);
								$hrs.text(event.offset.hours);
								$min.text(event.offset.minutes);
								if(!hideseconds) {
									$sec.text(event.offset.seconds);
								}								
								if(last_offset.hours != event.offset.hours) {
									$days_box.find('.box-bg').remove();
									var k_days=(365-event.offset.totalDays)/365;
									$('<div class="box-bg" />').css({
										opacity: 1,
										transform: 'translateY('+(k_days*transformY)+'%)',
										animationDuration: (216000-k_days*216000)+'s'
									}).prependTo($days_box);
								}
								if(last_offset.hours != event.offset.hours) {
									$hrs_box.find('.box-bg').remove();
									var k_hrs=(24-event.offset.hours)/24;
									$('<div class="box-bg" />').css({
										opacity: 1,
										transform: 'translateY('+(k_hrs*transformY)+'%)',
										animationDuration: (216000-k_hrs*216000)+'s'
									}).prependTo($hrs_box);
								}						
								if(last_offset.hours != event.offset.hours) {
									$min_box.find('.box-bg').remove();
									var k_min=(59-event.offset.minutes)/59;
									$('<div class="box-bg" />').css({
										opacity: 1,
										transform: 'translateY('+(k_min*transformY)+'%)',
										animationDuration: (3600-k_hrs*3600)+'s'
									}).prependTo($min_box);
								}
								if(!hideseconds && last_offset.seconds != event.offset.seconds) {
									$sec_box.find('.box-bg').remove();
									//$('<div class="box-bg" />').prependTo($sec_box);
									var k_sec=(59-event.offset.seconds)/59;
									$('<div class="box-bg" />').css({
										opacity: 1,
										transform: 'translateY('+(k_sec*transformY)+'%)',
										animationDuration: (60-k_sec*60)+'s'
									}).prependTo($sec_box);
								}
								
								last_offset=event.offset;
	   					});
	   				
	   				} else {
	   					// mobile view, no animation
	   					
	   					$('<div class="box-bg mobile-bg" />').prependTo($min_box);
	   					$('<div class="box-bg mobile-bg" />').prependTo($hrs_box);
							if(!hideseconds) {
								$('<div class="box-bg mobile-bg" />').prependTo($sec_box);
							}

							$obj.on('update.countdown', function(event) {
								$days.text(event.offset.totalDays);
								$hrs.text(event.offset.hours);
								$min.text(event.offset.minutes);
								if(!hideseconds) {
									$sec.text(event.offset.seconds);
								}
	   					});
	   					
	   				}
	   				
	   			} else {
   					$('<div class="box-bg mobile-bg" />').prependTo($min_box);
   					$('<div class="box-bg mobile-bg" />').prependTo($hrs_box);
						if(!hideseconds) {
							$('<div class="box-bg mobile-bg" />').prependTo($sec_box);
						}
						$days.text(0);
						$hrs.text(0);
						$min.text(0);
						if(!hideseconds) {
							$sec.text(0);
						}
   				}

				} else {
					$obj.remove();
				}
			}	else {
				$obj.remove();
			}
		}
	}