(function (win) {
    var form;
    function _bindEvent (opts) {
        $('body').on('click', '.btn-login',function () {
            _login(opts);
        })   
    }

    function _login (opts) {
        var username = $('input[name="username"]').val();
        var pwd = $('input[name="pwd"]').val();

        var regNull = /\S/;

        if (!regNull.test(username)) {
            layer.msg('用户名不能为空', {icon: 2});
        } else if (!regNull.test(pwd)) {
            layer.msg('密码不能为空', {icon: 2});
        } else {
            var params = {
                username: username,
                pwd: pwd
            } 

            ajax({
                url: opts.loginUrl,
                data: params,
                type: 'post',
                done: function (err, data, res) {
                    if (err) {
                        layer.msg(err.msg, {icon: 2, time: 1000}, function () {
                        });
                    } else {
                        layer.msg(res.msg, {icon: 1, time: 1000}, function () {
                        });
                    }
                }
            })
        }
    }

    function _initForm () {
        layui.use('form', function(){
          form = layui.form;
        });
    }

    win.demo = {
        login: {
            init: function (opts) {
                _initForm();
                _bindEvent(opts);
            }
        }
    }

})(window)