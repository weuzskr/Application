
    $(document).ready(function() {
        var clock = $('.clock').FlipClock({
            clockFace: 'TwelveHourClock' // Vous pouvez changer pour 'TwentyFourHourClock' si vous préférez
        });
    });

    document.getElementById('graph').addEventListener('mouseover', function() {
    document.getElementById('info').classList.add('active'); // Afficher l'aside au survol du diagramme
});

document.getElementById('graph').addEventListener('mouseout', function() {
    document.getElementById('info').classList.remove('active'); // Masquer l'aside lorsque le curseur quitte le diagramme
});

document.addEventListener('click', function(event) {
    if (!document.getElementById('info').contains(event.target) && !document.getElementById('graph').contains(event.target)) {
        document.getElementById('info').classList.remove('active'); // Masquer l'aside lorsque l'utilisateur clique en dehors de celui-ci
    }
});


    // Ajouter une animation au graphique circulaire
    Plotly.animate('graph', [{
        data: [{
            opacity: 0.8, // Ajouter de la transparence
            marker: {
                colors: ['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)'] // Définir des couleurs personnalisées
            }
        }]
    }], {
        transition: {
            duration: 1000, // Durée de l'animation en millisecondes
            easing: 'cubic-in-out' // Type d'animation
        },
        frame: {
            duration: 2000 // Durée entre chaque trame de l'animation en millisecondes
        }
    });



    window.onload = function() {
        var clientInfo = document.querySelector('meta[name="client-info"]').getAttribute('content');
        if (clientInfo === 'LOGIN_FAILURE') {
            alert('Tentative de connexion échouée détectée!');
        }
    };
// Liste des couleurs prédéfinies
var colors = ['rgba(255, 206, 86, 0.5)', 'rgba(75, 192, 192, 0.5)', 'rgba(153, 102, 255, 0.5)', 'rgba(255, 99, 132, 0.5)'];
var colorIndex = 0; // Index de la couleur actuelle

// Fonction pour récupérer la couleur suivante dans la liste prédéfinie
function getNextColor() {
    var color = colors[colorIndex];
    colorIndex = (colorIndex + 1) % colors.length; // Passer à la couleur suivante
    return color;
}

document.addEventListener('DOMContentLoaded', function () {
    var userList = document.querySelectorAll('ul li');

    userList.forEach(function (user) {
        // Appliquer une couleur à chaque élément de liste
        user.style.backgroundColor = getNextColor();
    });
});



        document.addEventListener('DOMContentLoaded', function() {
            const notification = document.querySelector('.notification');
            if (notification) {
                // Ajouter l'icône à la notification
                notification.innerHTML = '<i class="fas fa-exclamation-triangle"></i> ' + notification.innerHTML;
                
                // Ajouter la classe pour l'animation clignotante
                notification.classList.add('blink');
            }
        });
    







    var ctx = document.getElementById('myChart').getContext('2d');
    
    // Assurez-vous que les variables owners et num_rows sont correctement définies et non indéfinies
    var owners = {{ owners|default('[]')|tojson|safe }};
    var num_rows = {{ num_rows|default('[]')|tojson|safe }}; 
    
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: owners,
            datasets: [{
                label: 'Number of Rows per Owner',
                data: num_rows,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
                plugins: {
                    legend: {
                        display: true
                    },
                    title: {
                        display: true,
                        text: 'Utilisation de la mémoire par les tablespaces',
                        font: {
                            size: 16
                        }
                    }
                },
            maintainAspectRatio: false,
            legend: {
                position: 'right'
            },
            title: {
                display: true,
                text: 'Number of Rows per Owner'
            }
        }
    });



    // Réinitialiser le formulaire après soumission
    document.getElementById("auditForm").addEventListener("submit", function() {
        this.reset();
    });

