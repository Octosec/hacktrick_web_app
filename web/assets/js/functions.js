
$(window).scroll(function() { 
    $(".primary-menu").removeClass("fixed-top-menu");
    var scroll = $(window).scrollTop();
    if (scroll > 200) {
        $(".primary-menu").addClass("fixed-top-menu");
    }
});

$(window).scroll(function() { 
    $(".primary-menu").removeClass("fixed-top-menu1");
    var scroll = $(window).scrollTop();
    if (scroll > 90) {
        $(".primary-menu").addClass("fixed-top-menu1");
    }
});







// client section
var swiper = new Swiper('.testimonial-container', {
    spaceBetween: 50,
    grabCursor: false,
    autoplay: 3000,
    slidesPerView: 3,
     breakpoints: {
            1400: {
                slidesPerView: 2
            },
            768: {
                slidesPerView: 1
            }
        }
});


// sticky sider bar
$(document).ready(function() {
	$('#main-content, #sidebar')
		.theiaStickySidebar({
			additionalMarginTop: 30
		});
});


// product zoom
//initiate the plugin and pass the id of the div containing gallery images 
$("#img_01").elevateZoom({
    gallery:'gal1',  
    galleryActiveClass: 'active', 
    imageCrossfade: true, 
    zoomWindowWidth:430,
    zoomWindowHeight:500,
    scrollZoom : true ,
    zoomType  : "lens", 
    lensShape : "round", 
    lensSize : 200 
}); 


//pass the images to Fancybox 
$("#img_01").bind("click", function(e) { 
var ez = $('#img_01').data('elevateZoom');  
$.fancybox(ez.getGalleryList());
return false;
 });


$('#myTab a').click(function (e) {
  e.preventDefault();
  $(this).tab('show');
})


$('#myTab1 a').click(function (e) {
  e.preventDefault();
  $(this).tab('show');
})


// boxer
$(".boxer").boxer();


// price range js
$('.nstSlider').nstSlider({
    "left_grip_selector": ".leftGrip",
    "right_grip_selector": ".rightGrip",
    "value_bar_selector": ".bar",
    "value_changed_callback": function(cause, leftValue, rightValue) {
        $(this).parent().find('.leftLabel').text(leftValue);
        $(this).parent().find('.rightLabel').text(rightValue);
    }
});


$(window).load(function() {
    $("#loading").delay(2000).fadeOut(500);
    $("#loading-center").click(function() {
    $("#loading").fadeOut(500);
    })
})

// $('.countdown').final_countdown({
//     'start': 1362139200,
//     'end': 1388461320,
//     'now': 1387461319
// });