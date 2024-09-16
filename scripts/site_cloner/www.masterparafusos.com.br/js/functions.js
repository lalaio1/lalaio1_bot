$ = jQuery.noConflict();

jQuery(window).on("load", function () {
    "use strict";

    /*  ===================================
     Loading Timeout
     ====================================== */
    $("#loader-fade").fadeOut(800);
    $('.side-menu').removeClass('d-none');

});

jQuery(function ($) {
    "use strict";

    var $window = $(window);
    var windowsize = $(window).width();

    /* ===================================
       Nav Scroll
       ====================================== */

    $(".scroll").on("click", function(event){
        event.preventDefault();
        $('html,body').animate({
            scrollTop: $(this.hash).offset().top - 40}, 1100);
    });
    /* ====================================
       Nav Fixed On Scroll
       ======================================= */

    if ($("nav.navbar").hasClass("static-nav")) {
        $(window).on("scroll", function () {
            var $scroll = $window.scrollTop();
            var $navbar = $(".static-nav");
            if ($scroll >= 80) {
                $navbar.addClass("fixed-menu");
            } else {
                $navbar.removeClass("fixed-menu");
            }
        });
    }

    /*bottom menu fix*/
    if ($("nav.navbar").hasClass("bottom-nav")) {
        var navHeight = $(".bottom-nav").offset().top;
        $(window).on("scroll", function () {
            if ($window.scrollTop() > navHeight) {
                $('.bottom-nav').addClass('fixed-menu');
            } else {
                $('.bottom-nav').removeClass('fixed-menu');
            }
        });
    }
    

        $(window).on("scroll resize", function () {
            if ($window.scrollTop() < 80 || window.innerWidth > 991) {
                $("#header-search").css('display', 'none');
            } else {
                $("#header-search").css('display', 'inline');
            }

        });
        $("#header-search").css('display', 'none');
        





    if ($("nav.navbar").hasClass("bottom-nav")) {
        $(window).on("scroll", function () {
            var $scroll = $window.scrollTop();
            var $bottom = $(".bottom-nav");
            if ($scroll >= 400) {
                $bottom.addClass("scroll-menu");
            } else {
                $bottom.removeClass("scroll-menu");
            }
        });
    }
        $(window).on('scroll', function () {
        if ($(this).scrollTop() >= 80) { // Set position from top to add class
            $('header').addClass('header-appear');
        }
        else {
            $('header').removeClass('header-appear');
        }
    });

    /*nav headroom effect*/
    var headRoom = {};
    headRoom.fixedHeader = function () {
        // grab an element
        $('#headroom').headroom(
            {
                "offset": 210,
                "tolerance": 5,
                "classes": {
                    "initial": "animates",
                    "pinned": "swingInX",
                    "unpinned": "swingOutX"
                }
            }
        );
    };
    headRoom.fixedHeader();

    /* ===================================
       Side Menu
       ====================================== */

    if ($("#sidemenu_toggle").length) {
        $("#sidemenu_toggle").on("click", function () {
            $(".pushwrap").toggleClass("active");
            $(".side-menu").addClass("side-menu-active"), $("#close_side_menu").fadeIn(700)
        }), $("#close_side_menu").on("click", function () {
            $(".side-menu").removeClass("side-menu-active"), $(this).fadeOut(200), $(".pushwrap").removeClass("active")
        }), $(".side-nav .navbar-nav .nav-link").on("click", function () {
            $(".side-menu").removeClass("side-menu-active"), $("#close_side_menu").fadeOut(200), $(".pushwrap").removeClass("active")
        }), $("#btn_sideNavClose").on("click", function () {
            $(".side-menu").removeClass("side-menu-active"), $("#close_side_menu").fadeOut(200), $(".pushwrap").removeClass("active")
        })
    }

    /* =====================================
            Wow
       ======================================== */

    if ($(window).width() > 767) {
        var wow = new WOW({
            boxClass: 'wow',
            animateClass: 'animated',
            offset: 0,
            mobile: false,
            live: true
        });
        new WOW().init();
    }

    /* ----- Full Screen ----- */
    function resizebanner() {
        var $fullscreen = $(".full-screen");
        $fullscreen.css("height", $window.height());
        $fullscreen.css("width", $window.width());
    }
    resizebanner();
    $window.resize(function () {
        resizebanner();
    });


    /* ===================================
       Features Section Number Scroller
       ====================================== */

    $(".stats").each(function () {
        $('.numscroller').appear(function () {
            $(this).prop('Counter',0).animate({
                Counter: $(this).text()
            }, {
                duration: 5000,
                easing: 'swing',
                step: function (now) {
                    $(this).text(Math.ceil(now));
                }
            });
        });
    });

    /* ===================================
       Equal Heights
       ====================================== */
    checheight();
    $window.on("resize", function () {
        checheight();
    });

    function checheight() {
        var $smae_height = $(".equalheight");
        if ($smae_height.length) {
            if (windowsize > 767) {
                $smae_height.matchHeight({
                    property: "height",
                });
            }
        }
    }

    /* ===================================
       Animated Progress Bar
       ====================================== */

    $(".progress-bar").each(function () {
        $(this).appear(function () {
            $(this).animate({width: $(this).attr("aria-valuenow") + "%"}, 2000)
        });
    });

    /* ===================================
       Parallax
       ====================================== */

    if (windowsize > 992) {
        $(".parallaxie").parallaxie({
            speed: 0.4,
            offset: 0,
        });
    }

    /* =====================================
       Portfolio Filter
       ======================================= */

    /*Portfolio Two*/

    // isotope
    $('.gallery').isotope({
        // options
        itemSelector: '.items'
    });

    var $gallery = $('.gallery').isotope({
        // options
    });

    // filter items on button click
    $('.filtering').on('click', 'span', function () {

        var filterValue = $(this).attr('data-filter');

        $gallery.isotope({filter: filterValue});

    });

    $('.filtering').on('click', 'span', function () {

        $(this).addClass('active').siblings().removeClass('active');

    });

    setTimeout(function (){
        $('.filtering .active').click();
    }, 1500);

    /* ===================================
       Cube Portfolio
       ====================================== */

    (function ($, window, document, undefined) {

        /*Blog Masonry*/
        $("#blog-masonry").cubeportfolio({
            layoutMode: 'grid',
            defaultFilter: '*',
            animationType: "scaleSides",
            gapHorizontal: 30,
            gapVertical: 30,
            gridAdjustment: "responsive",
            mediaQueries: [{
                width: 1500,
                cols: 3
            }, {
                width: 1100,
                cols: 3
            }, {
                width: 992,
                cols: 2
            }, {
                width: 600,
                cols: 2
            }, {
                width: 480,
                cols: 1
            }, {
                width: 320,
                cols: 1
            }]
        });

        /* Portfolio */
        $('#js-grid-mosaic').cubeportfolio({
            filters: '.filtering',
            layoutMode: 'grid',
            sortByDimension: true,
            mediaQueries: [{
                width: 767,
                cols: 2
            }, {
                width: 479,
                cols: 1,
                options: {
                    gapHorizontal: 60
                }
            }],

            defaultFilter: '*',
            animationType: 'fadeOut',
            gapVertical: 130,
            gapHorizontal: 110,

            gridAdjustment: 'responsive',
            caption: 'zoom',
            // lightbox
            lightboxDelegate: '.cbp-lightbox',
            lightboxGallery: true,
            lightboxTitleSrc: 'data-title',
            lightboxCounter: '<div class="cbp-popup-lightbox-counter">{{current}} of {{total}}</div>',

            plugins: {
                loadMore: {
                    element: "#js-loadMore-lightbox-gallery",
                    action: "click",
                    loadItems: 5,
                }
            }

        });

        // Shop
        $('#js-grid-blog-posts').cubeportfolio({
            filters: '#js-filters-mosaic-flat',
            search: '#js-search-blog-posts',
            defaultFilter: '*',
            animationType: "scaleSides",
            gapHorizontal: 0,
            gapVertical: 0,
            gridAdjustment: 'responsive',
            mediaQueries: [{
                width: 600,
                cols: 4,
                options: {
                    gapHorizontal: 10,
                    gapVertical: 20
                }
            }, {
                width: 390,
                cols: 3,
                options: {
                    caption: 'zoom',
                    gapHorizontal: 50,
                    gapVertical: 20
                }
            }, {
                width: 179,
                cols: 2,
                options: {
                    caption: 'zoom',
                    gapHorizontal: 5,
                    gapVertical: 2
                }
            }],

            caption: 'revealBottom',
            displayType: 'fadeIn',
            displayTypeSpeed: 400,
        });

        // Shop Detail
        $('#js-grid-clients').cubeportfolio({
            layoutMode: 'slider',
            drag: true,
            auto: true,
            loop: true,
            animationType: "scaleSides",
            autoTimeout: 3000,
            autoPauseOnHover: true,
            showNavigation: false,
            showPagination: false,
            rewindNav: true,
            scrollByPage: false,
            gridAdjustment: 'responsive',
            mediaQueries: [{
                width: 600,
                cols: 5
            }, {
                width: 390,
                cols: 3,
                options: {
                    caption: 'zoom',
                    gapHorizontal: 50,
                    gapVertical: 20
                }

            }, {
                width: 179,
                cols: 2,
                options: {
                    caption: 'zoom',
                    gapHorizontal: 50,
                    gapVertical: 20
                }
            }],
            gapHorizontal: 0,
            gapVertical: 0,

            caption: 'revealBottom',
            displayType: 'fadeIn',
            displayTypeSpeed: 400,
        });

        // Portfolio three column
        $('#js-grid-mosaic-flat').cubeportfolio({
            filters: '#js-filters-mosaic-flat',
            layoutMode: 'mosaic',
            defaultFilter: '*',
            animationType: "scaleSides",
            gapHorizontal: 0,
            gapVertical: 0,
            gridAdjustment: 'responsive',
            caption: 'zoom',
            displayType: 'fadeIn',
            displayTypeSpeed: 100,
            sortByDimension: true,
            mediaQueries: [{
                width: 1500,
                cols: 4
            }, {
                width: 1100,
                cols: 3
            }, {
                width: 768,
                cols: 2
            }, {
                width: 480,
                cols: 1
            }, {
                width: 320,
                cols: 1
            }],

            // lightbox
            lightboxDelegate: '.cbp-lightbox',
            lightboxGallery: true,
            lightboxTitleSrc: 'data-title',
            lightboxCounter: '<div class="cbp-popup-lightbox-counter">{{current}} of {{total}}</div>',

            plugins: {
                loadMore: {
                    element: '#js-loadMore-mosaic-flat',
                    action: 'click',
                    loadItems: 3
                }
            }
        })

            .on('initComplete.cbp', function () {
                // your functionality
                var $this = $(this);
                if ($(".cbp-filter-item-active").attr("data-filter") === "*") {
                    $("#js-loadMore-mosaic-flat").addClass("active");
                } else {
                    $("#js-loadMore-mosaic-flat").removeClass("active");
                }
                $this.find(".cbp-wrapper").find(".cbp-item:not(.cbp-item-off)").each(function (index) {
                    $(this).removeClass("even");

                    console.log()
                    var val = index + 1;
                    if ($(this).css('left') !== "0px") {
                        $(this).addClass("even");

                    }
                });
            })
            .on('onAfterLoadMore.cbp', function () {
                // your functionality
                var $this = $(this);
                $("#js-loadMore-mosaic-flat a").addClass("d-nones");
                $("#js-loadMore-mosaic-flat").addClass("active-outer");
                $this.find(".cbp-wrapper").find(".cbp-item:not(.cbp-item-off)").each(function (index) {
                    $(this).removeClass("even");
                    console.log()
                    var val = index + 1;
                    if ($(this).css('left') !== "0px") {
                        $(this).addClass("even");
                    }
                });
            })
            .on('filterComplete.cbp', function () {
                // your functionality
                var $this = $(this);
                if ($(".cbp-filter-item-active").attr("data-filter") === "*") {
                    $("#js-loadMore-mosaic-flat").addClass("active");
                    $("#js-loadMore-mosaic-flat").removeClass("d-nones");
                } else {
                    $("#js-loadMore-mosaic-flat").removeClass("active");
                    $("#js-loadMore-mosaic-flat").addClass("d-nones");
                }
                $this.find(".cbp-wrapper").find(".cbp-item:not(.cbp-item-off)").each(function (index) {
                    $(this).removeClass("even");
                    var val = index + 1;
                    if ($(this).css('left') !== "0px") {
                        $(this).addClass("even");
                    }
                });
            });

    })(jQuery, window, document);
    /* ===================================
       Fancy Box
       ====================================== */
    $('[data-fancybox]').fancybox({
        protect: true,
        animationEffect: "fade",
        hash: null,
    });

    /* ===================================
   Type Text
   ====================================== */

    if ($("#typewriting").length) {
        var app = document.getElementById("typewriting");
        var typewriter = new Typewriter(app, {
            loop: true
        });
        typewriter.typeString('Way to achieve success').pauseFor(2000).deleteAll()
            .typeString('Style to achieve success').pauseFor(2000).deleteAll()
            .typeString('Method to achieve success').start();
    }

    if ($("#personal").length) {
        var app = document.getElementById("personal");
        var personal = new Typewriter(app, {
            loop: true
        });
        personal.typeString('Photographer').pauseFor(2000).deleteAll()
            .typeString('Traveler').pauseFor(2000).deleteAll()
            .typeString('Model').start();
    }

    /* ===================================
       Rotating Text
       ====================================== */

    $("#js-rotating").Morphext({
        // The [in] animation type. Refer to Animate.css for a list of available animations.
        animation: "flipInX",
        // An array of phrases to rotate are created based on this separator. Change it if you wish to separate the phrases differently (e.g. So Simple | Very Doge | Much Wow | Such Cool).
        separator: ",",
        // The delay between the changing of each phrase in milliseconds.
        speed: 3000,
        complete: function () {
            // Called after the entrance animation is executed.
        }
    });

    /* ===================================
       Team Flip
       ====================================== */

        $(function () {
            $(".flip").flip({
                trigger: 'hover',
                axis: 'x'
            });
        });

    /* ===================================
       Contact Us
       ====================================== */

    $("#submit_btn").on('click', function () {

        //disable submit button on click
        $("#submit_btn").attr("disabled", "disabled");
        $("#submit_btn b").text('Sending');
        $("#submit_btn i").removeClass('d-none');

        var user_name = $('input[name=name]').val();
        var user_email = $('input[name=email]').val();
        var user_phone = $('input[name=phone]').val();
        var user_message = $('textarea[name=message]').val();

        //simple validation at client's end
        var post_data, output;
        var proceed = true;
        if (user_name == "") {
            proceed = false;
        }
        if (user_email == "") {
            proceed = false;
        }
        // if (user_phone == "") {
        //proceed = false;
        // }

        if (user_message == "") {
            proceed = false;
        }
        //everything looks good! proceed...
        if (proceed) {

            //data to be sent to server
            post_data = {
                'userName': user_name,
                'userEmail': user_email,
                'userPhone': user_phone,
                'userMessage': user_message
            };

            //Ajax post data to server
            $.post('contact.php', post_data, function (response) {

                //load json data from server and output message
                if (response.type == 'error') {
                    output = '<div class="alert-danger" style="padding:10px 15px; margin-bottom:30px;">' + response.text + '</div>';
                } else {
                    output = '<div class="alert-success" style="padding:10px 15px; margin-bottom:30px;">' + response.text + '</div>';

                    //reset values in all input fields
                    $('.contact-form input').val('');
                    $('.contact-form textarea').val('');
                }

                $("#result").hide().html(output).slideDown();

                // enable submit button on action done
                $("#submit_btn").removeAttr("disabled");
                $("#submit_btn b").text('SUBMIT REQUEST');
                $("#submit_btn i").addClass('d-none');

            }, 'json');

        }
        else {
            output = '<div class="alert-danger" style="padding:10px 15px; margin-bottom:30px;">Please provide the missing fields.</div>';
            $("#result").hide().html(output).slideDown();

            // enable submit button on action done
            $("#submit_btn").removeAttr("disabled");
            $("#submit_btn b").text('SUBMIT REQUEST');
            $("#submit_btn i").addClass('d-none');
        }

    });

    /* ===================================
       Animated Cursor
       ====================================== */

    function animatedCursor() {

        if ($("#animated-cursor").length) {

            var e = {x: 0, y: 0}, t = {x: 0, y: 0}, n = .25, o = !1, a =    document.getElementById("cursor"),
                i = document.getElementById("cursor-loader");
            TweenLite.set(a, {xPercent: -50, yPercent: -50}), document.addEventListener("mousemove", function (t) {
                var n = window.pageYOffset || document.documentElement.scrollTop;
                e.x = t.pageX, e.y = t.pageY - n
            }), TweenLite.ticker.addEventListener("tick", function () {
                o || (t.x += (e.x - t.x) * n, t.y += (e.y - t.y) * n, TweenLite.set(a, {x: t.x, y: t.y}))
            }),
                $(".animated-wrap").mouseenter(function (e) {
                    TweenMax.to(this, .3, {scale: 2}), TweenMax.to(a, .3, {
                        scale: 2,
                        borderWidth: "1px",
                        opacity: .2
                    }), TweenMax.to(i, .3, {
                        scale: 2,
                        borderWidth: "1px",
                        top: 1,
                        left: 1
                    }), TweenMax.to($(this).children(), .3, {scale: .5}), o = !0
                }),
                $(".animated-wrap").mouseleave(function (e) {
                    TweenMax.to(this, .3, {scale: 1}), TweenMax.to(a, .3, {
                        scale: 1,
                        borderWidth: "2px",
                        opacity: 1
                    }), TweenMax.to(i, .3, {
                        scale: 1,
                        borderWidth: "2px",
                        top: 0,
                        left: 0
                    }), TweenMax.to($(this).children(), .3, {scale: 1, x: 0, y: 0}), o = !1
                }),

                $(".testimonial-images .animated-wrap").mouseenter(function (e) {
                    TweenMax.to(this, .3, {scale: 2}), TweenMax.to(a, .3, {
                        scale: 2,
                        borderWidth: "1px",
                        opacity: .2
                    }), TweenMax.to(i, .3, {
                        scale: 2,
                        borderWidth: "1px",
                        top: 1,
                        left: 1
                    }), TweenMax.to($(this).children(), .3, {scale: .5}), o = !0
                }),

                $(".animated-wrap").mousemove(function (e) {
                    var n, o, i, l, r, d, c, s, p, h, x, u, w, f, m;
                    n = e, o = 2, i = this.getBoundingClientRect(), l = n.pageX - i.left, r = n.pageY - i.top, d = window.pageYOffset || document.documentElement.scrollTop, t.x = i.left + i.width / 2 + (l - i.width / 2) / o, t.y = i.top + i.height / 2 + (r - i.height / 2 - d) / o, TweenMax.to(a, .3, {
                        x: t.x,
                        y: t.y
                    }), s = e, p = c = this, h = c.querySelector(".animated-element"), x = 20, u = p.getBoundingClientRect(), w = s.pageX - u.left, f = s.pageY - u.top, m = window.pageYOffset || document.documentElement.scrollTop, TweenMax.to(h, .3, {
                        x: (w - u.width / 2) / u.width * x,
                        y: (f - u.height / 2 - m) / u.height * x,
                        ease: Power2.easeOut
                    })
                }),
                $(".hide-cursor,.btn,.tp-bullets").mouseenter(function (e) {
                    TweenMax.to("#cursor", .2, {borderWidth: "1px", scale: 2, opacity: 0})
                }), $(".hide-cursor,.btn,.tp-bullets").mouseleave(function (e) {
                TweenMax.to("#cursor", .3, {borderWidth: "2px", scale: 1, opacity: 1})
            }),$(".link").mouseenter(function (e) {
                TweenMax.to("#cursor", .2, {
                    borderWidth: "0px",
                    scale: 3,
                    backgroundColor: "rgba(255, 255, 255, 0.27)",
                    opacity: .15
                })
            }), $(".link").mouseleave(function (e) {
                TweenMax.to("#cursor", .3, {
                    borderWidth: "2px",
                    scale: 1,
                    backgroundColor: "rgba(255, 255, 255, 0)",
                    opacity: 1
                })
            })

        }

    }

    if ($(window).width() > 991) {
        setTimeout(function () {
            animatedCursor();
        }, 1000);
    }

    /* ===================================
       Accordion + Tabs
   ====================================== */
    $(".faq-items > li:first-child .sub-items").fadeIn();
    $(".faq-items > li:first-child >").addClass("expanded");
    $(".faq-items > li > a").on('click', function (e) {
        e.preventDefault();
        var $this = $(this);
        if ($this.hasClass("expanded")) {
            $this.removeClass("expanded");
        } else {
            $(".faq-items a.expanded").removeClass("expanded");
            $this.addClass("expanded");
            $(".sub-items").filter(":visible").slideUp("normal");
        }
        $this.parent().children("ul").stop(true, true).slideToggle("normal");
    });

    /*----- Tabs init -----*/
    $(function () {
        initTabsToAccordion();
    });

    function initTabsToAccordion() {
        var animSpeed = 500;
        var win = $(window);
        var isAccordionMode = true;
        var tabWrap = $(".tab-to-accordion");
        var tabContainer = tabWrap.find(".tab-container");
        var tabItem = tabContainer.children("div[id]");
        var tabsetList = tabWrap.find(".tabset-list");
        var tabsetLi = tabsetList.find("li");
        var tabsetItem = tabsetList.find("a");
        var activeId = tabsetList
            .find(".active")
            .children()
            .attr("href");
        cloneTabsToAccordion();
        accordionMode();
        tabsToggle();
        hashToggle();
        win.on("resize orientationchange", accordionMode);

        function cloneTabsToAccordion() {
            $(tabsetItem).each(function () {
                var $this = $(this);
                var activeClass = $this.parent().hasClass("active");
                var listItem = $this.attr("href");
                var listTab = $(listItem);
                if (activeClass) {
                    var activeClassId = listItem;
                    listTab.show();
                }
                var itemContent = $this.clone();
                var itemTab = $this.attr("href");
                if (activeClassId) {
                    itemContent
                        .insertBefore(itemTab)
                        .wrap('<div class="accordion-item active"></div>');
                } else {
                    itemContent
                        .insertBefore(itemTab)
                        .wrap('<div class="accordion-item"></div>');
                }
            });
        }
        function accordionMode() {
            var liWidth = Math.round(tabsetLi.outerWidth());
            var liCount = tabsetLi.length;
            var allLiWidth = liWidth * liCount;
            var tabsetListWidth = tabsetList.outerWidth();
            if (tabsetListWidth <= allLiWidth) {
                isAccordionMode = true;
                tabWrap.addClass("accordion-mod");
            } else {
                isAccordionMode = false;
                tabWrap.removeClass("accordion-mod");
            }
        }
        function tabsToggle() {
            tabItem.hide();
            $(activeId).show();
            $(tabWrap).on("click", 'a[href^="#tab"]', function (e) {
                e.preventDefault();
                var $this = $(this);
                var activeId = $this.attr("href");
                var activeTabSlide = $(activeId);
                var activeOpener = tabWrap.find('a[href="' + activeId + '"]');
                $('a[href^="#tab"]')
                    .parent()
                    .removeClass("active");
                activeOpener.parent().addClass("active");
                if (isAccordionMode) {
                    tabItem.stop().slideUp(animSpeed);
                    activeTabSlide.stop().slideDown(animSpeed);
                } else {
                    tabItem.hide();
                    activeTabSlide.show();
                }
            });
        }
        function hashToggle() {
            var hash = location.hash;
            var activeId = hash;
            var activeTabSlide = $(activeId);
            var activeOpener = tabWrap.find('a[href="' + activeId + '"]');
            if ($(hash).length > 0) {
                $('a[href^="#tab"]')
                    .parent()
                    .removeClass("active");
                activeOpener.parent().addClass("active");
                tabItem.hide();
                activeTabSlide.show();
                win
                    .scrollTop(activeTabSlide.offset().top)
                    .scrollLeft(activeTabSlide.offset().left);
            }
        }
    }


    /* ===================================
       Swiper
       ======================================*/

    /* Team */
    if ($(".swiper-container").hasClass("team-member-slider")) {
    var mySwiper = new Swiper('.swiper-container', {
        slidesPerView: 3,
        allowTouchMove: true,
        loop: true,
        centeredSlides: true,
        slideToClickedSlide: true,
        effect: "coverflow",
        nav:true,
        touchRatio: 0,
        autoplay: {
            delay: 3000
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev'
        },
        coverflow: {
            rotate: 190,
            stretch: 100,
            depth: 200,
            modifier: 1,
            slideShadows: false
        },
        breakpoints: {
            991: {
                slidesPerView: 2,
                centeredSlides: false,
                effect: "slide",
                touchRatio: 1
            },

            // when window width is <= 768px
            767: {
                slidesPerView: 1,
                centeredSlides: false,
                effect: "slide",
                touchRatio: 1
            }
        }
    });
    }

    $('.swiper-container').on('mouseenter', function(e){
        console.log('stop autoplay');
        mySwiper.autoplay.stop();
    })
    $('.swiper-container').on('mouseleave', function(e){
        console.log('start autoplay');
        mySwiper.autoplay.start();
    })
    /* ===================================
       Owl Carousel
       ====================================== */

    /* Testimonial */
    $('.testimonial-two').owlCarousel({
        loop: true,
        smartSpeed: 500,
        responsiveClass: true,
        nav:false,
        dots: true,
        dotsContainer: ".owl-thumbs",
        autoplay: false,
        autoplayHoverPause: true,
        autoplayTimeout: 3000,
        responsive: {
            0: {
                items: 1,
                margin: 30,
            },
            480: {
                items: 1,
                margin: 30,
            },
            992: {
                items: 1,
                margin: 30,
            }
        }
    });

    /* Brand Carousel */
    $('.brand-carousel').owlCarousel({
        margin: 75,
        nav: false,
        navText: [
            '<i class="ti ti-angle-left"></i>',
            '<i class="ti ti-angle-right"></i>'
        ],
        dots: false,
        autoWidth: false,
        autoplay: 300,
        autoplayHoverPause: false,
        loop: true,
        responsive: {
            0: {
                items: 1
            },
            480: {
                items: 2
            },
            600: {
                items: 4
            },
            1000: {
                items: 5
            }
        }
    });

    /* Portfolio One Column */
    if($("#gallery-work").length) {
        $("#gallery-work").owlCarousel({
            items: 1,
            autoplay: true,
            autoplayHoverPause: true,
            mouseDrag: false,
            loop: true,
            margin: 30,
            dots: true,
            dotsContainer: "#work-thumbs",
            nav: false,
            animateIn: "fadeIn",
            animateOut: "fadeOut",
            responsive: {
                320: {
                    items: 1,
                }
            }
        });
    }

    /* Team Creative */
    $(".team-creative.owl-theme").owlCarousel({
        items: 3,
        margin: 30,
        loop: true,
        dots: false,
        nav: false,
        responsive: {
            1280: {
                items: 2,
            },
            768: {
                items: 2,
            },
            320: {
                items: 1,
            }
        }
    });

    /* Team Single */
    $('.team-single').owlCarousel({
        items: 1,
        autoplay: 1500,
        smartSpeed: 900,
        autoplayHoverPause:true,
        loop:true,
        margin:30,
        responsiveClass:true,
        dots:false,
        nav: true,

        responsive: {
            1280: {
                items: 1,
            },
            1200: {
                nav: false,
            },
            768: {
                items: 1,
            },
            320: {
                items: 1,
            }
        }

    });
    $( ".owl-prev").html('<span class="caret left"></span>');
    $( ".owl-next").html('<span class="caret right"></span>');

    /* Team Classic */
    $(".team-classic.owl-team").owlCarousel({
        items: 3,
        margin: 30,
        dots: false,
        nav: false,
        loop:true,
        autoplay: true,
        smartSpeed:1000,
        navSpeed: true,
        autoplayHoverPause:true,
        responsiveClass:true,
        responsive: {
            992: {
                items: 4,
            },
            600: {
                items: 2,
            },
            320: {
                items: 1,
            },
        }
    });

    /* Team Classic Half */
    $(".team-classic").owlCarousel({
        items: 2,
        margin: 30,
        dots: false,
        nav: false,
        loop:true,
        autoplay: true,
        smartSpeed:1000,
        navSpeed: true,
        autoplayHoverPause:true,
        responsiveClass:true,
        responsive: {
            992: {
                items: 2,
            },
            600: {
                items: 2,
            },
            320: {
                items: 1,
            },
        }
    });

    /* Laptop Slide */
    $("#laptop-slide").owlCarousel({
        items: 1,
        loop: true,
        dots: false,
        nav: false,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        autoplay:true,
        autoplayTimeout:3000,
        // mouseDrag:false,
        responsive: {
            1280: {
                items: 1,
            },
            600: {
                items: 1,
            },
            320: {
                items: 1,
            },
        }
    });

    /* Latest News */
    $(".news-slider").owlCarousel({
        items: 3,
        autoplay: 2500,
        autoplayHoverPause: true,
        loop: true,
        margin: 30,
        dots: true,
        nav: false,
        responsive: {
            1280: {
                items: 3
            },
            980: {
                items: 3
            },
            600: {
                items: 2
            },
            320: {
                items: 1
            }
        }
    });

    /*Simple text fading banner*/
    $("#text-fading").owlCarousel({
        items: 1,
        autoplay: true,
        autoplayHoverPause: true,
        loop: true,
        mouseDrag: false,
        animateIn: "fadeIn",
        animateOut: "fadeOut",
        dots: true,
        nav: false,
        responsive: {
            0: {
                items: 1
            }
        }
    });

    /* ===================================
       Revolution Slider
       ====================================== */

    if ($("#main-slider-four").length) {
        // Main Slider Four Revolution
        $("#main-slider-four").show().revolution({
            sliderType: "standard",
            jsFileLocation: "js/revolution",
            sliderLayout: "fullscreen",
            dottedOverlay: "none",
            delay: 9000,
            navigation: {
                keyboardNavigation: "off",
                keyboard_direction: "horizontal",
                mouseScrollNavigation: "off",
                mouseScrollReverse: "default",
                onHoverStop: "on",

                bullets: {
                    enable: true,
                    hide_onmobile: false,
                    style: "awaza",
                    hide_onleave: false,
                    direction: "vertical",
                    h_align: "left",
                    v_align: "center",
                    h_offset: 50,
                    v_offset: 0,
                    space: 5,
                    tmp: '<div class="animated-wrap"><div class="tp-bullet-number animated-element"><span class="tp-count">{{param1}}</span><span class="tp-bullet-line"></span></div></div>'
                }
            },

            responsiveLevels: [1240, 1240, 768, 575],
            visibilityLevels: [1240, 1240, 768, 575],
            gridwidth: [1200, 1200, 768, 575],
            gridheight: [800, 800, 500, 700],
            lazyType: "none",
            parallax: {
                type: "mouse+scroll",
                origo: "slidercenter",
                speed: 400,
                speedbg: 0,
                speedls: 0,
                levels: [1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 47, 48, 49, 50, 51, 55]
            },
            shadow: 0,
            spinner: "off",
            stopLoop:"off",
            stopAfterLoops:-1,
            stopAtSlide:-1,
            shuffle: "off",
            autoHeight: "off",
            fullScreenAutoWidth: "off",
            fullScreenAlignForce: "off",
            fullScreenOffsetContainer: "",
            fullScreenOffset: "",
            disableProgressBar: "on",
            hideThumbsOnMobile: "off",
            hideSliderAtLimit: 0,
            hideCaptionAtLimit: 0,
            hideAllCaptionAtLilmit: 0,
            debugMode: false,
            fallbacks: {
                simplifyAll: "off",
                nextSlideOnWindowFocus: "off",
                disableFocusListener: false
            }
        });

        // BEFORE/AFTER INITIALISATION
        RevSliderBeforeAfter(jQuery, jQuery("#main-slider-four"), {
            arrowStyles: {
                leftIcon: "fa fa-caret-left",
                rightIcon: "fa fa-caret-right",
                size: "30",
                color: "#18191d",
                bgColor: "transparent",
                spacing: "10",
                padding: "0",
                borderRadius: "0"
            },

            dividerStyles: {
                width: "1",
                color: "rgba(255, 255, 255, 0.25)"
            },
            onClick: {
                time: "500",
                easing: "Power2.easeOut"
            },
            cursor: "move",
            carousel: false
        });
    }

        /*Design Studio*/
    $("#rev_slider_8_1").show().revolution({
        sliderType:"standard",
        jsFileLocation:"//localhost/revslider/revslider/public/assets/js/",
        sliderLayout:"fullscreen",
        dottedOverlay:"none",
        delay:9000,
        navigation: {
            keyboardNavigation:"off",
            keyboard_direction: "horizontal",
            mouseScrollNavigation:"off",
            mouseScrollReverse:"default",
            onHoverStop:"on",
            touch:{
                touchenabled:"on",
                touchOnDesktop:"off",
                swipe_threshold: 75,
                swipe_min_touches: 50,
                swipe_direction: "horizontal",
                drag_block_vertical: false
            }
            ,
            arrows: {
                style:"uranus",
                enable:true,
                hide_onmobile:true,
                hide_under:600,
                hide_onleave:true,
                hide_delay:200,
                hide_delay_mobile:1200,
                tmp:'<div class="hvr-pulse"></div>',
                left: {
                    h_align:"left",
                    v_align:"center",
                    h_offset:30,
                    v_offset:0
                },
                right: {
                    h_align:"right",
                    v_align:"center",
                    h_offset:30,
                    v_offset:0
                }
            }
            ,
            bullets: {
                enable:true,
                hide_onmobile:true,
                hide_under:600,
                style:"hephaistos",
                hide_onleave:true,
                hide_delay:200,
                hide_delay_mobile:1200,
                direction:"horizontal",
                h_align:"center",
                v_align:"bottom",
                h_offset:0,
                v_offset:30,
                space:5,
                tmp:''
            }
        },
        responsiveLevels:[1240,1024,778,480],
        visibilityLevels:[1240,1024,778,480],
        gridwidth:[1240,1024,778,480],
        gridheight:[868,600,500,400],
        lazyType:"smart",
        parallax: {
            type:"mouse",
            origo:"slidercenter",
            speed:2000,
            speedbg:0,
            speedls:0,
            levels:[2,3,4,5,6,7,12,16,10,50,10,11,12,13,14,55],
        },
        shadow:0,
        spinner:"off",
        stopLoop:"off",
        stopAfterLoops:-1,
        stopAtSlide:-1,
        shuffle:"off",
        autoHeight:"off",
        fullScreenAutoWidth:"off",
        fullScreenAlignForce:"off",
        fullScreenOffsetContainer: "",
        fullScreenOffset: "",
        hideThumbsOnMobile:"off",
        hideSliderAtLimit:0,
        hideCaptionAtLimit:0,
        hideAllCaptionAtLilmit:0,
        debugMode:false,
        fallbacks: {
            simplifyAll:"off",
            nextSlideOnWindowFocus:"off",
            disableFocusListener:false,
        }
    });

       /*Agency, Flat Agency, Classic Startup*/
    $("#rev_slider_5_1").show().revolution({
        sliderType: "standard",
        jsFileLocation: "//localhost:82/revslider/revslider/public/assets/js/",
        sliderLayout: "fullscreen",
        dottedOverlay: "none",
        delay: 1000,
        navigation: {},
        responsiveLevels: [1240, 1024, 778, 480],
        visibilityLevels: [1240, 1024, 778, 480],
        gridwidth: [1240, 1024, 778, 480],
        gridheight: [868, 768, 960, 720],
        lazyType: "none",
        parallax: {
            type: "mouse",
            origo: "slidercenter",
            speed: 2000,
            speedbg: 0,
            speedls: 0,
            levels: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 55],
            disable_onmobile: "on"
        },
        shadow: 0,
        spinner: "off",
        autoHeight: "off",
        fullScreenAutoWidth: "off",
        fullScreenAlignForce: "off",
        fullScreenOffsetContainer: "",
        fullScreenOffset: "",
        disableProgressBar: "on",
        hideThumbsOnMobile: "off",
        hideSliderAtLimit: 0,
        hideCaptionAtLimit: 0,
        hideAllCaptionAtLilmit: 0,
        debugMode: false,
        fallbacks: {
            simplifyAll: "off",
            disableFocusListener: false,
        }
    });

    /*Modern Agency*/
    $("#secondary-banner").show().revolution({
        sliderType: "standard",
        sliderLayout: "fullscreen",
        scrollbarDrag: "true",
        dottedOverlay: "none",
        navigation: {
            keyboardNavigation: "off",
            keyboard_direction: "horizontal",
            mouseScrollNavigation: "off",
            mouseScrollReverse: "default",
            onHoverStop: "on",
            touch: {
                touchenabled: "on",
                swipe_threshold: 75,
                swipe_min_touches: 1,
                swipe_direction: "horizontal",
                drag_block_vertical: false
            },
            bullets: {
                enable: true,
                hide_onmobile: false,
                style: "awaza",
                hide_onleave: false,
                direction: "vertical",
                h_align: "left",
                v_align: "center",
                h_offset: 50,
                v_offset: 0,
                space: 5,
                tmp: '<div class="tp-bullet-number"><span class="tp-count">{{param1}}</span><span class="tp-bullet-line"></span></div>'
            }
        },
        viewPort: {
            enable: true,
            outof: "pause",
            visible_area: "90%"
        },
        responsiveLevels: [1240, 1024, 778, 480],
        visibilityLevels: [1240, 1024, 778, 480],
        gridwidth: [1240, 1024, 778, 480],
        gridheight: [868, 768, 960, 720],
        lazyType: "none",
        parallax: {
            type: "mouse",
            origo: "slidercenter",
            speed: 9000,
            levels: [2, 3, 4, 5, 6, 7, 12, 16, 10, 50],
            disable_onmobile: "on"
        },
        shadow: 0,
        spinner: "off",
        stopLoop: "off",
        stopAfterLoops: -1,
        stopAtSlide: -1,
        shuffle: "off",
        autoHeight: "off",
        hideThumbsOnMobile: "off",
        hideSliderAtLimit: 0,
        hideCaptionAtLimit: 0,
        hideAllCaptionAtLilmit: 0,
        debugMode: false,
        fallbacks: {
            simplifyAll: "off",
            nextSlideOnWindowFocus: "off",
            disableFocusListener: false,
        }
    });

    /*Classic, Interactive*/
    $("#wixer-2").show().revolution({
        sliderType: "standard",
        sliderLayout: "fullscreen",
        scrollbarDrag: "true",
        dottedOverlay: "none",
        navigation: {
            keyboardNavigation: "off",
            keyboard_direction: "horizontal",
            mouseScrollNavigation: "off",
            mouseScrollReverse: "default",
            onHoverStop: "on",
            bullets: {
                enable: true,
                hide_onmobile: true,
                hide_onleave: false,
                hide_under: 768,
                hide_over: 9999,
                style: "wixer-2",
                direction: "vertical",
                h_align: "right",
                v_align: "center",
                h_offset: 45,
                v_offset: 0,
                space: 5,
                tmp: '<div class="tp-bullet-number"><span class="tp-count">{{param1}}</span><span class="tp-bullet-line"></span></div>'
            },
            touch: {
                touchenabled: "on",
                swipe_threshold: 75,
                swipe_min_touches: 1,
                swipe_direction: "horizontal",
                drag_block_vertical: false
            },
            arrows: {
                style: "",
                enable: true,
                hide_onmobile: true,
                hide_onleave: false,
                tmp: '',
                left: {
                    h_align: "left",
                    v_align: "center",
                    h_offset: 20,
                    v_offset: 0
                },
                right: {
                    h_align: "right",
                    v_align: "center",
                    h_offset: 20,
                    v_offset: 0
                }
            }
        },
        viewPort: {
            enable: true,
            outof: "pause",
            visible_area: "90%",
            presize: true
        },
        responsiveLevels: [4096, 1025, 768, 480],
        gridwidth: [1400, 1024, 768, 480],
        gridheight: [720, 600, 500, 350],
        lazyType: "none",
        parallax: {
            type: "mouse",
            origon: "slidercenter",
            speed: 9000,
            levels: [2, 3, 4, 5, 6, 7, 12, 16, 10, 50],
        },
        shadow: 0,
        spinner: "off",
        stopLoop: "off",
        stopAfterLoops: -1,
        stopAtSlide: -1,
        shuffle: "off",
        autoHeight: "off",
        hideThumbsOnMobile: "off",
        hideSliderAtLimit: 0,
        hideCaptionAtLimit: 360,
        hideAllCaptionAtLilmit: 360,
        debugMode: false,
        fallbacks: {
            simplifyAll: "off",
            nextSlideOnWindowFocus: "off",
            disableFocusListener: false,
        }
    });

    /*Single*/
    $("#wixer-3").show().revolution({
        sliderType: "standard",
        sliderLayout: "fullscreen",
        scrollbarDrag: "true",
        dottedOverlay: "none",
        navigation: {
            keyboardNavigation: "off",
            keyboard_direction: "horizontal",
            mouseScrollNavigation: "off",
            mouseScrollReverse: "default",
            onHoverStop: "off",
            bullets: {
                enable: true,
                hide_onmobile: true,
                hide_under: 767,
                style: "wixer",
                hide_onleave: false,
                direction: "vertical",
                h_align: "left",
                v_align: "center",
                h_offset: 30,
                v_offset: 0,
                space: 5,
                tmp: '<div class="tp-bullet-inner"></div><div class="tp-line"></div>'
            },
            touch: {
                touchenabled: "on",
                swipe_threshold: 75,
                swipe_min_touches: 1,
                swipe_direction: "horizontal",
                drag_block_vertical: false
            },
        },
        viewPort: {
            enable: true,
            outof: "pause",
            visible_area: "90%",
            presize: true
        },
        responsiveLevels: [4096, 1025, 768, 480],
        gridwidth: [1400, 1024, 768, 480],
        gridheight: [720, 600, 500, 350],
        lazyType: "none",
        parallax: {
            type: "mouse",
            origon: "slidercenter",
            speed: 9000,
            levels: [2, 3, 4, 5, 6, 7, 12, 16, 10, 50],
        },
        shadow: 0,
        spinner: "off",
        stopLoop: "off",
        stopAfterLoops: -1,
        stopAtSlide: -1,
        shuffle: "off",
        autoHeight: "off",
        hideThumbsOnMobile: "off",
        hideSliderAtLimit: 0,
        hideCaptionAtLimit: 360,
        hideAllCaptionAtLilmit: 360,
        debugMode: false,
        fallbacks: {
            simplifyAll: "off",
            nextSlideOnWindowFocus: "off",
            disableFocusListener: false,
        }
    });

    /*Revolution Carousel 3 cols*/
    $("#rev-carousel").show().revolution({
        sliderType: "carousel",
        jsFileLocation: "js/revolution",
        sliderLayout: "fullscreen",
        dottedOverlay: "none",
        delay: 7000,
        navigation: {
            keyboardNavigation: "off",
            keyboard_direction: "horizontal",
            mouseScrollNavigation: "off",
            mouseScrollReverse: "default",
            onHoverStop: "off",
            bullets: {
                style: "uranus",
                enable: true,
                tmp: '<span class="tp-bullet-inner"></span>',
                hide_onmobile: true,
                hide_under: 480,
                hide_onleave: false,
                hide_delay: 200,
                direction: "horizontal",
                space: 10,
                h_align: "center",
                v_align: "bottom",
                h_offset: 0,
                v_offset: 30
            }
        },
        carousel: {
            horizontal_align: "center",
            vertical_align: "center",
            fadeout: "on",
            vary_fade: "on",
            maxVisibleItems: 3,
            infinity: "on",
            space: 0,
            stretch: "off",
            showLayersAllTime: "off",
            easing: "Power3.easeInOut",
            speed: "900"
        },
        responsiveLevels: [1240, 1024, 778, 480],
        visibilityLevels: [1240, 1024, 778, 480],
        gridwidth: [1140, 960, 750, 480],
        gridheight: [720, 720, 480, 360],
        lazyType: "none",
        parallax: {
            type: "scroll",
            origo: "enterpoint",
            speed: 400,
            speedbg: 0,
            speedls: 0,
            levels: [5, 7, 10, 15, 20, 25, 30, 35, 40, 45, 25, 47, 48, 49, 50, 51, 55],
        },
        shadow: 0,
        spinner: "off",
        stopLoop: "on",
        stopAfterLoops: 0,
        stopAtSlide: 1,
        shuffle: "off",
        autoHeight: "off",
        disableProgressBar: "on",
        hideThumbsOnMobile: "off",
        hideSliderAtLimit: 0,
        hideCaptionAtLimit: 0,
        hideAllCaptionAtLilmit: 0,
        debugMode: false,
        fallbacks: {
            simplifyAll: "off",
            nextSlideOnWindowFocus: "off",
            disableFocusListener: false,
        }
    });

});