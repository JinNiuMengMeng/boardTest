(function (win) {
    var form;

    // 初始化layui-form
    function _initForm () {
        layui.use('form', function(){
          form = layui.form;
        });
    }

    // 绑定事件
    function _bindEvent (opts) {
        form.on('switch', function(data){
            var isChecked = 0;
            if (data.elem.checked) {
                isChecked = 1;
            }
          _updateGpo($(data.elem).attr('name'),isChecked,opts);
        }); 
    }

    // 获取初始数据
    function _initData (opts) {
        ajax({
            url: opts.initUrl,
            data: {},
            type: 'post',
            done: function (err, data, res) {
                if (err) {
                    layer.msg(err.message, {icon: 2, time: 1000}, function () {
                    });
                } else {
                    var gpilist = data.gpilist;
                    var gpolist = data.gpolist;

                    for (var i = 0; i < gpilist.length; i++) {
                        if (gpilist[i].value == 1) {
                            $('.gpi-container').append('<input type="checkbox" name="'+gpilist[i].name+'" lay-skin="switch" lay-text="ON|OFF" checked disabled>');
                        } else {
                            $('.gpi-container').append('<input type="checkbox" name="'+gpilist[i].name+'" lay-skin="switch" lay-text="ON|OFF" disabled>');
                        }
                    }

                    for (var i = 0; i < gpolist.length; i++) {
                        var gpoName = gpolist[i].name;
                        if (gpolist[i].value == 1) {
                            $('.gpo-container').append('<input type="checkbox" name="'+gpolist[i].name+'" lay-skin="switch" lay-text="ON|OFF" checked >');
                        } else {
                            $('.gpo-container').append('<input type="checkbox" name="'+gpolist[i].name+'" lay-skin="switch" lay-text="ON|OFF"  >');
                        }
                    }
                    form.render();
                }
            }
        })
    }

    // 3s动态更新GPI数据
    function _updateGpi (opts) {
        setInterval(function () {

             $.ajax({
                dataType: 'json',
                type: 'post',
                url: opts.updateGpiUrl,
                data: {}
            }).done(function (data, textStatus, request) {
                if (data.error_code === 0) {
                    var gpilist = data;
                    for (var i = 0; i < gpilist.length; i++) {
                        if (gpilist[i].value == 1) {
                            $("[name='"+gpilist[i].name+"']").attr('checked', 'checked');
                        } else {
                            $("[name='"+gpilist[i].name+"']").removeAttr('checked');
                        }
                    }
                    form.render();
                } else {
                    layer.msg(err.message, {icon: 2, time: 1000}, function () {});
                }
            }).fail(function (XMLHttpRequest, status, info) {
                if (layer) {
                    layer.close(index);
                }
                opts.done({
                    code: -999,
                    msg: 'ajax请求出错或网络错误'
                });
            });
        },3000)
    }

    // 更改GPO数据
    function _updateGpo (name,value,opts) {
        var params = {
            portNum: name,
            gpoNum: value
        }

        ajax({
            url: opts.updateGpoUrl,
            data: params,
            type: 'get',
            done: function (err, data, res) {
                if (err) {
                    layer.msg(err.msg, {icon: 2, time: 1000}, function () {
                        if (value == 0) {
                            console.log(111);
                            $('[name="'+name+'"]').attr('checked', 'checked');
                        } else {
                            $('[name="'+name+'"]').removeAttr('checked');
                        }
                        form.render();
                    });
                } else {
                    layer.msg('ok', {icon:1, time:1000})
                }
            }
        })
    }

    win.demo = {
        index: {
            init: function (opts) {
                _initForm();
                _bindEvent(opts);
                _initData(opts);
                _updateGpi(opts);
            }
        }
    }

})(window)