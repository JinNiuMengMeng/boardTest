function ajax (opts) {
    var index;
    if (layer) {
        index = layer.load(1, {
            shade: [0.1, '#fff'] //0.1透明度的白色背景
        });
    }

    $.ajax({
        dataType: 'json',
        type: opts.type,
        url: opts.url,
        data: opts.data,
        headers: {
            "CSRFToken": $("#CSRFToken").val()
        }
    }).done(function (data, textStatus, request) {
        if (layer) {
            layer.close(index);
        }
        if (data.error_code === 0) {
            opts.done(null,data.data,data)
        } else {
            opts.done({
                code: data.error_code,
                msg: data.message
            })
        }
        $("#CSRFToken").val(request.getResponseHeader('CSRFToken'));
    }).fail(function (XMLHttpRequest, status, info) {
        if (layer) {
            layer.close(index);
        }
        opts.done({
            code: -999,
            msg: 'ajax请求出错或网络错误'
        });
    });
}