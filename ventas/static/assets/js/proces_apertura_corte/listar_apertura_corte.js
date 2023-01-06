function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function(){
    $("#btn_nueva_apertura").click(function(evt){
        let url_verificar_apertura_caja_activa = $("#url_verificar_apertura_caja_activa").val();
        const csrftoken=getCookie('csrftoken');
        let datos = {
            csrfmiddlewaretoken:csrftoken
        };
        $.ajax({
            url:url_verificar_apertura_caja_activa,
            type:'POST',
            data:datos,
            dataType:'json',
            success:function(data){
                console.log(data)
                let res = data.res;
                if(res==false){
                    let url_crear_apertura = $("#url_crear_apertura").val();
                    window.open(url_crear_apertura, "_parent");
                }else{
                    console.log("Ya hay una apertura")
                    toastr['warning']("Hay una apertura activa correspondiente a esta caja, porfavor haga corte en la apertura activa, y despues vuelva a crear otra apertura de caja");
                }
            }
        })       
    })

    let url_list_apecor_json=$("#url_list_apecor_json").val();
    const csrftoken=getCookie('csrftoken');
    $("#table-apertura-corte").DataTable({
        'processing':true,
        'serverSide':true,
        'serverMethod':'post',
        'ajax':{
            url:url_list_apecor_json,
            data:{
                csrfmiddlewaretoken:csrftoken,
            }
        },
        'columns':[
            {'data':'id'},
            {'data':'caja'},
            {'data':'usuario'},
            {'data':'fecha_de_apertura'},
            {'data':'monto_de_apertura'},
            {'data':'diferencia_de_apertura'},
            {'data':'fecha_de_corte'},
            {'data':'monto_de_corte'},
            {'data':'diferencia_de_corte'},
            {'data':'nombre_usuario_de_corte'},
            {'data':'estado_apertura'},
            {'data':'corte_global'},
            {'data':'ultima_apertura'},
            {'data':'action'}
        ]
    });


});