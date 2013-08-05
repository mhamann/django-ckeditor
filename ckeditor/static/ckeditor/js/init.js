/**
 * This whole file is a filthy hack to make django-ckeditor work with Grappelli's
 * inlines.
 *
 * Inlines can be dynamically added at any time, and we need to run CKEDITOR.replace
 * on their fields once they're added.
 *
 * But we do NOT run it on the "template" inline, of course.
 *
 * Oh, and there's no way to register a "callback" for Grappelli to call when it adds
 * a new inline without overriding the entire change form, which this tiny app does
 * not want to do.
 *
 * Basically: this file runs a function every second that checks for new
 * .django-ckeditor fields, and will convert them to CKEditors if it finds any.
 *
 * TODO: Handle removal of inlines too.
 * TODO: Experiment with frequencies to find a good combination of responsiveness and CPU-eating.
 */

(function() {

    var InitCKEditors = function() {
    	
    	var instances = document.querySelectorAll('.django-ckeditor');
    	var configs = window.ckeditor_config;
    	var instance;
    	    	
    	for (var i = 0; i < instances.length; i++) {
    		console.log(instances[i]);
    		instance = instances[i];
    		
    		if (instance.id.indexOf('__prefix__') == -1) {
				CKEDITOR.replace(instance.id, configs[instance.getAttribute('data-config')]);
			}
    	}

    };

    InitCKEditors();
})()
