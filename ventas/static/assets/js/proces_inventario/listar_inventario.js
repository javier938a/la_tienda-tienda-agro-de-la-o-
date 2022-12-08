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
    const csrftoken=getCookie('csrftoken');
    let url_listar_inv_json=$("#url_list_inv_json").val();
    $("#table-inventario").DataTable({
        'processing':true,
        'serverSide':true,
        'serverMethod':'post',
        "ajax":{
            url:url_listar_inv_json,
            data:{
                csrfmiddlewaretoken:csrftoken,
            }
        },
        "columns":[
            {'data':'id'},
            {'data':'sucursal'},
            {'data':'usuario'},            
            {'data':'fecha_de_registro'},
            {'data':'codigo'},
            {'data':'producto'},
            {'data':'cantidad'},
            {'data':'presentacion'},
            {'data':'categoria'},
            {'data':'costo'},
            {'data':'precio'},            
            {'data':'action'}
        ]
    });
});