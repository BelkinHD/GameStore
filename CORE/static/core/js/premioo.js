$(document).ready(function() {
  $.get('http://fakestoreapi.com/products', function(data) {
    console.log(data); // Agrega esta línea para depurar
    $('#fila-ropa').empty();
    $.each(data, function(i, item) {
      var fila = `
        <div class="col-sm-12 col-md-6 col-lg-4 col-xl-3 justify-content-center">
              <div class="card mb-4" style="margin:auto">
                <img src="${item.image}" class="card-img-top" alt="...">
                <div class="card-body">
                  <h5 class="card-title">${item.title}</h5>
                  <p class="card-text">${item.category}</p>
                  <br>
                  <p class="card-text">${item.description}</p>
                  <p class="card-text precio"> Precio: ${item.price}</p>      
                  <p class="card-text">Stock disponible: ${item.rating.count}</p>
                </div>
              </div>
            </div> 
      `;
      $('#fila-ropa').append(fila);
    });
  }).fail(function() {
    console.log('Error al obtener los datos de la API');
  });
});
