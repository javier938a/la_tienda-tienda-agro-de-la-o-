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
    let url_listar_trans_json=$("#url_lista_trans_json").val();
    const csrftoken=getCookie("csrftoken");
    $("#table-transacciones").DataTable({
      'processing':true,
      'serverSide':true,
      'serverMethod':'post',
      'ajax':{
        url:url_listar_trans_json,
        data:{
          csrfmiddlewaretoken:csrftoken,
        }
      },
      'columns':[
        {'data':'id'},
        {'data':'correlativo'},
        {'data':'usuario'},
        {'data':'fecha_transaccion'},
        {'data':'tipo_de_transaccion'},
        {'data':'sucursal'},
        {'data':'nombre_cliente'},
        {'data':'apellido_cliente'},
        {'data':'concepto'},
        {'data':'total'},
        {'data':'action'}
      ]
    });
});