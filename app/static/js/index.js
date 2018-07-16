(function (win) {
    // 获取初始数据
    function _initData() {
        $.ajax({
            url: 'http://127.0.0.1:5000/get/init/data',
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                var gpilist = JSON.parse(data.responseText).gpilist;
                var gpolist = JSON.parse(data.responseText).gpolist;

                for (var i = 0; i < gpilist.length; i++) {
                    if (gpilist[i].value == 1) {
                        $('.gpi-container').append('<input type="checkbox" name="' + gpilist[i].name + '" checked disabled>');
                        $("[name='" + gpilist[i].name + "']").bootstrapSwitch();
                    } else {
                        $('.gpi-container').append('<input type="checkbox" name="' + gpilist[i].name + '" disabled>');
                        $("[name='" + gpilist[i].name + "']").bootstrapSwitch();
                    }
                }

                for (var i = 0; i < gpolist.length; i++) {
                    var gpoName = gpolist[i].name;
                    if (gpolist[i].value == 1) {
                        $('.gpo-container').append('<input type="checkbox" name="' + gpolist[i].name + '" checked >');
                        $("[name='" + gpolist[i].name + "']").bootstrapSwitch({
                            onSwitchChange: function (event, state) {
                                _updateGpo(gpoName, state);
                            }
                        });
                    } else {
                        $('.gpo-container').append('<input type="checkbox" name="' + gpolist[i].name + '" >');
                        $("[name='" + gpolist[i].name + "']").bootstrapSwitch({
                            onSwitchChange: function (event, state) {
                                _updateGpo(gpoName, state)
                            }
                        });
                    }
                }
            }
        });
    }

    // 3s动态更新GPI数据
    function _updateGpi() {
        setInterval(function () {
            $.ajax({
                url: 'http://127.0.0.1:5000/get/gpi/data',
                type: 'POST',
                dataType: 'json',
                success: function () {
                    var gpilist = JSON.parse(data.responseText).gpilist;
                    for (var i = 0; i < gpilist.length; i++) {
                        if (gpilist[i].value == 1) {
                            $("[name='" + gpilist[i].name + "']").bootstrapSwitch('disabled', false);
                            $("[name='" + gpilist[i].name + "']").bootstrapSwitch('state', true);
                            $("[name='" + gpilist[i].name + "']").bootstrapSwitch('disabled', true);
                        } else {
                            $("[name='" + gpilist[i].name + "']").bootstrapSwitch('disabled', false);
                            $("[name='" + gpilist[i].name + "']").bootstrapSwitch('state', false);
                            $("[name='" + gpilist[i].name + "']").bootstrapSwitch('disabled', true);
                        }
                    }
                }
            });
        }, 3000)
    }

    // 更改GPO数据
    function _updateGpo(name, value) {
        var params = {
            name: name,
            value: value
        }
        $.ajax({
            url: 'http://127.0.0.1:5000/update/gpo',
            type: 'POST',
            dataType: 'json',
            data: params,
            success: function (data) {
                alert('success');
            }
        });
    }

    win.demo = {
        index: {
            init: function (opts) {
                _initData();
                _updateGpi();
            }
        }
    }

})(window)