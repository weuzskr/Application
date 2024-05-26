
        $(document).ready(function() {
            $('.sql-id').click(function() {
                $(this).next('.sql-text').toggle();
            });
        });
    
        // Fonction pour afficher le pop-up
        function showPopup() {
            document.getElementById('popup').style.display = 'block';
            document.getElementById('overlay').style.display = 'block';
            
            // Masquer le pop-up après 3 secondes
            setTimeout(closePopup, 3000);
        }

        // Fonction pour fermer le pop-up
        function closePopup() {
            document.getElementById('popup').style.display = 'none';
            document.getElementById('overlay').style.display = 'none';
        }

        // Événement de chargement de la page
        window.addEventListener('load', function() {
            // Afficher le pop-up
            showPopup();
        });
    
        var ctx = document.getElementById('line-chart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: {{ labels | tojson }},
                datasets: [{
                    label: 'Utilisation de la mémoire (Mo)',
                    data: {{ values | tojson }},
                    fill: false,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Utilisation de la mémoire par composante (Mo)',
                        font: {
                            size: 16
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Mémoire (Mo)'
                        }
                    }
                }
            }
        });
   
        // Récupérer les données depuis Flask (exemple de données)
        var data = {
            labels: ["SQL_ID1", "SQL_ID2", "SQL_ID3", "SQL_ID4", "SQL_ID5"],
            datasets: [{
                label: 'Exécutions',
                data: [10, 20, 30, 40, 50],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255,99,132,1)',
                borderWidth: 1
            },
            {
                label: 'Temps écoulé (s)',
                data: [15, 25, 35, 45, 55],
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        };

        // Configurer le graphique
        var options = {
            responsive: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Collecte de 5 rêquetes performantes de la base',
                        font: {
                            size: 16
                        }
                    }
                },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        };

        // Créer le graphique
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: data,
            options: options
        });
