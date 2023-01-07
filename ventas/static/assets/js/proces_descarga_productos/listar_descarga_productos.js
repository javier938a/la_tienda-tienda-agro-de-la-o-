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
    let url_list_descarga_prod_json=$("#url_list_descarga_prod_json").val();
    const csrftoken=getCookie('csrftoken');
    $("#table-descarga-productos").DataTable({
        'processing':true,
        'serverSide':true,
        'serverMethod':'post',
        'ajax':{
            url:url_list_descarga_prod_json,
            data:{
                csrfmiddlewaretoken:csrftoken,
            }
        },
        'columns':[
            {'data':'id'},
            {'data':'usuario'},
            {'data':'fecha_de_descarga'},
            {'data':'descripcion'},
            {'data':'sucursal'},
            {'data':'total'},
            {'data':'action'}
        ]
    });
});