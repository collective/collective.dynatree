jq(document).ready(function(){
    jq('.dynatree-atwidget').each(function () {
		// get parameters
		var rawparams = jq(this).find('.dynatree_parameters').val().split(';');
		var params = new Array();
		for (var idx=0; idx<params.length; idx++) {
			var pair = rawparams[idx].split(',');
			params[pair[0].trim()] = pair[1].trim();
		}
		
		// get json url       
        params['initAjax'] = {
			'url': jq(this).find('.dynatree_ajax_vocabulary').val()
		};
		
		// init tree
		jq(this).find('.collective-dynatree-tree').dynatree(params);
	});
});
