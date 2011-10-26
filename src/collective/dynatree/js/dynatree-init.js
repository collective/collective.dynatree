_.templateSettings = {
  interpolate : /\{\{(.+?)\}\}/g
};

var DataModel = Backbone.Model.extend({
    initialize: function(){
        function change_params(model, params){ 
            var real_params = new Array();
            _.each(params.split('/'), function(param){
                var pair = param.split(',');
	        var value = pair[1].replace(/^\s+|\s+$/g, "");
                if (!isNaN(value)) { value = parseInt(value); };
                if (value=='True') { value = true; };
                if (value=='False') { value = false; };		
	        real_params[pair[0].replace(/^\s+|\s+$/g, "")] = value;
            });
            model.set({params: real_params}, {silent: true});
        }

        _.bindAll(this, "update", "update_selected", "getDataFor");

        this.bind("change:params", change_params);

        this.trigger("change:params", this, this.get("params")); 
        jq.get(this.get("url"), this.update);
    },
    defaults: {sparse: false},
    update_selected: function(selected){
        if (this.get("params").selectMode == 1){ // Single Select
            selected = [_.last(selected)];
        }
        this.set({selected: selected});
    },
    update: function(result){
        this.set({children: JSON.parse(result)});
    },
    getChildren: function(){
        var selected = this.get("selected");
        var filter = this.get("filter") && this.get("filter").toLowerCase();
        var sparse_cache = {};
        function is_selected_or_has_selected_children(node){
            if (node.key in sparse_cache){
                return sparse_cache[node.key];
            }
            if(_.detect(selected, function(selected_key){
                return selected_key == node.key;
            })){
                sparse_cache[node.key] = true;
                return true;
            }else{
                if(_.detect(node.children, function(child){
                    return is_selected_or_has_selected_children(child);
                })){
                    sparse_cache[node.key] = true;
                    return true;
                }
            }
            sparse_cache[node.key] = false;
            return false;
        };
        function remove_unselected(node){
            if(!is_selected_or_has_selected_children(node)){
                return false;
            }
            node.children = _.filter(node.children, remove_unselected);
            return true;
        }
        function remove_non_matching(node){
            if(!is_selected_or_has_selected_children(node)){
                if (node.title.toLowerCase().indexOf(filter) != -1){
                    return true;
                }else{
                    node.children = _.filter(node.children, remove_non_matching, filter);
                    return !!node.children.length;
                }
            }
            node.children = _.filter(node.children, remove_non_matching, filter);
            return true;
        }
        function show_selected(node){
            if(_.detect(node.children, function(child){
                return is_selected_or_has_selected_children(child);
            })){
                node.expand = true;
            }
            _.each(node.children, show_selected);
        }
        var retval = this.get("children");
        if(this.get("sparse")){
            retval = _.filter(retval, remove_unselected);
        }
        if(this.get("filter")){
            retval = _.filter(retval, remove_non_matching);
        }
        _.each(retval, show_selected);
        return retval;
    },
    getDataFor: function(key){
        function getDataFromChildren(key, children){
            var retval = undefined;
            _.detect(children, function(child){
                if(child.key == key){
                    retval = child;
                    return true;
                }else{
                    var child_result = getDataFromChildren(key, child.children);
                    if(child_result !== undefined){
                        retval = child_result;
                        return true;
                    }
                }
                return false;
            });
            return retval;
        }
        return getDataFromChildren(key, this.get("children") || []);
    }
});

var Dynatree = Backbone.View.extend({
    initialize:function(){
        _.bindAll(this, "render");
        this.model.bind("change:children", this.render);
        this.model.bind("change:selected", this.render);
        this.model.bind("change:sparse", this.render);
        this.model.bind("change:filter", this.render);
    },
    render:function(model){
        var tree = this.el.dynatree("getTree");

        if(tree.getRoot === undefined){
            function onQuerySelect(selected, node){
                if(!this.isUserEvent()){
                    return true;
                }
                var new_selected = model.get("selected");
                var key = node.data.key;
                if(selected){
                    new_selected = _.union(new_selected, [key]);
                }else{
                    new_selected = _.without(new_selected, key);
                }
                model.update_selected(new_selected);
                return false;
            }

            var params = _.extend({}, 
                                  this.model.get("params"), 
                                  {children: this.model.getChildren(),
                                   onQuerySelect: onQuerySelect});
            this.el.dynatree(params);
            tree = this.el.dynatree("getTree");
        }else{
            if(model.changedAttributes && 
               (
                   'sparse' in model.changedAttributes() || 
                       'filter' in model.changedAttributes()
               )
              ){
                tree.options.children = this.model.getChildren();
            }
            tree.reload();
        }
        // We are faking here thet we are outside of the select event
        tree.phase = "idle"; 
        _.each(this.model.get("selected"), function(key){
            tree.getNodeByKey(key).select();
        });
    }
});

var HiddenForm = Backbone.View.extend({
    initialize: function(){
        _.bindAll(this, "render");
        this.model.bind("change:selected", this.render);
    },
    render: function(){
        var val = "";
        if(this.model.get("selected").length){
            val = _.reduce(this.model.get("selected"), 
                           function(a,b){return a + '|' + b;}
                          );
        }
        this.el.val(val);
    }
});

var Filter = Backbone.View.extend({
    initialize: function(){
        _.bindAll(this, 'updateFilter', 'render');
        this.model.bind("change:filter", this.render);
    },
    events: {
        'keyup input': "updateFilter"
    },
    updateFilter: function(){
        var filter = this.el.find('.filter').val();
        this.model.set({'filter': filter});
        if(filter && this.model.get("sparse")){
            this.model.set({sparse: false});
        }
        return false;
    },
    render: function(){
        this.el.find('input').val(this.model.get("filter"));
    }
    
});
var VariousUIElements = Backbone.View.extend({
    initialize: function(){
        _.bindAll(this, "toggleSparse", "render");
        this.model.bind("change:sparse", this.render);
        this.render();
    },
    events: {
        "click .sparse": "toggleSparse"
    },
    toggleSparse: function(){
        if(!this.model.get("filter")){
            this.model.set({sparse: !this.model.get("sparse")});
            this.render();
        }
    },
    render: function(){
        if(this.model.get("sparse")){
            this.el.find(".sparse").text("Expand");
        }else{
            this.el.find(".sparse").text("Sparse");
        }
    }
});

var FlatListDisplay = Backbone.View.extend({
    initialize: function(){
        _.bindAll(this, "render", "delete");
        this.template = _.template(this.el.find(".flatlist-template").html());
        this.model.bind("change:selected", this.render);
        this.model.bind("change:children", this.render);
    },
    events: {
        "click .delete": "delete"
    },
    render: function(){
        var last_elem = undefined;
        var ordered_keys = this.getOrderedKeys();
        var model = this.model;
        var template = this.template;
        var el = this.el;
        _.each(this.el.find(".flatlist-item").splice(1), function(item){
            jq(item).remove();
        });
        _.each(ordered_keys, function(key){
            var title = key;
            if(model.get("params").FlatListShow != "key"){
                title = model.getDataFor(key).title;
            }
            var new_elem = template({title: title,
                                     key: key});
            if(last_elem === undefined){
                el.append(new_elem);
            }else{
                last_elem.after(new_elem);
                last_elem = new_elem;
            }
        });
    },
    getOrderedKeys: function(){
        var model = this.model;
        var sortFunc = function(key){
            return model.getDataFor(key).title;
        };
        if(this.model.get("params").FlatListShow == "key"){
            sortFunc = function(key){
                return key;
            };
        }
        return _.sortBy(model.get("selected"), sortFunc);
    },
    delete: function(event){
        var key = jq(event.target).parent(".flatlist-item").attr("key");
        var new_selected = _.without(this.model.get("selected"), key);
        this.model.update_selected(new_selected);
    }
});

jq(document).ready(function() {
    jq('.dynatree-atwidget').each(function () {
	// get parameters 
	var jqthis = jq(this);
        var datamodel = new DataModel({url: jqthis.find(".dynatree_ajax_vocabulary").text(),
                                       selected: _.filter(jqthis.find('input.selected').val().split('|'),
                                                          function(elem){return elem;}),
                                       params: jqthis.find('.dynatree_parameters').text(),
                                       name: jqthis.find('input.selected').attr('id')
                                     });
        jqthis.data('collective.dynatree', datamodel);
        var tree = new Dynatree({el: jqthis.find('.collective-dynatree-tree'),
                                 model: datamodel});
        var hiddeninput = new HiddenForm({el: jqthis.find(".hiddeninput"),
                                    model: datamodel});
        if(datamodel.get("params").filter){            
            var filter = new Filter({el: jqthis.find(".dynatree_filter"),
                                     model: datamodel});
        }
        if(datamodel.get("params").sparse){
            var various = new VariousUIElements({el: jqthis.find(".ui_controls"),
                                                 model: datamodel});
        }
        if(datamodel.get("params").flatlist){
            var flatlist = new FlatListDisplay({el: jqthis.find(".flatlist_container"),
                                                model: datamodel});
        }
    });
});
