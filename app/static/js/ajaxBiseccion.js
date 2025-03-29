$(document).ready(function() {
    $('#formBiseccion').on('submit', function(event) {
        event.preventDefault();

        const data = {
            ecuacion: $('#ecuacion').val(),  // <-- Se obtiene del campo oculto
            a: parseFloat($('#a').val()),
            b: parseFloat($('#b').val()),
            tolerancia: parseFloat($('#tolerancia').val())
        };


        $.ajax({
            type: 'POST',
            url: '/unidad2/biseccion-json',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(resultado) {
                if (resultado.error) {
                    $('#resultado').html(`<p style="color:red;">${resultado.error}</p>`);
                    return;
                }

                let tabla = `
                    <table border="1">
                        <thead>
                            <tr>
                                <th>Iteración</th>
                                <th>X1</th>
                                <th>X2</th>
                                <th>Xr</th>
                                <th>f(X1)</th>
                                <th>f(X2)</th>
                                <th>f(Xr)</th>
                                <th>Error (%)</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                resultado.forEach(fila => {
                    tabla += `
                        <tr>
                            <td>${fila.iteracion}</td>
                            <td>${fila.Xi}</td>
                            <td>${fila.X2}</td>
                            <td>${fila.Xr}</td>
                            <td>${fila.fXi}</td>
                            <td>${fila.fX2}</td>
                            <td>${fila.fXr}</td>
                            <td>${fila.error}</td>
                        </tr>
                    `;
                });

                tabla += `</tbody></table>`;
                $('#resultado').html(tabla);
            },
            error: function(xhr) {
                console.error(xhr.responseText); // Muestra el error completo en consola
                $('#resultado').html('<p style="color:red;">Error en la solicitud AJAX</p>');
            }
            
        });
    });
});
