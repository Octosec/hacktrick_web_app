/*global $, jQuery, alert*/
(function ($) {
    "use strict";
    
    $('body').animate({opacity : 1}, 600);
    
    // Parallax
    
    var isOpera, isFirefox, isSafari, isIE, isEdge, isChrome, isBlink, isMob;
    isOpera = (!!window.opr && !!opr.addons) || !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;
    isFirefox = typeof InstallTrigger !== 'undefined';
    isSafari = Object.prototype.toString.call(window.HTMLElement).indexOf('Constructor') > 0;
    isIE =  navigator.userAgent.indexOf("MSIE ");
    isEdge = !isIE && !!window.StyleMedia;
    isChrome = !!window.chrome && !!window.chrome.webstore;
    isBlink = (isChrome || isOpera) && !!window.CSS;
    isMob =  (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent));
    if (isChrome || isFirefox  || isSafari) {
        if ($(window).width() > 992) {
            $('.parallax').vossenParallax();
        };
        $(window).scroll(function () {
            function parallaxHero() {
                var scrolled = $(window).scrollTop();
                if ($(window).width() > 992) {
                    $('.map-parallax').css('top', -(scrolled * 0.4) + 'px');
                    $(".slide").css({transform: 'translate3d(0px, ' + (scrolled * 0.4) + 'px, 0px)'});
                }
            }
            parallaxHero();
        });
    }
    
    $(window).load(function () {
        $('.parallax-bg img').animate({opacity : 1}, 1000);
        $('.white-until-load').css({color : "#191a1c"});
    });
    
    // Header Dropdown
    
    $('.dropdown-toggle, .dropdown-submenu>a').click(function () {
        $(this).closest('.dropdown').siblings().removeClass('open');
        $(this).closest('.dropdown').toggleClass('open');
        return false;
    });
    
    // Header Animation
    
    $(window).scroll(function () {
        if ($(this).scrollTop() > 1) {
            $('nav').addClass("nav-small");
        } else {
            $('nav').removeClass("nav-small");
        }
        if ($(this).scrollTop() > 600) {
            $("#back-to-top").stop().animate({ opacity: '1' }, 150);
        } else {
            $("#back-to-top").stop().animate({ opacity: '0' }, 150);
        }
    });
    
    // Lighbox
    
    $(".gallery-item").magnificPopup({
        type: 'image',
        gallery: { enabled: true },
        mainClass: 'my-mfp-slide-bottom'
    });
    $('.popup-youtube,.popup-vimeo,.popup-gmaps,.popup-video').magnificPopup({
        disableOn: 700,
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false
    });

    // Search Modal
    
    $('.popup-with-zoom-anim').magnificPopup({
        type: 'inline',
        fixedContentPos: false,
        fixedBgPos: true,
        overflowY: 'auto',
        closeBtnInside: true,
        preloader: false,
        midClick: true,
        removalDelay: 300,
        mainClass: 'my-mfp-slide-bottom'
    });
    
    $('.search').click(function () {
        setTimeout(function timeoutFunction() {
            $('#search-modal-input').focus();
        }, 100);
    });
     
    // Smooth Scroll to Anchor
    
    $('body').on('click', "scroll-btn,.btn-scroll", function (event) { 
        var $anchor = $(this);
        if ($(window).width() > 992) {
            $('html, body').stop().animate({
                scrollTop: $($anchor.attr('href')).offset().top - 53
            }, 1000, 'easeInOutExpo');
            event.preventDefault();
        } else {
            $('html, body').stop().animate({
                scrollTop: $($anchor.attr('href')).offset().top + 5
            }, 1000, 'easeInOutExpo');
            event.preventDefault();
        }
    });

    // Owl Sliders
    
    $(".hero-slider").owlCarousel({
        autoplay: true,
        items: 1,
        dots: false,
        nav: true,
        rewindNav: true,
        loop: true,
        navText: ["<img src='img/assets/slider-left-thin-arrow.png'>", "<img src='img/assets/slider-right-thin-arrow.png'>"]
    });
    
    $(".content-slider").owlCarousel({
        animateOut: 'bounceOut',
        animateIn: 'bounceIn',
        autoplay: true,
        autoplayTimeout: 2500,
        items: 1,
        dots: false,
        mouseDrag: false,
        touchDrag: false,
        loop: true
    });
    
    $(".team-slider").owlCarousel({
        autoplay : false,
        items: 3,
        dots: true,
        responsiveRefreshRate: 200,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1200: {
                items: 3
            }
        }
    });
    
    $(".testimonials").owlCarousel({
        autoplay : true,
        autoplayTimeout: 3000,
        autoplaySpeed: 700,
        loop: true,
        items: 1,
        dots: true,
        dotsSpeed: 400
    });
    
    $("#clients-slider-2").owlCarousel({
        autoplay : true,
        autoplayTimeout: 4000,
        loop: false,
        dots: false,
        nav: false,
        responsiveRefreshRate: 200,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 5
            },
            1200: {
                items: 7
            }
        }
    });
    
    $(".project-carousel,.slider-block-1").owlCarousel({
        autoplay : true,
        autoplayTimeout: 4000,
        loop: false,
        items: 1,
        dots: true,
        nav: true,
        navText: ["<img src='img/assets/slider-left-thin-arrow-dark.png'>", "<img src='img/assets/slider-right-thin-arrow-dark.png'>"]
    });
    
    $(".shop-product-slider").owlCarousel({
        autoplay : true,
        autoplayTimeout: 3000,
        nav: true,
        navText: ["<img src='img/assets/slider-left-thin-arrow-dark.png'>", "<img src='img/assets/slider-right-thin-arrow-dark.png'>"],
        dots: true,
        items: 1
    });
    
    $(".image-slider1,.image-slider2,.image-slider5,.image-slider6,.image-slider7").owlCarousel({
        nav: true,
        navText: ["<img src='img/assets/slider-left-thin-arrow.png'>", "<img src='img/assets/slider-right-thin-arrow.png'>"],
        slideSpeed : 300,
        dots: true,
        items: 1
    });
 
    $(".image-slider3,.image-slider4").owlCarousel({
        nav : false,
        dots: true,
        dotsSpeed : 400,
        items: 1,
    });
    
    // Contact Form
    
    $('#contactform').submit(function () {
		var action = $(this).attr('action');
		$("#message").slideUp(250, function () {
            $('#message').hide();
            $('#submit')
                .after('<img src="img/assets/contact-form-loader.gif" class="loader" />')
                .attr('disabled', 'disabled');
            $.post(action, {
                name: $('#name').val(),
                email: $('#email').val(),
                comments: $('#comments').val()
            },
                function (data) {
                    document.getElementById('message').innerHTML = data;
                    $('#message').slideDown(250);
                    $('#contactform img.loader').fadeOut('slow', function () {$(this).remove(); });
                    $('#submit').removeAttr('disabled');
                    if (data.match('success') !== null) {
                        $('#contactform').slideUp(850, 'easeInOutExpo');
                    }
                });
		});
		return false;
	});
    
    //Subscribe form
    
    $('#subscribe-form,#subscribe-form2').on('submit', function (e) {
        e.preventDefault();
        var $el = $(this),
            $alert = $el.find('.form-validation'),
            $submit = $el.find('button'),
            action = $el.attr('action');
        $submit.button('loading');
        $alert.removeClass('alert-danger alert-success');
        $alert.html('');
        $.ajax({
            type     : 'POST',
            url      : action,
            data     : $el.serialize() + '&ajax=1',
            dataType : 'JSON',
            success  : function (response) {
                if (response.status === 'error') {
                    $alert.html(response.message);
                    $alert.addClass('alert-danger').fadeIn(500);
                } else {
                    $el.trigger('reset');
                    $alert.html(response.message);
                    $alert.addClass('alert-success').fadeIn(500);
                }
                $submit.button('reset');
            }
        });
    });

    // Progress Bars
    
    $('.progress-bars,.progress-bars-2,.progress-bars-3,.progress-bars-4').waypoint(function () {
        $('.progress').each(function () {
            $(this).find('.progress-bar').animate({
                width: $(this).attr('data-percent')
            }, 800);
        });
    }, { offset: '100%', triggerOnce: true });

    // Progress Circles 
    
    $('.progress-circle').waypoint(function () {
        var totalProgress, progress, circles;
        circles = document.querySelectorAll('.progress-svg');
            for(var i = 0; i < circles.length; i++) {
                totalProgress = circles[i].querySelector('circle').getAttribute('stroke-dasharray');
                progress = circles[i].parentElement.getAttribute('data-circle-percent');
                circles[i].querySelector('.bar').style['stroke-dashoffset'] = totalProgress * progress / 100;
            }
    }, { offset: '70%', triggerOnce: true });
    
    // Counter Up
    
    $('.counter h1').counterUp({
        delay: 8,
        time: 1400
    });
    
    // Countdown
    
    $(function () {
        var dateUser, deadline, interval;
        dateUser = $("#countdown-timer").attr('data-date');
        deadline = new Date(dateUser);
        function updateClock() {
            var today, diff, seconds, minutes, hours, days, months;
            today = Date();
            diff = Date.parse(deadline) - Date.parse(today);
            if (diff <= 0) {
                clearInterval(interval);
            } else {
                seconds = Math.floor((diff / 1000) % 60);
                minutes = Math.floor((diff / 1000 / 60) % 60);
                hours = Math.floor((diff / 1000 / 60 / 60) % 24);
                days = Math.floor(diff / (1000 * 60 * 60 * 24) % 30.5);
                months = Math.floor(diff / (1000 * 60 * 60 * 24 * 30.5) % 12);
                $("#months").text(('0' + months).slice(-2));
                $("#days").text(('0' + days).slice(-2));
                $("#hours").text(('0' + hours).slice(-2));
                $("#minutes").text(('0' + minutes).slice(-2));
                $("#seconds").text(('0' + seconds).slice(-2));
            }
        }
        interval = setInterval(updateClock, 1000);
    });
    
    // Accordions, Toggles, Tooltips, Tabs
    
    $('#accordion,#accordion2').on('show.bs.collapse', function () {
        $('#accordion .in').collapse('hide');
    });
    $("[data-toggle='tooltip']").tooltip();
    $(".alert").alert();
    $('#buttonTabs a,#iconTabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });
    
    // Back to Top
    
    $('#back-to-top,.to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 700);
        return false;
    });
    
    // Instagram Feed
    
    $(function () {
        if ($('#instagram-feed').length) {
            $.fn.spectragram.accessData = {
                accessToken: '2985464939.7329358.026dd38d94c046c3aac748818d3c50c2',
                clientID: '7329358a04c0403c8389201ef5e4733b'
            };

            var instagramUser = document.getElementById("instagram-feed").getAttribute("data-instagram-username");
            $('#instagram-feed ul').spectragram('getUserFeed', {
                query: instagramUser,
                max: 8,
                size: 'small'
            });
        }
    });
  
    // Twitter Feed
    
    $(function () {
        if ($('#twitter-feed').length) {
            var twitterUser, tweets;
            twitterUser = document.getElementById("twitter-feed").getAttribute("data-twitter-widget-id");
            tweets = {
                "id": twitterUser,
                "domId": 'twitter-feed',
                "maxTweets": 2,
                "enableLinks": true,
                "showImages": false
            };
            twitterFetcher.fetch(tweets);
        }
    });
    
    // PortfolioGrid
    $('#js-grid').cubeportfolio({
        filters: '#js-filters',
        layoutMode: 'grid',
        sortToPreventGaps: true,
        mediaQueries: [{
            width: 1500,
            cols: 3
        }, {
            width: 1100,
            cols: 3
        }, {
            width: 800,
            cols: 3
        }, {
            width: 480,
            cols: 2
        }, {
            width: 320,
            cols: 1
        }],
        defaultFilter: '*',
        animationType: 'sequentially',
        gapHorizontal: 15,
        gapVertical: 15,
        caption: 'zoom',
        displayType: 'sequentially',
        displayTypeSpeed: 100
    });
    
    // Portfolio Metro 
    $('#js-grid-mosaic').cubeportfolio({
        filters: '#js-filters',
        layoutMode: 'mosaic',
        sortToPreventGaps: true,
        mediaQueries: [{
            width: 1500,
            cols: 4
        }, {
            width: 1100,
            cols: 4
        }, {
            width: 800,
            cols: 3
        }, {
            width: 480,
            cols: 2
        }, {
            width: 320,
            cols: 1
        }],
        defaultFilter: '*',
        animationType: 'sequentially',
        gapHorizontal: 0,
        gapVertical: 0,
        caption: 'zoom',
        displayType: 'sequentially',
        displayTypeSpeed: 100
    });
    
    // Portfolio Fullwidth
    $('#js-grid-no-gutter').cubeportfolio({
        filters: '#js-filters',
        layoutMode: 'grid',
        sortToPreventGaps: true,
        mediaQueries: [{
            width: 1500,
            cols: 3
        }, {
            width: 1100,
            cols: 3
        }, {
            width: 800,
            cols: 3
        }, {
            width: 480,
            cols: 2
        }, {
            width: 320,
            cols: 1
        }],
        defaultFilter: '*',
        animationType: 'sequentially',
        gapHorizontal: 0,
        gapVertical: 0,
        caption: 'zoom',
        displayType: 'sequentially',
        displayTypeSpeed: 100,
        // lightbox
        lightboxDelegate: '.cbp-lightbox',
        lightboxGallery: true,
        lightboxTitleSrc: 'data-title',
        lightboxCounter: ''
    });
    
    // Portfolio Masonry Fullwidth
    $('#js-masonry-fullwidth').cubeportfolio({
        filters: '#js-filters',
        layoutMode: 'grid',
        sortToPreventGaps: true,
        mediaQueries: [{
            width: 1500,
            cols: 4
        }, {
            width: 1100,
            cols: 4
        }, {
            width: 800,
            cols: 3
        }, {
            width: 480,
            cols: 2
        }, {
            width: 320,
            cols: 1
        }],
        defaultFilter: '*',
        animationType: 'sequentially',
        gapHorizontal: 15,
        gapVertical: 15,
        caption: 'zoom',
        displayType: 'sequentially',
        displayTypeSpeed: 100
    });
    
    // Portfolio Masonry Boxed
    $('#js-masonry-boxed').cubeportfolio({
        filters: '#js-filters',
        layoutMode: 'grid',
        sortToPreventGaps: true,
        mediaQueries: [{
            width: 1500,
            cols: 3
        }, {
            width: 1100,
            cols: 3
        }, {
            width: 800,
            cols: 3
        }, {
            width: 480,
            cols: 2
        }, {
            width: 320,
            cols: 1
        }],
        defaultFilter: '*',
        animationType: 'sequentially',
        gapHorizontal: 15,
        gapVertical: 15,
        caption: 'zoom',
        displayType: 'sequentially',
        displayTypeSpeed: 100
    });
    
    // Portfolio Carousel
    $('#js-grid-slider').cubeportfolio({
        layoutMode: 'slider',
        drag: true,
        auto: true,
        autoTimeout: 5000,
        autoPauseOnHover: true,
        showNavigation: false,
        showPagination: true,
        mediaQueries: [{
            width: 1680,
            cols: 3
        }, {
            width: 1350,
            cols: 3
        }, {
            width: 800,
            cols: 4
        }, {
            width: 480,
            cols: 2
        }, {
            width: 320,
            cols: 1
        }],
        gapVertical: 30,
        caption: 'zoom',
        displayType: 'fadeIn',
        displayTypeSpeed: 400
    });
    
    // Blog Carousel
    $('#js-blog-carousel').cubeportfolio({
        layoutMode: 'slider',
        drag: true,
        auto: true,
        autoTimeout: 5000,
        autoPauseOnHover: true,
        showNavigation: false,
        showPagination: true,
        mediaQueries: [{
            width: 1680,
            cols: 4
        }, {
            width: 1350,
            cols: 3
        }, {
            width: 800,
            cols: 3
        }, {
            width: 480,
            cols: 2
        }, {
            width: 320,
            cols: 1
        }],
        gapVertical: 30,
        caption: 'zoom',
        displayType: 'fadeIn',
        displayTypeSpeed: 400
    });
    
    // Blog Masonry Fullwidth
    $('#blog-grid,#js-gallery-5').cubeportfolio({
        filters: '#js-filters',
        layoutMode: 'grid',
        sortToPreventGaps: true,
        mediaQueries: [{
            width: 1500,
            cols: 5
        }, {
            width: 1100,
            cols: 4
        }, {
            width: 800,
            cols: 2
        }, {
            width: 480,
            cols: 2
        }, {
            width: 320,
            cols: 1
        }],
        defaultFilter: '*',
        animationType: 'sequentially',
        gapHorizontal: 15,
        gapVertical: 15,
        caption: 'zoom',
        displayType: 'sequentially',
        displayTypeSpeed: 100
    });
    
    // Shop
    $('#shop-grid').cubeportfolio({
        filters: '#js-filters',
        layoutMode: 'grid',
        sortToPreventGaps: true,
        mediaQueries: [{
            width: 1500,
            cols: 4
        }, {
            width: 1100,
            cols: 3
        }, {
            width: 800,
            cols: 2
        }, {
            width: 480,
            cols: 2
        }, {
            width: 320,
            cols: 1
        }],
        defaultFilter: '*',
        animationType: 'sequentially',
        gapHorizontal: 30,
        gapVertical: 30,
        caption: 'zoom',
        displayType: 'sequentially',
        displayTypeSpeed: 100
    });
    
}(jQuery));