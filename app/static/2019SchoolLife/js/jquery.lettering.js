/*!
* Lettering.JS 0.6.1
*
* Copyright 2010, Dave Rupert http://daverupert.com
* Released under the WTFPL license
* http://sam.zoy.org/wtfpl/
*
* Thanks to Paul Irish - http://paulirish.com - for the feedback.
*
* Date: Mon Sep 20 17:14:00 2010 -0600
*/
(function(b){function c(g,h,d,i){var e=g.text().split(h),f="";if(e.length){b(e).each(function(j,k){f+='<span class="'+d+(j+1)+'">'+k+"</span>"+i});g.empty().append(f)}}var a={init:function(){return this.each(function(){c(b(this),"","char","")})},words:function(){return this.each(function(){c(b(this)," ","word"," ")})},lines:function(){return this.each(function(){var d="eefec303079ad17405c889e092e105b0";c(b(this).children("br").replaceWith(d).end(),d,"line","")})}};b.fn.lettering=function(d){if(d&&a[d]){return a[d].apply(this,[].slice.call(arguments,1))}else{if(d==="letters"||!d){return a.init.apply(this,[].slice.call(arguments,0))}}b.error("Method "+d+" does not exist on jQuery.lettering");return this}})(jQuery);